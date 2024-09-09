# T. Atkins, 2024
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

plt.rc("text", usetex=True)
plt.rc("font", **{"family": "sans-serif", "sans-serif": ["Helvetica"]})


def check_normal(mode: str = "qq") -> None:
    """
    FUNCTION
    > Illustrates a variety of means by which to evaluate whether a dataset is distributed in a quasi-Gaussian manner
    """
    x = np.array([100, 112, 115, 115, 108, 97, 95, 90, 88, 86, 89])  # example data

    match mode:
        case "qq":
            # Q-Q Plot
            stats.probplot(x, dist="norm", plot=plt)
            plt.title("Q-Q Plot")
            plt.show()
            return None

        case "shapiro":
            # Shapiro-Wilk test
            stat, p_value = stats.shapiro(x)
            print(f"Shapiro-Wilk Test Statistic: {stat}")
            print(f"p-value: {p_value}")

            if p_value > 0.05:
                print("Data is normally distributed (fail to reject H0).")
            else:
                print("Data is not normally distributed (reject H0).")
            return None

        case "kolmogorov":
            # Kolmogorov-Smirnov test
            stat, p_value = stats.kstest(x, "norm", args=(np.mean(x), np.std(x)))
            print(f"KS Test Statistic: {stat}")
            print(f"p-value: {p_value}")

            if p_value > 0.05:
                print("Data is normally distributed (fail to reject H0).")
            else:
                print("Data is not normally distributed (reject H0).")
            return None

        case "anderson":
            # Anderson-Darling Test
            result = stats.anderson(x, dist="norm")
            print(f"Anderson-Darling Statistic: {result.statistic}")
            print(f"Critical Values: {result.critical_values}")
            print(f"Significance Level: {result.significance_level}")

            if (
                result.statistic < result.critical_values[2]
            ):  # use significance level of 0.05
                print("Data is normally distributed (fail to reject H0).")
            else:
                print("Data is not normally distributed (reject H0).")
            return None

        case _:
            raise Exception("Unexpected input.")


if __name__ == "__main__":
    check_normal()
