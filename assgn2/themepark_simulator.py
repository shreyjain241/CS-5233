import numpy as np


class SingaporeThemePark(object):
	"""Entity : Theme Park"""

	def __init__(
		self,
		num_docks_per_attraction, 
		num_bicycles_per_attraction, 
		run_length,
		random_seed,
		mean_inter_arrival,
		triangular_left,
		triangular_mode,
		triangular_right,
		mean_timespent,
		std_timespent
		):

		#INITIALIZATIONS
		np.random.seed(random_seed)

		#STATE VARIBLES
		self.last_event_time = 0.0
		self.current_time = 0.0
		self.event_list = []
		self.total_visitors = 0
		self.visitors_departed = 0
		self.visitors_in_park = []
		self.all_visitors = []
		

		#PROPERTIES
		self.run_length = run_length
		self.mean_inter_arrival = mean_inter_arrival
		self.triangular_left = triangular_left
		self.triangular_mode = triangular_mode
		self.triangular_right = triangular_right
		self.mean_timespent = mean_timespent
		self.std_timespent = std_timespent

		self.num_docks_per_attraction = num_docks_per_attraction
		self.num_bicycles_per_attraction = num_bicycles_per_attraction
		self.attractions = [
			Attraction(0,self.num_docks_per_attraction,self.num_bicycles_per_attraction,2.0,0), 
			Attraction(1,self.num_docks_per_attraction,self.num_bicycles_per_attraction,2.5, self.num_docks_per_attraction), 
			Attraction(2,self.num_docks_per_attraction,self.num_bicycles_per_attraction,3.0, 2*self.num_docks_per_attraction), 
			Attraction(3,self.num_docks_per_attraction,self.num_bicycles_per_attraction,1.0, 3*self.num_docks_per_attraction)
			]

		#STATISTICAL COUNTERS
		self.time_snapshot = []
		self.visitors_in_park_snapshot = []

		self.pickup_queue_total_snapshot = []
		self.pickup_queue_snapshot = [[] for i in range(0,4)]

		self.dropoff_queue_total_snapshot = []
		self.dropoff_queue_snapshot = [[] for i in range(0,4)]

		self.total_queue_snapshot = []

		self.avg_pickup_delay_snapshot = [[] for i in range(0,4)]
		self.avg_dropoff_delay_snapshot = [[] for i in range(0,4)]

		self.total_delay = 0.0
		self.total_delay_per_visitor = 0.0

		self.total_delay_per_visitor_snapshot = []

		self.arrivals = [0] * 4
		self.arrivals_snapshot = [[] for i in range(0,4)]

		self.avg_waiting_times_per_visitor = []

		self.happy_visitors = 0
		self.unhappy_visitors = 0
		self.percentage_happy_snapshot = []


	def __repr__(self):
		return "{}".format("The Singpore Theme Park")


	def simulate(self):

		#schedule first arrival into park
		self.event_list.append(Event(
			self.arrival_in_park, 
			np.random.exponential(scale=self.mean_inter_arrival),
			np.random.randint(0,4),
			self.create_new_visitor()))


		while (self.current_time<self.run_length):
			self.event_list.sort(reverse=True)
			self.timing()

	def timing(self):

		#Move system clock
		current_event = self.event_list.pop()
		self.last_event_time = self.current_time
		self.current_time = current_event.event_time

		#Update Statistical Counters
		self.update_statistical_counters()


		'''

		print ([self.current_time,
			len(self.visitors_in_park),self.percentage_happy_snapshot[-1]])
		print ([ 
			len(self.attractions[0].pickup_queue),
			len(self.attractions[1].pickup_queue),
			len(self.attractions[2].pickup_queue),
			len(self.attractions[3].pickup_queue)
			])
		print ([ 
			len(self.attractions[0].dropoff_queue),
			len(self.attractions[1].dropoff_queue),
			len(self.attractions[2].dropoff_queue),
			len(self.attractions[3].dropoff_queue)
			])

		print ("\n")

		'''

		#execute event
		current_event.event(current_event.event_location,current_event.event_owner)


	def update_statistical_counters(self):
		
		#update system_time snapshot
		self.time_snapshot.append(self.current_time)

		#update visitors in park snapshot
		self.visitors_in_park_snapshot.append(len(self.visitors_in_park))

		#update queue counts
		total_pickup_queue = 0
		total_dropoff_queue = 0
		total_queue = 0

		for i in range(0,4):
			self.pickup_queue_snapshot[i].append(len(self.attractions[i].pickup_queue))
			total_pickup_queue += len(self.attractions[i].pickup_queue)
			self.dropoff_queue_snapshot[i].append(len(self.attractions[i].dropoff_queue))
			total_dropoff_queue += len(self.attractions[i].dropoff_queue)
			total_queue += (len(self.attractions[i].pickup_queue))
			total_queue += (len(self.attractions[i].dropoff_queue))

		self.pickup_queue_total_snapshot.append(total_pickup_queue)
		self.dropoff_queue_total_snapshot.append(total_dropoff_queue)
		self.total_queue_snapshot.append(total_queue)


		#update waiting times for visitors
		time_since_last_event = (self.current_time - self.last_event_time)
		for i in range(0,4):
			for visitor in self.attractions[i].pickup_queue:
				visitor.pickup_waiting_time[i] += time_since_last_event
				visitor.total_waiting_time += time_since_last_event
			for visitor in self.attractions[i].dropoff_queue:
				visitor.dropoff_waiting_time[i] += time_since_last_event
				visitor.total_waiting_time += time_since_last_event


		#update average delay snapshots
		for i in range(0,4):
			self.avg_pickup_delay_snapshot[i].append(self.attractions[i].avg_pickup_delay)
			self.avg_dropoff_delay_snapshot[i].append(self.attractions[i].avg_dropoff_delay)

		self.total_delay_per_visitor_snapshot.append(self.total_delay_per_visitor)

		#update arrivals snapshots
		for i in range(0,4):
			self.arrivals_snapshot[i].append(self.arrivals[i])

		#Update % happy visitors
		denominator = self.happy_visitors+self.unhappy_visitors
		if denominator == 0:
			self.percentage_happy_snapshot.append(0.0)
		else:
			self.percentage_happy_snapshot.append(self.happy_visitors/denominator)


	def create_new_visitor(self):
		new_id = self.total_visitors + 1
		self.total_visitors += 1
		num_attraction_visit_intent = np.random.randint(2,5)
		speed = np.random.triangular(self.triangular_left,self.triangular_mode,self.triangular_right)
		return Visitor(new_id, num_attraction_visit_intent, speed)


	def arrival_in_park(self, location, visitor):

		#schedule next arrival uniformly between the attractions

		self.event_list.append(Event(
			self.arrival_in_park, 
			self.current_time + np.random.exponential(scale=self.mean_inter_arrival),
			np.random.randint(0,4),
			self.create_new_visitor())
		)

		#visitors arrive at the attraction which has zero pickup queue and the longest dropoff queue
		#if dropoff queues are zero, visitors arrive at the location just before the largest pickup queue

		'''
		dropoff_queues_at_attractions = [len(self.attractions[i].dropoff_queue) for i in range(0,4)]
		longest = max(dropoff_queues_at_attractions)
		idx = [index for index, element in enumerate(dropoff_queues_at_attractions) if longest == element]


		if not all([dropoff_queues_at_attractions[i] for i in idx]):
			pickup_queues_at_attractions = [len(self.attractions[i].pickup_queue) for i in range(0,4)]
			longest = max(pickup_queues_at_attractions)
			idx2 = [index for index, element in enumerate(pickup_queues_at_attractions) if longest == element]
			idx = [i-1 for i in idx2]
			idx = list(map(lambda x: 3 if x==-1 else x, idx))


		self.event_list.append(Event(
			self.arrival_in_park, 
			self.current_time + np.random.exponential(scale=self.mean_inter_arrival),
			np.random.choice(idx),
			self.create_new_visitor())
		)

		'''

		#increment park visitor count
		self.visitors_in_park.append(visitor)
		self.all_visitors.append(visitor)

		#start visiting the attraction that the visitor arrived at
		visitor.attractions_left -= 1
		self.attractions[location].num_current_visitors += 1

		#schedule finish_attraction_visit event or depart_from_park event
		if visitor.attractions_left > 0:
			self.event_list.append(Event(
				self.finish_attraction_visit,
				self.current_time + np.random.normal(loc=self.mean_timespent, scale=self.std_timespent),
				location,
				visitor)
				)
		else:
			self.event_list.append(Event(
				self.depart_from_park,
				self.current_time + np.random.normal(loc=self.mean_timespent, scale=self.std_timespent),
				location,
				visitor)
				)

		#increment arrivals by location
		self.arrivals[location] += 1


	def finish_attraction_visit(self, location, visitor):

		#decrement visitors at attraction
		self.attractions[location].num_current_visitors -= 1

		#check if there is no queue to pickup bicycle
		if not self.attractions[location].pickup_queue:

			#search for available bicycle in each dock
			bicycle_not_found = True
			for dock in self.attractions[location].docks:

				#pick up the first available bicyle
				if dock.state:

					bicycle_not_found = False

					#change properties of visitor, biycle and dock
					visitor.bicycle = dock.bicycle_at_dock

					visitor.bicycle.visitor = visitor
					visitor.bicycle.docked_at_attraction = None
					visitor.bicycle.docked_at_dock = None
					visitor.bicycle.docked = False
					visitor.bicycle.in_transit = True

					dock.state = False
					dock.bicycle_at_dock = None

					#update waiting times at attraction
					self.attractions[location].num_pickups_delayed += 1
					self.attractions[location].total_pickup_delay += visitor.pickup_waiting_time[location]
					self.attractions[location].avg_pickup_delay = self.attractions[location].total_pickup_delay/self.attractions[location].num_pickups_delayed

					#schedule arrival_on_bicycle event
					if location == 3:
						next_location = 0
					else:
						next_location = location + 1

					time_to_destination = 60*self.attractions[location].distance/visitor.speed

					self.event_list.append(Event(
						self.arrival_on_bicycle,
						self.current_time + time_to_destination,
						next_location,
						visitor)
						)

					#increment intransit count
					self.attractions[location].num_current_intransit += 1

					#check if there is a queue for drop-off
					if self.attractions[location].dropoff_queue:

						#get dropoff_visitor from queue
						dropoff_visitor = self.attractions[location].dropoff_queue.pop(0)

						#change properties of dropoff visitor, biycle and dock
						dock.state = True
						dock.bicycle_at_dock = dropoff_visitor.bicycle

						dropoff_visitor.bicycle.visitor = None
						dropoff_visitor.bicycle.docked_at_attraction = location
						dropoff_visitor.bicycle.docked_at_dock = dock
						dropoff_visitor.bicycle.docked = True
						dropoff_visitor.bicycle.in_transit = False


						dropoff_visitor.bicycle = None
						#dropoff_visitor.delayed_at_dropoff[location] = 1

						#update waiting times at attraction
						self.attractions[location].num_dropoffs_delayed += 1
						self.attractions[location].total_dropoff_delay += dropoff_visitor.dropoff_waiting_time[location]
						self.attractions[location].avg_dropoff_delay = self.attractions[location].total_dropoff_delay/self.attractions[location].num_dropoffs_delayed


						#start visiting the attraction that the visitor arrived at
						dropoff_visitor.attractions_left -= 1
						self.attractions[location].num_current_visitors += 1

						#schedule finish_attraction_visit event or depart_from_park event for dropoff_visitor
						if dropoff_visitor.attractions_left > 0:
							self.event_list.append(Event(
								self.finish_attraction_visit,
								self.current_time + np.random.normal(loc=self.mean_timespent, scale=self.std_timespent),
								location,
								dropoff_visitor)
								)
						else:
							self.event_list.append(Event(
								self.depart_from_park,
								self.current_time + np.random.normal(loc=self.mean_timespent, scale=self.std_timespent),
								location,
								dropoff_visitor)
								)

					#stop looking for more bicycles
					break

			if bicycle_not_found:
				#join the pickup queue
				self.attractions[location].pickup_queue.append(visitor)

		else:
			#join the pickup queue
			self.attractions[location].pickup_queue.append(visitor)


	def arrival_on_bicycle(self, location, visitor):

		#decrement intransit count
		if location == 0:
			self.attractions[3].num_current_intransit -= 1
		else:
			self.attractions[location - 1].num_current_intransit -= 1
		
		#check if there is no queue to dropoff bicycle
		if not self.attractions[location].dropoff_queue:
			
			#search for empty dock in each dock
			empty_dock_not_found = True
			for dock in self.attractions[location].docks:

				#dropoff at first available dock
				if not dock.state:
					
					empty_dock_not_found = False

					#change properties of visitor, bicycle and dock
					dock.state = True
					dock.bicycle_at_dock = visitor.bicycle

					visitor.bicycle.visitor = None
					visitor.bicycle.docked_at_attraction = location
					visitor.bicycle.docked_at_dock = dock
					visitor.bicycle.docked = True
					visitor.bicycle.in_transit = False
					
					visitor.bicycle = None

					#update waiting times at attraction
					self.attractions[location].num_dropoffs_delayed += 1
					self.attractions[location].total_dropoff_delay += visitor.dropoff_waiting_time[location]
					self.attractions[location].avg_dropoff_delay = self.attractions[location].total_dropoff_delay/self.attractions[location].num_dropoffs_delayed

					#start visiting the attraction that the visitor arrived at
					visitor.attractions_left -= 1
					self.attractions[location].num_current_visitors += 1

					#schedule finish_attraction_visit event or depart_from_park event for dropoff_visitor
					if visitor.attractions_left > 0:
						self.event_list.append(Event(
							self.finish_attraction_visit,
							self.current_time + np.random.normal(loc=self.mean_timespent, scale=self.std_timespent),
							location,
							visitor)
							)
					else:
						self.event_list.append(Event(
							self.depart_from_park,
							self.current_time + np.random.normal(loc=self.mean_timespent, scale=self.std_timespent),
							location,
							visitor)
							)

					#check if there is a queue for pickup
					if self.attractions[location].pickup_queue:

						#get pickup_visitor from queue
						pickup_visitor = self.attractions[location].pickup_queue.pop(0)

						#change properties of visitor, biycle and dock
						pickup_visitor.bicycle = dock.bicycle_at_dock

						pickup_visitor.bicycle.visitor = pickup_visitor
						pickup_visitor.bicycle.docked_at_attraction = None
						pickup_visitor.bicycle.docked_at_dock = None
						pickup_visitor.bicycle.docked = False
						pickup_visitor.bicycle.in_transit = True

						dock.state = False
						dock.bicycle_at_dock = None

						#update waiting times at attraction
						self.attractions[location].num_pickups_delayed += 1
						self.attractions[location].total_pickup_delay += pickup_visitor.pickup_waiting_time[location]
						self.attractions[location].avg_pickup_delay = self.attractions[location].total_pickup_delay/self.attractions[location].num_pickups_delayed

						#schedule arrival_on_bicycle event
						if location == 3:
							next_location = 0
						else:
							next_location = location + 1

						time_to_destination = 60*self.attractions[location].distance/pickup_visitor.speed

						self.event_list.append(Event(
							self.arrival_on_bicycle,
							self.current_time + time_to_destination,
							next_location,
							pickup_visitor)
							)

						#increment intransit count
						self.attractions[location].num_current_intransit += 1

					#stop looking for more docks
					break

			if empty_dock_not_found:
				#join the dropoff queue
				self.attractions[location].dropoff_queue.append(visitor)	

		else:
			#join the dropoff queue
			self.attractions[location].dropoff_queue.append(visitor)		


	def depart_from_park(self, location, visitor):
		self.attractions[location].num_current_visitors -= 1
		self.visitors_in_park.remove(visitor)
		self.visitors_departed +=1
		self.total_delay += visitor.total_waiting_time
		self.total_delay_per_visitor = self.total_delay/self.visitors_departed

		visitor.avg_waiting_time = visitor.total_waiting_time/(visitor.intent*2-2)
		self.avg_waiting_times_per_visitor.append(visitor.avg_waiting_time)

		if visitor.avg_waiting_time<=5:
			visitor.happy=True
			self.happy_visitors += 1
		else:
			visitor.happy=False
			self.unhappy_visitors += 1
		

