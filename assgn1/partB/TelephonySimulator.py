import math
import numpy as np

class TelephonySimulator(object):
	#define class for a telephony simulator

	def __init__ (self, mean_call_X, mean_call_Y, mean_call_length, system, channelsX2Y, channelsY2X,max_calls):
		#initialize an instance of the simulator class with the variables
		"""'system' defines whether the old unidirectional system (1) is in place or the 
		new bidirectional system is in place (2)"""

		self.mean_call_X = mean_call_X
		self.mean_call_Y = mean_call_Y
		self.mean_call_length = mean_call_length
		self.system = system
		self.channelsX2Y = channelsX2Y
		self.channelsY2X = channelsY2X
		self.max_calls = max_calls

		#initialize channels
		self.num_channels = self.channelsX2Y + self.channelsY2X
		self.channels = []
		if (system == 1):
			for i in range(0,self.channelsX2Y):
				channel = Channel(0)
				self.channels.append(channel)
			for i in range(0,self.channelsY2X):
				channel = Channel(1)
				self.channels.append(channel)
		elif (system == 2):
			for i in range (0,self.num_channels):
				channel = Channel(2)
				self.channels.append(channel)
		else:
			raise ValueError("incorrect system {:d} specified. must be either 1 or 2".format(system))


		#initialise system states and counters
		self.current_time = 0.0
		self.time_last_event = 0.0
		self.total_calls = 0
		self.num_calls_patched = 0
		self.num_calls_blocked = 0

		self.event_list = []
		self.event_list.append(Event(0,self.current_time + np.random.exponential(scale=self.mean_call_X),0,-1))
		self.event_list.append(Event(1,self.current_time + np.random.exponential(scale=self.mean_call_Y),0,-1))



	def run(self):
		
		while (self.event_list and self.total_calls<self.max_calls):
			self.timing()
			self.update_stats()
			
			event = self.event_list.pop()
			self.process_event(event)

		#self.report()
		#self.print_report()


	def timing(self):
		
		#sort event list
		self.event_list.sort(key=lambda x: x.time, reverse=True)
		self.current_time = self.event_list[-1].time


	def update_stats(self):
		
		time_since_last_event = self.current_time - self.time_last_event
		self.time_last_event = self.current_time
		for i in range (0,self.num_channels):
			self.channels[i].utilisation += time_since_last_event*self.channels[i].status

	def process_event(self,event):
		if (event.event_type == 0):
			call_patched = False
			self.total_calls +=1
			event.event_id = self.total_calls
			self.event_list.append(Event(0,self.current_time + np.random.exponential(scale=self.mean_call_X),0,-1))
			for i in range(0,self.num_channels):
				if (self.channels[i].X2Y and self.channels[i].status == 0):
					self.num_calls_patched +=1
					call_patched = True
					self.channels[i].engage(event.event_id)
					self.event_list.append(Event(2,self.current_time + np.random.exponential(scale=self.mean_call_length),event.event_id,i))
					break
			if(call_patched != True):
				self.num_calls_blocked +=1
		elif (event.event_type == 1):
			call_patched = False
			self.total_calls +=1
			event.event_id = self.total_calls
			self.event_list.append(Event(1,self.current_time + np.random.exponential(scale=self.mean_call_Y),0,-1))
			for i in range(0,self.num_channels):
				if (self.channels[i].Y2X and self.channels[i].status == 0):
					self.num_calls_patched +=1
					call_patched = True
					self.channels[i].engage(event.event_id)
					self.event_list.append(Event(2,self.current_time + np.random.exponential(scale=self.mean_call_length),event.event_id,i))
					break
			if(call_patched != True):
				self.num_calls_blocked +=1
		elif (event.event_type == 2):
			self.channels[event.channel_id].disengage()
		else:
			raise ValueError ("Wrong Event Type {:d} Passed. Must be 0,1 oe 2".format(event.event_type))


	def report(self):
		print ("\n\n")
		print ("-" * 50)
		print ("SIMULATION COMPLETE")
		print ("-" * 50)
		print ("\nSystem Configuration\n")
		print ("Mean inter-call time at X : {:d} mins".format(self.mean_call_X))
		print ("Mean inter-call time at Y : {:d} mins".format(self.mean_call_Y))
		print ("Mean call length time : {:d} mins".format(self.mean_call_length))
		if (self.system == 1):
			print ("Telephony System : Old (uni-directional)")
			print ("Channels from X to Y : {:d}".format(self.channelsX2Y))
			print ("Channels from Y to X : {:d}".format(self.channelsY2X))
		if (self.system == 2):
			print ("Telephony System : New (bi-directional)")
			print ("Birectional Channels : {:d}\n".format(self.num_channels))
		print ("-" * 50)
		print ("\nSimulation Results\n")
		print ("Simulation Ended at Time : {:.1f} seconds".format(self.current_time))
		print ("Total calls originated : {:d}".format(self.total_calls))
		print ("Total calls patched : {:d}".format(self.num_calls_patched))
		print ("Total calls blocked : {:d}".format(self.num_calls_blocked))
		print ("Percentage calls blocked : {:.2f} %".format(self.num_calls_blocked*100/self.total_calls))
		util = [o.utilisation/self.current_time for o in self.channels]
		print ("Average Channel Utilisation : {:.2f} %".format(np.mean(util)*100))
		print ("-" * 50)
		print ("\n\n")

class Channel(object):

	def __init__(self, direction, call_id=0):
		#initialise a channel

		#set status to 0
		self.status = 0

		#direction specifies which directions of call can a channel accommodate
		if (direction == 0):
			self.X2Y = True
			self.Y2X = False
		elif (direction == 1):
			self.X2Y = False
			self.Y2X = True
		elif (direction == 2):
			self.X2Y = True
			self.Y2X = True
		else:
			raise ValueError("Incorrect direction {:d} specified. must be either 0, 1 or 2".format(direction))

		#set channel utilisation to zero
		self.utilisation = 0.0
		

	def engage(self,call_id):
		#method to engage a channel
		self.status = 1
		self.call_id = call_id

	def disengage(self):
		#method to disengage a channel
		self.status = 0
		self.call_id = 0


class Event(object):
	def __init__(self, event_type, time,event_id,channel_id):
		self.event_type = event_type
		self.time = time
		self.event_id = event_id
		self.channel_id = channel_id
	def __str__ (self):
		return "Event : {:d} at: {:f} call_id {:d} channel_id {:d}".format(self.event_type,self.time,self.event_id,self.channel_id)
	def __repr__ (self):
		return "Event : {:d} at: {:f} call_id {:d} channel_id {:d}".format(self.event_type,self.time,self.event_id,self.channel_id)
		







