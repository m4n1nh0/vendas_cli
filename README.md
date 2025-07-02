## Vendas CLI – Gerador de Relatórios de Vendas Avançado

CLI em Python para processamento de arquivos CSV de vendas com filtros, agrupamentos e geração de relatórios em texto ou JSON.

> Desenvolvido como parte de um desafio técnico (nível Pleno-Sênior), com foco em **qualidade de código, testes, boas práticas e valor analítico**.

### Funcionalidades

* Leitura de arquivos CSV via linha de comando
* Filtros por data de venda (`--start`, `--end`)
* Relatórios em formato `text` ou `json`
* Cálculos:
  * Total de vendas por produto
  * Total de vendas por cliente
  * Produto mais vendido
  * Cliente que mais comprou
  * Total geral de vendas
  * Número de vendas realizadas
* Exibição de metadados:
  * Código e unidade do produto
  * Código, cidade e estado do cliente
* Estrutura modular com tipagem (`typing`)
* Logging e tratamento de erros
* Testes automatizados com `pytest` (cobertura > 90%)
* CLI empacotada via `setup.py`


### Estrutura esperada do CSV

| Coluna           | Descrição                      |
| ---------------- | ------------------------------ |
| `numero_venda`   | ID único da venda              |
| `data_venda`     | Data da venda (YYYY-MM-DD)     |
| `produto`        | Nome do produto vendido        |
| `codigo_produto` | Código interno do produto      |
| `unidade`        | Unidade de medida (ex: un, kg) |
| `valor_venda`    | Valor total da venda           |
| `cliente`        | Nome do cliente                |
| `codigo_cliente` | Código do cliente              |
| `cidade_cliente` | Cidade do cliente              |
| `estado_cliente` | Estado (UF) do cliente         |

### Instalação

```bash
git clone https://github.com/m4n1nh0/vendas_cli.git
cd vendas_cli
pip install .
```

> Instalará o comando `vendas-cli` no seu terminal.

### Como desinstalar

```bash
pip uninstall vendas_cli
```

> Desinstalará o comando `vendas-cli` no seu terminal.

### Testes

```bash
pytest --cov=vendas_cli --cov-report=term-missing
```

### Uso da CLI

```bash
vendas_cli caminho/para/arquivo.csv [opções]
```

#### Opções disponíveis:

| Parâmetro      | Descrição                                   |
| -------------- | ------------------------------------------- |
| `csv_path`     | Caminho do arquivo CSV de vendas            |
| `--format`     | Formato de saída: `text` (padrão) ou `json` |
| `--start`      | Data inicial do filtro (formato YYYY-MM-DD) |
| `--end`        | Data final do filtro (formato YYYY-MM-DD)   |
| `-h`, `--help` | Exibe o menu de ajuda                       |

#### Exibindo ajuda:

```bash
vendas_cli --help
```

Saída:

```
Gerador de Relatorio de Vendas

positional arguments:
  csv_path              Caminho do arquivo CSV

optional arguments:
  --format {text,json}  Formato de saída (padrão: text)
  --start START         Data inicial no formato YYYY-MM-DD
  --end END             Data final no formato YYYY-MM-DD
  -h, --help            Mostra este menu de ajuda
```

#### Exemplos de uso:

```bash
# Relatório padrão (texto)
vendas_cli dados/vendas.csv

# Saída JSON
vendas_cli dados/vendas.csv --format json

# Filtro por período
vendas_cli dados/vendas.csv --start 2025-01-01 --end 2025-03-31

# Ver menu de ajuda
vendas-cli --help
```

### Exemplo de saída (texto)

```
RELATORIO DE VENDAS
============================================================

>> Total por produto:
Caneta               (P001, un) - R$ 25,00
Caderno              (P002, un) - R$ 50,00

>> Total por cliente:
Ana Paula            (Cod: C123, Aracaju/SE) - R$ 40,00
João Souza           (Cod: C456, São Paulo/SP) - R$ 35,00

============================================================
TOTAL DE VENDAS REALIZADAS: 5
TOTAL GERAL:                R$ 75,00
PRODUTO MAIS VENDIDO:       Caderno
CLIENTE QUE MAIS COMPROU:   Ana Paula
```

### Exemplo com dados prontos

Este projeto já inclui um arquivo de exemplo com 50 vendas simuladas:

```
 dados/vendas_exemplo.csv
```

#### Como visualizar o relatório:

```bash
# Relatório em formato texto
vendas-cli dados/vendas_exemplo.csv

# Em formato JSON
vendas-cli dados/vendas_exemplo.csv --format json

# Filtrando por intervalo de datas
vendas-cli dados/vendas_exemplo.csv --start 2025-01-01 --end 2025-02-15
```

> Ideal para testar a CLI rapidamente sem precisar preparar dados reais.


### Diferenciais da solução

* Pensado para **uso real em empresas** com múltiplos produtos e clientes.
* Campos extras (`códigos`, `cidade`, `unidade`) **refletem necessidades de negócio**.
* Modularização clara permite fácil expansão (ex: filtros por cidade/UF).
* Inclusão de log detalhado e ajuste para que o log não interfira no relatório
* Inclusão de doc string nas funções


### Autor

Desenvolvido por **Mariano Mendonça** como parte de um processo seletivo para vaga Python Pleno-Sênior.