class Attraction(object):
	"""Entity : Attraction"""

	def __init__(self, _id, num_docks, num_bicycles, distance, dock_id_range):

		#STATE VARIBLES
		
		#PROPERTIES
		self.id = _id
		self.num_docks = num_docks
		self.num_bicycles = num_bicycles
		self.distance = distance
		self.docks = []
		for i in range(0,self.num_docks):
			self.docks.append(Dock(dock_id_range + i, self,i<self.num_bicycles))
		self.num_current_visitors = 0
		self.num_current_intransit = 0

		self.pickup_queue = []
		self.dropoff_queue = []


		#STATISTICAL COUNTERS
		self.total_pickup_delay = 0.0
		self.total_dropoff_delay = 0.0
		self.num_pickups_delayed = 0
		self.num_dropoffs_delayed = 0
		self.avg_pickup_delay = 0.0
		self.avg_dropoff_delay = 0.0

	def __repr__(self):
		return "{:d}".format(self.id)


class Dock(object):
	"""Entity : Attraction"""

	def __init__(self,_id, at_attraction, init_with_bicycle):
		
		#STATE VARIBLES
		self.state = False
		
		#PROPERTIES
		self.id = _id
		self.attraction = at_attraction
		if init_with_bicycle:
			self.bicycle_at_dock = Bicycle(self.id,at_attraction,self)
			self.state = True
	
	def __repr__(self):
		return "{:d}".format(self.id)


