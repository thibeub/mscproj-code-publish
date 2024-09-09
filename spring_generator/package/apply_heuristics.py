# T. Atkins, 2024
import math
import numpy as np
import pandas as pd
from package.save_spring import save_spring
from package.thickness_binning import thickness_binning
from typing import Sequence, Union


def apply_heuristics(
    param_file: str,
    tracker_file: str,
    policy: str,
    batch_code: str = "N/A",
    save_fingers: Union[Sequence[str], str] = "all",
) -> None:
    """
    FUNCTION
    > Generate springs based on a selected 'policy'
    > The process of "generating" and "saving" a spring relies fundamentally on two CSV files: the 'parameter' file and the 'tracker' file
    > The parameter file contains the pin spacing (d), alpha and thickness values for a given spring, and is in a format that can be read automatically by Autodesk Inventor CAD (as a result, it is not particularly human-readable)
    > The tracker file stores the parameters of the generated spring in a more human-readable format, allowing for easy lookup when writing test reports etc.
    > NB-1: The parameter file also contains the (fixed) measurements of the user's hand (e.g. range-of-motion (ROM) and pin spacing at max. ROM without preload)
    > NB-2: This process, or 'pipeline', for spring generation is explained in more detail in the report itself
    > For example, a very simplistic policy might state that the alpha of each spring should be proportional to its pin spacing
    > The policies listed below are more multi-faceted, and are more clearly detailed in the report itself
    """
    # List of possible policies
    POLICY_LST = [
        "batchB",
        "batchC",
        "batchD",
        "bin_fixed",
        "bin_lower",
        "bin_adaptive_lower",
        "bin_outlier",
    ]
    if policy not in POLICY_LST:
        exit(f"ERROR: Heuristic policy '{policy}' not recognised.")
    print(f"Applying heuristic policy '{policy}'.")

    # Setup
    FINGER_LST = ["thumb", "index", "middle", "ring", "little"]
    PRELOAD = 30
    ALPHA_SUFFIX = "alpha"

    # For fast prototpying (or the replacement of specific damaged or defective springs), it may not be required to print springs for an entire hand, but rather specific fingers
    if any(item not in FINGER_LST for item in save_fingers) and save_fingers != "all":
        exit("ERROR: Parameter 'save_fingers' contains an incorrect value.")
    if save_fingers == "all":
        save_fingers = FINGER_LST

    # Setup spring thicknesses (the "base" value is 'CENTRE_T')
    T_INCREMENT = 0.4
    CENTRE_T = 1.6
    LOWER_T = np.round(CENTRE_T - T_INCREMENT, 2)
    HIGHER_T = np.round(CENTRE_T + T_INCREMENT, 2)
    T_BINS = np.round([LOWER_T, CENTRE_T, HIGHER_T], 2)

    # Import parameters
    COL1_NAME = "param"
    COL2_NAME = "value"
    COL3_NAME = "unit"
    df_param = pd.read_csv(
        param_file,
        names=[COL1_NAME, COL2_NAME, COL3_NAME],
        usecols=[0, 1, 2],
        dtype={COL1_NAME: str, COL2_NAME: float, COL3_NAME: str},
    )

    phalange_strs = []
    d_all = []
    alpha_all = []
    alpha_base_lst = []  # for debugging / prototyping
    t_all = []
    # Springs are numbered '01', '12' and '23' (from proximal to distal) depending on their position on the finger
    for finger in FINGER_LST:
        if finger == "thumb":
            locs = ["01", "12"]
        else:
            locs = ["01", "12", "23"]

        for loc in locs:
            phalange = finger + loc  # e.g. 'index12'
            phalange_strs.append(phalange)
            alpha_param_str = phalange + ALPHA_SUFFIX

            # Retrieve measured values from the parameter file
            d_base = df_param.loc[df_param[COL1_NAME] == phalange][COL2_NAME].iloc[0]
            alpha_base = df_param.loc[df_param[COL1_NAME] == alpha_param_str][
                COL2_NAME
            ].iloc[0]

            if math.isnan(d_base) or math.isnan(alpha_base):
                exit("ERROR: Pin spacing and/or alpha measurement not found in CSV.")

            # Apply preload
            d = d_base * (1 + PRELOAD / 100)

            # Adaptive alpha
            # print("base", alpha_base)
            alpha = alpha_base * (1 + PRELOAD / 100)

            alpha_base_lst.append(alpha_base)

            # Determine thickness based on the selected policy (if not binning and tiebreaking, which is detailed in the next section)
            match policy:
                case "batchB":
                    if loc in ["01", "12"]:
                        t_all.append(CENTRE_T)
                    else:
                        t_all.append(LOWER_T)
                case "batchC":
                    if loc == "12":
                        t_all.append(CENTRE_T)
                    elif loc == "23":
                        t_all.append(LOWER_T)
                    elif loc == "01" and finger in ["index", "middle", "ring"]:
                        t_all.append(HIGHER_T)
                    else:
                        t_all.append(CENTRE_T)
                case "batchD":
                    t_all.append(LOWER_T)
                    alpha = min(160.0, alpha * 1.1)
                case _:
                    pass

            # Storage
            d_all.append(d)
            alpha_all.append(alpha)

    test_alpha = (
        np.round(alpha_all.copy()).astype(int).tolist()
    )  # for debugging/prototyping

    # The below contains the code used to select parameters based on binning logic (more details available in the report)
    if "bin_" in policy:
        check = input("Applying tiebreaking, do you wish to continue (y/n)?: ")
        if check != "y":
            exit("WARNING: Execution halted.")

        # Binning wrt alpha
        binned_t_alpha = thickness_binning(alpha_all, T_BINS)

        # Binning wrt d
        binned_t_d = thickness_binning(d_all, T_BINS)

        # print(phalange_strs)
        # print("---Thickness options")
        # print(binned_t_alpha)
        # print(binned_t_d)

        # Determine thickness to use via binning and a tiebreak policy
        idx = 0
        for t_alpha, t_d in zip(binned_t_alpha, binned_t_d):
            if t_alpha != t_d:
                match policy:
                    case "bin_fixed":
                        t_use = CENTRE_T
                    case "bin_lower":
                        t_use = min(t_alpha, t_d)
                    case "bin_adaptive_lower":
                        # pct = T_INCREMENT / CENTRE_T # 25% is quite high
                        pct = 0.1  # NB: this is a number found through trial and error
                        t_use = min(t_alpha, t_d)
                        alpha_all[idx] = alpha_all[idx] * (1 + pct)
                    case "bin_outlier":
                        exit("ERROR: Tiebreak policy 'outlier' not yet implemented.")
                    case _:
                        exit(f"ERROR: Binning policy '{policy}' not recognised.")
            else:
                t_use = t_alpha
            t_all.append(t_use)
            idx += 1

    # Prepare data for storage
    alpha_all = np.round(alpha_all).astype(int).tolist()
    d_all = np.round(d_all).astype(int).tolist()

    # Debugging/confirmation readout
    # print("--- Alpha")
    # print(alpha_base_lst)
    # print(test_alpha)
    # print(alpha_all)
    # # print(d_all)
    # print("--- Final thickness")
    # print(t_all)

    # Save spring
    save_spring(
        param_file,
        tracker_file,
        df_param,
        phalange_strs,
        alpha_all,
        d_all,
        t_all,
        PRELOAD,
        batch_code,
        save_fingers,
    )


if __name__ == "__main__":
    apply_heuristics()
