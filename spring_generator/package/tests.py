# T. Atkins, 2024
from package.mk_spring_testing import mk_spring_testing


def tests(run: str) -> None:
    """
    FUNCTION
    > Similarly to main(), this is just a top-level runner that calls mk_spring_testing in a variety of parameter configurations for faster spring generation
    > NB-1: The contents of this function do not reflect the entire use history of this function throughout ALL testing, but rather examples/snapshots of its use
    > NB-2: See further details in the comments of the functions of the 'package' directory
    """
    # Conclusions (for index12)
    ALPHA_CONCL = 80
    PRELOAD_CONCL = 0
    THICKNESS_CONCL = 16

    check = input(f"Are you sure you want to proceed with test run '{run}' (y/n): ")
    print("---")

    if check == "y":
        match run:
            case "alpha":
                for alpha in [50, 60, 70, 80, 90]:
                    mk_spring_testing(
                        2,
                        "12",
                        alpha,
                        16,
                        0,
                        save_mode="yes",
                        comment="Alpha variation with increased thickness",
                    )
                return None
            case "preload":
                for preload in [30, 40, 50]:
                    mk_spring_testing(
                        2,
                        "12",
                        ALPHA_CONCL,
                        # ALPHA_CONCL * (1 + preload / 100),
                        THICKNESS_CONCL,
                        preload,
                        save_mode="yes",
                        comment="Preload variation (alpha NOT varied in proportion)",
                    )
                return None
            case "thickness":
                for thickness in [8, 12, 16, 20]:
                    mk_spring_testing(
                        2,
                        "12",
                        ALPHA_CONCL,
                        thickness,
                        PRELOAD_CONCL,
                        save_mode="yes",
                        comment="Preload variation",
                    )
                return None
            case _:
                raise Exception("Unknown input.")

    else:
        exit("WARNING: Spring generation prevented.")


if __name__ == "__main__":
    tests()
