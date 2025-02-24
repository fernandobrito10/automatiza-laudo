from requisicao import requisicaoIDs, requisicaoCentrodeCusto
from centro_de_custos import encontrar_aprovador
from user_ad import pegarUser

atd_id = input("Digite o número do atendimento: ")

try:
    id_responsavel, dados_solicitante = requisicaoIDs(atd_id)
    cc_usuario = requisicaoCentrodeCusto(dados_solicitante['slug'])
    aprovador = encontrar_aprovador(cc_usuario)
    user_aprovador = pegarUser(aprovador)
    print(f"""
          Solicitante: {dados_solicitante['title']} ({dados_solicitante['slug']})
          Centro de custo: {cc_usuario}
          Aprovador: {aprovador} ({user_aprovador})
          """)
except Exception as e:
    print(f"\nErro ao coletar dados: {str(e)}")