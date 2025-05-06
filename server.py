from flask import Flask, render_template, request, jsonify, send_file
import csv
import os
import pandas as pd  # For Excel conversion
import requests  # For web scraping

app = Flask(__name__)

CSV_FILE = "user_logins.csv"
EXCEL_FILE = "user_logins.xlsx"  # Excel file

# Ensure CSV file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Password"])

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/save_login', methods=['POST'])
def save_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Both fields are required!"}), 400

    # Save login details to CSV
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

    return jsonify({"message": "Login successful!"})

@app.route('/dashboard')
def dashboard():
    return render_template('WebScraper.html')

@app.route('/download_logins', methods=['GET'])
def download_logins():
    return send_file(CSV_FILE, as_attachment=True)

@app.route('/download_logins_excel', methods=['GET'])
def download_logins_excel():
    # Convert CSV to Excel
    df = pd.read_csv(CSV_FILE)  # Read CSV file
    df.to_excel(EXCEL_FILE, index=False)  # Save as Excel file

    # Send Excel file for download
    return send_file(EXCEL_FILE, as_attachment=True, download_name="user_logins.xlsx")

# ✅ NEW: Flask Proxy for Web Scraping
@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a real browser
        response = requests.get(url, headers=headers)
        return response.text  # Send raw HTML back
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)        