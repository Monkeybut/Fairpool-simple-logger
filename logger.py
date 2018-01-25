#!/usr/bin/python
#---------------- Instructions ------------------#
# This is setup to run straight through and stop after making one pull.
# I use this as a cron job on a linux server to run several times a day.
# This is released under the Apache license with no implied guarantee or
# support.

# This python app will pull your data from fairpool and update files depending on where you would like them sent.
# I've set this up to potentiall push to csv and/or a sqllite db. I'm open to any suggestions for modifications or useful additions.
# If this changes the way you live your life feel free to drop a line at SuboK3RBj8BU4bVTQBwE1pXhszkfrRGn53CFfE7Usf2YbdNhrAGqDcDHTBGWbFvzjzRkFs7bVLFf5cmRFhrsJy25ALsYhVxemo
# If you have suggestions please feel free to make a note or pull request on the repo.




import sqlite3
import requests
import os
import json
import datetime

# Select the outputs you would like
sqlitedb_output = False
csv_output = True

#Enter Address between two hashes 'ADDRESS'
address = 'FILL IN ADDRESS HERE'

# API address
api_address = 'https://sumo.fairpool.cloud/api/network'
# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# -------------------------------  Begin Definitions  -------------------------------
# --------------------------  Do not edit below this line.  -------------------------
# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

class get_stats():
    def __init__(self):
        self.miner = self.pull_miner()
        self.network = self.pull_network()


    def pull_miner(self):
        try:
            r = requests.get('https://sumo.fairpool.cloud/api/stats?login='+address)
            if r.status_code == 200:
                returninfo = r.text
                jsoninfo = json.loads(returninfo)
                return jsoninfo
            else:
                raise Exception
        except:
            print('Tis All Broken: check your address')

    def pull_network(self):
        try:
            r = requests.get(api_address)
            if r.status_code == 200:
                returninfo = r.text
                jsoninfo = json.loads(returninfo)
                return jsoninfo
            else:
                raise Exception
        except:
            print('Tis All Broken: website down?')

class mining_history_db():
    def __init__(self):
        if not os.path.isfile('mining_history.db'):
            self.create()
        self.conn = sqlite3.connect('mining_history.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()


    def create(self):
        print("Creating new DB")
        conn = sqlite3.connect('mining_history.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE network
		             (id INTEGER PRIMARY KEY, difficulty text, hashrate int, blockheight int, time text)''')

        c.execute('''CREATE TABLE miners
        		             (id INTEGER PRIMARY KEY, miner text, hashrate text, coins text, time text)''')

        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

    def insert_network(self, network):
        time = datetime.datetime.now()
        # Insert a row of data
        self.cursor.execute("INSERT INTO network VALUES (?,?,?,?,?)",
                            (None, str(network[0]), str(network[1]), str(network[2]), time))

        # Save (commit) the changes
        self.conn.commit()
        return True


    def insert_miner(self, miner):
        time = datetime.datetime.now()
        # Insert a row of data
        self.cursor.execute("INSERT INTO miners VALUES (?, ?,?,?,?)",
                            (None, str(miner[0]), str(miner[1]), str(miner[2]), time))

        # Save (commit) the changes
        self.conn.commit()
        return True


class mining_csv():
    def __init__(self):
        if not os.path.isfile('miner_stats.csv'):
            f = open('miner_stats.csv', "a+")
            f.write("Miner,Hashrate,Coins,Time")

        if not os.path.isfile('network.csv'):
            f = open('network.csv', "a+")
            f.write("Difficulty,Hashrate,Blockheight,Time")
        self.time = datetime.datetime.now()


    def write_miner(self, miner):
        f = open('miner_stats.csv', "a+")
        command = '\n' + str(miner[0]) + ',' + str(miner[1]) + ',' + str(miner[2]) + ',' + str(self.time)
        f.write(command)

    def write_network(self, network):
        f = open('network.csv', "a+")
        command = '\n' + str(network[0]) + ',' + str(network[1]) + ',' + str(network[2]) + ',' + str(self.time)
        f.write(command)

def organize_miner_data(data):
    workerinfo = data['workers']
    unconfirmed = data['unconfirmed']
    balance = data['balance']
    paid = data['paid']
    worker = workerinfo[0][0]
    workerhash = workerinfo[0][1]
    total = unconfirmed + balance + paid
    processedtotal = total * .000000001
    info = [worker, workerhash, processedtotal]
    return info

def organize_network_data(data):
    difficulty = data['currentDifficulty']
    hashrate = int(data['networkHashrate'])
    blocks = data['blockchainHeight']
    info = [difficulty, hashrate, blocks]
    return info



# -------------------------------  Begin MAIN  -------------------------------

# Initialize classes
pull_data = get_stats()
miningcsv = mining_csv()
mining_db = mining_history_db()

miner_data = organize_miner_data(pull_data.miner)
network_data = organize_network_data(pull_data.network)


# If sqlite specified above write data to sqlite
if sqlitedb_output == True:
    mining_db.insert_miner(miner_data)
    mining_db.insert_network(network_data)

# If CSV selected write to csv
if csv_output == True:
    miningcsv.write_miner(miner_data)
    miningcsv.write_network(network_data)
