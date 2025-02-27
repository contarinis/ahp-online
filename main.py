from flask import Flask, request, render_template, jsonify
import csv
import os
import pandas as pd

app = Flask(__name__)

CSV_FILE = "responses.csv"  # CSV file to store responses

# Ensure CSV file exists with headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "email", "gender", "age", "education", "education_other",
            "employment", "employment_other", "experience", "gdpr",
            "cargo_1", "cargo_2", "cargo_3", "cargo_4", "cargo_5", 
            "cargo_6", "cargo_7", "cargo_8", "cargo_9", "cargo_10",
            "passenger_1", "passenger_2", "passenger_3", "passenger_4", "passenger_5", 
            "passenger_6", "passenger_7", "passenger_8", "passenger_9", "passenger_10"
        ])
        
@app.route("/")
def index():
    return render_template("form.html")  # Load the form

@app.route("/submit", methods=["POST"])
def submit():
    form_data = request.form

    # ✅ Ensure correct order of collected data
    email = form_data.get("email", "").strip()
    gdpr = form_data.get("gdpr", "no")  # Default to "no" if missing

    if not email:
        return jsonify({"error": "Το email είναι απαραίτητο!"}), 400
    if gdpr != "on":
        return jsonify({"error": "Η συγκατάθεση GDPR είναι υποχρεωτική!"}), 400

    # ✅ Check if email exists (skip the header)
    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        existing_emails = [row[0] for row in reader]

    if email in existing_emails:
        return jsonify({"error": "Αυτό το email έχει ήδη χρησιμοποιηθεί!"}), 400

    # ✅ Collect responses in correct order
    data = [
        email, form_data["gender"], form_data["age"],
        form_data["education"], form_data.get("education_other", ""),
        form_data["employment"], form_data.get("employment_other", ""),
        form_data["experience"], gdpr,
        *[form_data.get(f"cargo_{i}", "") for i in range(10)],  # Cargo AHP
        *[form_data.get(f"passenger_{i}", "") for i in range(10)]   # Passenger AHP
    ]

    # ✅ Save data to CSV
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(data)

    return jsonify({"message": "Η απάντησή σας καταγράφηκε επιτυχώς!"}), 200

@app.route("/responses")
def view_submissions():
    try:
        df = pd.read_csv(CSV_FILE)
        return df.to_html()  # Show as an HTML table
    except Exception as e:
        return f"No responses found. Error: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
