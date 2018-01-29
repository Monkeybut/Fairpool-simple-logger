# Fairpool-simple-logger
Simple python script for pulling information from fairpool mining pool. 


## Description
This is a very simple script for tracking the network as well as miner stats on the fairpool pool. I've only used this with their Sumo pool but its possible it would work for their other coins. I just haven't checked out their other coins API.

## Usage

This script can output in two formats. CSV and a sqlite database. To change what you would prefer simple change the sqlite/CSV boolean from True to false to disable. Or vice versa to enable it. The csv should work for just about everyone so I disabled the sqlite db output by default. 

I run this on a linux machine in AWS that is initiated hourly via a cron job. For reference my cron job is "0 */1 * * * /usr/bin/python3 /home/ubuntu/logger.py"

It can be run at your own schedule. A faster timeframe would give you a better picture of your hashing speeds but I'm more concerned with coin growth and total network performance than hash rates. 

Sumokoin donations are not expected but welcome at: SuboK3RBj8BU4bVTQBwE1pXhszkfrRGn53CFfE7Usf2YbdNhrAGqDcDHTBGWbFvzjzRkFs7bVLFf5cmRFhrsJy25ALsYhVxemo


### Web UI

I've slowly started building a web UI. Still in development and testing but fairly straightforward app built using flask. This utilizes the sqlite db so that needs to be enabled in the main logging script. I'll add instructions for a detailed setup soon. 

##### Not so detailed instructions for WebUI setup

Set ```sqlitedb_output = True``` from false to True inside ```logger.py```. 
Configure it to run every hour (more or less). One suggestion is via a crontab.
Configure nginx as a front end with redirection to flask port 5000. I would suggest using LetsEncrypt to configure SSL. 
Configure supervisor to start flask.
Ensure whatever host you use has ports 80/443 allowed through your firewall. 



### Future plans

I'm open to suggestions if anybody has any opinions or requests that they think would make it better or more powerful. I asked the fairpool admin's for permission to release this and they were fine with it with the information that they may need to change the API at some point. They didn't see that happenning but I would likely update this as well if I'm still using it. 

The way I've built this I don't think it would handle multiple miners on one address very well. I only have one currently on the same address so I can't confirm its behavior. Its a dam simple script so take it with a grain of salt. I plan to fix this later.

With the addition of the UI I will continue to add features and better reporting. Additionally I'd like to get multiple miners configured better. 


### License

Released under the Apache license with no implied guarantee. 

