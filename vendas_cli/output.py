import json
from typing import Dict


def formatar_como_texto(relatorio: Dict) -> str:
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


def formatar_como_json(relatorio: Dict) -> str:
    return json.dumps(relatorio, indent=2, ensure_ascii=False)
