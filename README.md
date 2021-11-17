# ADF : Utility to explore Azure Data Factory configuration

## Step by Step

- install poetry: `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`
- configure virtual env: `echo "layout python /usr/local/bin/python3" >> .local.envrc`
- generate a pipeline graph : `poetry run adf draw --root <ADF-ROOT-FOLDER>`
