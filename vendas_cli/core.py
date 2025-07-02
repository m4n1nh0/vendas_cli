import csv
import logging
from typing import List, Dict, Optional
from datetime import datetime
from logging import Logger


def setup_logger(name: str = "vendas_cli") -> Logger:
    logger_csv = logging.getLogger(name)
    logger_csv.setLevel(logging.INFO)

    if not logger_csv.handlers:
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

        file_handler = logging.FileHandler("vendas_cli.log", mode="w", encoding="utf-8")
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger_csv.addHandler(file_handler)
        logger_csv.addHandler(console_handler)

    return logger_csv


logger_sys = setup_logger()


def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")


def load_sales(csv_path: str, start: Optional[str], end: Optional[str]) -> list[str]:
    sales = []
    start_date = parse_date(start) if start else None
    end_date = parse_date(end) if end else None

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                date = parse_date(row["data_venda"])
                if (not start_date or date >= start_date) and (not end_date or date <= end_date):
                    sales.append(row)
            except Exception as e:
                logger_sys.warning(f"Erro ao processar linha: {row} - {e}")
    return sales


def calcular_relatorio(sales: List[Dict[str, str]]) -> Dict:
    total_por_produto = {}
    total_por_cliente = {}
    produtos_info = {}
    clientes_info = {}
    total_geral = 0.0
    numeros_de_vendas = set()

    for venda in sales:
        produto = venda["produto"]
        cliente = venda.get("cliente", "Desconhecido")
        valor = float(venda["valor_venda"])
        numero = venda.get("numero_venda")
        cod_produto = venda.get("codigo_produto")
        unidade = venda.get("unidade")
        cod_cliente = venda.get("codigo_cliente")
        cidade = venda.get("cidade_cliente", "N/A")
        estado = venda.get("estado_cliente", "N/A")

        if numero:
            numeros_de_vendas.add(numero)

        if produto not in produtos_info:
            produtos_info[produto] = {"codigo_produto": cod_produto, "unidade": unidade}

        if cliente not in clientes_info:
            clientes_info[cliente] = {
                "codigo_cliente": cod_cliente,
                "cidade": cidade,
                "estado": estado
            }

        total_por_produto[produto] = total_por_produto.get(produto, 0.0) + valor
        total_por_cliente[cliente] = total_por_cliente.get(cliente, 0.0) + valor
        total_geral += valor

    produto_mais_vendido = max(total_por_produto, key=total_por_produto.get, default=None)
    cliente_mais_comprou = max(total_por_cliente, key=total_por_cliente.get, default=None)

    return {
        "total_por_produto": total_por_produto,
        "produtos_info": produtos_info,
        "total_por_cliente": total_por_cliente,
        "clientes_info": clientes_info,
        "total_geral": total_geral,
        "produto_mais_vendido": produto_mais_vendido,
        "cliente_mais_comprou": cliente_mais_comprou,
        "numero_total_vendas": len(numeros_de_vendas)
    }
