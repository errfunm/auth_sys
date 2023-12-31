import pyotp
from datetime import datetime, timedelta

def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session["otp_valid_date"] = str(valid_date)
    request.session["otp_secret_key"] = totp.secret
    print(f"Your otp is {otp}") 