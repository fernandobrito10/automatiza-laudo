import requests
from dotenv import load_dotenv
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

def requisicaoIDs(id):
    url = "https://grendene.agidesk.com/api/v1/issues?"
    
    params = {
        "app_key": os.getenv("AGIDESK_API_KEY"),
        "id": id,
        "forecast": "teams"
    }
    
    headers = {
        "X-Tenant-ID": "grendene",
        "Authorization": f"Bearer {os.getenv('AGIDESK_API_KEY')}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, verify=False)
        response.raise_for_status()
        
        data = response.json()
        
        responsible_id = data[0]['responsible_id']
        first_follower = data[0]['followers'][0]
        follower_data = {
            'id': first_follower['id'],
            'title': first_follower['title'],
            'slug': first_follower['slug']
        }
        
        return responsible_id, follower_data
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {str(e)}")
        raise

def requisicaoCentrodeCusto(id):
    url = "https://grendene.agidesk.com/api/v1/contacts?"
    
    params = {
        "app_key": os.getenv("AGIDESK_API_KEY"),
        "username": id
    }
    
    headers = {
        "Authorization": f"Bearer {os.getenv('AGIDESK_API_KEY')}"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, verify=False)
        response.raise_for_status()
        
        data = response.json()
        
        return data[0]['costcenter']['title']
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {str(e)}")
        raise
