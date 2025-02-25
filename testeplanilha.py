import requests
import os
from dotenv import load_dotenv

load_dotenv()

def download_excel():
    try:
        # URL da planilha
        url = "https://grendenecombr-my.sharepoint.com/personal/fernando_brito_grendene_com_br/_layouts/15/download.aspx?SourceUrl=/personal/fernando_brito_grendene_com_br/Documents/Centro%20de%20custos_Maio2024.xlsx"
        
        # Headers para simular um navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cookie': os.getenv("SHAREPOINT_COOKIE")  # Você precisará adicionar o cookie de autenticação
        }
        
        # Fazer o download
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            with open('planilha_local.xlsx', 'wb') as f:
                f.write(response.content)
            print("Arquivo baixado com sucesso!")
            return True
        else:
            print(f"Erro ao baixar arquivo. Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Erro ao acessar arquivo: {str(e)}")
        return False

if __name__ == "__main__":
    download_excel()
