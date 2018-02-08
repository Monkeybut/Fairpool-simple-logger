from flask import Flask
from flask import render_template
import os
import sqlite3
import logging
import statistics
from werkzeug.contrib.fixers import ProxyFix
from dateutil import parser
from datetime import datetime, date, time, timedelta
import time

# Configure the table height. Max table is top of x axis. Steps is number of increments on x axis.
steps_in_table = 5
# This is the top of the x axis. Adjust according to number of coins you are at.
max_table = 90

# This pulls every 3rd data point to show in the graph. Edit this to suite your needs. If you poll the API more frequently this number will be higher.
chart_interval = 5

# Number of rows to display in table
pull_database_rows = 24

app = Flask(__name__)

@app.route('/')
def Miner_History():
    
    pull_rows = pull_database_rows * chart_interval
    miner_data = database.get_miner(rows=pull_rows)
    network_data = database.get_network(rows=pull_rows)
    values = []
    labels = []
    all_coins = []
    index = pull_rows - 1
    by_day = False



    row_check = '2018-02-05'
    
    if by_day == True:
        last_date = parser.parse(miner_data[0][4])
    
        dayDates = []
        dayDates.append(last_date.strftime("%m%d%Y"))
        
        for row in miner_data:    
            for i in range(0,14):
                day = last_date - timedelta(days=i)
                # print(day.day)
                if (day.hour == parser.parse(row[4]).hour) and (day.minute == parser.parse(row[4]).minute):
                    print(row[3])
            
    elif by_day== False:
        # TODO
        # By hour growth changes
        # datetime.now() + timedelta(hours=1)
        
        last_date = parser.parse(miner_data[0][4])
    
        dayDates = []
        dayDates.append(last_date.strftime("%m%d%Y"))
        
        for row in miner_data:    
            for i in range(0,14):
                day = last_date - timedelta(hours=i)
                # print(day.day)
                if (day.day == parser.parse(row[4]).day) and (day.hour == parser.parse(row[4]).hour) and (day.minute == parser.parse(row[4]).minute):
                    print(row[3])
        
    # else:
        #TODO
        # By month growth changes
    #    pass
    

    # This ugly iteration grabs rows as configured in the interval above. Adjust this (chart_interval variable) to see longer or shorter trends.
    for i in miner_data:
        # Uses every 3rd entry to show better trend line.
        if i[0] % chart_interval == 0:
            values.append(i[3])

            # Cut off beginning date and following period
            labels.append(i[4].split(" ")[1].rpartition('.')[0][0:5])
        all_coins.append(float(i[3]))

    # Still in testing doing an average growth of coins per data point.
    difference = []
    last_row = miner_data[0]
    for row in miner_data:
        # if float("{0:.3f}".format(last_row[3])) != float("{0:.3f}".format(row[3])):
        number = last_row[3] - row[3]
        number = float("{0:.7f}".format(number))
        last_row = row
        difference.append(number)


    # Find average growth of coins
    # difference = set(difference) # remove duplicates meaning no growth
    average = [statistics.mean(difference)]
    average.append(average[0] * 4)
    average.append(average[1] * 24)
    # print(average[1])
        
    # Find average hash rate over selected period
    hash_average_list = []
    for row in miner_data:
        number = row[2]
        hash_average_list.append(number)   
            
    hash_average = statistics.mean(hash_average_list)

            
    # Table miner/network information            
    miner_data = miner_data[:pull_rows // chart_interval]
    network_data = network_data[:pull_rows // chart_interval]

    return render_template('miner.html', data=miner_data, network=network_data, values=reversed(values), labels=reversed(labels), steps=steps_in_table, max=max_table, hash_average=hash_average, growth_rate=average)



class pull_mining_history():
    def __init__(self):
        if not os.path.isfile('mining_history.db'):
            self.create()



    def create(self):
        print("Creating new DB")
        conn = sqlite3.connect('mining_history.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE network
		             (id INTEGER PRIMARY KEY, difficulty text, hashrate int, blockheight int, time text)''')

        c.execute('''CREATE TABLE miners
        		             (id INTEGER PRIMARY KEY, miner text, hashrate int, coins real, time text)''')

        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

    def get_miner(self, rows=50):
        logging.debug('Getting miners')
        self.conn = sqlite3.connect('mining_history.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute('''SELECT * FROM miners ORDER BY id DESC''', ())
        logging.debug('Fetched miners')
        # data = self.cursor.fetchall()
        data = self.cursor.fetchmany(rows)
        self.conn.close()
        return data
        
    def get_network(self, rows=50):
        logging.debug('Getting network')
        self.conn = sqlite3.connect('mining_history.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute('''SELECT * FROM network ORDER BY id DESC''', ())
        logging.debug('Fetched network')
        # data = self.cursor.fetchall()
        data = self.cursor.fetchmany(rows)
        self.conn.close()
        return data

database = pull_mining_history()

miner_data = database.get_miner()
network_data = database.get_network()

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()
