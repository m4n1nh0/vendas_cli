import argparse
from typing import Tuple, Optional

from vendas_cli.core import logger_sys


def parse_args() -> Tuple[str, str, Optional[str], Optional[str], Optional[str]]:
    """
    Parseia os argumentos da linha de comando para o gerador de relatório de vendas.

    Argumentos aceitos:
    - csv_path: caminho do arquivo CSV com os dados de vendas (obrigatório).
    - --format: formato da saída do relatório, pode ser 'text' ou 'json', ou 'pdf' (‘default’: 'text').
    - --start: data inicial para filtro no formato 'YYYY-MM-DD' (opcional).
    - --end: data final para filtro no formato 'YYYY-MM-DD' (opcional).
    - --name: noem do arquivo ex: sou_arquivo.pdf (opcional).

    Exemplo de uso:
      vendas_cli vendas.csv
      vendas_cli vendas.csv --format json
      vendas_cli vendas.csv --start 2025-01-01 --end 2025-03-31 --format text

    :return: Tupla contendo (csv_path, format, start, end, name)
    """
    logger_sys.info("Iniciando parsing dos argumentos da linha de comando")
    parser = argparse.ArgumentParser(
        description="Gerador de Relatorio de Vendas",
        epilog="""
Exemplos:
  vendas_cli vendas.csv
  vendas_cli vendas.csv --format (json ou text)
  vendas_cli vendas.csv --start 2025-01-01 --end 2025-03-31 --format (json ou text ou pdf)
  vendas_cli vendas.csv --start 2025-01-01 --end 2025-03-31 --format pdf --name meu_arquivo.pdf
""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("csv_path", help="Caminho do arquivo CSV")
    parser.add_argument("--format", choices=["text", "json", "pdf"],
                        default="text", help="Formato da saída")
    parser.add_argument("--start", help="Data inicial (YYYY-MM-DD)")
    parser.add_argument("--end", help="Data final (YYYY-MM-DD)")
    parser.add_argument("--name", help="file name ex: arquivo.pdf")

    args = parser.parse_args()

    logger_sys.info(f"Argumentos parseados: csv_path={args.csv_path}, "
                    f"format={args.format}, start={args.start}, end={args.end},"
                    f"name={args.name}")
    return args.csv_path, args.format, args.start, args.end, args.name
