import pandas as pd


def clean_dataset(df):
    """
    Cleans the uploaded dataset and returns:
    1. Cleaned DataFrame
    2. Cleaning Summary
    """

    cleaned_df = df.copy()

    summary = []

    # --------------------------------
    # Remove completely empty rows
    # --------------------------------

    before = len(cleaned_df)

    cleaned_df.dropna(how="all", inplace=True)

    removed = before - len(cleaned_df)

    summary.append(f"Removed {removed} completely empty rows.")

    # --------------------------------
    # Remove duplicate rows
    # --------------------------------

    before = len(cleaned_df)

    cleaned_df.drop_duplicates(inplace=True)

    removed = before - len(cleaned_df)

    summary.append(f"Removed {removed} duplicate rows.")

    # --------------------------------
    # Handle Missing Values
    # --------------------------------

    numeric_columns = cleaned_df.select_dtypes(include="number").columns

    categorical_columns = cleaned_df.select_dtypes(exclude="number").columns

    # Numeric → Median

    for col in numeric_columns:

     if cleaned_df[col].isnull().sum() > 0:

        cleaned_df[col] = cleaned_df[col].fillna(
            cleaned_df[col].median()
        )

    # Categorical → Mode

    for col in categorical_columns:

     if cleaned_df[col].isnull().sum() > 0:

        mode = cleaned_df[col].mode()

        if not mode.empty:

            cleaned_df[col] = cleaned_df[col].fillna(
                mode[0]
            )

    summary.append("Handled missing values successfully.")

    # --------------------------------
    # Reset Index
    # --------------------------------

    cleaned_df.reset_index(drop=True, inplace=True)

    summary.append("Dataset index reset.")

    summary.append("Dataset is ready for further preprocessing.")

    return cleaned_df, summary