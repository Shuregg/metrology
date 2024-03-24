
import nidmm
import time
import sys
import numpy as np


sample = []

with nidmm.Session("PXI-4065") as session:
    while True:
        try:
            session.configure_measurement_digits(nidmm.Function.DC_VOLTS, 10, 5.5)
            sample.append(session.read()) 
            print("Measurement: " + str(session.read()))
            time.sleep(0.01)
        except KeyboardInterrupt:
            print("to be able to exit script gracefully")
            mean = np.mean(sample)
            f = open("sample %s.txt" %str(mean)[:4], "w+")
            for i in range(len(sample)):            
                f.write("%s\n" % str(sample[i]))
            f.close()
            sys.exit()


