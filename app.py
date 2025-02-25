from openai import OpenAI
import os
import requests
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk, ThemedStyle
from dotenv import load_dotenv

load_dotenv()

# Configurações globais
AGIDESK_API_KEY = os.getenv("AGIDESK_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
AGIDESK_API_URL = "https://api.agidesk.com/v1"

# Cliente DeepSeek
deepseek_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1",
)

def buscar_contato_agidesk(query):
    """Busca contatos na API do Agidesk"""
    headers = {"Authorization": f"Bearer {AGIDESK_API_KEY}"}
    try:
        response = requests.get(
            f"{AGIDESK_API_URL}/contacts/search",
            headers=headers,
            params={"query": query}
        )
        response.raise_for_status()
        data = response.json()
        return data["contacts"][0] if data.get("total", 0) > 0 else None
    except Exception as e:
        print(f"Erro na consulta ao Agidesk: {e}")
        return None

def fetch_by_id(user_id):
    """Busca nome pelo ID usando Agidesk"""
    contato = buscar_contato_agidesk(user_id)
    return contato.get("name") if contato else ""

def fetch_by_name(name):
    """Busca ID pelo nome usando Agidesk"""
    contato = buscar_contato_agidesk(name)
    return str(contato.get("id")) if contato else ""

def generate_technical_summary(texto):
    """Gera resumos com DeepSeek"""
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "Gere:\n1. FINALIDADE: Resumo curto (15 palavras)\n2. SUPORTE TÉCNICO: Resumo detalhado (2-3 frases)"
                },
                {"role": "user", "content": texto}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro na Deepseek: {e}")
        return "FINALIDADE: \nSUPORTE TÉCNICO: "

def parse_ai_response(response):
    """Processa resposta da IA"""
    lines = response.split('\n')
    finalidade = lines[0].replace("FINALIDADE: ", "").strip() if lines else "Não especificado"
    suporte = lines[1].replace("SUPORTE TÉCNICO: ", "").strip() if len(lines) > 1 else "Não especificado"
    return finalidade, suporte

def on_id_change(*args):
    """Atualiza nome ao mudar ID"""
    if user_id := user_id_entry.get():
        if hasattr(on_id_change, 'after_id'):
            janela.after_cancel(on_id_change.after_id)
        on_id_change.after_id = janela.after(500, lambda: update_name_from_id(user_id))

def update_name_from_id(user_id):
    """Atualiza campo de nome"""
    name_entry.delete(0, tk.END)
    name_entry.insert(0, fetch_by_id(user_id))

def on_name_change(*args):
    """Atualiza ID ao mudar nome"""
    if name := name_entry.get():
        if hasattr(on_name_change, 'after_id'):
            janela.after_cancel(on_name_change.after_id)
        on_name_change.after_id = janela.after(500, lambda: update_id_from_name(name))

def update_id_from_name(name):
    """Atualiza campo de ID"""
    user_id_entry.delete(0, tk.END)
    user_id_entry.insert(0, fetch_by_name(name))

def generate_fixed_content():
    """Gera conteúdo do laudo"""
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

def show_preview():
    """Exibe pré-visualização"""
    preview_window = tk.Toplevel(janela)
    preview_window.title("Pré-visualização do Laudo")
    preview_window.geometry("600x800")
    
    preview_text = tk.Text(preview_window, height=50, width=80)
    preview_text.pack(pady=10, padx=10)
    preview_text.insert(1.0, generate_fixed_content())
    preview_text.config(state="disabled")

# Configuração da interface principal
janela = ThemedTk(theme="equilux")
janela.title("Fazedor de laudo")
janela.geometry("600x800")

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

# Rastreamento de alterações
name_var.trace('w', on_name_change)
user_id_var.trace('w', on_id_change)

# Botão de geração
preview_button = ttk.Button(main_frame, text="Gerar Laudo", command=show_preview)
preview_button.pack(pady=15)

# Iniciar aplicação
janela.mainloop()