# -*- coding: utf-8 -*-
"""PROVA_02_IA_ELAINE_SOUZA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dstGE5i96VaXmCtUc9xBhBiiHt21rGWk
"""

#Importando as bibliotecas
import time
import warnings
import numpy as np # linear algebra
import pandas as pd # data processing
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from imblearn.under_sampling import NearMiss
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

warnings.filterwarnings("ignore")

# configurar o estilo dos gráficos com o Seaborn
sns.set_style('dark')

#importando o Dataset
df = pd.read_csv('hcvdat0.csv', encoding = "ISO-8859-1") #abrindo o arquivo

#Printando o Dataset
print('Quantidade de instâncias: {}\nQuantidade de atributos: {}\n'.format(len(df), len(df.columns)))
df[0:7]
df

# Verificando dados iniciais do dataset importado
df.head()

# Entendendo o dataset, colunas, data types, quantidade de registros por coluna
df.info()

"""**Pré-Processamento**"""

# Verificando detalhes estatísticos do dataset
df.describe()

df.mean() #cálculo da mediana

x = df['Age'].value_counts() #cálculo das quantidades dos tipos do atributo label
x/len(df)  #cáculo das quantidades em relação ao conjunto completo (entre 0 e 1)

df['Age'].mode() #cálculo da moda

df['Age'].median()

df['Age'].mean() #cálculo da mediana

np.random.seed(1234) #gráfico de boxplot de outliers
dataf = pd.DataFrame(np.random.randn(10000, 13),
                  columns=['Category', 'Age', 'Sex', 'ALB', 'ALP', 'ALT', 'AST', 'BIL', 'CHE', 'CHOL', 'CREA', 'GGT', 'PROT'])
boxplot = dataf.boxplot(column=['Category', 'Age', 'Sex', 'ALB', 'ALP', 'ALT', 'AST', 'BIL', 'CHE', 'CHOL', 'CREA', 'GGT', 'PROT'], grid=False, rot=45, fontsize=15, figsize = (15,7))

df['Age'].var() #cálculo da variância

df['Age'].std() #cálculo do desvio padrão

corr = df.corr()
corr.style.background_gradient(cmap='coolwarm') #mapa de correlação

df.loc[df['Category'] == "3=Cirrhosis"].sample(n=4, random_state =2) #gerando uma amostra aleatória com 4 elementos

print('Valores faltantes:', df.isnull().sum()) #quantidade de valores faltantes para todos os atributos

print('Valores duplicados:', df.duplicated()) #quantidade de valores duplicados para todos os atributos

median = df['ALB'].median()
df['ALB'].fillna(median, inplace = True) #subtitui os elementos faltosos pela mediana
df

median = df['ALT'].median()
df['ALT'].fillna(median, inplace = True) #subtitui os elementos faltosos pela mediana
df

median = df['PROT'].median()
df['PROT'].fillna(median, inplace = True) #subtitui os elementos faltosos pela mediana
df

df = df.dropna(how ='any') #elimina todas as linhas com dados ausentes
df

print('Valores faltantes:', df.isnull().sum()) #quantidade de valores faltantes para todos os atributos

df.head()

df.drop(columns=['Unnamed: 0']) #excluir a coluna Unnamed: 0

"""**Verificação de registros úncios no dataset**"""

def distribuicao (data):
    '''
    Esta função exibirá a quantidade de registros únicos para cada coluna
    existente no dataset
    
    dataframe -> Histogram
    '''
    # Calculando valores unicos para cada label: num_unique_labels
    num_unique_labels = data.apply(pd.Series.nunique)

    # plotando valores
    num_unique_labels.plot( kind='bar')
    
    # Nomeando os eixos
    plt.xlabel('Campos')
    plt.ylabel('Número de Registros únicos')
    plt.title('Distribuição de dados únicos do DataSet')
    
    # Exibindo gráfico
    plt.show()

distribuicao(df)

"""**Visualizando a distribuição das classes**"""

#Mostra a quantidade de registros de cada uma das classes.
#Mostra de forma gráfica
e = pd.value_counts(df['Category']) [0]
p = pd.value_counts(df['Category']) [1]
a = pd.value_counts(df['Category']) [2]
b = pd.value_counts(df['Category']) [3]
c = pd.value_counts(df['Category']) [4]

