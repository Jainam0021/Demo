import os
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ---------------- MAIL CONFIG ---------------- #
app.config.update(
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_USERNAME"),
)

mail = Mail(app)

# ---------------- ROUTES ---------------- #
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ---------------- CONTACT FORM SUBMIT ---------------- #
@app.route("/submit-contact", methods=["POST"])
def submit_contact():
    data = request.form

    try:
        msg_body = f"""
New Event Inquiry Received 🎉

Full Name: {data.get('fullName')}
Phone: {data.get('phone')}
Email: {data.get('email')}
Event Date: {data.get('eventDate')}
Event City: {data.get('eventCity')}
Event Type: {data.get('eventType')}
Guests: {data.get('guestCount')}

Description:
{data.get('description')}
"""

        msg = Message(
            subject="📩 New Wedding Inquiry - Parampara",
            recipients=[os.getenv("MAIL_RECEIVER")],
            body=msg_body,
        )

        mail.send(msg)
        print("✅ Email sent successfully")

        return jsonify({"success": True}), 200

    except Exception as e:
        print("❌ Mail Error:", e)   # THIS WILL SHOW IN RENDER LOGS
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


