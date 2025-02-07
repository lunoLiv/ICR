from datetime import datetime, timedelta
import re


class Funcs():
    
    def __init__(self) -> None:
        pass
    
    def get_codigo(self,text_boleto:str) -> str|bool:
       
        
        text_boleto = text_boleto.replace('  ',' ')
            
        padrao = r'\[\d{3}\-\d{6}.\d{5}\s\d{5}.\d{6}\s\d{5}.\d{6}\s\d{1}\s\d{14}'
            
        encontrado = re.search(padrao, text_boleto)
        if encontrado:
            codigo = encontrado.group()#retirar texto do objeto
            codigo = codigo.replace('[033-7','').strip()
        
        else:
            codigo = False
            
        return codigo

    def primeiro_sabado(self) -> str:
        # Obter a data atual
        data_atual = datetime.now()

        # Calcular os dias restantes até o próximo sábado (0 = segunda-feira, 1 = terça-feira, ..., 5 = sábado)
        dias_restantes = (5 - data_atual.weekday() + 7) % 7

        # Calcular a data do próximo sábado
        data_sabado = data_atual + timedelta(days=dias_restantes)
        data_sabado = str(data_sabado).split(' ')
        data_sabado = data_sabado[0].split('-')
        ano = data_sabado[0]
        mes = data_sabado[1]
        dia = data_sabado[2]
        
        data_correta = dia+'/'+mes+'/'+ano
        
        return data_correta

    def verifica_atraso(self,data_venct:str) -> str:
        
        dados_data = data_venct.split('/')
        dia = dados_data[0]
        mes = dados_data[1]
        ano = dados_data[2]
        
        
        # Obter a data atual
        data_atual = datetime.now()

        # Suponha que você tenha uma data fornecida, por exemplo, 2023-10-15
        data_fornecida = datetime(int(ano),int(mes),int(dia))

        # Verificar se a data fornecida está em atraso
        if data_fornecida < data_atual:
            
            dia_fornecido = data_fornecida.day
            mes_fornecido = data_fornecida.month
            ano_fornecido = data_fornecida.year

            data1 = f'{dia_fornecido}/{mes_fornecido}/{ano_fornecido}'

            dia_atual = data_atual.day
            mes_atual = data_atual.month
            ano_atual = data_atual.year

            data2 = f'{dia_atual}/{mes_atual}/{ano_atual}'


            if data1 == data2:
                return 'nao esta em atraso'
            else:
                return 'esta em atraso'
    
        else:
            return 'nao esta em atraso'

    def separar_lista(self,lista: list, quantidade: int) -> list:
        new_list = []
        for index in range(0, len(lista), quantidade):
            new_list.append(lista[index:index+quantidade])
        return new_list


