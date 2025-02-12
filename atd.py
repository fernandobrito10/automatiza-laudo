import os
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from dotenv import load_dotenv
from ttkthemes import ThemedTk

load_dotenv()

class AgideskApp:
    def __init__(self, master):
        self.master = master
        master.title("Consulta AGIDESK - Grendene")
        master.geometry("1000x800")
        
        # Configurações da API
        self.app_key = os.getenv("AGIDESK_APP_KEY")
        self.base_url = "https://grendene.agidesk.com/api/v1"
        self.tenant_id = "grendene"
        
        # Interface
        self.create_widgets()
        
    def create_widgets(self):
        # Configuração do layout
        main_frame = ttk.Frame(self.master)
        main_frame.pack(pady=30, padx=30, fill="both", expand=True)
        
        # Campo de entrada
        ttk.Label(main_frame, text="Nº do Atendimento:", font=('Helvetica', 14)).pack(anchor="w")
        self.atendimento_entry = ttk.Entry(main_frame, width=20, font=('Helvetica', 14))
        self.atendimento_entry.pack(fill="x", pady=15)
        
        # Botão de consulta
        consulta_btn = ttk.Button(
            main_frame,
            text="Buscar Atendimento",
            command=self.fazer_consulta,
            style="primary.TButton"
        )
        consulta_btn.pack(pady=20)
        
        # Área de resultados
        self.resultado_text = tk.Text(
            main_frame,
            height=25,
            width=100,
            state="disabled",
            font=('Consolas', 11),
            wrap="word",
            bg="#2E2E2E",
            fg="#FFFFFF"
        )
        self.resultado_text.pack(fill="both", expand=True, pady=10)
        
        # Configurar estilo
        self.configure_styles()
        
    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("primary.TButton", 
                        font=('Helvetica', 12, 'bold'),
                        padding=10,
                        foreground="#FFFFFF",
                        background="#1E88E5")
        
    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "X-Tenant-ID": self.tenant_id,
            "Authorization": f"Bearer {self.app_key}"
        }
        
    def fazer_consulta(self):
        atendimento_id = self.atendimento_entry.get().strip()
        
        if not atendimento_id.isdigit():
            error_msg = "O número do atendimento deve conter apenas dígitos"
            print(f"[ERRO] Validação: {error_msg}")
            messagebox.showerror("Erro", error_msg)
            return
            
        params = {
            "app_key": self.app_key,
            "id": atendimento_id,
            "forecast": "teams"
        }
        
        try:
            print(f"\n[INFO] Iniciando consulta ao atendimento #{atendimento_id}")
            print(f"[DEBUG] Parâmetros: {params}")
            
            response = requests.get(
                f"{self.base_url}/issues",
                headers=self.get_headers(),
                params=params,
                timeout=20
            )
            
            print(f"[DEBUG] Status Code: {response.status_code}")
            response.raise_for_status()
            
            data = response.json()
            print("[INFO] Dados recebidos com sucesso!")
            
            processed_data = self.processar_dados(data)
            self.mostrar_resultados(processed_data)
            
        except requests.exceptions.HTTPError as e:
            error_msg = self.parse_error(e)
            print(f"[ERRO] HTTP: {e.request.url}")
            print(f"[ERRO] Status: {e.response.status_code}")
            print(f"[ERRO] Resposta: {e.response.text}")
            messagebox.showerror("Erro na API", error_msg)
            
        except requests.exceptions.RequestException as e:
            print(f"[ERRO] Conexão: {str(e)}")
            messagebox.showerror("Erro de Conexão", f"Falha na comunicação com a API: {str(e)}")
            
        except Exception as e:
            print(f"[ERRO] Inesperado: {str(e)}")
            messagebox.showerror("Erro Inesperado", f"Erro: {str(e)}")
            
    def parse_error(self, error):
        try:
            error_response = error.response.json()
            error_msg = f"{error_response.get('error', 'Erro desconhecido')}\nDetalhes: {error_response.get('message', 'Sem detalhes')}"
            print(f"[ERRO] API: {error_msg}")
            return error_msg
        except:
            error_msg = f"Erro {error.response.status_code}: {error.response.text}"
            print(f"[ERRO] Parse: {error_msg}")
            return error_msg
            
    def processar_dados(self, data):
        issue = data.get('issue', {})
        print("[DEBUG] Estrutura dos dados recebidos:", data.keys())
        
        return {
            "id": issue.get('id', 'N/A'),
            "subject": issue.get('subject', 'Sem assunto'),
            "description": issue.get('description', 'Sem descrição'),
            "status": issue.get('status', {}).get('name', 'N/A'),
            "priority": issue.get('priority', {}).get('name', 'N/A'),
            "contact": {
                "name": issue.get('contact', {}).get('name', 'N/A'),
                "email": issue.get('contact', {}).get('email', 'N/A'),
                "phone": issue.get('contact', {}).get('phone', 'N/A')
            },
            "cost_centers": [cc.get('name', '') for cc in issue.get('cost_centers', [])],
            "responsible": {
                "name": issue.get('responsible', {}).get('name', 'N/A'),
                "team": issue.get('responsible_team', {}).get('name', 'N/A'),
                "slug": issue.get('responsible', {}).get('slug', 'N/A')
            },
            "created_at": issue.get('created_at', 'N/A'),
            "updated_at": issue.get('updated_at', 'N/A'),
            "content": issue.get('content', 'N/A')
        }
            
    def mostrar_resultados(self, data):
        self.resultado_text.config(state="normal")
        self.resultado_text.delete(1.0, tk.END)
        
        template = f"""══════════════[ DETALHES DO ATENDIMENTO #{data['id']} ]══════════════

▸ Status: {data['status']}
▸ Prioridade: {data['priority']}
▸ Criado em: {data['created_at']}
▸ Última atualização: {data['updated_at']}

══════════════[ RESPONSÁVEIS ]══════════════
• Responsável: {data['responsible']['name']}
• Equipe: {data['responsible']['team']}
• ID Responsável: {data['responsible']['slug']}

══════════════[ CONTATO ]══════════════
• Nome: {data['contact']['name']}
• Email: {data['contact']['email']}
• Telefone: {data['contact']['phone']}

══════════════[ CENTROS DE CUSTO ]══════════════
{'\n'.join([f'• {cc}' for cc in data['cost_centers'] if cc]) or '• Nenhum centro de custo associado'}

══════════════[ CONTEÚDO ]══════════════
{data['content']}

══════════════[ DESCRIÇÃO ]══════════════
{data['description']}
"""
        self.resultado_text.insert(1.0, template)
        self.resultado_text.config(state="disabled")
        print("[INFO] Resultados exibidos com sucesso!")

if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = AgideskApp(root)
    root.mainloop()