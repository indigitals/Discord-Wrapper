# This does not currently work and is in development 
<!-- Title -->
<p align="center">
  <h1 align="center"><a href="https://github.com/indigitals/Discord-Wrapper" title="Discord Socket Wrapper py">Discord Websocket Wrapper in py</a></h1>
</p>

## About the Project
This will be a complete wrapper specifically for the discord gateway (not the REST api however) that simplifies tedious boring JSON sending into a few function calls returning all the necessary data as quick as possible. This will also not be restrictive to specifically bots and will be made with everyone in mind. A more descriptive README will replace this one once I finish the project.

Note: This is entirely a proof of concept and for educational use. I am not responsible for anything malicious done with this and any consequences one may face for doing anything malicious. This IS against discord TOS if you use it as a selfbot so be warned but I will not stop you from doing so

### Plans
- [x] `Connect`: Simply connect to the websocket successfully
- [x] `Log Session`: Grab the session id and log messages
- [ ] `Specific Features`: Specific areas that the wrapper covers so far
    - [ ] `Voice Channels` (stream automatically and input custom audio)
    - [ ] `Parse Messages` (can be used to log deleted messages for example)
    - [ ] `Get Open Sessions` (prevent token logging?)
    - [ ] `Guild Member Scraping` 
    - [ ] `Authentication Websockets?` (not really connected to the main discord gateway but this is used for logging into accounts) 


Will not be commiting for a little bit until I get the voice connection working 
