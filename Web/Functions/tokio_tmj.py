from bs4 import BeautifulSoup
from time import sleep
from io import BytesIO
import requests
import PyPDF2

from Functions.funcs import Funcs



class TokioTmj():
    
    def __init__(self,login_user:str,senha:str) -> None:
        
        self.login_user = login_user
        self.senha = senha
        self.funcoes = Funcs()
        
        
        self.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-api-version": "protocol=1.0,resource=2.1",
            "accept-language": "en-US,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Brave\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "x-nosession": "true",
            "x-password": "anonymous",
            "x-requested-with": "XMLHttpRequest",
            "x-username": "anonymous",
            "Referer": "https://ssoportais3.tokiomarine.com.br/openam/XUI/?realm=TOKIOLFR&goto=http://portalparceiros.tokiomarine.com.br/sin/TMJ/home?perfil_simulado=6",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        
        self.session = requests.Session()
        
        
        self.response = self.login_tmj()

    def acessa_tokio_token(self) -> requests.Response: #retorna um objeto de tipo response da lib requests 
     
        self.session.get("https://ssoportais3.tokiomarine.com.br/openam/XUI/?realm=TOKIOLFR&goto=http://portalparceiros.tokiomarine.com.br/#login/",headers=self.headers)
        
        response = self.session.post(
            'https://ssoportais3.tokiomarine.com.br/openam/json/realms/root/realms/tokiolfr/authenticate?goto=http://portalparceiros.tokiomarine.com.br/',headers=self.headers)
        
        return response
       
    def get_auth_id(self) -> str: 
        
        contador = 0

        while True:

            response = self.acessa_tokio_token()

            if 'META NAME="robots"' in response.text or 'META NAME="ROBOTS"' in response.text:
                contador+= 1 
                sleep(1)

                print(f"Tentando novo acesso N{contador}")
                pass

            else:
                break


        auth_id = response.json()['authId']
        print(auth_id)

        return auth_id

    def login_tmj(self) -> requests.Response: #retorna um objeto de tipo response da lib requests 
        
        auth_id = self.get_auth_id()

        body = {"authId": auth_id, "template": "", "stage": "JDBC1", "header": "Sign in", "callbacks": [{"type": "NameCallback", "output": [{"name": "prompt", "value": "UserName"}], "input": [
            {"name": "IDToken1", "value": self.login_user}]}, {"type": "PasswordCallback", "output": [{"name": "prompt", "value": "Password"}], "input": [{"name": "IDToken2", "value": self.senha}]}]}
      

        response = self.session.post('https://ssoportais3.tokiomarine.com.br/openam/json/realms/root/realms/tokiolfr/authenticate?goto=http://portalparceiros.tokiomarine.com.br/sin/TMJ/home?perfil_simulado=6', json=body, headers=self.headers)

        url_1 = 'https://portalparceiros.tokiomarine.com.br/group/portal-prestador#/juridico'
        response = self.session.get(url_1,timeout=30)

        url_2 = 'https://portalparceiros.tokiomarine.com.br/sin/TMJ/login/externo/final'
        response = self.session.get(url_2,timeout=30)
        
        return response
    
    def emitir_boleto(self,cod_parcela:str,data_venct:str,headers:dict[str,str]) -> str:
                                
        try:
            url_parcela = f'https://portalparceiros.tokiomarine.com.br/sin/TMJ/operacoes/pasta/acordo/ress/abrirparcela/{cod_parcela}'
            response = self.session.get(url_parcela,headers=headers,timeout=30)
            
            url_emitir = f'https://portalparceiros.tokiomarine.com.br/sin/TMJ/operacoes/pasta/acordo/ress/emitir'
            
            payload = {
                
                "idParcelaRessarcimento":f"{cod_parcela}",
                "novaDataVencimento": f"{data_venct}"
                
            }
        
            response = self.session.post(url_emitir,data=payload)
            if response.status_code == 200:
                message = 'Boleto emitido'
            return message
        except:
            return 'Nao foi possivel emitir o boleto'
    
    def reemitir_boleto(self,cod_parcela:str,headers:dict[str,str],data_venct:str) -> str:

        try:
            url_parcela = f'https://portalparceiros.tokiomarine.com.br/sin/TMJ/operacoes/pasta/acordo/ress/parcela'
            response = self.session.get(url_parcela,headers=headers,timeout=30)
            
            url_reemitir = f'https://portalparceiros.tokiomarine.com.br/sin/TMJ/operacoes/pasta/acordo/ress/reemitir'

            
            payload = {
                
                "idParcelaRessarcimento":f"{cod_parcela}",
                "novaDataVencimento": f"{data_venct}"
                
            }
        
            response = self.session.post(url_reemitir,data=payload)
            if response.status_code == 200:
                message = 'Boleto emitido'
            return message
        except:
            return 'Nao foi possivel emitir o boleto'
        
    def baixa_boleto(self, cod_parcela:str, headers:dict[str,str], url_base:str) -> str|bool:
        url_parcela = f'https://portalparceiros.tokiomarine.com.br/sin/TMJ/operacoes/pasta/acordo/ress/abrirparcela/{cod_parcela}'
        
        try:
            response = self.session.get(url_parcela, headers=headers, timeout=30)
            
            soup2 = BeautifulSoup(response.text, "html.parser")
            row2 = soup2.select('tbody')[8]

            if row2:
                row2 = row2.select('tr')
                tamanho = len(row2) - 1
             

                for index, row in enumerate(row2):
              
                    try:
                        itens_row = [row.get_text().strip() for row in row]
                        if 'SOLICITADO' in itens_row[17]:
                            columns = row.find_all('td')
                            
                            for column in columns:
                                link = column.find('a')
                                if link:
                                    href = link.get('href')
                                    url_boleto = url_base + href
                                    
                                    r = self.session.get(url_boleto)
                                    r.raise_for_status()  # Verifica se houve erro no download
                                    
                                    
                                    with BytesIO(r.content) as bytes_io:
                                        pdf_reader = PyPDF2.PdfReader(bytes_io)
                                        pdf_text = (
                                            "".join([page.extract_text() for page in pdf_reader.pages]).replace("  ", " ").split("\n") 
                                        )
                                        
                                    
                                    joined_pdf_text = " ".join(pdf_text)
                                    valor = itens_row[21]
           
                                    return joined_pdf_text, valor

                    except IndexError:
                        print("Erro ao acessar índice em itens_row")

                print("Nenhum boleto solicitado encontrado.")

            else:
                print("Não foi possível encontrar a tabela de boletos.")

        except requests.RequestException as e:
            print(f"Erro durante a requisição: {e}")

            return False, False  

    def main_tmj(self,pasta:str) -> tuple[str|bool,str|bool,str|bool]:
        url_base =  str('https://portalparceiros.tokiomarine.com.br')
        
        try:
        
            url_3 = f'https://portalparceiros.tokiomarine.com.br/sin/TMJ/operacoes/pasta/geral/abrir/{pasta}'
            response = self.session.get(url_3)

            current_url = response.url


            if current_url == 'https://portalparceiros.tokiomarine.com.br/sin/TMJ/operacoes/pasta/geral/fianca/editar':

                url_5 = 'https://portalparceiros.tokiomarine.com.br/sin/TMJ/operacoes/pasta/acordo/ress/listar'
                response = self.session.get(url_5,headers=self.headers,timeout=30)
                soup = BeautifulSoup(response.content,'html.parser')
                rows = soup.select('tbody tr')
                
                qtd_rows = len(rows)

                qtd_rows2 = qtd_rows - 5 #COLETANDO APENAS O INDICE TOTAL DAS LINHAS DE ACORDO

                if qtd_rows == 0:
                    
                    return 'acordo novo','acordo novo'

                

                if qtd_rows > 2:
                    for index,row in enumerate(rows[4:]):
                                        
                        columns = row.find_all('td')  # Find all 'td' elements within the row
                        row = [column.get_text().strip() for column in columns] 
                        cod = row[0]
                        stts_acordo = row[2]
                        sacado = row[3]
                        
                        if sacado == '39422277000148 - FORTE ASSESSORIA & DOCUMENTACAO IMOBILIARIA LTDA':
                            
                            if stts_acordo == 'AUTORIZADO (PROVISIONADO)' or stts_acordo == 'AUTORIZADO (AGUARDANDO PROVISIONAMENTO)' :
                            
                                
                                url_6 = f'https://portalparceiros.tokiomarine.com.br/sin/TMJ/operacoes/pasta/acordo/ress/abrir/{cod}'          
                                response = self.session.get(url_6,headers=self.headers,timeout=30)
                                soup = BeautifulSoup(response.text , "html.parser")

                        
                                tamanho =  len(soup.select('tbody')) -1
                                tbody = soup.select('tbody')[tamanho]
                                    
                            
                                if tbody:
                                    rows_parcelas = tbody.select('tr')

                                
                                for row in rows_parcelas:
                                    columns = row.find_all('td')  
                                    row_parcela = [column.get_text().strip() for column in columns]
                                    
                                    try:
                                    
                                        cod_parcela = str(row_parcela[0])
                                        parcela = str(row_parcela[1])
                                        data_venct = str(row_parcela[2])
                                        stts_parc = str(row_parcela[10])

                                        if stts_parc == 'AGUARDANDO EFETIVAÇÃO':
                                            
                                            r = self.funcoes.verifica_atraso(data_venct)
                                            
                                            if r == 'nao esta em atraso':
                                            
                                                dados_baixa = self.baixa_boleto(cod_parcela,self.headers,url_base)
                                                text_boleto = dados_baixa[0]
                                                valor_boleto = dados_baixa[1]
                                                return text_boleto, valor_boleto, parcela
                                                
                                            
                                            
                                            if r == 'esta em atraso':
                                                data =  self.funcoes.primeiro_sabado()
                                                resposta = self.reemitir_boleto(cod_parcela,self.headers,data)
                                                if resposta == 'Boleto emitido':
                                                    dados_baixa = self.baixa_boleto(cod_parcela,self.headers,url_base)
                                                    text_boleto = dados_baixa[0]
                                                    valor_boleto = dados_baixa[1]
                                                    return text_boleto, valor_boleto, parcela
                                                else:
                                                    
                                                    return 'acordo novo', 'acordo novo', 'acordo novo'
                                                                        
                                        elif stts_parc == 'AGUARDANDO INTEGRAÇÃO':
                                            
                                            
                                            emitir = self.emitir_boleto(cod_parcela,data_venct,self.headers)
                                            if emitir == 'Boleto emitido':
                                                dados_baixa = self.baixa_boleto(cod_parcela,self.headers,url_base)
                                                text_boleto = dados_baixa[0]
                                                valor_boleto = dados_baixa[1]
                                                return text_boleto,valor_boleto,parcela
                                                    
                                        else:          
                                            pass
                                        
                                
                                        
                                    except Exception as e:
                                        
                                        print(e)

                            #Verificar os stts 
                            if index == qtd_rows2 and stts_acordo  == 'AGUARDANDO AUTORIZAă├O - ANALISTA INTERNO' or index == qtd_rows2 and stts_acordo == 'RECUSADO' or index == qtd_rows2 and stts_acordo == 'LIQUIDADO' or index == qtd_rows2 and stts_acordo == 'ENCERRADO':
                                
                                return stts_acordo,stts_acordo,stts_acordo
                        

        
                        else:
                            if index == qtd_rows2 and stts_acordo  == 'AGUARDANDO AUTORIZAă├O - ANALISTA INTERNO' or index == qtd_rows2 and stts_acordo == 'RECUSADO' or index == qtd_rows2 and stts_acordo == 'LIQUIDADO' or index == qtd_rows2 and stts_acordo == 'ENCERRADO':
                                
                                return stts_acordo,stts_acordo,stts_acordo
                           

                        
                
                else:
                    return 'acordo novo', 'acordo novo' , 'acordo novo'
            
            else:
                return 'Pasta nao é da forte','Pasta nao é da forte','Pasta nao é da forte'

           
        except:
            text_boleto = False
            valor_boleto = False
            parcela = False
            return text_boleto,valor_boleto,parcela


