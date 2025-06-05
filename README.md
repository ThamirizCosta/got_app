# Análise de Mortes em Game of Thrones 

Esta aplicação realiza análise de dados das mortes de personagens de Game of Thrones, utilizando o dataset `character-deaths.csv`.

## Arquivos Corrigidos

Os seguintes arquivos foram corrigidos para garantir a compatibilidade com o dataset e a correta integração entre os módulos:

- `DataLoader.py`: Carrega os dados do CSV (separado por ';'), adiciona uma coluna 'ID' e utiliza os nomes originais das colunas.
- `DataAnalise.py`: Realiza o pré-processamento, tratando valores nulos e codificando o gênero ('Gender') para uma coluna string ('Gender_Str'). Cria a coluna 'Morreu' com base em 'Death_Year'.
- `ContadorMorte.py`: Calcula estatísticas sobre as mortes utilizando as colunas corretas ('Morreu', 'Death_Year').
- `api.py`: Implementa a API Flask com endpoints para estatísticas de mortes, contagem de gênero e busca de registros por ID, utilizando as classes corrigidas.
- `app.py`: Interface Streamlit que carrega e processa os dados, exibe a tabela de personagens e estatísticas básicas, utilizando as classes corrigidas.

## Requisitos

Para executar a aplicação, você precisa ter instalado:

- Python 3.6+
- Flask
- Streamlit
- Pandas
- NumPy

Você pode instalar todas as dependências com o comando:

```bash
pip install flask streamlit pandas numpy
```

## Como Executar

1.  **Extraia** o arquivo zip em um diretório local.
2.  **Navegue** até o diretório criado.
3.  **Execute a API Flask** (em um terminal):
    ```bash
    python api.py
    ```
    A API estará rodando em `http://localhost:5000`.
4.  **Execute a Interface Streamlit** (em outro terminal):
    ```bash
    streamlit run app.py
    ```
    A interface estará acessível em `http://localhost:8501` (ou outra porta indicada pelo Streamlit).

## Funcionalidades

- **Interface Streamlit (`app.py`)**: 
    - Carrega e exibe os dados processados dos personagens.
    - Permite selecionar colunas para visualização.
    - Mostra estatísticas rápidas (total de personagens, contagem por gênero, total de mortes).
- **API Flask (`api.py`)**:
    - `GET /api/statistics`: Retorna estatísticas detalhadas sobre as mortes.
    - `GET /api/gender_count`: Retorna a contagem de personagens por gênero.
    - `GET /api/record/<id>`: Retorna os dados de um personagem específico pelo seu ID (índice).

## Observações

- O dataset `character-deaths.csv` deve estar no mesmo diretório dos scripts Python.
- A aplicação Streamlit (`app.py`) não consome a API Flask diretamente neste exemplo corrigido, mas calcula as estatísticas usando as classes importadas. Para uma integração completa onde o Streamlit consome a API, o `app.py` precisaria ser modificado para fazer requisições HTTP (usando `requests`, por exemplo) aos endpoints da API Flask.
