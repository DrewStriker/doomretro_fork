import os
import re

# Caminho da pasta onde estão os arquivos .txt
caminho_da_pasta = "C:/UnityProjectsSSD/GitHub/Doom Retro Fork/doomretro_fork/msvc/x64/Debug/console"

# Expressão para detectar "x of 0 (z%)"
padrao = re.compile(r"(\d+)\s+of\s+0\s+\(\d+%?\)")

# Processa todos os arquivos .txt na pasta
arquivos_txt = [f for f in os.listdir(caminho_da_pasta) if f.endswith(".txt")]

if arquivos_txt:
    for arquivo_txt in arquivos_txt:
        caminho_completo = os.path.join(caminho_da_pasta, arquivo_txt)

        with open(caminho_completo, 'r', encoding='latin1') as arquivo:
            linhas = arquivo.readlines()

        # Extrai nome da fase com status do nome do arquivo
        nome_base = os.path.splitext(arquivo_txt)[0]  # remove extensão .txt

        if 's ' in nome_base:
            fase_status = nome_base.split('s ', 1)[1]
        else:
            fase_status = nome_base  # fallback

        # Coleta os itens das colunas
        coluna_1 = []
        coluna_2 = []

        for linha in linhas:
            partes = linha.strip().split('  ')
            partes = [p for p in partes if p.strip()]
            if len(partes) >= 2:
                coluna_1.append(partes[0])
                coluna_2.append(partes[1])

        # Remove cabeçalho (se houver)
        if coluna_1 and coluna_2:
            coluna_1 = coluna_1[1:]
            coluna_2 = coluna_2[1:]

        # Remove linhas onde a coluna 2 contém "x of 0 (z%)"
        nova_coluna_1 = []
        nova_coluna_2 = []

        for i in range(len(coluna_2)):
            resultado = padrao.search(coluna_2[i])
            if not resultado:
                nova_coluna_1.append(coluna_1[i])
                nova_coluna_2.append(coluna_2[i])

        coluna_1 = nova_coluna_1
        coluna_2 = nova_coluna_2

        # Adiciona títulos
        coluna_1.insert(0, "MAP")
        coluna_2.insert(0, fase_status)

        # Formata os resultados
        resultado_coluna_1 = '; '.join(coluna_1)
        resultado_coluna_2 = '; '.join(coluna_2)

        # Gera nome do arquivo de saída com base no nome do arquivo de entrada
        nome_arquivo_saida = os.path.splitext(arquivo_txt)[0] + ".csv"
        caminho_saida = os.path.join(caminho_da_pasta, nome_arquivo_saida)

        # Salva no arquivo
        with open(caminho_saida, 'w', encoding='utf-8') as saida:
            saida.write(resultado_coluna_1 + '\n')
            saida.write(resultado_coluna_2 + '\n')

        print(f"Processado: {arquivo_txt} → {nome_arquivo_saida}")

else:
    print("Nenhum arquivo .txt encontrado na pasta.")