# This flask app shows miner history as well as network history. 
# Displays in both Table and graph form for each. 
# Also displays averages for mining performance. 
#
#
#

from flask import Flask
from flask import render_template
import sqlite3, logging, statistics, time, pygal, os
from werkzeug.contrib.fixers import ProxyFix
from dateutil import parser
from datetime import datetime, date, time, timedelta

# Configure the table height. Max table is top of x axis. Steps is number of increments on x axis.
steps_in_table = 5
# This is the top of the x axis. Adjust according to number of coins you are at.
max_table = 90

# This pulls every 3rd data point to show in the graph. Edit this to suite your needs. If you poll the API more frequently this number will be higher.
chart_interval = 5

# Number of rows to display in table
pull_database_rows = 50

app = Flask(__name__)

class calculator():
    def daily_income(self, sql_list, period):
        today_coin = 0
        yesterday_coin = 0
        for row in sql_list:
            if str(row[4])[:10] == str(period)[:10]:
                if (row[4][11:16] == '00:00'):
                    yesterday_coin = float(row[3])
                elif (row[4][11:16] == '23:45'):
                    today_coin = float(row[3])
        
        # print(str(today_coin) + ' : ' + str(yesterday_coin))
        yesterdays_coins = today_coin - yesterday_coin
        return yesterdays_coins
        
    def hashes(self, sql_list, item):
        misc_list = []
        for row in reversed(sql_list):
            if row[item] != 'None':
                misc_list.append(int(row[item]))
            else:
                misc_list.append(0)
        return misc_list
    
    def coins_list(self, sql_list):
        coins = []
        for row in reversed(sql_list):
            coins.append(row[3])
        return coins
    
    def times_list(self, sql_list):
        times = []    
        for row in reversed(sql_list):
            times.append(row[4][10:16])
        return times    
    
    def average_hashes(self, sql_list):
        hash_average_list = []
        for row in sql_list:
            number = row[2]
            if number != 'None':
                hash_average_list.append(number)
            else:
                hash_average_list.append(0)
        return statistics.mean(hash_average_list)
        
@app.route('/')
def Miner_History():
    
    pull_rows = pull_database_rows * chart_interval
    miner_data = database.get_miner(rows=pull_rows)
    network_data = database.get_network(rows=pull_rows)
    weekly_miner_data = database.get_miner(rows=850)
    values = []
    labels = []
    all_coins = []
    index = pull_rows - 1


    last_date = parser.parse(miner_data[0][4])
    dayDates = []
    dayDates.append(last_date.strftime("%m%d%Y"))

                
    
    #  -------------- Predictions ----------------
    difference = []
    last_row = miner_data[0]
    for row in miner_data:
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
    hash_average = mining_calculator.average_hashes(miner_data)

            
    # Table miner/network information            
    miner_data = miner_data[:pull_rows // chart_interval]
    network_data = network_data[:pull_rows // chart_interval]

    # ------------------ Get Date ------------------
    dayDates = []
    today = datetime.now()
    dayDates.append(today.strftime("%m%d%Y"))
    
    yesterday = today + timedelta(days=-1)
    
    
    
    # ------------------ Gather webpage Data ------------------
    yesterdays_income = mining_calculator.daily_income(weekly_miner_data, yesterday)
    time_list = mining_calculator.times_list(miner_data)
    hashrate_list = mining_calculator.hashes(miner_data, 2)
    coins = mining_calculator.coins_list(miner_data)
    
    weekly_income = []
    for i in range(-1, -7, -1):
        week_day = today + timedelta(days=i)
        weekly_income.append(mining_calculator.daily_income(weekly_miner_data, week_day))
        print weekly_income

    # ------------------   Miner Graph   --------------------   
    
    chart = pygal.Line(secondary_range=(8000, 12000))
    chart.x_labels = time_list
    chart.add('Coins', coins)
    chart.add('Hashrate', hashrate_list, secondary=True)
    
    miner_graph_data = chart.render_data_uri()
    
    # ------------------   End Miner Graph   --------------------   


    
    # ------------------   Network Graph   ------------------   
    network_hashrate_list = mining_calculator.hashes(network_data, 2)
    difficulty_list = mining_calculator.hashes(network_data, 1)
    chart = pygal.Line(secondary_range=(15000000, 40000000))
    chart.x_labels = time_list
    chart.add('Difficulty', difficulty_list)
    chart.add('Network Hash Rate', network_hashrate_list, secondary=True)
    network_graph_data = chart.render_data_uri()

    # ------------------  End Network Graph   ------------------

    return render_template('miner.html', 
    yesterday_income=yesterdays_income, 
    miner_graph_data=miner_graph_data, 
    network_graph_data=network_graph_data, 
    data=miner_data, 
    network=network_data, 
    values=reversed(values), 
    labels=reversed(labels), 
    hash_average=hash_average, 
    growth_rate=average,
    weekly_income=weekly_income)



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

    def get_miner(self, rows=750):
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
        
    def get_network(self, rows=750):
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
mining_calculator = calculator()

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()