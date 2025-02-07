import os, time


def limpar_data(t):
    
    dia = t[8:-14]

    if dia[0] == ' ':
        dia = f'0{dia[1]}'

    if 'Dec' in t:
        mes = '12'

    if 'Jan' in t:
        mes = '01'
    
    if 'Feb' in t:
        mes = '02'

    ano = t[-4:]
    
    data = f'{dia}/{mes}/{ano}'
    return data


local = 'arquivos'

os.chdir(local)
lista = os.listdir()

tempo = []

for i in lista: 
    t = time.ctime(os.path.getmtime(i))
    tempo.append(limpar_data(t))

counter = 0

for i,j in zip(lista,tempo):

    end = f';{i};{j}'
    with open(i, "r",encoding='utf-8') as f:
        rows = f.readlines()[1:]

        print(counter)
        for k in rows:
            k = k[:-1]

            with open('main.csv','a',encoding='utf-8') as main:
                main.write(f'{k}{end}\n')

    counter+=1
    
