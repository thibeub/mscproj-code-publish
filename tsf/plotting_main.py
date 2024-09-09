# T. Atkins, 2024
import sys
from package.plotting import plotting_standard, plotting_fatigue


def plotting_main(mode: str, save: bool = False):
    """
    FUNCTION
    > Run different plotting functions (located in the 'package' directory) based on user CLI input
    """
    mode = mode.upper()
    if mode == "STD":
        TEST_CODE = input("Enter test code: ").capitalize()
        plotting_standard(test_code=TEST_CODE, save=save)
    elif mode == "F-LOAD":
        TEST_CODE = input("Enter test code: ").capitalize()
        plotting_fatigue(mode="load", test_code=TEST_CODE, save=save)
    elif mode == "F-LEN":
        TEST_CODE = input("Enter test code: ").capitalize()
        plotting_fatigue(mode="len", test_code=TEST_CODE, save=save)
    else:
        exit(
            f"ERROR: Plotting mode '{mode}' not recognised: must be 'STD', 'F-LOAD' or 'F-LEN' (not case-sensitive)."
        )


if __name__ == "__main__":
    # The below allows for this function to be run from the command line with: 'python plotting_main.py [mode] [save]' ([save] is optional, default is False)
    try:
        MODE = str(sys.argv[1])
    except:
        exit("ERROR: Please specify a plotting mode.")

    try:
        SAVE = str(sys.argv[2])
        if SAVE == "y":
            SAVE = True
        else:
            SAVE = False
    except:
        SAVE = False

    plotting_main(MODE, SAVE)
