from flask import Flask
from flask import render_template
import os
import sqlite3
import logging
import statistics

# Configure the table height. Max table is top of x axis. Steps is number of increments on x axis.
steps_in_table = 10
# This is the top of the x axis. Adjust according to number of coins you are at.
max_table = 100

# This pulls every 3rd data point to show in the graph. Edit this to suite your needs. If you poll the API more frequently this number will be higher.
chart_interval = 5 

# Number of rows to display in table
pull_database_rows = 20

app = Flask(__name__)

@app.route('/')
def Miner_History():
    pull_rows = pull_database_rows * chart_interval
    miner_data = database.get_miner(rows=pull_rows)
    network_data = database.get_network(rows=pull_rows)
    values = []
    labels = []
    all_coins = []
    index = pull_rows -1
    


    for i in miner_data:
        # Uses every 3rd entry to show better trend line.
        if i[0] % chart_interval == 0:
            values.append(i[3][:6])

            # Cut off beginning date and following period
            labels.append(i[4].split(" ")[1].rpartition('.')[0][0:5])
        all_coins.append(float(i[3]))


    # Still under construction
    average_coin = statistics.variance(all_coins)
    total_coin = float(miner_data[0][3]) - float(miner_data[index][3])
    
    # Table miner/network information            
    miner_data = miner_data[:pull_rows // chart_interval]
    network_data = network_data[:pull_rows // chart_interval]

    return render_template('miner.html', data=miner_data, network=network_data, values=reversed(values), labels=reversed(labels), steps=steps_in_table, max=max_table, average_coin_income=average_coin, total_coin=total_coin)



class pull_mining_history():
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

    def get_miner(self, rows=50):
        logging.debug('Getting miners')
        self.cursor.execute('''SELECT * FROM miners ORDER BY id DESC''', ())
        logging.debug('Fetched miners')
        # data = self.cursor.fetchall()
        data = self.cursor.fetchmany(rows)
        return data
    def get_network(self, rows=50):
        logging.debug('Getting network')
        self.cursor.execute('''SELECT * FROM network ORDER BY id DESC''', ())
        logging.debug('Fetched network')
        # data = self.cursor.fetchall()
        data = self.cursor.fetchmany(rows)
        return data

database = pull_mining_history()

miner_data = database.get_miner()
network_data = database.get_network()


