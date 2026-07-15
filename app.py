from flask import Flask, render_template, request, send_file
import pandas as pd
import os

from utils.charts import generate_charts
from utils.analyzer import generate_insights
from utils.pdf_generator import create_pdf
from utils.cleaner import clean_dataset
from utils.ml_recommender import recommend_ml

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

analysis_data = {}
cleaned_dataset = None
cleaning_summary = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    global analysis_data
    global cleaned_dataset
    global cleaning_summary

    if "file" not in request.files:
        return "No file selected."

    file = request.files["file"]

    if file.filename == "":
        return "No file selected."

    # Save uploaded file
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Read CSV
    encodings = ["utf-8", "latin1", "cp1252", "ISO-8859-1"]

    df = None

    for enc in encodings:
        try:
            df = pd.read_csv(filepath, encoding=enc)
            print(f"CSV loaded successfully using {enc}")
            break
        except Exception:
            continue

    if df is None:
        return "Unable to read the uploaded CSV."

    # Dataset Information
    rows = df.shape[0]
    cols = df.shape[1]

    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()

    columns = list(df.columns)

    preview = df.head(10).to_html(classes="table", index=False)

    # Generate Charts
    charts = generate_charts(df)

    # Generate AI Insights
    insights = generate_insights(df)
    ml_info = recommend_ml(df)

    # AI Dataset Preparation
    cleaned_dataset, cleaning_summary = clean_dataset(df)

    print("Original Missing :", df.isnull().sum().sum())
    print("Cleaned Missing  :", cleaned_dataset.isnull().sum().sum())

    print(cleaning_summary)

    # Save Cleaned Dataset
    cleaned_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "Cleaned_Dataset.csv"
    )

    cleaned_dataset.to_csv(
        cleaned_path,
        index=False
    )

    # Generate PDF
    pdf_path = os.path.join(
        app.config["REPORT_FOLDER"],
        "DataLensAI_Report.pdf"
    )

    create_pdf(
        pdf_path,
        file.filename,
        rows,
        cols,
        missing,
        duplicates,
        columns,
        insights
    )

    # -----------------------------
    # Dataset Quality Score
    # -----------------------------

    original_score = 100

    if rows > 0:
        original_score -= int((missing / (rows * cols)) * 100)
        original_score -= int((duplicates / rows) * 100)

    original_score = max(0, original_score)

    clean_score = 100

    if cleaned_dataset.shape[0] > 0:

        clean_missing = cleaned_dataset.isnull().sum().sum()
        clean_duplicates = cleaned_dataset.duplicated().sum()

        clean_score -= int(
            (clean_missing /
             (cleaned_dataset.shape[0] * cleaned_dataset.shape[1])) * 100
        )

        clean_score -= int(
            (clean_duplicates /
             cleaned_dataset.shape[0]) * 100
        )

    clean_score = max(0, clean_score)

    # Store Analysis Data

    analysis_data = {

        "filename": file.filename,

        # Original Dataset
        "rows": rows,
        "cols": cols,
        "missing": missing,
        "duplicates": duplicates,

        # Prepared Dataset
        "clean_rows": cleaned_dataset.shape[0],
        "clean_cols": cleaned_dataset.shape[1],
        "clean_missing": cleaned_dataset.isnull().sum().sum(),
        "clean_duplicates": cleaned_dataset.duplicated().sum(),

        # Quality Score
        "original_score": original_score,
        "clean_score": clean_score,
        "ml_info": ml_info,
        # Other Data
        "columns": columns,
        "preview": preview,
        "charts": charts,
        "insights": insights
    }

    return render_template("menu.html", **analysis_data)


@app.route("/menu")
def menu():
    return render_template("menu.html", **analysis_data)


@app.route("/preview")
def preview():
    return render_template("preview.html", **analysis_data)


@app.route("/charts")
def charts():
    return render_template("charts.html", **analysis_data)


@app.route("/insights")
def insights():
    return render_template("insights.html", **analysis_data)


@app.route("/prepare")
def prepare():

    return render_template(
        "prepare.html",
        **analysis_data,
        summary=cleaning_summary
    )


@app.route("/download_cleaned_dataset")
def download_cleaned_dataset():

    cleaned_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "Cleaned_Dataset.csv"
    )

    return send_file(
        cleaned_path,
        as_attachment=True
    )


@app.route("/download_report")
def download_report():

    pdf_path = os.path.join(
        app.config["REPORT_FOLDER"],
        "DataLensAI_Report.pdf"
    )

    return send_file(
        pdf_path,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)