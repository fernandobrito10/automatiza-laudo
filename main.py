from scrape import pegarDados
from centro_de_custos import encontrar_aprovador
from user_ad import pegarUser

atd_id = input("Digite o número do atendimento: ")

try:
    id_usuario, nome_usuario, cc_usuario = pegarDados(atd_id)
    aprovador = encontrar_aprovador(cc_usuario)
    user_aprovador = pegarUser(aprovador)
    print(f"""
        Solicitante: {nome_usuario} ({id_usuario})
        Centro de custo: {cc_usuario}
        Aprovador: {aprovador} ({user_aprovador})
    """)
except Exception as e:
    print(f"\nErro ao coletar dados: {str(e)}")