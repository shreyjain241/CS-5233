# CS-5233
Simulation and Modelling Techniques


#Steps:
1) Clone Repo
2) Run main.py to start the simulations
3) Look at the results in the results.csv file


#Overall flow of main.py:
 - calls initializes and runs multiple instances of the MultiTerminal_Simulator class.
 - runs 1000 simulations for each value of lambda1, lambda2 and #terminals. 
 - number of simulations per config can be changed by changing the variable (N)
 - Mean and Standard Deviations of the entities of interest are written to results.csv


#Entities of Interest:
- Average Delay per customer
- Number of customers delayed
- Percentage customers who waited more than 5 mins
- Percentage customers who waited less than 4 mins

#Notes on the Simulator:
- The simulation ends in 16 hours (simulation time). This is because we want to simulate the operation of the travel agency office. 
- There are no limits on length of queue or number of customers delayed/served
- It is necessary to run the simulation many times and take the mean because results vary significantly between each run using the same parameters
