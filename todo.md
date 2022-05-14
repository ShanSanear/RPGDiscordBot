# RPGDiscordBot
Simple Python Discord bot handling our group stuff

### stream.py
- [x] starting stream
  - [ ] check if OBS is turned on
    - [x] If not, run it
  - [ ] check if discord is turned on directly on the recording machine
    - [ ] If not, run it
  - [ ] check if recording account is in the voice channel
    - [ ] If not, connect it (maybe tricky, no direct API to Discord here)
  - [x] check if Discord is foreground application (or maybe make a scene in OBS where ONLY Discord is being shown?)
    - [x] Discord as sole scene in the recording/streaming, rather then checking for Discord to be foreground
      application
- [ ] This functionality shall not explicitly check for things already working or not internally, since some things may
  be already turned on manually
- [ ] Rename streaming account appropriately (i.e. when streaming - Recording, when not - not Recording)
- [ ] Rename stream itself appropriately
  - [ ] Don't forget about limiting this only to the administrator/owner of the bot or specific group in Discord
- [ ] Add timestamps for youtube stream
  - [ ] Maybe it is possible to get current timestamp from the stream itself using YT API?
  - [ ] If not, just get the timing from start of the stream till the end of it
  - [ ] Maybe handle storage of this data somehow (sqlite db?)

### maintain.py

- [x] divide it a bit, now it has too much responsibilities

### config.toml

- [x] Make config based on dacite and dataclasses for easier manipulation
  - [x] this will make it possible to also get configuration data from different parts of the code and not only from the
    main bot class

### renamer.py

- [x] Make it possible to rename guild members
- [x] Those renaming must be possible to specify by some sort of profile
- [ ] Renaming should be persistent, i.e. using database 
