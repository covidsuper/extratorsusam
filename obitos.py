import tabula
import pandas as pd
from pandas import Series, DataFrame
import numpy as np

#--------------------------------------------------------------------------------------------------#
#inserindo a data da planilha
def insere_data(df,data):
    df['Data'] = data
    df['Data'] = pd.to_datetime(df['Data'])
    
    return df

#--------------------------------------------------------------------------------------------------#

def criaDataframe(obitos,data):
    colunas = obitos.shape[1]
    if(colunas == 10):
        #deletando colunas nulas
        obitos = obitos.dropna(axis=1, how='all')

        #renomeando as colunas
        obitos.columns = ['Notificados', 'Acumulado','Acumulado%','Ultimas24h','ConfirmacaoDiagnostica','Total',
                        'Descartados','EmInvestigacao']

        #a partir do dia 08 a tabela passa a ter mais colunas
        #sera adicionada uma coluna 'Aguardando Resultado' para os boletins antes do dia 08 
        obitos['AguardandoResultado'] = pd.Series(['-','-','-'])
        
        #deletando as duas primeiras linhas que nao contem dados
        obitos=obitos.drop(0)
        obitos=obitos.drop(1)
        
        #colocando coluna 'Aguardando Resultado no lugar correto'
        obitos=obitos[['Notificados', 'Acumulado','Acumulado%','Ultimas24h','ConfirmacaoDiagnostica','Total',
                        'Descartados','AguardandoResultado','EmInvestigacao']]
        
        #removendo a coluna total
        obitos=obitos.drop(columns=['Total'])

        #convertendo valores
        obitos = tipagemDados(obitos,data)

        #inserindo a data
        obitos = insere_data(obitos,data)
    
    else:
        #deletando as tres primeiras linhas que nao contem dados
        obitos=obitos.drop(0)
        obitos=obitos.drop(1)
        obitos=obitos.drop(2)
        
        #deletando colunas nulas
        obitos = obitos.dropna(axis=1, how='all')
        
        #renomeando as colunas
        obitos.columns = ['Notificados', 'Acumulado','Acumulado%','Ultimas24h','ConfirmacaoDiagnostica','Total',
                            'Descartados','AguardandoResultado','EmInvestigacao','Total2']

        #drop das colunas de total
        obitos=obitos.drop(columns=['Total'])
        obitos=obitos.drop(columns=['Total2'])

        #inserindo a data
        obitos = insere_data(obitos,data)
        
        #convertendo valores
        obitos = tipagemDados(obitos,data)

    return obitos
#--------------------------------------------------------------------------------------------------#
def tipagemDados(obitos,data):
    dia=data[0]+data[1]
    dia=int(dia)

    #convertendo valores em inteiros
    obitos['Notificados'] = obitos['Notificados'].values.astype(np.float32)*1000
    obitos['Notificados'] = obitos['Notificados'].values.astype(np.int64)
    
    obitos['Acumulado'] = obitos['Acumulado'].values.astype(np.float32)*1000
    obitos['Acumulado'] = obitos['Acumulado'].values.astype(np.int64)
    
    obitos['Ultimas24h'] = obitos['Ultimas24h'].values.astype(np.int64)
    
    obitos['ConfirmacaoDiagnostica'] = obitos['ConfirmacaoDiagnostica'].values.astype(np.int64)
    
    obitos['Descartados'] = obitos['Descartados'].values.astype(np.int64)
        
    obitos['EmInvestigacao'] = obitos['EmInvestigacao'].values.astype(np.int64)

    if(dia>=8):
        obitos['AguardandoResultado'] = obitos['AguardandoResultado'].values.astype(np.int64)

    return obitos
#--------------------------------------------------------------------------------------------------#
#cria o arquivo csv
def geraCSV(destino,operacao,dfObitos,csv_completo):
    if(operacao == 'n'):
        nome = str(destino+'OBITOS.csv')
        dfObitos.to_csv(nome)
        print('Finalizada a criação do csv!')
    else:
        #recupera o df completo a ser concatenado
        dfCompleto = pd.read_csv(csv_completo)
        dfFinal = pd.concat([dfObitos,dfCompleto], ignore_index = True)
        dfFinal = dfFinal.drop('Unnamed: 0', axis = 1)
        nome = str(csv_completo)
        dfFinal.to_csv(nome)
        print('Finalizada a concatenação do csv!')
        
#--------------------------------------------------------------------------------------------------#

continua = 'y'

while (continua == 'y'):
    operacao = input('(c) Concatenar | (n) Criar novo csv: ')

    operacao = operacao.lower()

    if(operacao == 'n'):
        origem = input('Digite o caminho para o PDF: ')

        data = input('Digite a data do arquivo (MM-DD-YYYY): ')

        destino = input('Digite o caminho para ser salvo: ')

        #gera o df
        dfObitos = tabula.read_pdf(origem, pages ='1',multiple_tables=True,lattice=True)
        dfObitos = criaDataframe(dfObitos[4],data)

        #gera o csv
        geraCSV(destino,operacao,dfObitos,0)
        
    else:
        origem = input('Digite o caminho para o PDF: ')

        data = input('Digite a data do arquivo (MM-DD-YYYY): ')

        csv_completo = input('Digite o caminho para o CSV a ser concatenado: ')

        #cria o novo df
        dfObitos = tabula.read_pdf(origem, pages=1,multiple_tables=True,lattice=True)
        dfObitos = criaDataframe(dfObitos[4],data)
        
        #salva o CSV
        geraCSV(0,operacao,dfObitos,csv_completo)
    
    continua = input('Realizar outra operação? (Y/n)')
    continua = continua.lower()
