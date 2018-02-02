from multi_terminal_simulator import MultiServer_Simulator


#To run the simulator once for a given value of mean inter-arrival, and #terminals.

mean_inter_arrival = float(input("\nMean Inter-arrival Time?\n"))
mean_service = float(input("\nMean Service Time?\n"))
num_terminals = int(input("\nNumber of Terminals?\n"))

simulator = MultiServer_Simulator(mean_inter_arrival,mean_service, num_terminals)
simulator.run()
simulator.print_report()

