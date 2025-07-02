from vendas_cli.parser import parse_args
from vendas_cli.core import load_sales, calcular_relatorio, logger_sys
from vendas_cli.output import formatar_como_texto, formatar_como_json


def main():
    csv_path, formato, start, end = parse_args()
    logger_sys.info(f"Execução iniciada com arquivo: {csv_path}")
    vendas = load_sales(csv_path, start, end)
    relatorio = calcular_relatorio(vendas)

    if formato == "json":
        print(formatar_como_json(relatorio))
    else:
        print(formatar_como_texto(relatorio))
    logger_sys.info("Relatório calculado com sucesso.")

if __name__ == "__main__":
    main()
