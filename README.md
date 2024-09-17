Para a realização desse projeto, foi utilizado o documento "Visitação ao Centro Cultural Banco do Brasil , 2015 - 2021 no Município do Rio de Janeiro", disponível [aqui]([url](https://www.data.rio/documents/614ad116a32746fc8d85e93f70df568d/about)), que contém o registro quantitativo mensal de visitantes ao CCBB/RJ no período descrito.

Os dados originais estão em formato .xls (data/ccbb.xls). 
Assim, inicialmente, foi feita a conversão dos dados para o formato .csv (data/ccbb.csv) e sua transformação em um dataframe pandas (arquivo src/data_cleaning.py).
O ano de 2021 possui a quantidade de visitantes apenas para os meses de janeiro, fevereiro e março, mas como são poucos dados e é fácil visualizar a ausência dessas informações, não realizamos o tratamento dos dados ausentes.

O arquivo src/main.py contém o código da aplicação Streamlit.
