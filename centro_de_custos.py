import pandas as pd

url = r"C:\Users\fo0192\Downloads\Centro de custos_Maio2024.xlsx"

def encontrar_aprovador(centro_de_custo):
    df = pd.read_excel(url, sheet_name="CENTROS DE CUSTOS")
    
    try:
        centro_de_custo = str(centro_de_custo)
        df.iloc[:, 2] = df.iloc[:, 2].astype(str)
        
        matches = df.iloc[:, 2] == centro_de_custo
        
        if matches.sum() > 0:
            aprovador = df.loc[matches, df.columns[3]].iloc[0]
            return aprovador
        return None
    except Exception as e:
        return None
