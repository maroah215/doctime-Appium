import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

desired_caps = {
    "platformName": "Android",
    "deviceName": "Android Device",
    "automationName": "UiAutomator2",
    "appPackage": "com.media365ltd.doctime",
    "appActivity": "com.media365ltd.doctime.ui.activities.HomeActivity",  # Home screen after login
    "noReset": True  # Keeps the app logged in
}

driver = webdriver.Remote("http://localhost:4723/wd/hub", options=None, capabilities=desired_caps)
wait = WebDriverWait(driver, 20)

try:
    print("✅ App launched and home screen loaded...")

    # Wait for the search bar and click it
    search_bar = wait.until(EC.presence_of_element_located(
        (AppiumBy.ID, "com.media365ltd.doctime:id/et_search")
    ))
    search_bar.click()
    print("🔍 Search bar clicked")

    time.sleep(1)
    search_bar.send_keys("cardiologist")
    print("⌨️ Typed 'cardiologist'")

    # Wait for the result list and click the Cardiologist department option
    cardiologist_option = wait.until(EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR, 
         'new UiSelector().textContains("Cardiologist")')
    ))
    cardiologist_option.click()
    print("🩺 Selected Cardiologist department")

    # Wait for doctor list to load
    wait.until(EC.presence_of_element_located(
        (AppiumBy.ID, "com.media365ltd.doctime:id/tv_name")  # Assuming doctor names have this ID
    ))
    print("✅ Cardiologist doctors loaded successfully.")

except Exception as e:
    print(f"❌ Test failed: {str(e)}")

finally:
    driver.quit()



