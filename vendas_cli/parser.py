import argparse
from typing import Tuple, Optional

from vendas_cli.core import logger_sys


def parse_args() -> Tuple[str, str, Optional[str], Optional[str]]:
    """
    Parseia os argumentos da linha de comando para o gerador de relatório de vendas.

    Argumentos aceitos:
    - csv_path: caminho do arquivo CSV com os dados de vendas (obrigatório).
    - --format: formato da saída do relatório, pode ser 'text' ou 'json' (default: 'text').
    - --start: data inicial para filtro no formato 'YYYY-MM-DD' (opcional).
    - --end: data final para filtro no formato 'YYYY-MM-DD' (opcional).

    Exemplo de uso:
      vendas-cli vendas.csv
      vendas-cli vendas.csv --format json
      vendas-cli vendas.csv --start 2025-01-01 --end 2025-03-31 --format text

    :return: Tupla contendo (csv_path, format, start, end)
    """
    logger_sys.info("Iniciando parsing dos argumentos da linha de comando")
    parser = argparse.ArgumentParser(
        description="Gerador de Relatorio de Vendas",
        epilog="""
Exemplos:
  vendas-cli vendas.csv
  vendas-cli vendas.csv --format (json ou text)
  vendas-cli vendas.csv --start 2025-01-01 --end 2025-03-31 --format (json ou text)
""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("csv_path", help="Caminho do arquivo CSV")
    parser.add_argument("--format", choices=["text", "json"],
                        default="text", help="Formato da saída")
    parser.add_argument("--start", help="Data inicial (YYYY-MM-DD)")
    parser.add_argument("--end", help="Data final (YYYY-MM-DD)")

    args = parser.parse_args()

    logger_sys.info(f"Argumentos parseados: csv_path={args.csv_path}, "
                    f"format={args.format}, start={args.start}, end={args.end}")
    return args.csv_path, args.format, args.start, args.end
