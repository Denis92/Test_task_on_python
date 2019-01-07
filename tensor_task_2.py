from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
class Class_main(object):
	def __init__(self, driver):
		self.wait = WebDriverWait(driver, 100)
		
	def click_element(self, xpath_input):
		element = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, xpath_input)))
		return element[0].click()

	def text_img(self):
		text_images = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "layout__desc__text")))
		return str(text_images[0].text)

driver = webdriver.Chrome(executable_path=r"C:\\chromedriver.exe")
driver.get("https://www.yandex.ru")
assert "Яндекс" in driver.title
dict_element_located = {
			"link_to_pictures" : '//a [@data-id = "images"]',
			"link_to_firts_picture" :'//div [@class = "cl-teaser cl-teaser_card cl-teaser_fixed"]',
			"link_to_next_picture" : '//div [@title = "Следующая"]',
			"link_to_previous_picture" : '//div [@title = "Предыдущая"]'
			}
Class_main(driver).click_element(dict_element_located.get("link_to_pictures"))
Class_main(driver).click_element(dict_element_located.get("link_to_firts_picture"))
first_text_img = Class_main(driver).text_img()
Class_main(driver).click_element(dict_element_located.get("link_to_next_picture"))
Class_main(driver).click_element(dict_element_located.get("link_to_previous_picture"))
prev_text_img = Class_main(driver).text_img()
if prev_text_img == first_text_img:
	print('The same image')
#driver.close()

