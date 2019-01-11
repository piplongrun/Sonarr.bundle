# Sonarr Agent for Plex

SERIES_URL = "{}/api/series"
EPISODES_URL = "{}/api/episode?seriesId={}"

RE_STRIP_YEAR = Regex('( \(\d{4}\))$')

####################################################################################################
def Start():

	pass

####################################################################################################
def GetApiData(url):

	if not Prefs['sonarr_api_key']:
		Log("Enter your Sonarr API key in the agent's preferences")
		return None

	try:
		data = HTTP.Request(url, headers={"X-Api-Key": Prefs['sonarr_api_key']}).content
		return data
	except:
		Log("Error requesting URL {}".format(url))
		return None

####################################################################################################
class SonarrAgent(Agent.TV_Shows):

	name = 'Sonarr'
	languages = [Locale.Language.English]
	primary_provider = True
	accepts_from = ['com.plexapp.agents.localmedia']
	contributes_to = ['com.plexapp.agents.thetvdb']

	def search(self, results, media, lang, manual):

		if media.primary_agent == 'com.plexapp.agents.thetvdb':
			results.Append(MetadataSearchResult(
				id = media.primary_metadata.id,
				score = 100
			))

		else:
			sonarr_series = SERIES_URL.format(Prefs['sonarr_url'].rstrip('/'))
			json = GetApiData(sonarr_series)

			if not json:
				return None

			json_obj = JSON.ObjectFromString(json)

			for series in json_obj:

				show = RE_STRIP_YEAR.sub("", media.show).lower()
				series_title = RE_STRIP_YEAR.sub("", series['title']).replace('-', ' ').lower()

				if show != series_title:
					continue

				if media.year and int(media.year) > 1900 and int(media.year) == series['year']:
					score = 100
				else:
					score = 90

				results.Append(MetadataSearchResult(
					id = str(series['tvdbId']),
					name = series['title'],
					year = series['year'],
					score = score,
					lang = lang
				))

	def update(self, metadata, media, lang):

		sonarr_series = SERIES_URL.format(Prefs['sonarr_url'].rstrip('/'))
		json = GetApiData(sonarr_series)

		if not json:
			return None

		json_series = JSON.ObjectFromString(json)

		for series in json_series:

			if str(series['tvdbId']) != metadata.id:
				continue

			# For now
			if series['seriesType'] != "standard":
				continue

			# Start adding metadata
			metadata.title = series['title']
			metadata.originally_available_at = Datetime.ParseDate(series['firstAired']).date()
			metadata.summary = series['overview']
			metadata.duration = series['runtime'] * 60 * 1000
			metadata.studio = series['network']
			metadata.content_rating = series['certification'] if 'certification' in series else None

			metadata.genres.clear()
			for genre in series['genres']:
				metadata.genres.add(genre)

			valid_names = list()

			for image in series['images']:

				image_url = "{}/api/MediaCover/{}".format(Prefs['sonarr_url'].rstrip('/'), image['url'].split('/MediaCover/')[-1])
				valid_names.append(image_url)

				if image['coverType'] == "fanart":
					metadata.art[image_url] = Proxy.Media(GetApiData(image_url))
				elif image['coverType'] == "poster":
					metadata.posters[image_url] = Proxy.Media(GetApiData(image_url))
				elif image['coverType'] == "banner":
					metadata.banners[image_url] = Proxy.Media(GetApiData(image_url))

			metadata.art.validate_keys(valid_names)
			metadata.posters.validate_keys(valid_names)
			metadata.banners.validate_keys(valid_names)

			# Add show to 'Ended' collection if status is 'ended'
			metadata.collections.clear()
			if series['status'] == "ended" and Prefs['sonarr_ended_collection'] and Prefs['sonarr_ended_collection_name'] != "":
				metadata.collections.add(Prefs['sonarr_ended_collection_name'])

			# Add available episode data
			sonarr_episodes = EPISODES_URL.format(Prefs['sonarr_url'].rstrip('/'), series['id'])
			json = GetApiData(sonarr_episodes)

			if not json:
				return None

			json_episodes = JSON.ObjectFromString(json)

			# Loop over seasons
			for s in media.seasons:

				# Loop over episodes in a season
				for e in media.seasons[s].episodes:

					for episode in json_episodes:

						if episode['seasonNumber'] == int(s) and episode['episodeNumber'] == int(e):

							metadata.seasons[s].episodes[e].title = episode['title'] if 'title' in episode else None
							metadata.seasons[s].episodes[e].summary = episode['overview'] if 'overview' in episode else None
							metadata.seasons[s].episodes[e].originally_available_at = Datetime.ParseDate(episode['airDate']).date() if 'airDate' in episode else None

							break

			break
