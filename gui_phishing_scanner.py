import re
import tkinter as tk
from tkinter import messagebox

# Function to calculate score based on patterns
def calculate_score(url):
    score = 0

    # Suspicious keywords
    suspicious_keywords = ['login', 'verify', 'update', 'secure', 'account', 'signin', 'confirm']
    for word in suspicious_keywords:
        if word in url.lower():
            score += 1

    # Check for IP address pattern
    if re.search(r'\b\d{1,3}(\.\d{1,3}){3}\b', url):
        score += 3

    # Long URLs
    if len(url) > 75:
        score += 2

    # Use of HTTP instead of HTTPS
    if url.startswith("http://"):
        score += 1

    # Special characters often seen in phishing
    if re.search(r'[@%=&]', url):
        score += 1

    # Too many URL parameters
    if url.count('&') >= 2:
        score += 1

    # Too many subdomains
    if url.count('.') > 3:
        score += 1

    return score

# Function to scan URL and display result
def scan_url():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL")
        return

    score = calculate_score(url)

    if score >= 6:
        result_text = "❌ LIKELY UNSAFE"
        result_color = "red"
    elif 3 <= score < 6:
        result_text = "⚠️ SUSPICIOUS"
        result_color = "orange"
    else:
        result_text = "✅ SAFE"
        result_color = "green"

    result_label.config(text=result_text, fg=result_color)

    with open("scan_logs.txt", "a") as log:
        log.write(f"{url} -> Score: {score} -> {result_text}\n")

# GUI setup
app = tk.Tk()
app.title("Phishing Link Scanner - Day 4")
app.geometry("480x220")
app.config(bg="white")

title = tk.Label(app, text="🔍 Phishing Link Scanner", font=("Helvetica", 16, "bold"), bg="white")
title.pack(pady=10)

url_entry = tk.Entry(app, font=("Arial", 12), width=50)
url_entry.pack(pady=5)

scan_button = tk.Button(app, text="Scan URL", font=("Arial", 12), bg="#1e90ff", fg="white", command=scan_url)
scan_button.pack(pady=5)

result_label = tk.Label(app, text="", font=("Arial", 14, "bold"), bg="white")
result_label.pack(pady=10)

app.mainloop()
