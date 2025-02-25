import pandas as pd
import os

def limpar_csv():
    try:
        # Ler o arquivo CSV com separador ponto e vírgula
        df = pd.read_csv('centros_de_custos.csv', sep=';', encoding='latin1')
        
        # Remover linhas onde todas as colunas são vazias ou apenas contém ponto e vírgula
        df = df.dropna(how='all')
        
        # Remover espaços em branco extras de todas as colunas
        for column in df.columns:
            if df[column].dtype == 'object':  # Apenas para colunas de texto
                df[column] = df[column].str.strip()
        
        # Converter CENTRO_DE_CUSTO para inteiro (removendo o .0)
        df['CENTRO_DE_CUSTO'] = df['CENTRO_DE_CUSTO'].astype(int).astype(str)
        
        # Remover linhas onde CENTRO_DE_CUSTO está vazio
        df = df[df['CENTRO_DE_CUSTO'].notna()]
        
        # Resetar os índices
        df = df.reset_index(drop=True)
        
        # Criar backup do arquivo original
        if os.path.exists('centros_de_custos.csv'):
            os.rename('centros_de_custos.csv', 'centros_de_custos_backup.csv')
        
        # Salvar o arquivo limpo mantendo o separador ponto e vírgula
        df.to_csv('centros_de_custos.csv', index=False, sep=';', encoding='latin1')
        
        print("Arquivo CSV limpo com sucesso!")
        print(f"Total de linhas após limpeza: {len(df)}")
        
        # Mostrar as primeiras e últimas linhas para verificação
        print("\nPrimeiras linhas do arquivo:")
        print(df.head())
        print("\nÚltimas linhas do arquivo:")
        print(df.tail())
        
    except Exception as e:
        print(f"Erro ao limpar o arquivo: {str(e)}")

if __name__ == "__main__":
    limpar_csv()
