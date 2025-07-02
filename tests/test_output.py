from vendas_cli.output import formatar_como_texto, formatar_como_json


def test_saida_formatada():
    relatorio = {
        "total_por_produto": {"Caneta": 10.0},
        "produtos_info": {"Caneta": {"codigo_produto": "P001", "unidade": "un"}},
        "total_por_cliente": {"Lucas": 10.0},
        "clientes_info": {"Lucas": {"codigo_cliente": "C123", "cidade": "Aracaju", "estado": "SE"}},
        "total_geral": 10.0,
        "produto_mais_vendido": "Caneta",
        "cliente_mais_comprou": "Lucas",
        "numero_total_vendas": 1
    }
    texto = formatar_como_texto(relatorio)
    json_str = formatar_como_json(relatorio)
    assert "Caneta" in texto
    assert "Aracaju/SE" in texto
    assert '"codigo_cliente": "C123"' in json_str
