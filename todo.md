# RPGDiscordBot
Simple Python Discord bot handling our group stuff

### stream.py
- [ ] starting stream
  - [ ] check if OBS is turned on
    - [ ] If not, run it
  - [ ] check if discord is turned on on recording machine
    - [ ] If not, run it
  - [ ] check if recording account is in the voice channel
    - [ ] If not, connect it (may be tricky, no direct API to Discord here)
  - [ ] check if Discord is foreground application (or maybe make a scene in OBS where ONLY Discord is being shown?)  
- [ ] Rename streaming account appropietly (i.e. when streaming - Recording, when not - not Recording)
- [ ] Add timestamps for youtube stream
  - [ ] Maybe it is possible to get current timestamp from the stream itself using YT API?
  - [ ] If not, just get the timing from start of the stream till the end of it
  - [ ] Maybe handle storage of this data somehow (sqlite db?)

### maintain.py
- [ ] divide it a bit, now it has too much responsibilities

### config.toml
- [ ] Make config based on dacite and dataclasses for easier manipulation
  - [ ] this will make it possible to also get configuration data from different parts of the code and not only from the main bot class

