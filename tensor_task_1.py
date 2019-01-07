from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


driver = webdriver.Chrome(executable_path=r"C:\\chromedriver.exe")
driver.get("https://www.yandex.ru")
assert "Яндекс" in driver.title
search_field = driver.find_element_by_name("text")
search_field.send_keys("Тензор")
wait = WebDriverWait(driver, 100)
searchText_yandex_suggestion = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//li [@class="suggest2-item i-bem suggest2-item_js_inited"]')))
for item in searchText_yandex_suggestion :
	if str(item.text).lower() == "тензор ярославль официальный сайт":
		item.click()
		break 
element = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, ("organic__url"))))
for link in element:
	if link.text == "Тензор — IT-компания":
		link.click()
#driver.close()
