from datetime import datetime, timezone
from time import sleep

import psycopg2
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condicao_esperada
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

conexao = psycopg2.connect(
    database='railway',
    user='postgres',
    password= password,
    host= 'containers-us-west-46.railway.app',
    port='7327'
)


sql = conexao.cursor()


def new_product(sql, conexao, name, price, site, link_image, quote_date):
    query = "SELECT * FROM app_price_search_product WHERE name=%s and price=%s and site=%s"
    values = (name, price, site)
    result = sql.execute(query, values)
    dados = sql.fetchall()
    
    if len(dados) == 0:
        query = 'INSERT INTO app_price_search_product(name, price, site, quote_date, link_image) VALUES( %s, %s, %s, %s, %s)'
        values = (name, price, site, quote_date, link_image)
        sql.execute(query, values)
    else:
        print('Dados já cadastrados')
        

# new_product(sql, conexao, 'Xbox Series X', 4000.59, 'https://www.xbox.com/pt-BR/consoles/xbox-series-x', datetime.now(), 'https://i.ibb.co/Lt6WnJ8/console-microsoft-xbox-series-x-1tb-preto-rrt-00006-1601067024-g.jpg' )
    conexao.commit()    


def start_driver():
    chrome_options = Options()
     #--headless    
    arguments = ['--lang=en-US', '--window-size=1920,1080',
                 '--incognito', ] 
        
    for argument in arguments:
        chrome_options.add_argument(argument)     
        
    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False, 
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_settings_values.automatic_downloads': 1
    })
    
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException,
        ]
    )
    return driver, wait



def scan_site_1(item):
    #casas bahia
    driver, wait = start_driver()
    driver.get('https://www.casasbahia.com.br/'+item+'/b')
    names = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="sc-2b5b888e-0 jEybNn"]/h3')))
    prices = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="sc-c0914aad-2 hdvMuk"]/span[@class="sc-c0914aad-9 hTVULn"]' )))
    site = driver.current_url                                                                  
    link_image = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH, '//div[@class="sc-b78556c4-5 jkQmcY"]/span/img'))) 
    name = names[0].text
    price1 = prices[0].text.split(' ')[2].replace('.','')
    price = price1.replace(',', '.')
    image = link_image[0].get_attribute('src')
    
    new_product(sql, conexao, name, price, site, image, datetime.now())
    
def scan_site_2():
    #magazine luiza
    pass

def scan_site_3():
    #mercado livre
    pass




item = 'iphone 14 pro max'
prod = item.replace(' ', '-')
scan_site_1(prod)