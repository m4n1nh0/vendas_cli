import json
from typing import Dict
from fpdf import FPDF

from vendas_cli.core import logger_sys


def formatar_como_texto(relatorio: Dict) -> str:
    """
    Formata o relatório de vendas numa string de texto legível para exibição no console ou arquivo.

    O formato inclui:
    - Título e separadores visuais.
    - Listagem do total vendido por produto, com código e unidade.
    - Listagem do total vendido por cliente, com código, cidade e estado.
    - Resumo final com total de vendas, valor total, produto mais vendido e cliente que mais comprou.

    :param relatorio: Dicionário contendo os dados agregados do relatório de vendas.
    :return: String formatada contendo o relatório em formato textual.
    """
    logger_sys.info("Formatando relatório como texto")
    try:
        linhas = ["RELATORIO DE VENDAS", "=" * 60, "\n>> Total por produto:"]

        for produto, total in relatorio["total_por_produto"].items():
            info = relatorio["produtos_info"].get(produto, {})
            cod = info.get("codigo_produto", "N/A")
            unidade = info.get("unidade", "N/A")
            linhas.append(f"{produto:<20} ({cod}, {unidade}) - R$ {total:,.2f}")

        linhas.append("\n>> Total por cliente:")
        for cliente, total in relatorio["total_por_cliente"].items():
            info = relatorio["clientes_info"].get(cliente, {})
            cod = info.get("codigo_cliente", "N/A")
            cidade = info.get("cidade", "N/A")
            estado = info.get("estado", "N/A")
            linhas.append(f"{cliente:<20} (Cod: {cod}, {cidade}/{estado}) - R$ {total:,.2f}")

        linhas.append("\n" + "=" * 60)
        linhas.append(f"TOTAL DE VENDAS REALIZADAS: {relatorio['numero_total_vendas']}")
        linhas.append(f"TOTAL GERAL:                R$ {relatorio['total_geral']:,.2f}")
        linhas.append(f"PRODUTO MAIS VENDIDO:       {relatorio['produto_mais_vendido']}")
        linhas.append(f"CLIENTE QUE MAIS COMPROU:   {relatorio['cliente_mais_comprou']}")
        return "\n".join(linhas)

    except Exception as e:
        logger_sys.error(f"Erro ao formatar relatório como texto: {e}")
        raise


def formatar_como_json(relatorio: Dict) -> str:
    """
    Formata o relatório de vendas numa string JSON formatada.

    Utiliza indentação para facilitar a leitura e mantém caracteres Unicode legíveis.

    :param relatorio: Dicionário contendo os dados agregados do relatório de vendas.
    :return: String JSON formatada do relatório.
    """
    logger_sys.info("Formatando relatório como JSON")
    try:
        return json.dumps(relatorio, indent=2, ensure_ascii=False)
    except Exception as e:
        logger_sys.error(f"Erro ao formatar relatório como JSON: {e}")
        raise


def formatar_como_pdf(relatorio: Dict, file_name=None) -> str:
    """
    Formata o relatório de vendas para um aquivo pdf.

    O formato inclui:
    - Título e separadores visuais.
    - Listagem do total vendido por produto, com código e unidade.
    - Listagem do total vendido por cliente, com código, cidade e estado.
    - Resumo final com total de vendas, valor total, produto mais vendido e cliente que mais comprou.

    :param relatorio: Dicionário contendo os dados agregados do relatório de vendas.
    :param file_name: Noem do arquivo que será salvo o PDF.

    :return: nome do aqruivo PDF formatado.
    """
    if file_name is None:
        file_name = "output_fpdf.pdf"

    logger_sys.info("Formatando relatório como texto")
    try:
        pdf = FPDF(format="A4")
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.set_title("RELATORIO DE VENDAS")
        pdf.cell(200, 10, txt="RELATORIO DE VENDAS", ln=1, align="C")
        pdf.cell(200, 10, txt="Total por produto:", ln=2, align="C")
        for produto, total in relatorio["total_por_produto"].items():
            info = relatorio["produtos_info"].get(produto, {})
            cod = info.get("codigo_produto", "N/A")
            unidade = info.get("unidade", "N/A")
            linha = f"{produto:<20} ({cod}, {unidade}) - R$ {total:,.2f}"
            pdf.cell(200, 10, txt=linha, ln=1, align="L")

        pdf.cell(200, 10, txt="Total por cliente", ln=2, align="C")
        for cliente, total in relatorio["total_por_cliente"].items():
            info = relatorio["clientes_info"].get(cliente, {})
            cod = info.get("codigo_cliente", "N/A")
            cidade = info.get("cidade", "N/A")
            estado = info.get("estado", "N/A")
            linha = f"{cliente:<20} (Cod: {cod}, {cidade}/{estado}) - R$ {total:,.2f}"
            pdf.cell(200, 10, txt=linha, ln=1, align="L")

        pdf.cell(200, 10, txt="RESUMO", ln=2, align="C")

        pdf.cell(200, 10, txt=f"TOTAL DE VENDAS REALIZADAS: {relatorio['numero_total_vendas']}", ln=1, align="L")
        pdf.cell(200, 10, txt=f"TOTAL GERAL:                R$ {relatorio['total_geral']:,.2f}", ln=1, align="L")
        pdf.cell(200, 10, txt=f"PRODUTO MAIS VENDIDO:       {relatorio['produto_mais_vendido']}", ln=1, align="L")
        pdf.cell(200, 10, txt=f"CLIENTE QUE MAIS COMPROU:   {relatorio['cliente_mais_comprou']}", ln=1, align="L")
        pdf.output(file_name)
        logger_sys.info(f"relatório PDF savo como: {file_name}")
        return file_name
    except Exception as e:
        logger_sys.error(f"Erro ao gerar relatório como PDF: {e}")
        raise
