# T. Atkins
# NOTE: Close Arduino IDE Serial Monitor and any other applications communicating over COM ports before running

import serial  # WARNING: refers to a package installed with 'pip install pyserial', NOT 'pip install serial'
import numpy as np
from os import listdir
from os.path import isfile, join


def tsf_rx(test_code: str, test_num: int):
    """
    FUNCTION
    > Read data from sent over serial sent by an Arduino, in this case readouts from a load cell
    > Store retrieved data in a CSV upon receiving the code '1000'
    > Terminate test upon receiving the code '2000'
    """
    # Data storage setup
    FOLDER = "output/"
    FNAME = f"test{test_code}_{str(test_num).zfill(3)}.csv"
    FFULL = FOLDER + FNAME
    files_lst = [f for f in listdir(FOLDER) if isfile(join(FOLDER, f))]
    if FNAME in files_lst:  # overwrite protection
        print("WARNING: Current output file name matches existing file.")
        proceed = input(
            "Type 'c' to continue and overwrite, or any other key to halt: "
        )
        if proceed != "c":
            print("Execution halted to avoid overwrite.")
            exit()

    store = np.zeros((50, 2))
    idx = 0

    # Communication with Arduino over serial
    port = "COM3"  # change as needed
    rate = 9600  # ensure this matches the value in the Arduino code
    arduino = serial.Serial(port=port, baudrate=rate, timeout=0.1)
    readout_prev = 0.0

    # pcts = [0.5]
    pcts = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

    while True:
        try:
            data = arduino.readline().decode().strip()
        except:
            raise Exception("Issue with serial communication, re-run program.")

        if data:
            readout = float(data)
            print(f"Raw: {readout}")
            if readout == 1000:
                # Record data point
                store[idx, 0] = abs(readout_prev)
                # comp = input("Input compression in mm: ")
                # comp = float(comp)
                comp = pcts[idx]
                store[idx, 1] = comp
                print(f"Stored {readout_prev} kg LOAD @ {int(comp*100)} % COMPRESSION.")
                idx += 1
            elif readout == 2000:
                # Save to CSV
                store = store[~np.all(store == 0, axis=1)]  # remove trailing zeros
                np.savetxt(FFULL, store, delimiter=",")
                print(f"Test data stored in {FFULL}. Terminating test.")
                break
            else:
                pass
            readout_prev = readout  # this ensures that the codes ('1000' and '2000') are not stored as load data


if __name__ == "__main__":
    tsf_rx("fC", 31)