class Bicycle(object):
	"""Entity : Attraction"""

	def __init__(self,_id, starting_attraction, starting_dock):

		#STATE VARIBLES
		self.docked = True
		self.in_transit = False

		#PROPERTIES
		self.id = _id
		self.visitor = None
		self.docked_at_attraction = starting_attraction
		self.docked_at_dock = starting_dock

	def __repr__(self):
		return "{:d}".format(self.id)



class Event(object):
	"""Events"""

	def __init__(self, event, event_time, event_location, event_owner):
		self.event_time = event_time
		self.event_location = event_location
		self.event_owner = event_owner
		self.event = event

	def __lt__(self, other):
		return self.event_time < other.event_time

	def __repr__(self):
		return "{}".format(self.event)




class Visitor(object):
	"""Visitor"""

	def __init__(self, _id, num_attraction_visit_intent,speed):

		#PROPERTIES
		self.id = _id
		self.intent = num_attraction_visit_intent
		self.speed = speed
		self.bicycle = None
		self.attractions_left = self.intent

		#STATISTICAL COUNTERS
		self.pickup_waiting_time = [0.0] * 4
		self.dropoff_waiting_time = [0.0] * 4
		self.total_waiting_time = 0.0
		self.avg_waiting_time = 0.0
		self.happy = None

		
	def __repr__(self):
		return "{:d}".format(self.id)
		

def main():
	num_docks = 80
	num_bicycles = 80
	run_length = 52560
	random_seed = 2
	mean_inter_arrival = 2.7942875
	triangular_left = 10
	triangular_mode = 20
	triangular_right = 30
	mean_timespent = 29.988125
	std_timespent = 5.0959956323


	park = SingaporeThemePark(
		num_docks, 
		num_bicycles, 
		run_length,
		random_seed,
		mean_inter_arrival,
		triangular_left,
		triangular_mode,
		triangular_right,
		mean_timespent,
		std_timespent
		)

	park.simulate()

main()