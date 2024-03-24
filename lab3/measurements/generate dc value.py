import nifgen
import sys

with nifgen.Session("PXI-5402") as session:
    session.output_mode = nifgen.OutputMode.FUNC
    session.load_impedance = -1.0;
    session.configure_standard_waveform(waveform=nifgen.Waveform.DC, amplitude=0.0, frequency=0, dc_offset=0.0, start_phase=0.0)
    with session.initiate():
        value = 0.0;
        print('Generation dc voltage...')
        while True:
            try:
                print('Press "+" to increment voltage and "-" to decrement by 1 Volt or just a number from -10. to 10 V and then "Enter" or press Ctrl+C to exit')
                bp = input()
                if bp == '+':
                    value += 0.5
                elif bp == '-':
                    value -= 0.5
                elif float(bp)>= -10.0 and float(bp)<= 10.0:
                    value = float(bp)/2
                session.configure_standard_waveform(waveform=nifgen.Waveform.DC, amplitude=0.0, frequency=0,
                                                    dc_offset=value, start_phase=0.0)
            except KeyboardInterrupt:
                print("to be able to exit script gracefully")
                sys.exit()

