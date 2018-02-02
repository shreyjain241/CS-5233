from multi_terminal_simulator import MultiServer_Simulator
import csv

def main():
	#main function that calls the MultiServer Simulator

	#How many iterations to run per config of lambda1 lambda2 and Terminals?
	N = 1000

	#write simulation results to a csv file
	results = open("results.csv", "w")
	csv_writer = csv.writer(results, delimiter=",",
                            quotechar="'", quoting=csv.QUOTE_MINIMAL)
	csv_writer.writerow(["Mean Interarrival Time", "Mean Service Time", "Number of Terminals",
		"Mean Avg Waiting Time", "Std Average Waiting Time",
		"Mean Customers Delayed", "Std Customers Delayed",
		"Mean Percentage > 5min Delay", "Std Percentage > 5min Delay",
		"Mean Percentage < 4min Delay", "Std Percentage < 4min Delay"])

	#define result variables

	avg_waiting_time = [0.0] * N
	customers_delayed = [0.0] * N
	perc_5mins = [0.0] * N
	perc_4mins = [0.0] * N

	#run the simulator N times for each value of lambda1, lambda2 and Terminals to ensure uniformity of data
	for lambda1 in range (5,15):
		for lambda2 in range (5,15):
			for num_terminals in range(1,6):
				for i in range(0,N):
					simulator = MultiServer_Simulator(lambda1,lambda2,num_terminals)
					simulator.run()
					avg_waiting_time[i] = simulator.avg_delay
					customers_delayed[i] = simulator.num_custs_delayed
					perc_5mins[i] = simulator.percentage_more_than_5_mins
					perc_4mins[i] = simulator.percentage_less_than_4_mins
				



					#print progress of the iterations on terminal
					print ("-" * 20)
					print ("Mean Interarrival: {:d} minutes".format(lambda1))
					print ("Mean Service: {:d} minutes".format(lambda2))
					print ("Number of Terminals: {:d}".format(num_terminals))
					print ("Iteration : {:d}/{:d}".format((i+1),N))
					print ("-" * 20)

				#write mean and standard deviation data to CSV
				csv_writer.writerow([lambda1,lambda2,num_terminals, 
					round(mean(avg_waiting_time)),round(stddev(avg_waiting_time)),
					round(mean(customers_delayed)),round(stddev(customers_delayed)),
					round(mean(perc_5mins)*100,1), round(stddev(perc_5mins)*100,1),
					round(mean(perc_4mins)*100,1),round(stddev(perc_4mins)*100,1)])

	results.close()


# function definitions for mean and variance

def mean(data):
    #Return the sample arithmetic mean of data.
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n

def _ss(data):
    #Return sum of square deviations of sequence data.
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def stddev(data, ddof=0):
    #Calculates the population standard deviation
    #by default; specify ddof=1 to compute the sample
    #standard deviation.
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/(n-ddof)
    return pvar**0.5






	#simulator.print_report()

main()