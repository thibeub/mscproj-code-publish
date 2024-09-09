# T. Atkins, 2024
import sys
from package.plotting import plotting


def plotting_main(save: bool = False) -> None:
    """
    FUNCTION
    > Run plotting functions (located in the 'package' directory) based on user CLI input
    """
    plotting(save)


if __name__ == "__main__":
    # The below allows for this function to be run from the command line with: 'python plotting_main.py [save]' ([save] is optional, default is False)
    try:
        SAVE = str(sys.argv[1])
        if SAVE == "y":
            SAVE = True
        else:
            SAVE = False
    except:
        SAVE = False

    plotting_main(SAVE)
