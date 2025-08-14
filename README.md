# desafio-vendas-cli

O objetivo deste projeto é ler um arquivo CSV cujo cabeçalho é "produto,quantidade,preco_unitario,data"

## Desenvolvimento / Execução Local
Passo a passo para configuração de execução em ambiente local

### Crie uma Venv
`$ python -m venv venv`

### Ative a Venv e exponha o caminho do python
`$ source venv/bin/activate && export PYTHONPATH=.`

### Instalando as dependências
- Atualize o pip: `$ pip install --no-cache-dir -U pip`
- Instale as dependências do projeto, incluindo o CLI: `$ pip install -r requirements.txt`

## Lint e qualidade
Ruff foi a ferramenta de linting e formatação por ser de fácil configuração, permite personalização e é bastante performática em identificar quebras de PEPs e/ou formatar código conforme o arquivo [pyproject.toml](pyproject.toml) nas sessões `tool.ruff` e `tool.ruff.format`, bem como formatação de imports sem precisar instalar a dependência `isort` para tal.

- Uso: `$ ruff format . && ruff check .`

## Testes
Para verificar a cobertura de testes, execute no terminal:
```bash
pytest --collect-only
coverage run -m pytest
coverage report --fail-under 80
```