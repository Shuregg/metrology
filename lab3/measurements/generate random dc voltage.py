import nifgen
import sys
import random

with nifgen.Session("PXI-5402") as session:
    session.output_mode = nifgen.OutputMode.FUNC
    session.load_impedance = -1.0;
    with session.initiate():
        value = random.uniform(-5, 5)
        print('Generating random dc voltage')
        print('Press  Ctrl+C to exit')
        while True:
            try:
                session.configure_standard_waveform(waveform=nifgen.Waveform.DC, amplitude=0.0, frequency=0,
                                                    dc_offset=value, start_phase=0.0)
            except KeyboardInterrupt:
                print("to be able to exit script gracefully")
                sys.exit()

