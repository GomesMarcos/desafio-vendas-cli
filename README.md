# desafio-vendas-cli

O objetivo deste projeto é ler um arquivo CSV cujo cabeçalho é "produto,quantidade,preco_unitario"

## Desenvolvimento / Execução Local
Passo a passo para configuração de execução em ambiente local

### Crie uma Venv
`$ python -m venv venv`

### Ative a Venv
`$ source venv/bin/activate`

### Instalando as dependências
- Atualize o pip: `$ pip install --no-cache-dir -U pip`
- Instale as dependências do projeto, incluindo o CLI: `$ pip install -r requirements.txt`

## Lint e qualidade
Ruff foi a ferramenta de linting e formatação por ser de fácil configuração, permite personalização e é bastante performática em identificar quebras de PEPs e/ou formatar código conforme o arquivo [pyproject.toml](pyproject.toml) nas sessões `tool.ruff` e `tool.ruff.format`

- Uso: `$ ruff format . && ruff check .`