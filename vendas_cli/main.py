from vendas_cli.parser import parse_args
from vendas_cli.core import load_sales, calcular_relatorio, logger_sys
from vendas_cli.output import formatar_como_texto, formatar_como_json, formatar_como_pdf


def main():
    """
    Função principal da CLI de relatório de vendas.

    - Parseia argumentos da linha de comando.
    - Carrega e filtra vendas a partir do CSV informado.
    - Calcula relatório agregado.
    - Formata e imprime o relatório no formato solicitado (texto ou JSON).
    - Realiza logs das etapas principais e erros, se ocorrerem.
    """
    try:
        csv_path, formato, start, end, name = parse_args()
        logger_sys.info(f"Execução iniciada com arquivo: {csv_path}, formato: "
                        f"{formato}, intervalo: {start} a {end}, nome_pdf: {name}")

        vendas = load_sales(csv_path, start, end)
        logger_sys.info(f"{len(vendas)} vendas carregadas e filtradas")

        relatorio = calcular_relatorio(vendas)

        if formato == "json":
            print(formatar_como_json(relatorio))
        elif formato == "texto":
            print(formatar_como_texto(relatorio))
        else:
            print(formatar_como_pdf(relatorio, name))

    except Exception as e:
        logger_sys.error(f"Erro durante a execução do programa: {e}", exc_info=True)
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
