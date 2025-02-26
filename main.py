from flask import Flask, request, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

CSV_FILE = "responses.csv"  # CSV file to store responses

# Ensure CSV exists
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Email", "Criterion 1", "Criterion 2", "Criterion 3"]).to_csv(CSV_FILE, index=False)

@app.route("/")
def index():
    return render_template("form.html")  # Load the form

@app.route("/submit", methods=["POST"])
def submit():
    email = request.form.get("email")
    responses = [request.form.get(f"criterion_{i}") for i in range(1, 4)]

    # Check if email already exists
    df = pd.read_csv(CSV_FILE)
    if email in df["Email"].values:
        return jsonify({"error": "Email already used!"}), 400

    # Save to CSV
    new_entry = pd.DataFrame([[email] + responses], columns=df.columns)
    new_entry.to_csv(CSV_FILE, mode="a", header=False, index=False)

    return jsonify({"message": "Response saved successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
