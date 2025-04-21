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


def CreateGraph(dataframes, graphType='linha', save=False):
    """
    Cria gráficos a partir dos DataFrames lidos dos arquivos CSV
    """
    for name, df in dataframes.items():
        try:
            plt.figure(figsize=(10, 6))
            
            numeric_cols = df.select_dtypes(include=['number']).columns
            non_numeric_cols = df.select_dtypes(exclude=['number']).columns
            
            if len(numeric_cols) < 1:
                print(f"DataFrame '{name}' não possui colunas numéricas para plotar.")
                continue
                
            if len(non_numeric_cols) > 0:
                labels = df[non_numeric_cols[0]]
                x_values = range(len(labels))
            else:
                x_values = range(len(df))
                labels = None
            
            if graphType.lower() == 'linha':
                for col in numeric_cols:
                    plt.plot(x_values, df[col], label=col)
                plt.title(f"Gráfico de Linha - {name}")
                if labels is not None:
                    plt.xticks(x_values, labels, rotation=45, ha='right')
                
            elif graphType.lower() == 'barra':
                if labels is not None:
                    x_pos = range(len(labels))
                    for i, col in enumerate(numeric_cols):
                        plt.bar([x + i*0.2 for x in x_pos], df[col], width=0.2, label=col)
                    plt.xticks([x + 0.2*(len(numeric_cols)-1)/2 for x in x_pos], labels, rotation=45, ha='right')
                else:
                    df[numeric_cols].plot(kind='bar')
                plt.title(f"Gráfico de Barras - {name}")
                
            # elif graphType.lower() == 'histograma':
            #     for col in numeric_cols:
            #         plt.hist(df[col], alpha=0.5, label=col)
            #     plt.title(f"Histograma - {name}")
                
            # elif graphType.lower() == 'dispersao' and len(numeric_cols) >= 2:
            #     plt.scatter(df[numeric_cols[0]], df[numeric_cols[1]])
            #     plt.xlabel(numeric_cols[0])
            #     plt.ylabel(numeric_cols[1])
            #     plt.title(f"Gráfico de Dispersão - {name}")
                
            else:
                print(f"Tipo de gráfico '{graphType}' não suportado ou dados insuficientes.")
                continue
            
            plt.legend()
            plt.grid(True)
            
            if save:
                fileName = f"{name}_{graphType}.png"
                plt.savefig(fileName, dpi=300, bbox_inches='tight')
                print(f"Gráfico salvo como '{fileName}'")
            
            plt.show()
            
        except Exception as e:
            print(f"Erro ao criar gráfico para '{name}': {e}")



def main():
    
    # pasta_csv = input("Digite o caminho da pasta com os arquivos CSV: ").strip()
    path = "C:/UnityProjectsSSD/GitHub/Doom Retro Fork/doomretro_fork/msvc/x64/Debug/console".strip()
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
    # print("3 - Histograma")
    # print("4 - Gráfico de Dispersão")
    
    graphOption = input("Escolha o tipo de gráfico: ").strip()
    
    types = {
        '1': 'linha',
        '2': 'barra',
    }
    
    graphType = types.get(graphOption, 'linha')
    
    saveOption = input("Deseja salvar os gráficos? (s/n): ").strip().lower() == 's'
    
    CreateGraph(dataframes, graphType, saveOption)

if __name__ == "__main__":
    main()