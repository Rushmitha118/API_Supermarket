import requests
import smtplib
from email.mime.text import MIMEText

# API URL (Mock API)
url = "https://demo60206020.mockable.io/mydummy_data"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    name, email = data["full_name"], data["email"]
    bread_qty = data["items"].get("bread", 0)  # Get bread quantity

    if bread_qty > 0:
        bread_price = 50  # Per unit
        total = bread_qty * bread_price
        gst = total * 0.05  # 5% GST
        final_amount = total + gst

        # Bill message
        bill = f"Hi {name}!\nYour total bill for {bread_qty} bread(s) is {final_amount} (including 5% GST)."

        # Ask if user wants email
        if input("Send bill via email? (yes/no): ").strip().lower() == "yes":
            sender, password = "your_email@gmail.com", "your_password"
            msg = MIMEText(bill)
            msg["From"], msg["To"], msg["Subject"] = sender, email, "Your Bread Bill"

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender, password)
                server.sendmail(sender, email, msg.as_string())
                server.quit()
                print(f"Bill sent to {email}!")
            except Exception as e:
                print("Email failed:", e)
        else:
            print(bill)
    else:
        print("No bread purchased.")

else:
    print("API error!")