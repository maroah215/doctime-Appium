import time
from appium.webdriver import Remote
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .smsreader import get_last_otp_sms  # Your custom OTP fetch function

def safe_print(msg):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(repr(msg))

# Appium Options
options = UiAutomator2Options().load_capabilities({
    "platformName": "Android",
    "deviceName": "emulator-5554",  # Change if needed
    "appPackage": "com.media365ltd.doctime",
    "appActivity": ".ui.activities.LoginActivity",
    "automationName": "UiAutomator2",
    "noReset": True,
    "newCommandTimeout": 600,
})

driver = Remote("http://localhost:4723/wd/hub", options=options)
wait = WebDriverWait(driver, 15)

try:
    safe_print("📱 Launching Doctime app...")

    # 1. Try dismissing advertisement
    try:
        ad_close_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.media365ltd.doctime:id/btn_close_ad"))
        )
        ad_close_btn.click()
        safe_print("✅ Advertisement dismissed")
    except TimeoutException:
        safe_print("✅ No advertisement appeared")

    # 2. Language switch
    try:
        lang_toggle = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                          'new UiSelector().textContains("English")')
        lang_toggle.click()
        safe_print("🌐 Switched language from Bangla to English")
        time.sleep(2)
    except NoSuchElementException:
        safe_print("✅ Language already English or toggle not found")

    # 3. Enter phone number
    phone_input = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, "com.media365ltd.doctime:id/et_phone_number"))
    )
    safe_print("⏳ Waiting for phone number input field...")
    phone_input.clear()
    phone_input.send_keys("01877366800")
    safe_print("✅ Phone number entered")

    # 4. Click Send OTP
    send_otp_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Send OTP")'))
    )
    send_otp_btn.click()
    safe_print("📨 OTP requested... waiting for SMS...")

    # 5. Wait for OTP screen
    time.sleep(4)

    # 6. Fetch OTP
    otp_code = get_last_otp_sms()
    safe_print(f"✅ OTP received: {repr(otp_code)}")

    # 7. Input OTP
    for i, digit in enumerate(otp_code):
        otp_box = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, f'(//android.widget.EditText)[{i+1}]'))
        )
        otp_box.send_keys(digit)
        time.sleep(0.3)

    # 8. Click Confirm OTP
    confirm_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Confirm OTP")'))
    )
    confirm_btn.click()
    safe_print("🎉 Login successful!")

    # 9. Dismiss Notification Permission Popup
    try:
        notif_deny_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "android:id/button2"))  # Usually DENY or CANCEL
        )
        notif_deny_btn.click()
        safe_print("🔕 Notification permission denied.")
    except TimeoutException:
        safe_print("✅ No notification permission popup.")

    # 10. Keep app open for 4 hours (14400 seconds)
    safe_print("🕒 App will stay open for 4 hours... Please present your test.")
    time.sleep(14400)

except Exception as e:
    safe_print(f"❌ Test failed: {repr(e)}")
finally:
    # Comment this out if you want app to remain open after script ends
    # driver.quit()
    pass

   










