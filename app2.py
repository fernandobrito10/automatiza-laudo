from openai import OpenAI
import os
import ldap3
from supabase import create_client, Client
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk, ThemedStyle
load_dotenv()
# Configurações
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
# Variáveis globais
user_credentials = {"username": "", "password": ""}
# Cliente Deepseek
deepseek_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1",
)
def generate_technical_summary(texto):
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": """Você é um assistente técnico especializado em redação de laudos corporativos. 
                    Gere dois campos baseados no motivo informado:
                    1. FINALIDADE: Uma frase curta e direta (máx. 15 palavras)
                    2. SUPORTE TÉCNICO: Resumo técnico objetivo (2-3 frases)"""
                },
                {
                    "role": "user", 
                    "content": f"Motivo informado: {texto}"
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro na API: {e}")
        return "FINALIDADE: Não especificado\nSUPORTE TÉCNICO: Não especificado"
def parse_ai_response(response):
    lines = response.split('\n')
    finalidade = lines[0].replace("FINALIDADE: ", "").strip() if len(lines) > 0 else "Não especificado"
    suporte = lines[1].replace("SUPORTE TÉCNICO: ", "").strip() if len(lines) > 1 else "Não especificado"
    return finalidade, suporte
def generate_fixed_content():
    quantidade = quantidade_entry.get() or "01"
    motivo = motivo_entry.get("1.0", tk.END).strip()
    
    ai_response = generate_technical_summary(motivo)
    finalidade, suporte = parse_ai_response(ai_response)
    
    return f"""ITENS DA REQUISIÇÃO COM VALORES ESTIMADOS:
{quantidade} UN - NOTEBOOK HOMOLOGADO PARA T.I
Obs.: Alocar bem para o colaborador {name_entry.get()} ({user_id_entry.get()})
FINALIDADE: {finalidade}
SUPORTE TÉCNICO (Resumo): {suporte}
Link de referência: Homologado pela equipe de TI , Item de estoque.
LICENCIAMENTO:
01 Licença Call de WTS (Licença padrão para uso - Microsoft):.......................................... R$ 370,00
01 Licença Call de Windows (Licença padrão para uso - Microsoft):................................... R$ 97,00
01 Licença Call de Antivírus (Licença padrão para Software Antivírus - Anual):....................... R$ 71,00
01 Licença Call de Worktime (Software controle de Produtividade):.................................... R$ 14,00
01 Licença Call Desktop Central UEM Single user Anual (Valor em dólares):........................... $ 7,32"""
def fetch_by_id(user_id):
    response = supabase.table('users').select('name').eq('user', user_id).execute()
    return response.data[0]['name'] if response.data else ''
def fetch_by_name(name):
    response = supabase.table('users').select('user').eq('name', name).execute()
    return response.data[0]['user'] if response.data else ''
def on_id_change(*args):
    if user_id := user_id_entry.get():
        if hasattr(on_id_change, 'after_id'):
            janela.after_cancel(on_id_change.after_id)
        on_id_change.after_id = janela.after(500, lambda: update_name_from_id(user_id))
def update_name_from_id(user_id):
    name_entry.delete(0, tk.END)
    name_entry.insert(0, fetch_by_id(user_id))
def on_name_change(*args):
    if name := name_entry.get():
        if hasattr(on_name_change, 'after_id'):
            janela.after_cancel(on_name_change.after_id)
        on_name_change.after_id = janela.after(500, lambda: update_id_from_name(name))
def update_id_from_name(name):
    user_id_entry.delete(0, tk.END)
    user_id_entry.insert(0, fetch_by_name(name))
def show_preview():
    preview_window = tk.Toplevel(janela)
    preview_window.title("Pré-visualização do Laudo")
    preview_window.geometry("600x800")
    
    preview_text = tk.Text(preview_window, height=50, width=80)
    preview_text.pack(pady=10, padx=10)
    
    content = generate_fixed_content()
    preview_text.insert(1.0, content)
    preview_text.config(state="disabled")
def attempt_login():
    global user_credentials
    user_credentials["username"] = username_entry.get()
    user_credentials["password"] = password_entry.get()
    
    if user_credentials["username"] and user_credentials["password"]:
        login_window.destroy()
        janela.deiconify()
# Configuração da janela principal
janela = ThemedTk(theme="equilux")
janela.title("Fazedor de laudo")
janela.geometry("600x800")
janela.withdraw()
# Configuração do Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
# Janela de login
login_window = ThemedTk(theme="equilux")
login_window.title("Login")
login_window.geometry("300x150")
style = ThemedStyle(login_window)
style.set_theme("equilux")
login_frame = ttk.Frame(login_window)
login_frame.pack(pady=20, padx=20, fill="both", expand=True)
ttk.Label(login_frame, text="Usuário:").grid(row=0, column=0, sticky="w")
username_entry = ttk.Entry(login_frame)
username_entry.grid(row=0, column=1, pady=5)
ttk.Label(login_frame, text="Senha:").grid(row=1, column=0, sticky="w")
password_entry = ttk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, pady=5)
login_button = ttk.Button(login_frame, text="Entrar", command=attempt_login)
login_button.grid(row=2, columnspan=2, pady=10)
# Configuração da interface principal
style = ThemedStyle(janela)
style.set_theme("equilux")
main_frame = ttk.Frame(janela)
main_frame.pack(pady=10, padx=10, fill="both", expand=True)
# Campos superiores
user_frame = ttk.Frame(main_frame)
user_frame.pack(fill="x", pady=5)
# Campo de quantidade
quantidade_frame = ttk.Frame(user_frame)
quantidade_frame.pack(side="left", padx=5)
ttk.Label(quantidade_frame, text="Quantidade:").pack()
quantidade_entry = ttk.Entry(quantidade_frame, width=5)
quantidade_entry.insert(0, "01")
quantidade_entry.pack()
# Campos de ID e Nome
id_frame = ttk.Frame(user_frame)
id_frame.pack(side="left", padx=5)
ttk.Label(id_frame, text="ID do Colaborador:").pack()
user_id_entry = ttk.Entry(id_frame, width=15)
user_id_entry.pack()
name_frame = ttk.Frame(user_frame)
name_frame.pack(side="left", padx=5)
ttk.Label(name_frame, text="Nome do Colaborador:").pack()
name_entry = ttk.Entry(name_frame, width=30)
name_entry.pack()
# Campo de motivo
motivo_frame = ttk.Frame(main_frame)
motivo_frame.pack(fill="x", pady=10, padx=5)
ttk.Label(motivo_frame, text="Descreva o motivo da compra:").pack(anchor="w")
motivo_entry = tk.Text(motivo_frame, height=5, width=50)
motivo_entry.pack(fill="x")
# Variáveis de controle
name_var = tk.StringVar()
user_id_var = tk.StringVar()
name_entry.config(textvariable=name_var)
user_id_entry.config(textvariable=user_id_var)
name_var.trace('w', on_name_change)
user_id_var.trace('w', on_id_change)
# Botão de geração
preview_button = ttk.Button(main_frame, text="Gerar Laudo", command=show_preview)
preview_button.pack(pady=15)
# Iniciar aplicação
login_window.mainloop()
janela.mainloop()