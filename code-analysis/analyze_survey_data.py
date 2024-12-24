import argparse
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns

from effect_size import cohend
from power_analysis import parametric_power_analysis
from stats_tests import summary, wilcoxon_test


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", help="Path to the survey raw data file")

    args = parser.parse_args()
    input_file = args.input_file

    model_dev_written = "dev-written"

    alpha = 0.05
    power = 0.80

    fig_size = (17, 10)
    font_size = 30
    font_weight = "bold"

    assert os.path.exists(input_file), f"The file {input_file} does not exist"
    assert input_file.endswith(".json"), f"The file {input_file} must be a json file"

    with open(input_file, "r+", encoding="utf-8") as f:
        data = json.load(f)

    models = list(data.keys())
    X_LABELS = models
    assert (
        model_dev_written in models
    ), f"The model {model_dev_written} is not in the data"
    values_model_dev_written = data[model_dev_written]["scores"]
    print(f"Scores {model_dev_written}: {summary(a=values_model_dev_written)}")

    for model in models:

        if model == model_dev_written:
            continue

        values_1 = data[model_dev_written]["scores"]
        values_2 = data[model]["scores"]

        print(f"Scores {model}: {summary(a=values_2)}")

        _, p_value = wilcoxon_test(a=values_1, b=values_2)
        if p_value < alpha:
            print(
                f"The models {model_dev_written} and {model} are significantly different"
            )
        else:
            effect_size, _ = cohend(a=values_1, b=values_2)
            nobs = parametric_power_analysis(
                effect=effect_size, alpha=alpha, power=power
            )
            print(
                f"The models {model_dev_written} and {model} are not significantly different. "
                f"The number of observations needed for statistical significance is {nobs} (with a power of {power})"
            )

    values = list(map(lambda x: x["scores"], list(data.values())))

    plt.figure(figsize=fig_size)
    plt.rcParams["font.size"] = font_size
    plt.rcParams["font.weight"] = font_weight
    sns.boxplot(data=values)
    plt.ylabel("Redability Scores", fontweight=font_weight)
    plt.xticks(range(len(X_LABELS)), X_LABELS)
    # plt.boxplot(values, labels=models)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig("boxplots.svg", format="svg")


if __name__ == "__main__":
    main()
