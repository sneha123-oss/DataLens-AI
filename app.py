from flask import Flask, render_template, request, send_file
import pandas as pd
import os

from utils.charts import generate_charts
from utils.analyzer import generate_insights
from utils.pdf_generator import create_pdf

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# Store latest uploaded dataset analysis
analysis_data = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    global analysis_data

    if "file" not in request.files:
        return "No file selected."

    file = request.files["file"]

    if file.filename == "":
        return "No file selected."

    # Save uploaded file
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Read CSV using multiple encodings
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

    # Save analysis data
    analysis_data = {
        "filename": file.filename,
        "rows": rows,
        "cols": cols,
        "missing": missing,
        "duplicates": duplicates,
        "columns": columns,
        "preview": preview,
        "charts": charts,
        "insights": insights
    }

    # Open Menu
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


@app.route("/download_report")
def download_report():

    pdf_path = os.path.join(
        app.config["REPORT_FOLDER"],
        "DataLensAI_Report.pdf"
    )

    return send_file(pdf_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)