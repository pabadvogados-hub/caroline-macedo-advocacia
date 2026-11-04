from calculo_revisional import pmt, taxa_implicita, calcular, saldo_devedor


def test_roundtrip_taxa():
    p = pmt(50000, 0.0215, 48)
    assert abs(taxa_implicita(50000, p, 48) - 0.0215) < 1e-9


def test_taxa_igual_media_sem_diferenca():
    p = pmt(30000, 0.02, 36)
    r = calcular(30000, p, 36, 2.0, pagas=10)
    assert abs(r["diferenca_por_parcela"]) < 0.01
    assert abs(r["razao_contratada_sobre_media"] - 1) < 1e-3


def test_taxa_acima_da_media():
    p = pmt(50000, 0.035, 48)
    r = calcular(50000, p, 48, 2.0, pagas=12)
    assert r["diferenca_por_parcela"] > 0
    assert r["saldo_devedor_contrato"] > r["saldo_devedor_revisado"]


def test_saldo_final_zero():
    assert abs(saldo_devedor(10000, 0.02, 12, 12)) < 1e-6
