import pandas as pd
import matplotlib.pyplot as plt
import os

def readCsvFile(path):
    """
    Lê todos os arquivos CSV de uma pasta, tentando diferentes codificações,
    e retorna um dicionário com os DataFrames
    """
    dataframes = {}
    code = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252'] 
    
    for file in os.listdir(path):
        if file.endswith('.csv'):
            fullPath = os.path.join(path, file)
            readSucessfull = False
            
            for encoding in code:
                try:
                    df = pd.read_csv(fullPath, encoding=encoding)
                    fileName = os.path.splitext(file)[0]
                    dataframes[fileName] = df
                    print(f"Arquivo '{file}' lido com sucesso usando codificação {encoding}!")
                    readSucessfull = True
                    break
                except Exception as e:
                    continue
            
            if not readSucessfull:
                print(f"Falha ao ler o arquivo '{file}' com todas as codificações tentadas")

    return dataframes

def criar_graficos(dataframes, graphType='linha', salvar=False):
    """
    Cria gráficos a partir dos DataFrames lidos dos arquivos CSV
    """
    for name, df in dataframes.items():
        try:
            plt.figure(figsize=(10, 6))
            
            collNum = df.select_dtypes(include=['number']).columns
            
            if len(collNum) < 1:
                print(f"DataFrame '{name}' não possui colunas numéricas para plotar.")
                continue
            
            if graphType.lower() == 'linha':
                for coll in collNum:
                    plt.plot(df[coll], label=coll)
                plt.title(f"Gráfico de Linha - {name}")
                
            elif graphType.lower() == 'barra':
                df[collNum].plot(kind='bar')
                plt.title(f"Gráfico de Barras - {name}")
                
            elif graphType.lower() == 'histograma':
                for coll in collNum:
                    plt.hist(df[coll], alpha=0.5, label=coll)
                plt.title(f"Histograma - {name}")
                
            elif graphType.lower() == 'dispersao' and len(collNum) >= 2:
                plt.scatter(df[collNum[0]], df[collNum[1]])
                plt.xlabel(collNum[0])
                plt.ylabel(collNum[1])
                plt.title(f"Gráfico de Dispersão - {name}")
                
            else:
                print(f"Tipo de gráfico '{graphType}' não suportado ou dados insuficientes.")
                continue
            
            plt.legend()
            plt.grid(True)
            
            if salvar:
                fileName = f"{name}_{graphType}.png"
                plt.savefig(fileName, dpi=300, bbox_inches='tight')
                print(f"Gráfico salvo como '{fileName}'")
            
            plt.show()
            
        except Exception as e:
            print(f"Erro ao criar gráfico para '{name}': {e}")

def main():
    
    # pasta_csv = input("Digite o caminho da pasta com os arquivos CSV: ").strip()
    path = "C:\Projects\doomretro_fork\msvc\Release\console".strip()
    if not os.path.isdir(path):
        print("Pasta não encontrada!")
        return
    
    dataframes = readCsvFile(path)
    if not dataframes:
        print("Nenhum arquivo CSV válido encontrado.")
        return
    
    print("\nOpções de gráfico disponíveis:")
    print("1 - Gráfico de Linha")
    print("2 - Gráfico de Barras")
    print("3 - Histograma")
    print("4 - Gráfico de Dispersão")
    
    graphOption = input("Escolha o tipo de gráfico (1-4): ").strip()
    
    types = {
        '1': 'linha',
        '2': 'barra',
        '3': 'histograma',
        '4': 'dispersao'
    }
    
    graphType = types.get(graphOption, 'linha')
    
    saveOption = input("Deseja salvar os gráficos? (s/n): ").strip().lower() == 's'
    
    # Cria os gráficos
    criar_graficos(dataframes, graphType, saveOption)

if __name__ == "__main__":
    main()