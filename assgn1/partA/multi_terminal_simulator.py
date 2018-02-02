
import math
import numpy as np

class MultiServer_Simulator(object):

	def __init__(self, mean_interarrival,mean_service,num_servers):
		#initialize the Simulator Object

		self.mean_interarrival = mean_interarrival
		self.mean_service = mean_service
		self.num_servers = num_servers

		#number of event types are (S+1), 1 slot for arrival events, and 1 slot per departure events from each server
		self.num_events= 1 + self.num_servers
		self.current_time = 0.0
		self.server_status = [0] * self.num_servers
		self.num_in_q = 0
		self.time_last_event = 0.0
		self.num_custs_delayed = 0
		self.total_of_delays = 0.0
		self.area_num_in_q = 0.0
		self.area_server_status = [0] * self.num_servers
		self.time_next_event = [1.0e+30] * (self.num_events)

		#define a delay_array to store individual delay times
		self.delay_array = []

		#using Numpy to generate an exponential RV instead of writing the RNG code
		self.time_next_event[0] = self.current_time + np.random.exponential(scale=self.mean_interarrival)
		self.time_arrival = []

	def arrive(self):
		#set next arrival event
		self.time_next_event[0] = self.current_time + np.random.exponential(scale=self.mean_interarrival)
		
		#if all terminals are occupeied, add new arrival to queue
		if (sum(self.server_status) == self.num_servers):
			self.num_in_q += 1
			self.time_arrival.append(self.current_time)

		#if a terminal is available, make it busy
		else:
			self.delay = 0.0
			self.total_of_delays += self.delay
			self.num_custs_delayed = self.num_custs_delayed + 1
			self.delay_array.append(self.delay)
			for i in range (0,self.num_servers):
				if (self.server_status[i] == 0):
					self.server_status[i] = 1

					#schedule departure
					self.time_next_event[i + 1] = self.current_time + np.random.exponential(scale=self.mean_service)
					break


	def depart(self):

		#if queue is empty, make the server idle
		if (self.num_in_q == 0):
			self.server_status[self.next_event_type-1] = 0
			self.time_next_event[self.next_event_type] = 1.0e+30

		#if queue is not empty, then get the head of queue
		else:
			self.num_in_q -= 1
			self.delay = self.current_time - self.time_arrival[0]
			self.total_of_delays += self.delay
			self.num_custs_delayed+=1
			self.delay_array.append(self.delay)

			#schedule departure
			self.time_next_event[self.next_event_type] = self.current_time + np.random.exponential(scale=self.mean_service)
			
			#move all the customers by one place in the queue
			for i in range (0,self.num_in_q):
				self.time_arrival[i] = self.time_arrival[i+1]
			discard = self.time_arrival.pop()

	def print_report(self):

		print ("\nAverage delay in queue: {:f} minutes\n\n".format(self.avg_delay))
		for i in range (0, self.num_servers):
			print ("Server Utilization for Terminal {:d} : {:f}\n\n".format( i+1, self.area_server_status[i]/self.current_time))

		print ("Average number in queue: {:f}\n\n".format( self.area_num_in_q/self.current_time))
		print ("Customers Delayed: {:d}\n\n".format(self.num_custs_delayed))
		print ("Percentage Customers Delayed more than 5 mins: {:f}\n\n".format(self.percentage_more_than_5_mins))
		print ("Percentage Customers Delayed less than 4 mins: {:f}\n\n".format(self.percentage_less_than_4_mins))
		print ("Time simulation ended: {:f}\n".format(self.current_time))
		#pass

	def report(self):
		#calculate avg delay
		self.avg_delay = self.total_of_delays/ self.num_custs_delayed
		
		#calculate % customers delayed by more than 5 mins
		self.num_delayed_more_than_5_mins = 0
		for i in self.delay_array:
			if i>5:
				self.num_delayed_more_than_5_mins += 1
		self.percentage_more_than_5_mins = self.num_delayed_more_than_5_mins/len(self.delay_array)

		#calculate % customers delayed by less than 4 mins
		self.num_delayed_less_than_4_mins = 0
		for i in self.delay_array:
			if i<4:
				self.num_delayed_less_than_4_mins += 1
		self.percentage_less_than_4_mins = self.num_delayed_less_than_4_mins/len(self.delay_array)


	def timing(self):
		self.min_time_next_event = 1.0e+29
		self.next_event_type = -1

		#get next event from EL
		for i in range (0, self.num_events):
			if (self.time_next_event[i] < self.min_time_next_event):
				self.min_time_next_event = self.time_next_event[i]
				self.next_event_type = i

		if (self.next_event_type == -1):
			print ("\nEvent list empty at time {:f}".format(self.current_time))
			exit(1)

		#advance time to next event
		self.current_time = self.min_time_next_event


	def update_time_avg_stats(self):
		self.time_since_last_event = self.current_time - self.time_last_event
		self.time_last_event = self.current_time
		self.area_num_in_q += (self.num_in_q * self.time_since_last_event)

		#calculate server utilisation for all the servers
		for i in range (0,self.num_servers):
			self.area_server_status[i] += (self.server_status[i] * self.time_since_last_event)

	def run(self):

		#The simulator should run for 1 working day at the travel agency i.e 960 minutes
		while (self.current_time < 960):
			self.timing()
			self.update_time_avg_stats()
			if (self.next_event_type == 0):
				self.arrive()
			else:
				self.depart()
		self.report()


	def print_stats(self):
		#for debugging system stats at any point
		print ("-" * 20)
		print (self.next_event_type)
		print (self.current_time)
		print (self.server_status)
		print (self.num_in_q)
		print ("-" * 20)
