from flask import Flask, request, render_template, jsonify
import csv
import os

app = Flask(__name__)

CSV_FILE = "responses.csv"  # CSV file to store responses

# Ensure CSV file exists with headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["email"] + 
                [f"cargo_{i}" for i in range(1, 11)] + 
                [f"passenger_{i}" for i in range(1, 11)] + 
                ["gender", "age", "education", "education_other", 
                 "employment", "employment_other", "experience", "gdpr"])
        
@app.route("/")
def index():
    return render_template("form.html")  # Load the form

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form.to_dict()

    email = data.get("email")
    gdpr = data.get("gdpr", "no")  # Default to "no" if missing
    if not email:
        return jsonify({"error": "Το email είναι απαραίτητο!"}), 400
    if gdpr != "on":
        return jsonify({"error": "Η συγκατάθεση GDPR είναι υποχρεωτική!"}), 400

    # Check if email exists
    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        existing_emails = [row[0] for row in reader]

    if email in existing_emails:
        return jsonify({"error": "Αυτό το email έχει ήδη χρησιμοποιηθεί!"}), 400

    # Save data to CSV
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([email] + [data[key] for key in sorted(data.keys()) if key != "email"])  # Save in order

    return jsonify({"message": "Your submission was saved successfully!"}), 200

@app.route("/responses")
def view_submissions():
    import pandas as pd
    try:
        df = pd.read_csv("responses.csv")
        return df.to_html()  # Show as an HTML table
    except:
        return "No responses found."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
