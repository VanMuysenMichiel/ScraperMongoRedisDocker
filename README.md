# ScraperMongoRedisDocker
Updated Version of my Scraper with Mongo and Redis. I also added Docker Images

Nodige vereiste : 
- python (nieuwst mogelijke versie)
- package : !pip install BeautifulSoup4 , !pip install pymongo , !pip install redis
- MongoDB : go to "https://www.mongodb.com/try/download/community". Take the current version, choose your platform and select download. I use Windows for my scraper.
- Redis : go to "https://github.com/microsoftarchive/redis/releases/tag/win-3.2.100". Select "Redis-x64-3.2.100.zip" and it will dowload a ZIP file. Extract this ZIP file and save all the files. When using Redis you will first open "redis-server.exe", than you will open "redis-cli.exe" and this is the interface of Redis. Let those 2 programs open when working with Python.
- Docker : go to "https://docs.docker.com/desktop/windows/install/" and download. Put 2 commands in Windows PowerShell : 
- docker run -d --name scraper-redis -p 6555:6379 redis 
- docker run -d --name scraper-docker -p 27777:27017 mongo
