from vendas_cli.core import calcular_relatorio


def test_com_dados_completos():
    vendas = [
        {
            "numero_venda": "001",
            "produto": "Caneta",
            "codigo_produto": "P001",
            "unidade": "un",
            "valor_venda": "10.00",
            "data_venda": "2025-01-01",
            "cliente": "Lucas",
            "codigo_cliente": "C123",
            "cidade_cliente": "Aracaju",
            "estado_cliente": "SE"
        }
    ]
    rel = calcular_relatorio(vendas)
    assert rel["produtos_info"]["Caneta"]["codigo_produto"] == "P001"
    assert rel["clientes_info"]["Lucas"]["cidade"] == "Aracaju"
    assert rel["numero_total_vendas"] == 1
