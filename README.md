# VIV Calculator on FastAPI 

Esta é uma API desenvolvida com FastAPI para realizar cálculos definidos em outros arquivos `.py`.

## Requisitos

- Python 3.11+
- FastAPI
- Uvicorn

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/VictorPuca/viv-fastapi
    cd viv-fastapi
    ```

2. Crie um ambiente virtual:
    ```bash
    python -m venv .venv
    .venv/Scripts/activate 
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
## Estrutura do Projeto

- `api_pipes.py`: Diretório com os arquivos relacionados à API.
- `calc_pipes.py`: Diretório com os arquivos relacionados aos cálculos.
- `Pipe.py`: Arquivo contendo a definição da classe `Pipe`.
- `db.json` e `db2.json`: Arquivos de catálogo e propriedades geométricas e mecânicas (estão especificadas em Pipe.py) inerentes ao cálculo de dutos em formato JSON.
- `soil_stiffness.py`: Arquivo contendo cálculos relacionados à rigidez do solo de acordo com o tipo de solo escolhido.
- `Soil.py`: Arquivo contendo a definição da classe `Soil`.

## Rodando a API

Para iniciar o servidor da API, use o comando:

```bash
uvicorn api_pipes.main:app --reload