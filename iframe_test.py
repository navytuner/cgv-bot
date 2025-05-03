from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# URL with corrected syntax
url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0013&date=20250503'

# Set up headless mode
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Open the URL
driver.get(url)

# Wait until the iframe is loaded (adjust timeout if necessary)
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))

# Now that we're inside the iframe, we can extract the content
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Print the prettified HTML
print(soup.prettify())

# Quit the driver after scraping
driver.quit()

