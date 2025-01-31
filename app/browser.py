def estado_boleto():
  estado = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div[3]/div[2]/div/div[2]/div')

  if estado.text == 'Quebra':
    numParcela = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div[4]/div[1]/div[2]/div[3]/div[2]/p[2]').text
    valorTotal = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div[4]/div[1]/div[2]/div[3]/div[5]/p[2]').text
