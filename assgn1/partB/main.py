from TelephonySimulator import TelephonySimulator
import csv
import numpy as np

#Calls originating from X and Y and call lengths are exponentially distributed
mean_calls_X = 12
mean_calls_Y = 15
mean_call_length = 300

#sytem in place. 1 for unidirectional old system. 2 for new bidirectional system
system = 2

#channels in place from X to Y and Y to X. Channels will be assumed bidirectional if system=2
channels_X2Y_range = 30
channels_Y2X_range = 30

#number of calls to run the simulation for. The simulation will end when N calls have originated
N = 1000

#number of simulations to run
sims = 100

#total number of simulations to run: for visualising progress
tot_sims = (channels_X2Y_range-10)*(channels_Y2X_range-10)*sims*2

results = open("results.csv", "w")
csv_writer = csv.writer(results, delimiter=",",
                            quotechar="'", quoting=csv.QUOTE_MINIMAL)

csv_writer.writerow([
    "Mean inter-call time at X",
    "Mean inter-call time at Y",
    "Mean call length time",
    "Telephony System",
    "Channels from X to Y",
    "Channels from Y to X",
    "Total calls originated",
    "Total calls patched (mean)",
    "Total calls patched (std)",
    "Total calls blocked (mean)",
    "Total calls blocked (std)",
    "Percentage calls blocked (mean)",
    "Percentage calls blocked (std)",
    "Average Channel Utilisation (mean)",
    "Average Channel Utilisation (std)",
    ])



sim_count = 0
for s in [1,2]:
    for j in range (11,channels_X2Y_range + 1):
        for k in range (11,channels_Y2X_range + 1):
            calls_blocked = [0.0] * sims
            calls_patched = [0.0] * sims
            perc_calls_blocked = [0.0] * sims
            channel_util = [0.0] * sims
            for i in range (0,sims):
                sim_count += 1
                print ("Running simulation : {:d}/{:d}".format(sim_count,tot_sims))
                simulator = TelephonySimulator(mean_calls_X,mean_calls_Y,mean_call_length,s,j,k,N)
                simulator.run()
                calls_blocked[i] = simulator.num_calls_blocked
                calls_patched[i] = simulator.num_calls_patched
                perc_calls_blocked[i] = simulator.num_calls_blocked*100/simulator.total_calls
                util = [o.utilisation/simulator.current_time for o in simulator.channels]
                channel_util[i] = np.mean(util)*100
            
            csv_writer.writerow([
                simulator.mean_call_X,
                simulator.mean_call_Y,
                simulator.mean_call_length,
                s,
                j,
                k,
                N,
                round(np.mean(calls_patched)),
                round(np.std(calls_patched)),
                round(np.mean(calls_blocked)),
                round(np.std(calls_blocked)),
                round(np.mean(perc_calls_blocked),1),
                round(np.std(perc_calls_blocked),1),
                round(np.mean(channel_util),1),
                round(np.std(channel_util),1)
                ])



csv_writer.writerow([
    simulator.mean_call_X,
    simulator.mean_call_Y,
    simulator.mean_call_length,
    simulator.system,
    simulator.channelsX2Y,
    simulator.channelsY2X,
    N,
    round(np.mean(calls_patched)),
    round(np.std(calls_patched)),
    round(np.mean(calls_blocked)),
    round(np.std(calls_blocked)),
    round(np.mean(perc_calls_blocked),1),
    round(np.std(perc_calls_blocked),1),
    round(np.mean(channel_util),1),
    round(np.std(channel_util),1)
    ])

results.close()
#simulator.report()

'''
print ("\n\n")
print ("-" * 50)
print ("SIMULATION COMPLETE")
print ("-" * 50)
print ("\nSystem Configuration\n")
print ("Mean inter-call time at X : {:d} mins".format(simulator.mean_call_X))
print ("Mean inter-call time at Y : {:d} mins".format(simulator.mean_call_Y))
print ("Mean call length time : {:d} mins".format(simulator.mean_call_length))
if (simulator.system == 1):
    print ("Telephony System : Old (uni-directional)")
    print ("Channels from X to Y : {:d}".format(simulator.channelsX2Y))
    print ("Channels from Y to X : {:d}".format(simulator.channelsY2X))
if (simulator.system == 2):
    print ("Telephony System : New (bi-directional)")
    print ("Birectional Channels : {:d}\n".format(simulator.num_channels))
print ("-" * 50)
print ("\nSimulation Results\n")
print ("Simulation Ended at Time : {:.1f} seconds".format(simulator.current_time))
print ("Total calls originated : {:d}".format(simulator.total_calls))
print ("Total calls patched : {:.0f}".format(round(np.mean(calls_patched))))
print ("Total calls blocked : {:.0f}".format(round(np.mean(calls_blocked))))
print ("Percentage calls blocked : {:.2f} %".format(round(np.mean(perc_calls_blocked),1)))
print ("Average Channel Utilisation : {:.2f} %".format(round(np.mean(channel_util),1)))
print ("-" * 50)
print ("\n\n")
'''

