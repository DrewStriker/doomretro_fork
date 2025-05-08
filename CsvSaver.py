import os
import re

# Caminho da pasta onde estão os arquivos .txt
caminho_da_pasta = os.path.dirname(os.path.abspath(__file__)) + "/msvc/x64/Debug/console"

padrao_percentual = re.compile(r'\(\d+%?\)')
padrao_x_of_y = re.compile(r'(\d+)\s+of\s+(\d+)')

arquivos_txt = [f for f in os.listdir(caminho_da_pasta) if f.endswith(".txt")]

if arquivos_txt:
    for arquivo_txt in arquivos_txt:
        caminho_completo = os.path.join(caminho_da_pasta, arquivo_txt)

        with open(caminho_completo, 'r', encoding='latin1') as arquivo:
            linhas = arquivo.readlines()

        nome_base = os.path.splitext(arquivo_txt)[0]

        if 's ' in nome_base:
            fase_status = nome_base.split('s ', 1)[1]
        else:
            fase_status = nome_base

        coluna_1 = []
        coluna_2 = []

        linha_contador = 0  # para rastrear a posição da linha válida

        for linha in linhas:
            partes = linha.strip().split('  ')
            partes = [p for p in partes if p.strip()]
            if len(partes) >= 2:
                header = partes[0].strip()

                # Ignorar as linhas especificadas
                if header in ["Maps finished", "Games saved", "Games loaded"]:
                    continue

                valor = partes[1].strip()

                # Remove o símbolo % apenas da segunda linha válida
                if linha_contador == 1:
                    valor = valor.replace('%', '').strip()

                # Remove a palavra "feet" da linha "Distance traveled"
                if header == "Distance traveled":
                    valor = valor.replace("feet", "").strip()

                coluna_1.append(header)
                coluna_2.append(valor)
                linha_contador += 1

        if coluna_1 and coluna_2:
            coluna_1 = coluna_1[1:]
            coluna_2 = coluna_2[1:]

        nova_linha_header = ["MAP"]
        nova_linha_valor = [fase_status]

        for i in range(len(coluna_2)):
            header = coluna_1[i]
            valor = coluna_2[i]

            match = padrao_x_of_y.search(valor)

            if match:
                x_valor = match.group(1)
                y_valor = match.group(2)

                header_executado = header + " Executado"
                nova_linha_header.append(header_executado)
                nova_linha_valor.append(x_valor)

                header_total = header + " Total"
                nova_linha_header.append(header_total)
                nova_linha_valor.append(y_valor)
            else:
                valor_sem_percentual = padrao_percentual.sub('', valor).strip()
                nova_linha_header.append(header)
                nova_linha_valor.append(valor_sem_percentual)

        nome_arquivo_saida = os.path.splitext(arquivo_txt)[0] + ".csv"
        caminho_saida = os.path.join(caminho_da_pasta, nome_arquivo_saida)

        with open(caminho_saida, 'w', encoding='utf-8') as saida:
            saida.write(', '.join(nova_linha_header) + '\n')
            saida.write(', '.join(nova_linha_valor) + '\n')

        print(f"Processado: {arquivo_txt} → {nome_arquivo_saida}")

else:
    print("Nenhum arquivo .txt encontrado na pasta.")
