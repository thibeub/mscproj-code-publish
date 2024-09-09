# T. Atkins, 2024
# NOTE: Close Arduino IDE Serial Monitor and any other applications communicating over COM ports before running

import serial  # WARNING: refers to a package installed with 'pip install pyserial', NOT 'pip install serial'
import numpy as np
from os import listdir
from os.path import isfile, join


def ttf_rx(mode: str):
    """
    FUNCTION
    > Read data from sent over serial sent by an Arduino, in this case readouts from a load cell
    > Store retrieved data in a CSV upon receiving the code '1000'
    > Terminate test upon receiving the code '2000'
    > 'mode' indicates the spacing of the T-TF rig
    """
    # Data storage setup
    FOLDER = "output/"
    mode = mode.upper()
    FNAME = f"ttf{mode}.csv"
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

    store = np.zeros((50, 1))
    idx = 0

    # Communication with Arduino over serial
    port = "COM3"  # change as needed
    rate = 9600  # ensure this matches the value in the Arduino code
    arduino = serial.Serial(port=port, baudrate=rate, timeout=0.1)
    readout_prev = 0.0

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
                store[idx] = abs(readout_prev)
                print(f"Stored {readout_prev} kg for finger {idx+2}.")
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
    flag = input(
        "Type '0' for 'LOW' mode, '1' for 'MID', '2' for 'HIGH' and '3' for 'VHIGH': "
    )
    match flag:
        case "0":
            mode = "LOW"
        case "1":
            mode = "MID"
        case "2":
            mode = "HIGH"
        case "3":
            mode = "VHIGH"
        case _:
            exit(f"ERROR: Flag '{flag}' not recognised.")

    ttf_rx(mode)
