import pandas as pd


def generate_insights(df):

    insights = []

    rows = len(df)
    cols = len(df.columns)

    numeric = len(df.select_dtypes(include="number").columns)
    categorical = len(df.select_dtypes(exclude="number").columns)

    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()

    # -----------------------------
    # Dataset Overview
    # -----------------------------
    insights.append(
        f"📁 This dataset contains {rows} rows and {cols} columns."
    )

    # -----------------------------
    # Data Quality
    # -----------------------------
    if missing == 0:
        insights.append(
            "✅ Great! No missing values were found in the dataset."
        )

    elif missing < 50:
        insights.append(
            f"🟢 Only {missing} values are missing. The dataset is almost complete."
        )

    else:
        insights.append(
            f"🟡 {missing} values are missing. Cleaning the dataset is recommended."
        )

    if duplicates == 0:
        insights.append(
            "✅ No duplicate rows were found."
        )

    else:
        insights.append(
            f"⚠ {duplicates} duplicate rows were found. Removing them will improve the quality of your analysis."
        )

    # -----------------------------
    # Dataset Type
    # -----------------------------
    insights.append(
        f"📊 The dataset contains {numeric} numeric column(s). These are useful for graphs, calculations, and machine learning."
    )

    if categorical > 0:
        insights.append(
            f"📝 The dataset also contains {categorical} text column(s). These may need to be converted into numbers before training a machine learning model."
        )

    # -----------------------------
    # Final Recommendation
    # -----------------------------
    insights.append(
        "💡 Overall, this dataset looks good. After basic cleaning, it is ready for further analysis and machine learning."
    )

    return insights