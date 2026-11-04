"""
Calculo de revisao de financiamento (Tabela Price) - Caroline Macedo Advocacia.

Compara o contrato com a taxa media de mercado do BACEN (mesmo mes e modalidade) e
apura a diferenca por parcela e no total. A taxa media NAO e inventada aqui: voce informa,
com a fonte (serie SGS do BACEN) e o mes. Resultado e subsidio para o revisor, nunca laudo final.

Uso:
  python CALCULO/calculo_revisional.py --valor 50000 --parcela 1850 --prazo 48 \
      --taxa-media-mensal 2.15 --pagas 14 [--tarifas 1200] [--json]
  (--valor = valor financiado sem tarifas financiadas; --tarifas = TAC/seguro etc. embutidos)
"""
import argparse
import json


def pmt(pv: float, i: float, n: int) -> float:
    """Parcela Price. i em fracao mensal (0.02 = 2%)."""
    if i == 0:
        return pv / n
    return pv * i / (1 - (1 + i) ** -n)


def taxa_implicita(pv: float, parcela: float, n: int) -> float:
    """Taxa mensal que iguala valor presente e n parcelas (bissecao)."""
    if parcela * n <= pv:
        return 0.0
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if pmt(pv, mid, n) > parcela:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def saldo_devedor(pv: float, i: float, n: int, pagas: int) -> float:
    p = pmt(pv, i, n)
    return pv * (1 + i) ** pagas - p * (((1 + i) ** pagas - 1) / i if i else pagas)


def calcular(valor, parcela, prazo, taxa_media_mensal_pct, pagas=0, tarifas=0.0):
    pv = valor + tarifas
    i_contrato = taxa_implicita(pv, parcela, prazo)
    i_media = taxa_media_mensal_pct / 100
    parcela_rev = pmt(pv, i_media, prazo)
    dif = parcela - parcela_rev
    r = {
        "valor_financiado_total": round(pv, 2),
        "taxa_mensal_implicita_pct": round(i_contrato * 100, 4),
        "taxa_anual_implicita_pct": round(((1 + i_contrato) ** 12 - 1) * 100, 2),
        "taxa_media_mensal_pct": taxa_media_mensal_pct,
        "razao_contratada_sobre_media": round(i_contrato / i_media, 3) if i_media else None,
        "parcela_contrato": round(parcela, 2),
        "parcela_revisada": round(parcela_rev, 2),
        "diferenca_por_parcela": round(dif, 2),
        "total_contrato": round(parcela * prazo, 2),
        "total_revisado": round(parcela_rev * prazo, 2),
        "diferenca_total_prazo": round(dif * prazo, 2),
    }
    if pagas:
        pagas = min(pagas, prazo)
        r["parcelas_pagas"] = pagas
        r["pago_a_maior_ate_agora_simples"] = round(dif * pagas, 2)
        r["saldo_devedor_contrato"] = round(saldo_devedor(pv, i_contrato, prazo, pagas), 2)
        r["saldo_devedor_revisado"] = round(saldo_devedor(pv, i_media, prazo, pagas), 2)
    r["aviso"] = ("Subsidio ao revisor. Conferir CET, tarifas, datas e capitalizacao no contrato; "
                  "taxa media deve citar fonte BACEN e mes. Repeticao em dobro/simples e decisao da advogada.")
    return r


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--valor", type=float, required=True)
    ap.add_argument("--parcela", type=float, required=True)
    ap.add_argument("--prazo", type=int, required=True)
    ap.add_argument("--taxa-media-mensal", type=float, required=True, help="em %% a.m., fonte BACEN")
    ap.add_argument("--pagas", type=int, default=0)
    ap.add_argument("--tarifas", type=float, default=0.0)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    res = calcular(a.valor, a.parcela, a.prazo, a.taxa_media_mensal, a.pagas, a.tarifas)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        for k, v in res.items():
            print(f"{k}: {v}")
