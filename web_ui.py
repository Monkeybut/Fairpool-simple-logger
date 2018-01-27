from flask import Flask
from flask import render_template
import os
import sqlite3
import logging
from flask import Markup

# Configure the table height. Max table is top of x axis. Steps is number of increments on x axis.
steps_in_table = 5
max_table = 50


app = Flask(__name__)

@app.route('/')
def Miner_History():
    miner_data = database.get_miner()
    network_data = database.get_network()
    values = []
    labels = []

    for i in miner_data:
        print(i)
        values.append(i[3])

        # Cut off beginning date and following period
        labels.append(i[4].split(" ")[1].rpartition('.')[0][0:5])

    return render_template('miner.html', data=miner_data, network=network_data, values=reversed(values), labels=reversed(labels), steps=steps_in_table, max=max_table)



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

    def get_miner(self, rows=20):
        logging.debug('Getting miners')
        self.cursor.execute('''SELECT * FROM miners ORDER BY id DESC''', ())
        logging.debug('Fetched miners')
        # data = self.cursor.fetchall()
        data = self.cursor.fetchmany(rows)
        return data
    def get_network(self, rows=20):
        logging.debug('Getting network')
        self.cursor.execute('''SELECT * FROM network ORDER BY id DESC''', ())
        logging.debug('Fetched network')
        # data = self.cursor.fetchall()
        data = self.cursor.fetchmany(rows)
        return data

database = pull_mining_history()