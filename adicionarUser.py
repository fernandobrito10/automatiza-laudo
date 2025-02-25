import pandas as pd
from user_ad import pegarUser
import os

def recheckar_usuarios():
    try:
        # Ler o arquivo CSV
        df = pd.read_csv('centros_de_custos.csv', sep=';', encoding='latin1')
        
        # Identificar linhas com "Usuário não encontrado"
        nao_encontrados = df[df['USERNAME'] == 'Usuário não encontrado']
        total_recheckar = len(nao_encontrados)
        
        print(f"Iniciando nova busca para {total_recheckar} usuários não encontrados...")
        atualizados = 0
        
        # Recheckar apenas usuários não encontrados
        for index, row in nao_encontrados.iterrows():
            try:
                print(f"Verificando {row['APROVADOR']}...", end='\r')
                
                # Buscar username no novo servidor AD
                novo_username = pegarUser(row['APROVADOR'])
                
                # Atualizar apenas se encontrou um usuário válido
                if novo_username != "Usu�rio n�o encontrado":
                    df.at[index, 'USERNAME'] = novo_username
                    atualizados += 1
                    print(f"\nEncontrado: {row['APROVADOR']} -> {novo_username}")
                
            except Exception as e:
                print(f"\nErro ao buscar {row['APROVADOR']}: {str(e)}")
        
        # Criar backup do arquivo atual
        if os.path.exists('centros_de_custos.csv'):
            os.rename('centros_de_custos.csv', 'centros_de_custos_backup.csv')
        
        # Salvar arquivo atualizado
        df.to_csv('centros_de_custos.csv', sep=';', index=False, encoding='latin1')
        
        print("\nProcesso concluído!")
        print(f"Total de usuários atualizados: {atualizados} de {total_recheckar}")
        
        # Mostrar usuários que ainda não foram encontrados
        ainda_nao_encontrados = df[df['USERNAME'] == 'Usuário não encontrado']
        if len(ainda_nao_encontrados) > 0:
            print("\nUsuários que ainda não foram encontrados:")
            for aprovador in ainda_nao_encontrados['APROVADOR'].unique():
                print(f"- {aprovador}")
            
    except Exception as e:
        print(f"Erro ao processar arquivo: {str(e)}")

if __name__ == "__main__":
    recheckar_usuarios()
