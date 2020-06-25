import tabula
import pandas as pd

#inserindo a data da planilha
def insere_data(df,data):
    df['Data'] = data
    df['Data'] = pd.to_datetime(df['Data'])
    
    return df

#------------------------------------------------------------------------------------------------#

#troca linha i pela linha j
def organizaLinha(i,j,dfLeitos):
    dfLeitos.loc[-1] = dfLeitos.loc[i]  # add row temp
    dfLeitos.loc[i] = dfLeitos.loc[j] # sobe a row 5
    dfLeitos.loc[j] = dfLeitos.loc[-1] # subst a row pela temp
    dfLeitos = dfLeitos.drop(-1) #del row temp
    
    #ordenando ocupados e nao ocupados
    dfLeitos.loc[-1] = dfLeitos.loc[i+1]  # add row temp
    dfLeitos.loc[i+1] = dfLeitos.loc[j-2] # sobe a row 5
    dfLeitos.loc[j-2] = dfLeitos.loc[-1] # subst a row pela temp
    dfLeitos = dfLeitos.drop(-1) #del row temp
    return dfLeitos

#------------------------------------------------------------------------------------------------#

#Organizar dataframe de OC_LEITOS
def organizaOC_LEITOS(dfLeitos):
    #removendo taxa de ocupação
    #resolvi remover a taxa de ocupação pois pode ser um valor calculável com os dados que existem no dataframe
    count=16
    while count <=22:
        dfLeitos = dfLeitos.drop(count)
        count+=1
    
    #deletando a row 0 que deveria ser as colunas
    dfLeitos = dfLeitos.drop(0)
    
    #renomeando as columns
    dfLeitos.columns = ['INDICADOR','TOTAL', 'HOSPITAIS','FUNDACOES', 'MATERNIDADES','SPA','UPA','REDE_MUNICIPAL','REDE_PRIVADA','FORCAS_ARMADAS']
    
    #reordenando as colunas para melhor visualizacao
    dfLeitos = dfLeitos[['INDICADOR','HOSPITAIS','FUNDACOES','MATERNIDADES','SPA','UPA','REDE_MUNICIPAL','REDE_PRIVADA','FORCAS_ARMADAS','TOTAL']]
    
    #organizando as linhas de total
    dfLeitos = organizaLinha(1,5,dfLeitos)
    dfLeitos = organizaLinha(6,10,dfLeitos)
    dfLeitos = organizaLinha(11,15,dfLeitos)

    #eliminando as colunas e linhas com os totais
    dfLeitos = dfLeitos.drop(columns=['TOTAL'])
    dfLeitos = dfLeitos.drop(5) #tot sala vermelha
    dfLeitos = dfLeitos.drop(10) #tot leitos clin
    dfLeitos = dfLeitos.drop(15) #tot leitos uti

    dfLeitos = insere_data(dfLeitos,data)
       
    return dfLeitos

#------------------------------------------------------------------------------------------------#
#cria o arquivo csv
def geraCSV(destino,operacao,dfLeitos,csv_completo):
    if(operacao == 'n'):
        nome = str(destino+'OC_LEITOS.csv')
        dfLeitos.to_csv(nome)
        print('Finalizada a criação do csv!')
    else:
        #recupera o df completo a ser concatenado
        dfCompleto = pd.read_csv(csv_completo)
        dfFinal = pd.concat([dfLeitos,dfCompleto], ignore_index = True)
        dfFinal = dfFinal.drop('Unnamed: 0', axis = 1)
        nome = str(csv_completo)
        dfFinal.to_csv(nome)
        print('Finalizada a concatenação do csv!')
        
#------------------------------------------------------------------------------------------------#
continua='y'

while (continua == 'y'):
    operacao = input('(c) Concatenar | (n) Criar novo csv: ')

    operacao = operacao.lower()

    if(operacao == 'n'):
        origem = input('Digite o caminho para o PDF: ')

        data = input('Digite a data do arquivo (MM-DD-YYYY): ')

        destino = input('Digite o caminho para ser salvo: ')

        #gera o df
        dfLeitos = tabula.read_pdf(origem, pages=1, lattice=True)
        dfLeitos = organizaOC_LEITOS(dfLeitos[0])

        #gera o csv
        geraCSV(destino,operacao,dfLeitos,0)
        
    else:
        origem = input('Digite o caminho para o PDF: ')

        data = input('Digite a data do arquivo (MM-DD-YYYY): ')

        csv_completo = input('Digite o caminho para o CSV a ser concatenado: ')

        #cria o novo df
        dfLeitos = tabula.read_pdf(origem, pages=1, lattice=True)
        dfLeitos = organizaOC_LEITOS(dfLeitos[0])
        
        #salva o CSV
        geraCSV(0,operacao,dfLeitos,csv_completo)
    
    continua = int(input('Realizar outra operação? (Y/n)'))
    continua = continua.lower()
