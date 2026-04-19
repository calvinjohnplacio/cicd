from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # required for Jenkins

driver = webdriver.Chrome(options=options)

driver.get("file://" + "/var/lib/jenkins/workspace/simple-ci-cd/index.html")

title = driver.find_element(By.ID, "title").text

assert title == "Hello CI/CD"

driver.quit()
