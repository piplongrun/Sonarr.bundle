Sonarr Agent
============

What is the Sonarr Agent?
-------------------------
It's a metadata agent for Plex. It retrieves metadata from the Sonarr API. This agent can come in handy for people using both Plex and Sonarr.

Lately a lot of my TV shows were missing metadata (titles listed as "Episode 4", or episodes with missing summaries). This agent tries to fill in the blanks by using data that Sonarr usually already has.

How do I install this agent?
----------------------------
You can install the agent:

 - From within the Unsupported AppStore, or:
 - Manually: See the support article "[How do I manually install a channel?](https://support.plex.tv/hc/en-us/articles/201187656-How-do-I-manually-install-a-channel-)" over at the Plex support website.

How do I use this agent?
------------------------
There are 2 options you have:

1. You can use the agent as a standalone (primary) agent. That way only data from Sonarr will be used. Please note that this will not give you the same data rich library you're probably used to. Most important data will be present, but some pieces will be missing, because Sonarr doesn't provide some details.
2. You can use the agent as a secondary agent to TheTVDB agent. Activate it under TheTVDB in *Settings* > *Server* > *Agents* > *Shows*. Drag it to just below TheTVDB to let this agent fill in the blanks from TheTVDB.

Before using the agent, go into the agent's preferences and enter your Sonarr URL and API key (you can find your Sonarr API key in Sonarr under *Settings* > *General* > *Security*).

Where do I download this agent?
-------------------------------
If you want to install the agent manually or if you are interested in the source code, you can download the latest copy of the agent from Github directly: [ZIP](https://github.com/piplongrun/Sonarr.bundle/archive/master.zip)

Where do I report issues?
-------------------------
Create an [issue on Github](https://github.com/piplongrun/Sonarr.bundle/issues) and add as much information as possible:
 - Plex Media Server version
 - Primary agent and order of any secondary agents
 - Log files, `com.plexapp.agents.sonarr.log`
