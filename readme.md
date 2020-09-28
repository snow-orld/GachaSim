# A Gacha Simulation Project for gacha games like FGO.

## Goal
Make a universal gacha framework that adapts to different gacha games by simply 
replacing assets. 

## TODO
- [ ] Make a universal framework that works for different gacha games.
    - [x] Define the content of a config.txt file that describes setting-up for 
    a specific game.
- [x] Crawling servant / craft essence details from web.
	- [ ] Implement an OTA based on local cache. Current parsing time is too 
	slow, around 0.5s per card.
- [ ] Crawling pool info from web.
    - [ ] As of 2020/9/27, pool data is temporarily stored in config/conf_fgo_pool.json. 
- [x] Define classes:
    - [x] Data Fetcher
    - [x] Servant
    - [x] Essence Craft
    - [x] Card
    - [x] Pool
    - [x] Gacha Core
- [x] **MileStone** Finish the terminal version of basic game mechanism.
- [ ] Integrate current data model into Django.
- [ ] Figure out a format (video or gif) and a way of using the gacha animation.
- [ ] Integration on Django.
    - [ ] Integrate animation and sound.
- [ ] Deploy on github.