tam = len(df)

print('0: ',e)
print('1: ',p )
print('2: ',a )
print('3: ',b )
print('4: ',c )

pie = pd.DataFrame([['0',e],['1',p], ['2',a], ['3',b], ['4',c]],columns=['Tipo' , 'Quantidade'])


def pie_chart(data,col1,col2,title): 
    labels = {'0':0,'1':1, '2':2, '3':3, '4':4}
    sizes = data[col2]
    colors = ['#B0E0E6', '#D8BFD8', '#FFE4C4', '#F5F5DC', '#FF7F50']

    plt.pie(sizes, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140, labeldistance =1.2)
    plt.title( title )
    
    plt.axis('equal')
    plt.show()

pie_chart(pie,'Tipo' , 'Quantidade','Distribuição Percentual dos Rótulos de Classificação')


plt.bar(pie.Tipo,pie.Quantidade, color = ['#000080', '#D2691E', '#008000', '#B22222', '#8B008B'])
plt.title("Distribuição dos Rótulos de Classificação")
plt.xlabel("Tipo de Classificação")
plt.ylabel('Quantidade de Registros')
plt.show()

# ver o balanceamento das classes
print("\nCategorias representam {:.4f}% do dataset.\n".format((df[df.Category == 1].shape[0] / df.shape[0]) * 100))

le = preprocessing.LabelEncoder() #transforma atributos qualitativos em quantitativos
for column in df.columns:
    if df[column].dtypes == 'object':
        df[column] = le.fit_transform(df[column])
        
print(df)

#Tratamento de outlier
dfTrat = RobustScaler().fit_transform(df.copy())  #normalização dos dados e para isso remove a mediana e dimensiona os dados de acordo com o intervalo quantil

print(dfTrat)

pd.DataFrame(dfTrat)

"""**Regressão logística com dados desbalanceados e sem tratamento de outliers**"""

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1, stratify=y) #Separando os dados em 70% para treino e 30% para teste

lr = LogisticRegression() #Instância o classificador

lr.fit(X_train, y_train) #Treinando o algoritmo

y_pred = lr.predict(X_test) #Coloca as classificações na variável y_pred

accuracy_score(y_test, y_pred) #Checa a acurácia do modelo

print (classification_report(y_test, y_pred)) #Recall

print (pd.crosstab(y_test, y_pred, rownames=['Real'], colnames=['Predito'], margins=True)) #Matriz de confusão

"""**Regressão logística com dados desbalanceados e com tratamento de outliers**"""

#X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1, stratify=y) #Separando os dados em 70% para treino e 30% para teste

#lr = LogisticRegression() #Instância o classificador

#lr.fit(X_train, y_train) #Treinando o algoritmo

#y_pred = lr.predict(X_test) #Coloca as classificações na variável y_pred

#accuracy_score(y_test, y_pred) #Checa a acurácia do modelo

#print (classification_report(y_test, y_pred)) #Recall

#print (pd.crosstab(y_test, y_pred, rownames=['Real'], colnames=['Predito'], margins=True)) #Matriz de confusão

"""https://sigmoidal.ai/como-lidar-com-dados-desbalanceados/
https://minerandodados.com.br/lidando-com-classes-desbalanceadas-machine-learning/

**Balanceamento de Dados**
"""

nr = NearMiss()#Instância o NearMiss

X, y = nr.fit_sample(X, y)#Aplicando o NearMiss

ax = sns.countplot(x=y)#Checa a quantidade de amostras entre as classes

np.bincount(y) #Visualiza a quantidade de dados por classe

"""**Regressão logistíca para dados balanceados**"""

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1, stratify=y) #Separando os dados em 70% para treino e 30% para teste

lr = LogisticRegression() #Instância o classificador

lr.fit(X_train, y_train) #Treinando o algoritmo

y_pred = lr.predict(X_test) #Coloca as classificações na variável y_pred

accuracy_score(y_test, y_pred) #Checa a acurácia do modelo

print (classification_report(y_test, y_pred)) #Recall

print (pd.crosstab(y_test, y_pred, rownames=['Real'], colnames=['Predito'], margins=True)) #Matriz de confusão