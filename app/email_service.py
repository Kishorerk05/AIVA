import random
import time
import re
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Load environment variables
load_dotenv()

# Store OTPs in memory
otp_store = {}  # { email: (otp, expiry_timestamp) }

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_mobile(mobile):
    """Validate mobile number format"""
    # Remove any spaces, dashes, or parentheses
    clean_mobile = re.sub(r'[\s\-\(\)]', '', mobile)
    # Check if it's 10 digits (Indian format) or starts with +91
    # Handle both +91xxxxxxxxxx and xxxxxxxxxx formats
    if len(clean_mobile) == 10 and clean_mobile[0] in '6789':
        return True
    elif len(clean_mobile) == 13 and clean_mobile.startswith('+91') and clean_mobile[3] in '6789':
        return True
    elif len(clean_mobile) == 12 and clean_mobile.startswith('91') and clean_mobile[2] in '6789':
        return True
    return False

def send_otp(receiver_email):
    """Send OTP to the provided email address using SendGrid"""
    try:
        otp = str(random.randint(100000, 999999))
        expiry = time.time() + 300  # 5-minute expiry

        # Save OTP
        otp_store[receiver_email] = (otp, expiry)

        # Create SendGrid email
        message = Mail(
            from_email=os.getenv("FROM_EMAIL", "kishorerk2025@gmail.com"),
            to_emails=receiver_email,
            subject="AIVA Insurance - Your OTP Verification Code",
            html_content=f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #2c3e50;">AIVA Insurance</h2>
                <p>Dear Customer,</p>
                <p>Your One-Time Password (OTP) for email verification is:</p>
                <div style="background-color: #f8f9fa; padding: 20px; text-align: center; margin: 20px 0;">
                    <h1 style="color: #007bff; font-size: 32px; margin: 0;">{otp}</h1>
                </div>
                <p>This OTP is valid for <strong>5 minutes</strong>. Please do not share this OTP with anyone.</p>
                <p>If you did not request this verification, please ignore this email.</p>
                <br>
                <p>Best regards,<br>AIVA Insurance Team</p>
            </div>
            """
        )
        
        # Send email using SendGrid
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        
        if response.status_code == 202:
            print(f"OTP sent to {receiver_email}")
            return True, "OTP sent successfully"
        else:
            print(f"Failed to send OTP. Status code: {response.status_code}")
            return False, f"Failed to send OTP. Status code: {response.status_code}"
            
    except Exception as e:
        print(f"Error sending OTP: {str(e)}")
        return False, f"Failed to send OTP: {str(e)}"

def verify_otp(email, entered_otp):
    """Verify the OTP provided by user"""
    stored = otp_store.get(email)

    if not stored:
        return False, "No OTP found for this email. Please request a new one."

    otp, expiry = stored
    if time.time() > expiry:
        return False, "OTP expired. Please request a new one."

    if entered_otp == otp:
        del otp_store[email]
        return True, "OTP verified successfully!"
    else:
        return False, "Incorrect OTP."

# Legacy function name for compatibility
def send_otp_email(receiver_email, otp=None):
    """Legacy wrapper for send_otp function"""
    return send_otp(receiver_email)

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def clear_otp(email):
    """Clear OTP for an email (cleanup function)"""
    if email in otp_store:
        del otp_store[email]
