import argparse
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", help="Path to the stability raw data file")

    args = parser.parse_args()
    input_file = args.input_file

    fig_size = (48, 9)
    font_size = 35
    font_weight = "bold"

    assert os.path.exists(input_file), f"The file {input_file} does not exist"
    assert input_file.endswith(".json"), f"The file {input_file} must be a json file"

    with open(input_file, "r+", encoding="utf-8") as f:
        data = json.load(f)

    all_data = []
    for i, model in enumerate(data.keys()):
        all_data += data[model]["similarities"]
        if i != len(data.keys()) - 1:
            all_data += [[]]
    # data = data["gpt-3.5-turbo"]["similarities"] + data["gpt-4"]["similarities"]

    CUSTOM_PALETTE = ["blue", "orange", "green", "red", "purple"]
    X_LABELS = ["Cli", "Csv", "Lang", "Gson", "Chart"]
    custom_palette = []
    x_labels = []
    for i in range(len(data.keys())):
        x_labels += X_LABELS
        custom_palette += CUSTOM_PALETTE
        if i != len(data.keys()) - 1:
            x_labels += [" "]
            custom_palette += ["white"]

    plt.figure(figsize=fig_size)
    plt.rcParams["font.size"] = font_size
    plt.rcParams["font.weight"] = font_weight
    sns.violinplot(data=all_data, palette=custom_palette)
    plt.ylabel("Cosine Similarity", fontweight=font_weight)
    plt.xticks(range(len(x_labels)), x_labels)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig("violin-similarities.svg", format="svg")


if __name__ == "__main__":
    main()
