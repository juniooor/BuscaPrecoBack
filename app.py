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

with open("password.txt", "r") as arquivo:
    senha = arquivo.readline()
    
with open("host.txt", "r") as arquivo:
    host = arquivo.readline()


conexao = psycopg2.connect(
    database='railway',
    user='postgres',
    password=senha,
    host=host,
    port='7327'
)


sql = conexao.cursor()


def new_product(sql, conexao, name, price, site, link_image, quote_date):
    query = "SELECT * FROM app_price_search_product WHERE name=%s and price=%s and site=%s"
    values = (name, price, site)
    result = sql.execute(query, values)
    dados = sql.fetchall()
    
    if len(dados) == 0:
        query = 'INSERT INTO app_price_search_product(name, price, site, quote_date, link_image) VALUES( %s, %s, %s, %s, %s,)'
        values = (name, price, site, quote_date, link_image)
        

# new_product(sql, conexao, 'Xbox Series X', 4000.59, 'https://www.xbox.com/pt-BR/consoles/xbox-series-x', datetime.now(), 'https://i.ibb.co/Lt6WnJ8/console-microsoft-xbox-series-x-1tb-preto-rrt-00006-1601067024-g.jpg' )
conexao.commit()    

def start_driver():
    chrome_options = Options()
    
    arguments = ['--lang=en-US', '--window-size=1920,1080',
                 '--incognito', ''] #--headless
    
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

item = 'iphone 14 pro max'
item = item.replace(' ', '-')

def scan_site_1(item):
    driver, wait = start_driver()
    driver.get('https://www.americanas.com.br/busca'+item)
    
def scan_site_2():
    pass

def scan_site_3():
    pass
