import argparse
from typing import Tuple, Optional


def parse_args() -> Tuple[str, str, Optional[str], Optional[str]]:
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
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Formato da saída")
    parser.add_argument("--start", help="Data inicial (YYYY-MM-DD)")
    parser.add_argument("--end", help="Data final (YYYY-MM-DD)")

    args = parser.parse_args()
    return args.csv_path, args.format, args.start, args.end
