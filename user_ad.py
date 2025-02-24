from ldap3 import Server, Connection, ALL
from dotenv import load_dotenv
import os

load_dotenv()

AD_SERVER = "ldap://adsrvsob03"
USERNAME = os.getenv("ad_login") 
PASSWORD = os.getenv("ad_senha")  
BASE_DN = "DC=sob,DC=ad-grendene,DC=com"  

def pegarUser(nomeAprovador):
    server = Server(AD_SERVER, get_info=ALL)
    conn = Connection(server, user=USERNAME, password=PASSWORD, auto_bind=True)
    search_filter = f"(cn={nomeAprovador})"
    conn.search(BASE_DN, search_filter, attributes=['sAMAccountName'])
    if conn.entries:
        idAprovador = conn.entries[0]['sAMAccountName'].value
    return idAprovador