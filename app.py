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
        
        
        

new_product(sql, conexao, 'Xbox Series X', 4000.59, 'https://www.xbox.com/pt-BR/consoles/xbox-series-x', datetime.now(), 'https://i.ibb.co/Lt6WnJ8/console-microsoft-xbox-series-x-1tb-preto-rrt-00006-1601067024-g.jpg' )
conexao.commit()    