from requisicao import requisicaoIDs, requisicaoCentrodeCusto, encontrarResponsavel, encontrarAprovador
from centro_de_custos import encontrar_aprovador
from user_ad import pegarUser
from interface import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

class AtendimentoApp(MainWindow):
    def __init__(self):
        super().__init__()
        self.search_button.clicked.connect(self.process_request)
        
    def process_request(self):
        atd_id = self.input_field.text()
        if not atd_id:
            self.result_display.setText("Por favor, digite um número de atendimento.")
            return
            
        try:
            id_responsavel, dados_solicitante = requisicaoIDs(atd_id)
            cc_usuario = requisicaoCentrodeCusto(dados_solicitante['slug'])
            aprovador = encontrar_aprovador(cc_usuario)
            user_aprovador = pegarUser(aprovador)
            nome_responsavel, user_responsavel = encontrarResponsavel(id_responsavel)
            
            result = f"""
            Solicitante: {dados_solicitante['title']} ({dados_solicitante['slug']})
            Centro de custo: {cc_usuario}
            Aprovador: {aprovador} ({user_aprovador})
            Chamado: ATD-{atd_id} de 13/01/2024
            Avaliação técnica da T.I: {nome_responsavel} ({user_responsavel})
            """
            
            self.result_display.setText(result)
            
        except Exception as e:
            self.result_display.setText(f"Erro ao coletar dados: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = AtendimentoApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()