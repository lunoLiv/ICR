import time
from selenium import webdriver
from selenium.webdriver.common.by import By


login = 'luiz.leite'
senha = '12345678'
pasta = input('Insira o número da pasta: ')

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get('http://10.149.30.10:3000/')

caixaLogin = driver.find_element('name','login')
caixaLogin.send_keys(login)

caixaSenha = driver.find_element('name','password')
caixaSenha.send_keys(senha)

caixaSenha.submit()

botaoCobranca = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/button[1]')
botaoCobranca.click()

botaoConsulta1 = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div[1]/div/ul/li[7]/a')
botaoConsulta1.click()

botaoConsulta2 = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[1]/div/ul/ul/a[1]')
botaoConsulta2.click()

inputPasta = driver.find_element(By.NAME,'folder_number')
inputPasta.send_keys(pasta)
inputPasta.submit()

valorTotal = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div[4]/div[1]/div/div[3]/div[5]/p[2]')
valorTotal = valorTotal.text[3:]

parcelas = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div[4]/div[1]/div/div[3]/div[3]/p[2]')
parcelas = parcelas.text

driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div[4]/div[1]/div/button').click()

driver.quit()
