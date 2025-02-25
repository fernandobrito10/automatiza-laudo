from ldap3 import Server, Connection, ALL
from dotenv import load_dotenv
import os

load_dotenv()

AD_SERVER = "ldap://adsrvsob01"
USERNAME = os.getenv("ad_login") 
PASSWORD = os.getenv("ad_senha")  
BASE_DN = "DC=ad-grendene,DC=com"  

def pegarUser(nomeAprovador):
    try:
        server = Server(AD_SERVER, get_info=ALL)
        conn = Connection(server, user=USERNAME, password=PASSWORD, auto_bind=True)
        search_filter = f"(cn={nomeAprovador})"
        conn.search(BASE_DN, search_filter, attributes=['sAMAccountName'])
        
        if conn.entries:
            return conn.entries[0]['sAMAccountName'].value
        else:
            return "Usuário não encontrado"
            
    except Exception as e:
        return f"Erro ao buscar usuário: {str(e)}"
    finally:
        if 'conn' in locals():
            conn.unbind()