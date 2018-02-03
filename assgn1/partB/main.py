from TelephonySimulator import TelephonySimulator

#Calls originating from X and Y and call lengths are exponentially distributed
mean_calls_X = 12
mean_calls_Y = 15
mean_call_length = 300

#sytem in place. 1 for unidirectional old system. 2 for new bidirectional system
system = 2

#channels in place from X to Y and Y to X. Channels will be assumed bidirectional if system=2
channels_X2Y = 20
channels_Y2X = 20

#number of calls to run the simulation for. The simulation will end when N calls have originated
N = 1000


simulator = TelephonySimulator(mean_calls_X,mean_calls_Y,mean_call_length,system,channels_X2Y,channels_Y2X,N)
simulator.run()
simulator.report()