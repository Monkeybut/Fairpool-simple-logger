# Fairpool-simple-logger
Simple python script for pulling information from fairpool mining pool. 


## Description
This is a very simple script for tracking the network as well as miner stats on the fairpool pool. I've only used this with their Sumo pool but its possible it would work for their other coins. I just haven't checked out their other coins API.

I run this on a linux machine in AWS that is initiated hourly via a cron job. For reference my cron job is "0 */1 * * * /usr/bin/python3 /home/ubuntu/logger.py"

It can be run at your own schedule. A faster timeframe would give you a better picture of your hashing speeds but I'm more concerned with coin growth and total network performance than hash rates. 

### Future plans

I'm open to suggestions if anybody has any opinions or requests that they think would make it better or more powerful. I asked the fairpool admin's for permission to release this and they were fine with it with the information that they may need to change the API at some point. They didn't see that happenning but I would likely update this as well if I'm still using it. 

Going forward I'd like to build a web UI possibly with graphs to show current and projected growth as well as seperate miners actions. This is low priority unless someone really wanted this.

The way I've built this I don't think it would handle multiple miners on one address very well. I only have one currently on the same address so I can't confirm its behavior. Its a dam simple script so take it with a grain of salt. 

### License

Released under the Apache license with no implied guarantee. 
