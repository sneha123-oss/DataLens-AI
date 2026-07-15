def recommend_ml(df):
    """
    Recommend a suitable Machine Learning algorithm
    based on the uploaded dataset.
    """

    rows, cols = df.shape

    if cols <= 5:
        algorithm = "Linear Regression / Decision Tree"
        reason = "Small number of features."

    elif cols <= 15:
        algorithm = "Random Forest"
        reason = "Moderate number of features."

    else:
        algorithm = "XGBoost"
        reason = "Large number of features."

    return {
        "algorithm": algorithm,
        "reason": reason
    }