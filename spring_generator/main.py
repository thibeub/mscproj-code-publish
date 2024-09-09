# T. Atkins, 2024
from package.mk_spring_testing import mk_spring_testing
from package.apply_heuristics import apply_heuristics

# from spring_generator.package.tests import tests


def main() -> None:
    """
    FUNCTION
    > Run various functions (mainly with the aim of generating springs) contained in the 'package' directory
    > NB-1: The contents of this main() function do not reflect the entire use history of this function throughout ALL testing, but rather examples/snapshots of its use
    > NB-2: See further details in the comments of the functions of the 'package' directory
    """
    # Code to MANUALLY create springs using mk_spring_testing()
    # # TSF Test A: vary thickness (75%, 100%, 125%)
    # SAVE_MODE = "yes"
    # print("Test A: vary thickness")
    # mk_spring_testing(2, "12", 80, 12, 0, save_mode=SAVE_MODE, comment="TSF-testA")
    # mk_spring_testing(2, "12", 80, 16, 0, save_mode=SAVE_MODE, comment="TSF-testA")
    # mk_spring_testing(2, "12", 80, 20, 0, save_mode=SAVE_MODE, comment="TSF-testA")
    # print("***")
    # # TSF Test B: vary alpha (75%, 100%, 125%)
    # print("Test B: vary alpha")
    # mk_spring_testing(2, "12", 60, 16, 0, save_mode=SAVE_MODE, comment="TSF-testB")
    # mk_spring_testing(2, "12", 80, 16, 0, save_mode=SAVE_MODE, comment="TSF-testB")
    # mk_spring_testing(2, "12", 100, 16, 0, save_mode=SAVE_MODE, comment="TSF-testB")
    # print("***")
    # # TSF Test C: vary preload (i.e. pin spacing)
    # print("Test C: vary preload")
    # mk_spring_testing(2, "12", 80, 16, 0, save_mode=SAVE_MODE, comment="TSF-testC")
    # mk_spring_testing(2, "12", 80, 16, 10, save_mode=SAVE_MODE, comment="TSF-testC")
    # mk_spring_testing(2, "12", 80, 16, 30, save_mode=SAVE_MODE, comment="TSF-testC")

    # ---------------#

    # Use HEURISTICS to generate springs, i.e. using apply_heuristics()
    # -> Author's hand
    PARAM_FILE = "[INSERT PATH TO PARAMETER CSV (HUMAN) HERE]"
    TRACKER_FILE = "[INSERT PATH TO TRACKER CSV (HUMAN) HERE]"
    # -> Passive hand
    PARAM_FILE = "[INSERT PATH TO PARAMETER CSV (PASSIVE HAND) HERE]"
    TRACKER_FILE = "[INSERT PATH TO TRACKER CSV (PASSIVE HAND) HERE]"
    apply_heuristics(
        PARAM_FILE,
        TRACKER_FILE,
        policy="batchC",
        batch_code="Batch C",
        save_fingers="all",
    )


if __name__ == "__main__":
    main()
