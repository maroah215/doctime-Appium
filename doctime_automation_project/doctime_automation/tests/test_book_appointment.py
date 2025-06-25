import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

caps = {
    "platformName": "Android",
    "deviceName": "Android Device",
    "automationName": "UiAutomator2",
    "appPackage": "com.media365ltd.doctime",
    "appActivity": "com.media365ltd.doctime.ui.activities.LoginActivity",
    "noReset": True,
    "newCommandTimeout": 600
}

options = UiAutomator2Options().load_capabilities(caps)
driver = webdriver.Remote("http://localhost:4723/wd/hub", options=options)
wait = WebDriverWait(driver, 20)

def fail_and_exit(msg):
    print(msg)
    try:
        driver.quit()
    except:
        pass
    exit()

try:
    print("📱 App launched...")

    # Switch language if needed
    try:
        lang_btn = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("English")')
        lang_btn.click()
        print("🌐 Switched to English")
        time.sleep(2)
    except:
        print("✅ Language already English or not found")

    # Step 1: Click search field
    try:
        search_field = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.media365ltd.doctime:id/et_search")))
        search_field.click()
        print("🔍 Search field clicked")
    except TimeoutException:
        fail_and_exit("❌ Could not click on search field")

    # Step 2: Type 'Cardiologist'
    try:
        search_input = wait.until(EC.presence_of_element_located((AppiumBy.ID, "com.media365ltd.doctime:id/et_search")))
        search_input.send_keys("Cardiologist")
        print("🔍 Typed 'Cardiologist'")
        time.sleep(2)
    except TimeoutException:
        fail_and_exit("❌ Could not type in search field")

    # Step 3: Select department suggestion
    try:
        dept_suggestion = wait.until(EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Cardiologist")')
        ))
        dept_suggestion.click()
        print("📂 Cardiologist department selected")
    except TimeoutException:
        fail_and_exit("❌ Could not select Cardiologist department")

    # Step 4: Find doctor with "Appointment" label and click
    try:
        doctor_appointment_text = wait.until(EC.presence_of_all_elements_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Appointment")')
        ))

        if not doctor_appointment_text:
            fail_and_exit("❌ No doctor with Appointment available.")

        # Go to parent CardView and click it
        appointment_doctor = doctor_appointment_text[0]
        bounds = appointment_doctor.get_attribute("bounds")
        x = int(bounds.split("][")[0][1:].split(",")[0]) + 20
        y = int(bounds.split("][")[0][1:].split(",")[1]) + 20
        driver.tap([(x, y)])
        print("👨‍⚕️ Appointment doctor selected")

    except TimeoutException:
        fail_and_exit("❌ Could not find doctor with 'Appointment' label")

    # Step 5: Book Appointment button
    try:
        book_btn = wait.until(EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Book Online Appointment")')
        ))
        book_btn.click()
        print("📅 'Book Online Appointment' clicked")
    except TimeoutException:
        fail_and_exit("❌ Could not find Book Online Appointment button")

    # Step 6: Wait for time slot screen
    try:
        wait.until(EC.presence_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Select your appointment time")')
        ))
        print("🕒 Time slot page reached.")
    except TimeoutException:
        fail_and_exit("❌ Time slot page not found")

    print("✅ Test Completed: Appointment flow successful.")
    print("⏳ Keeping app open for 1 hour...")
    time.sleep(3600)

except Exception as e:
    print(f"❌ Unexpected error: {e}")
finally:
    driver.quit()













