#Contains two classes called Display and Database.
#Display plots data using Matplotlib, all its methods will plot a different chart
#Database stores SnG data into a db file using sqlite3 and retrivies stats from it using pandas and sqlite3

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt 
import collections

plt.style.use('seaborn-darkgrid')

class Display(object):
	def __init__(self):
		self.conn = sqlite3.connect('SnG.db')
		self.cursor = self.conn.cursor()
	
	def close_connection(self):
		self.cursor.close()
		self.conn.close()

	def WPNC(self):
		fd = pd.read_sql_query("SELECT * from main_data", self.conn)
		values_winper = fd['WinPer'].tolist()
		values_netcash = fd['NetCash'].tolist()
		values_accumulated_netcash = []
		accumulation = 0
		for value in values_netcash:
			accumulation = accumulation + float(value)
			values_accumulated_netcash.append(accumulation)
		plt.title('WinPer and NetCash')
		plt.plot(values_winper, 'b^', alpha = 0.25, label = 'Win Percentage')
		plt.plot(values_accumulated_netcash, '-g', label = 'Cash Won')
		plt.ylabel('Net Cash')
		plt.xlabel('Sessions')
		plt.legend(loc='best')
		plt.show()
		self.close_connection()

	def DAILY(self):
		fd = pd.read_sql_query("SELECT * from main_data", self.conn)
		date_list = fd.groupby('d')['NetCash'].sum()
		labels_unrefined = fd['d']
		labels_unrefined2 = collections.Counter(labels_unrefined)
		final_labels = []
		for key, value in labels_unrefined2.iteritems():
			final_labels.append(key)
		final_labels.sort()
		numbers = date_list.tolist()
		plt.title('Daily Profit/Loss Chart')
		plt.ylabel('Cash')
		plt.xlabel('Days')
		plt.ylim([int(min(numbers))-50, int(max(numbers) + 50)])
		plt.plot(numbers, '-g', label = 'Profit/Loss')
		plt.legend(loc='best')
		plt.show()
		self.close_connection()

class Database(object):
	def write(self, initial_write):	
		def return_stats(config):
			T_matches = config[0]
			in_stake = config[1]
			out_stake = config[2]
			Played = config[3]
			Won = config[4]
			Lost = config[5]
			GLTP = float(int(T_matches) - int(Played))
			c = round(100 - (GLTP/float(T_matches)*100),2)
			win_per = round(float((float(Won)/float(Played)) * 100),2)
			net_cash = int(out_stake)*int(Won) - int(in_stake)*int(Lost)
			return net_cash, win_per

		conn = sqlite3.connect('SnG.db')
		c = conn.cursor()
		
		d = str(raw_input("Enter Date [YYMMDD]: "))
		p = float(raw_input("Enter P : "))
		w = float(raw_input("Enter W : "))
		in_s = int(raw_input('Enter in_stake : '))
		out_s = int(raw_input('Enter out_stake : '))
		
		l = p-w
		
		data = [p, in_s, out_s, p, w, l]
		nc, wp = return_stats(data)
		#nc = float(raw_input("Enter NET CASH : "))
		#find out by func
		#wp = float(raw_input("Enter WIN PERC : "))
		#find out by func
		
		if initial_write is 1:
			c.execute('''CREATE TABLE main_data
		              (d real, P real, W real, L real, NetCash real, WinPer real)''')
		
		c.execute("INSERT INTO main_data VALUES ({data})".format(data = str(d) + ',' + str(p) 
		+ ',' + str(w) + ',' + str(l)+ ',' +str(nc)+ ',' +str(wp)))
		
		if initial_write is 1:
			c.execute('''CREATE TABLE minor_data
			 			(in_stake real, out_stake real)''')
		
		c.execute("INSERT INTO minor_data VALUES ({data})".format(data = str(in_s) + ',' 
		+ str(out_s)))
		
		conn.commit()
		c.close()
		conn.close()

	def read(self):

		def forecastor(games_played):
			d = round(float(games_played) / float(50),2)
			elements = []
			for x in xrange(games_played, games_played + 200,50):
				elements.append(str(x))
			return elements
		
		conn = sqlite3.connect('SnG.db')
		c = conn.cursor()
		fd = pd.read_sql_query("SELECT * from main_data", conn)
		fd2 = pd.read_sql_query("SELECT * from minor_data", conn)
		print fd
		print fd2
		
		c.close()
		conn.close()

		played = str(int(fd['P'].sum()))
		won = str(int(fd['W'].sum()))
		winper = round((float((fd['W'].sum())/float(fd['P'].sum()))),3) * 100
		Net_Cash = round(float(fd['NetCash'].sum()),2)
		Per_Game = round(Net_Cash/float(played),2)
		ForeCast_Labels = forecastor(int(played))

		print '\nTotal'
		print 'Played : ' + played
		print 'Won    : ' + won
		print 'WinPerG: ' + str(winper)
		print 'NetCash: ' + str(Net_Cash)
		print 'PerGame: ' + str(Per_Game)
		print 'Forecast -'
		print 'Games' + '\t' + 'NetCash Estimated'
		for x in xrange(0,4): print ForeCast_Labels[x] + '\t' +  str(Per_Game * 
		int(ForeCast_Labels[x]))