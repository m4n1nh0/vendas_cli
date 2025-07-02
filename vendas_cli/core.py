import csv
import logging
from typing import List, Dict, Optional
from datetime import datetime
from logging import Logger


def setup_logger(name: str = "vendas_cli") -> Logger:
    """
    Configura e retorna um logger para a aplicação.

    - Cria um logger com nível INFO.
    - Adiciona handlers para console e arquivo de log 'vendas_cli.log'.
    - O arquivo de log é sobrescrito a cada execução (modo 'w').
    - Formata as mensagens com timestamp, nível e mensagem.

    :param name: Nome do logger (default: "vendas_cli").
    :return: Logger configurado.
    """
    logger_csv = logging.getLogger(name)
    logger_csv.setLevel(logging.INFO)

    if not logger_csv.handlers:
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

        file_handler = logging.FileHandler("vendas_cli.log", mode="w", encoding="utf-8")
        file_handler.setFormatter(formatter)

        import sys
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(formatter)

        logger_csv.addHandler(file_handler)
        logger_csv.addHandler(console_handler)

    return logger_csv


logger_sys = setup_logger()


def parse_date(date_str: str) -> datetime:
    """
    Converte uma string no formato 'YYYY-MM-DD' para um objeto datetime.

    :param date_str: Data em formato string (ex: "2023-05-01").
    :return: Objeto datetime correspondente.
    :raises ValueError: Se o formato da data for inválido.
    """
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        logger_sys.debug(f"Data convertida com sucesso: {date_str} -> {date}")
        return date
    except ValueError as e:
        logger_sys.error(f"Falha ao converter data '{date_str}': {e}")
        raise


def load_sales(csv_path: str, start: Optional[str], end: Optional[str]) -> List[Dict[str, str]]:
    """
    Carrega e filtra os dados de vendas de um arquivo CSV com base num intervalo de datas.

    - Lê o arquivo CSV no caminho `csv_path`.
    - Filtra as vendas cuja data está entre `start` e `end` (inclusive).
    - Se `start` ou `end` forem None, não aplica filtro respectivo.
    - Registra warnings em caso de linhas com erro de formatação ou dados inválidos.

    :param csv_path: Caminho do arquivo CSV contendo os dados das vendas.
    :param start: Data inicial do filtro no formato 'YYYY-MM-DD' ou None para sem filtro inicial.
    :param end: Data final do filtro no formato 'YYYY-MM-DD' ou None para sem filtro final.
    :return: Lista de dicionários representando as vendas filtradas.
    """
    sales = []
    start_date = parse_date(start) if start else None
    end_date = parse_date(end) if end else None

    logger_sys.info(f"Iniciando carregamento do arquivo CSV: {csv_path}")
    logger_sys.info(f"Filtro de data - início: {start_date}, fim: {end_date}")

    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            linhas_lidas = 0
            linhas_filtradas = 0

            for row in reader:
                linhas_lidas += 1
                try:
                    date = parse_date(row["data_venda"])
                    if (not start_date or date >= start_date) and (not end_date or date <= end_date):
                        sales.append(row)
                        linhas_filtradas += 1
                except Exception as e:
                    logger_sys.warning(f"Erro ao processar linha {linhas_lidas}: {row} - {e}")

            logger_sys.info(f"Linhas lidas: {linhas_lidas}, linhas filtradas: {linhas_filtradas}")

    except FileNotFoundError:
        logger_sys.error(f"Arquivo CSV não encontrado: {csv_path}")
        raise
    except Exception as e:
        logger_sys.error(f"Erro ao carregar arquivo CSV: {e}")
        raise

    return sales


def calcular_relatorio(sales: List[Dict[str, str]]) -> Dict:
    """
    Gera um relatório agregado das vendas recebidas.

    - Calcula totais por produto e por cliente.
    - Mantém informações adicionais de produtos e clientes.
    - Determina o produto mais vendido e o cliente que mais comprou.
    - Conta o número total de vendas únicas.

    :param sales: Lista de dicionários com os dados das vendas.
    :return: Dicionário contendo os dados agregados do relatório.
    """
    total_por_produto = {}
    total_por_cliente = {}
    produtos_info = {}
    clientes_info = {}
    total_geral = 0.0
    numeros_de_vendas = set()

    logger_sys.info(f"Iniciando cálculo do relatório para {len(sales)} vendas")

    for idx, venda in enumerate(sales, start=1):
        try:
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
                logger_sys.debug(f"Novo produto encontrado: {produto} - {produtos_info[produto]}")

            if cliente not in clientes_info:
                clientes_info[cliente] = {
                    "codigo_cliente": cod_cliente,
                    "cidade": cidade,
                    "estado": estado
                }
                logger_sys.debug(f"Novo cliente encontrado: {cliente} - {clientes_info[cliente]}")

            total_por_produto[produto] = total_por_produto.get(produto, 0.0) + valor
            total_por_cliente[cliente] = total_por_cliente.get(cliente, 0.0) + valor
            total_geral += valor

        except Exception as e:
            logger_sys.warning(f"Erro ao processar venda #{idx}: {venda} - {e}")

    produto_mais_vendido = max(total_por_produto, key=total_por_produto.get, default=None)
    cliente_mais_comprou = max(total_por_cliente, key=total_por_cliente.get, default=None)

    logger_sys.info(f"Relatório calculado: total geral = {total_geral:.2f}, produto mais vendido = "
                    f"{produto_mais_vendido}, cliente que mais comprou = {cliente_mais_comprou}")

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
