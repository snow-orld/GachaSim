# A Gacha Simulation Project for gacha games like FGO.

## Goal
Make a universal gacha framework that adapts to different gacha games by simply 
replacing assets. 

## TODO
- [ ] Make a universal framework that works for different gacha games.
    - [ ] Define the content of a config.txt file that describes setting-up for 
    a specific game.
- [ ] Crawling servant details from web.
	- [ ] Implement an OTA based on local cache. Current parsing time is too 
	slow, around 0.5s per card.
- [ ] Define classes:
    - [ ] Data Fetcher
    - [ ] Servant
    - [ ] Essence Craft
    - [ ] Card
    - [ ] Pool
    - [ ] Gacha Core
- [ ] **MileStone** Finish the terminal version of basic game mechanism.
- [ ] Figure out a format (video or gif) and a way of using the gacha animation.
- [ ] Integration on Django.
    - [ ] Integrate animation and sound.
- [ ] Deploy on github.
