# T. Atkins, 2024
import sys
import pandas as pd
from string import digits


def mk_spring_testing(
    finger: int,
    loc: str,
    alpha: int | float,
    thick_raw: int,
    preload_raw: int,
    shape="triangle",
    mode="prototype",
    save_mode="manual",
    comment="-",
) -> None:
    """
    FUNCTION
    > Unlike apply_heuristics(), which generates springs based on pre-set rules, this function serves to manually generate springs given user-specified spring parameters
    > The process of "generating" and "saving" a spring relies fundamentally on two CSV files: the 'parameter' file and the 'tracker' file
    > The parameter file contains the pin spacing (d), alpha and thickness values for a given spring, and is in a format that can be read automatically by Autodesk Inventor CAD (as a result, it is not particularly human-readable)
    > The tracker file stores the parameters of the generated spring in a more human-readable format, allowing for easy lookup when writing test reports etc.
    > NB-1: The parameter file also contains the (fixed) measurements of the user's hand (e.g. range-of-motion (ROM) and pin spacing at max. ROM without preload)
    > NB-2: This process, or 'pipeline', for spring generation is explained in more detail in the report itself
    """
    # Input type checking
    if (
        not isinstance(finger, int)
        or not isinstance(loc, str)
        or not isinstance(alpha, (int, float))
        or not isinstance(thick_raw, int)
        or not isinstance(preload_raw, int)
        or shape not in ["triangle", "bell"]
        or mode not in ["prototype", "final"]
        or save_mode not in ["manual", "yes", "no"]
        or not isinstance(comment, str)
    ):
        raise Exception("Parameter error.")

    # Given the numeric finger integer passed to the function, assign a finger name
    # NB: This name is used in the parameter CSV, e.g. 'index01' refers to the pin spacing for the (from proximal to distal) first spring on the index
    finger_lst = ["thumb", "index", "middle", "ring", "little"]
    finger_select = finger_lst[finger - 1]
    phalange = finger_select + loc

    # Convert inputs
    thick = thick_raw / 10
    preload = preload_raw / 100
    alpha = round(alpha)

    # Parameter file location
    FILE_LOC = "[INSERT PATH TO PARAMETER CSV HERE]"
    # Tracker file location
    TRACKER_LOC = "[INSERT PATH TO TRACKER CSV HERE]"

    # Retrieve the measured pin spacing at max. ROM for the selected finger and apply the preload to compute the pin spacing (d) of the spring
    COL1_NAME = "param"
    COL2_NAME = "value"
    COL3_NAME = "unit"
    df = pd.read_csv(
        FILE_LOC,
        names=[COL1_NAME, COL2_NAME, COL3_NAME],
        usecols=[0, 1, 2],
        dtype={COL1_NAME: str, COL2_NAME: float, COL3_NAME: str},
    )
    try:
        d_base = df.loc[df[COL1_NAME] == phalange][COL2_NAME].iloc[0]
    except:
        exit("ERROR: Pin spacings not located in reference CSV.")
    d = d_base * (1 + preload)

    ALPHA_PREFIX = "a"
    D_PREFIX = "d"
    THICK_PREFIX = "t"

    # Generate a unique ID for the new spring (this is the same process as in save_spring())
    tail = df.tail(1).iloc[0, 0]
    numeric_tail = "".join(c for c in tail if c in digits)
    letter_tail = "".join(i for i in tail if not i.isdigit())
    if numeric_tail == "" or letter_tail not in [ALPHA_PREFIX, D_PREFIX, THICK_PREFIX]:
        id_str = "001"
    else:
        id_str = str(int(numeric_tail) + 1).zfill(3)

    # Store the d, alpha and thickness of the new spring in a DataFrame
    new_spring = pd.DataFrame(
        [
            [D_PREFIX + id_str, d, "mm"],
            [ALPHA_PREFIX + id_str, alpha, "deg"],
            [THICK_PREFIX + id_str, thick, "mm"],
        ]
    )

    # Generate the spring code for storage in the tracker file (the structure of this code is detailed in the report and details all characteristics of the spring) and store it in a DataFrame
    if shape == "triangle":
        name_code = "T"
    else:
        name_code = "B"

    if mode == "prototype":
        mode_code = "P"
    else:
        mode_code = "F"
    code_str = f"{name_code}({mode_code})-{finger_lst[finger-1]}{loc}-{str(alpha).zfill(3)}.{str(thick_raw).zfill(2)}.{str(preload_raw).zfill(2)}"
    new_code = pd.DataFrame([[id_str, code_str, comment]])

    print(f"Specification for spring {id_str}:")
    print(new_spring.to_string(index=False, header=False))
    print(f"Spring code: {code_str}")

    # Append the details of the new spring to the relevant CSV file
    if (
        save_mode == "manual"
    ):  # in this mode the user provides input for every spring; for later programmatic spring generation, "yes" and "no" overrides are provided
        save = input("Confirm storing of new spring (y/n): ")
        if save == "y":
            new_spring.to_csv(FILE_LOC, index=False, header=False, mode="a")
            new_code.to_csv(TRACKER_LOC, index=False, header=False, mode="a")
            save_bool = True
        else:
            save_bool = False
    elif save_mode == "yes":
        new_spring.to_csv(FILE_LOC, index=False, header=False, mode="a")
        new_code.to_csv(TRACKER_LOC, index=False, header=False, mode="a")
        save_bool = True
    else:
        save_bool = False
    print(f"Saved: {save_bool}")
    print("-----")


if __name__ == "__main__":
    # The below allows for this function to (alternatively) be run from the command line with: 'python mkspring.py [finger] [loc] [alpha] [thick] [preload]'
    finger = int(sys.argv[1])
    loc = str(sys.argv[2])
    alpha = float(sys.argv[3])
    thick = int(sys.argv[4])
    preload = int(sys.argv[5])

    mk_spring_testing(finger, loc, alpha, thick, preload)
