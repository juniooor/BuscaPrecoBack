from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.americanas.com.br/busca/iphone-14-pro-max')

# Localiza o primeiro elemento img dentro do xpath especificado na página
element = driver.find_element_by_xpath("//div[@class='src__Wrapper-sc-xr9q25-1 ebFfaU']/picture[@class='src__Picture-sc-xr9q25-2 ghIIuE']/img")

# Imprime o atributo src do elemento
print(element.get_attribute('src'))

driver.quit()
