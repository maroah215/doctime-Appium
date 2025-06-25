import subprocess
import re

def get_last_otp_sms():
    try:
        # Get last few SMS messages from the device
        output = subprocess.check_output(
            ['adb', 'shell', 'content query --uri content://sms/inbox --projection body --sort "date DESC"'],
            universal_newlines=True
        )

        # Find 4–6 digit code from the SMS body
        otp_match = re.search(r'\b(\d{4,6})\b', output)
        if otp_match:
            return otp_match.group(1)
        else:
            raise Exception("OTP not found in latest SMS.")

    except subprocess.CalledProcessError as e:
        raise Exception("ADB error while reading SMS: " + str(e))
