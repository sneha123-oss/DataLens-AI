import os
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns


def generate_charts(df):

    chart_folder = os.path.join("static", "charts")
    os.makedirs(chart_folder, exist_ok=True)

    chart_files = []

    numeric_columns = df.select_dtypes(include=["number"]).columns

    # -------------------------------
    # Histograms (first 6 columns)
    # -------------------------------

    for column in numeric_columns[:6]:

        plt.figure(figsize=(6,4))

        df[column].dropna().hist(
            bins=20,
            edgecolor="black"
        )

        plt.title(f"{column} Distribution")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        safe_name = column.replace(" ", "_")

        filename = f"{safe_name}.png"

        filepath = os.path.join(chart_folder, filename)

        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close()

        chart_files.append(filename)

    # -------------------------------
    # Correlation Heatmap
    # -------------------------------

    plt.figure(figsize=(10,8))

    corr = df[numeric_columns].corr()

    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title("Correlation Heatmap")

    heatmap_name = "correlation_heatmap.png"

    plt.savefig(
        os.path.join(chart_folder, heatmap_name),
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    chart_files.append(heatmap_name)

    return chart_files