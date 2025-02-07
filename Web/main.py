from datetime import datetime
from time import sleep
import pandas as pd
import threading
import queue
import os

from Functions.funcs import Funcs
from Functions.tokio_tmj import TokioTmj
from Config.configs import LOGIN,SENHA,FILE_PATH_EXCEL_TO_READ,FILE_PATH_EXCEL_EXIT


class Worker():
        
    def __init__(self,lista:list,data_queue:object) -> None:
        self.df = pd.DataFrame(lista)
        
        self.data_queue = data_queue
    
        self.acess_tmj = TokioTmj(LOGIN,SENHA)
        self.funcoes = Funcs()
        
    def start_coleta_codigos(self) -> None:
        
        status_code_tmj = self.acess_tmj.response.status_code
        if status_code_tmj == 200:
        
            for _,row in self.df.iterrows():
                pasta = str(row['PASTAS']).strip()

                try:
                    
                    response = self.acess_tmj.main_tmj(pasta)
                
                    text_boleto = response[0]
                    valor_boleto = response[1]
                    parcela = response[2]
                    

                    if text_boleto == 'AGUARDANDO AUTORIZAă├O - ANALISTA INTERNO':
                        text_boleto = 'AGUARDANDO AUTORIZAÇÃO - ANALISTA INTERNO'

                   
                    if text_boleto != 'acordo novo' and text_boleto != 'Pasta nao é da forte' and text_boleto != 'Não foi possivel' and text_boleto != 'AGUARDANDO AUTORIZAÇÃO - ANALISTA INTERNO'and text_boleto != 'RECUSADO' and text_boleto != 'LIQUIDADO' and text_boleto != 'ENCERRADO':
                        codigo = self.funcoes.get_codigo(text_boleto)
                        
                        if codigo:
                            if valor_boleto:
                                message = f'Pasta:{pasta}\nCodigo:{codigo}\nValor:{valor_boleto}\nParcela:{parcela}'
                                
                        else:
                            codigo = 'acordo novo'
                            valor_boleto = 'acordo novo'
                            parcela = 'acordo novo'
                  
                            message = f'Pasta:{pasta}\nCodigo:{codigo}\nValor:{valor_boleto}\nParcela:{parcela}'
                    
                    else:
                        
                        codigo = str(text_boleto)
                        valor_boleto = str(text_boleto)
                        parcela = str(text_boleto)
                        
                        message = f'Pasta:{pasta}\nCodigo:{codigo}\nValor:{valor_boleto}\nParcela:{parcela}'
                  

                except Exception as e:
                    
                    codigo = 'não encontrado'
                    valor_boleto = 'não encontrado'
                    parcela = 'não encontrado'
                    
                    message = f'Pasta:{pasta}\nCodigo:{e}\nValor:{e}\nParcela:{e}'
                   

                
                finally:
                    
                    s = pd.Series(
                        {'PASTAS':pasta , 
                        'PARCELA' : parcela,
                        'COD' : codigo,
                        'VALOR' : valor_boleto              
                    }, name='0')
                    
                    self.data_queue.put(s)
                    
                    print(message)
                    print(60 * '__')
                        

    
    
    
class Gerenciador():
    
    def __init__(self) -> None:
        self.funcoes = Funcs()
      
    def start(self,excel_path_to_read:str,excel_exit:str) -> None:
        data_queue = queue.Queue() 
        
        df = pd.read_excel(excel_path_to_read ,dtype=str)

        numero_raw = len(df)  /  1 # < Número que deve ser trocado para divisão < 
        
        try:
            numero_raw = len(df)  /  1# < Número que deve ser trocado para divisão < 
            lista_separada = self.funcoes.separar_lista(df,int(numero_raw))
        
        
        except:
            numero_raw = len(df)  /  1# < Número que deve ser trocado para divisão < 
            lista_separada = self.funcoes.separar_lista(df,int(numero_raw))
        
        inicio = datetime.now()

        threads = []
        for index,lista in enumerate(lista_separada):

                
            instancia = Worker(lista,data_queue)
            
            sleep(2)
            t = threading.Thread(target=instancia.start_coleta_codigos)
            threads.append(t)
            t.start()

        # Aguarda todas as threads terminarem
        for t in threads:
            t.join()

        fim = datetime.now()

        tempo = fim - inicio

        print(tempo)
            
        # Cria um DataFrame do pandas a partir dos dados coletados
        df1 = pd.DataFrame(list(data_queue.queue))
        
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        df1.to_excel(fr"{desktop}\{excel_exit}" , index=False)  



  
if __name__ == '__main__':                  
    Gerenciador().start(FILE_PATH_EXCEL_TO_READ,FILE_PATH_EXCEL_EXIT)               
