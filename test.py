from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Import WebDriver Manager
import time

# Setup Chrome options
options = Options()
options.add_argument("--headless")  # Required for Jenkins (headless mode)
options.add_argument("--no-sandbox")  # Disable sandboxing (required in CI environments)
options.add_argument("--disable-dev-shm-usage")  # Fixes issue with limited shared memory in Docker/CI environments
options.add_argument("--remote-debugging-port=9222")  # Useful if you need to debug the browser
options.add_argument("--disable-gpu")  # Disable GPU acceleration in headless mode
options.add_argument("--disable-software-rasterizer")  # Disable software rasterizer

# Initialize the WebDriver using WebDriver Manager
try:
    # Use WebDriver Manager to automatically download the correct chromedriver version
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # Open the local file
    driver.get("file://" + "/var/lib/jenkins/workspace/simple-ci-cd/index.html")

    # Wait for the element to be visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "title"))
    )

    # Fetch the title text
    title = driver.find_element(By.ID, "title").text

    # Assert the title is as expected
    assert title == "Hello CI/CD", f"Expected 'Hello CI/CD' but got '{title}'"

    print(f"Test Passed: Title is '{title}'")

except Exception as e:
    print(f"Test Failed: {e}")

finally:
    # Quit the driver to close the browser session
    driver.quit()
