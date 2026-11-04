"""
Passagem de bastao do comercial para o juridico - o maior gargalo do escritorio.

O comercial preenche um JSON curto (ou responde as perguntas no terminal) e este script
gera o DOSSIE DO CASO: ficha padronizada, checklist de documentos, o que falta cobrar do
cliente, prazos e o briefing pronto para o agente `macedo-revisional` / `macedo-busca-apreensao`.

  python HANDOFF/passagem_bastao.py --dados casos/joao_silva.json
  python HANDOFF/passagem_bastao.py --modelo > casos/novo.json     (gera o JSON em branco)
  python HANDOFF/passagem_bastao.py --interativo

Saida: SAIDA/casos/<CLIENTE>/DOSSIE_<CLIENTE>.md  (+ o JSON normalizado ao lado)
O dossie NAO e peca e nao vai ao cliente: e o que a Luysa le para abrir o caso.
"""
import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from config.escritorio import EQUIPE  # noqa: E402

MODELO = {
    "cliente": {
        "nome": "", "cpf": "", "rg": "", "estado_civil": "", "profissao": "",
        "endereco": "", "telefone": "", "email": "",
    },
    "caso": {
        "tipo": "revisional | busca_apreensao | rmc | consignado | superendividamento | outro",
        "banco": "",
        "contrato_numero": "",
        "data_contratacao": "",
        "valor_financiado": None,
        "valor_parcela": None,
        "prazo_meses": None,
        "parcelas_pagas": None,
        "tarifas_financiadas": None,
        "objetivo_cliente": "",
        "ja_tem_acao_judicial": "",
        "processo_numero": "",
        "prazo_judicial": "",
        "comarca": "",
    },
    "comercial": {
        "quem_atendeu": "", "origem_lead": "", "honorarios": "",
        "entrada_paga": False, "link_entrada": "", "observacoes": "",
    },
    "documentos_recebidos": [],
}

DOCS_ESSENCIAIS = {
    "revisional": ["contrato integral com CET", "extrato de evolucao da divida",
                   "comprovantes de pagamento", "documento pessoal (CNH/RG)",
                   "comprovante de residencia"],
    "busca_apreensao": ["copia da inicial", "copia da liminar/citacao", "contrato integral",
                        "notificacao extrajudicial e AR", "comprovantes de pagamento",
                        "documento pessoal (CNH/RG)"],
    "rmc": ["extrato de emprestimos consignados (Meu INSS)", "extrato do beneficio",
            "contrato ou proposta, se houver", "faturas do cartao consignado",
            "documento pessoal (CNH/RG)"],
    "consignado": ["extrato de emprestimos consignados (Meu INSS)", "extrato do beneficio",
                   "contrato integral", "documento pessoal (CNH/RG)"],
    "superendividamento": ["relacao de todas as dividas com credor, saldo, parcela e taxa",
                           "comprovante de renda", "comprovante das despesas essenciais",
                           "documento pessoal (CNH/RG)"],
    "outro": ["contrato", "documento pessoal (CNH/RG)", "comprovante de residencia"],
}


def slug(texto):
    t = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()
    return re.sub(r'[^A-Za-z0-9]+', '_', t).strip('_').upper() or 'SEM_NOME'


def pendencias_cadastro(cliente):
    rotulos = {'nome': 'nome completo', 'cpf': 'CPF', 'rg': 'RG',
               'estado_civil': 'estado civil', 'profissao': 'profissao',
               'endereco': 'endereco completo', 'telefone': 'telefone', 'email': 'e-mail'}
    return [rotulos[k] for k in rotulos if not str(cliente.get(k, '')).strip()]


def calculo_preliminar(caso):
    """So roda se o comercial trouxe valor, parcela e prazo. Taxa media fica [CONFERIR]."""
    v, p, n = caso.get('valor_financiado'), caso.get('valor_parcela'), caso.get('prazo_meses')
    if not (v and p and n):
        return None
    sys.path.insert(0, os.path.join(RAIZ, 'CALCULO'))
    from calculo_revisional import taxa_implicita
    pv = float(v) + float(caso.get('tarifas_financiadas') or 0)
    i = taxa_implicita(pv, float(p), int(n))
    return {
        'valor_financiado_total': round(pv, 2),
        'taxa_mensal_contrato_pct': round(i * 100, 4),
        'taxa_anual_contrato_pct': round(((1 + i) ** 12 - 1) * 100, 2),
    }


def gerar_dossie(dados):
    cliente = dados.get('cliente', {})
    caso = dados.get('caso', {})
    com = dados.get('comercial', {})
    tipo = (caso.get('tipo') or 'outro').strip().lower()
    if tipo not in DOCS_ESSENCIAIS:
        tipo = 'outro'

    recebidos = [d.strip().lower() for d in dados.get('documentos_recebidos', [])]
    faltando = [d for d in DOCS_ESSENCIAIS[tipo]
                if not any(d.lower()[:12] in r for r in recebidos)]
    falta_cadastro = pendencias_cadastro(cliente)
    calc = calculo_preliminar(caso)

    agente = {'busca_apreensao': 'macedo-busca-apreensao'}.get(tipo, 'macedo-revisional')

    L = []
    A = L.append
    A(f"# DOSSIE DO CASO - {cliente.get('nome') or '[PREENCHER: nome]'}")
    A('')
    A(f"Aberto em {datetime.now():%d/%m/%Y %H:%M} | Tipo: **{tipo}** | "
      f"Revisao: **{EQUIPE['revisora_pecas']}**")
    A('')
    if caso.get('prazo_judicial'):
        A(f"> **PRAZO JUDICIAL INFORMADO: {caso['prazo_judicial']}** - conferir contagem "
          f"antes de qualquer coisa.")
        A('')
    A('## 1. Cliente')
    for k, v in cliente.items():
        A(f"- {k.replace('_', ' ').capitalize()}: {v or '[PREENCHER]'}")
    A('')
    A('## 2. Caso')
    for k, v in caso.items():
        A(f"- {k.replace('_', ' ').capitalize()}: {v if v not in (None, '') else '[PREENCHER]'}")
    A('')
    A('## 3. Comercial')
    for k, v in com.items():
        A(f"- {k.replace('_', ' ').capitalize()}: {v if v not in (None, '') else '[PREENCHER]'}")
    A('')
    A('## 4. Numeros preliminares')
    if calc:
        for k, v in calc.items():
            A(f"- {k.replace('_', ' ').capitalize()}: {v}")
        A('- Taxa media BACEN do mes e da modalidade: `[CONFERIR - serie SGS, citar fonte]`')
        A('- Rodar depois: `python CALCULO/calculo_revisional.py --valor ... --parcela ... '
          '--prazo ... --taxa-media-mensal <media BACEN>`')
    else:
        A('- Sem valor financiado, parcela e prazo nao ha numero nenhum. **Cobrar do comercial.**')
    A('')
    A('## 5. Documentos')
    A(f"Recebidos: {', '.join(dados.get('documentos_recebidos') or ['nenhum'])}")
    A('')
    if faltando:
        A('**Faltam (cobrar do cliente):**')
        for d in faltando:
            A(f"- [ ] {d}")
    else:
        A('Checklist de documentos essenciais completo.')
    A('')
    if falta_cadastro:
        A('**Falta no cadastro (bloqueia contrato e procuracao):** ' + ', '.join(falta_cadastro))
        A('')
    A('## 6. Proximos passos')
    A(f"1. Luysa confere este dossie e decide a via com a Dra. Caroline "
      f"(a IA nao define estrategia).")
    A(f"2. Com os documentos em maos, acionar o agente **{agente}** para o parecer de viabilidade.")
    A('3. Contrato/procuracao/declaracao: agente `macedo-contratacao` + assinatura no Autentique.')
    A('4. Lancar o caso e a tarefa no Astrea (manual - Astrea sem API).')
    if not com.get('entrada_paga'):
        A('5. Entrada ainda nao consta paga: conferir no Asaas antes de iniciar a producao '
          '(`ENTRADA/gerar_entrada.py` gera o link).')
    A('')
    A('---')
    A('Dossie interno. Nao e peca, nao vai ao cliente. Nenhum dado foi inventado: '
      'o que falta esta marcado [PREENCHER] ou [CONFERIR].')
    return '\n'.join(L)


def interativo():
    print('Passagem de bastao - responda o que tiver (Enter pula).\n')
    d = json.loads(json.dumps(MODELO))
    d['caso']['tipo'] = ''
    for secao in ('cliente', 'caso', 'comercial'):
        print(f'[{secao}]')
        for k in d[secao]:
            v = input(f'  {k}: ').strip()
            if v:
                if isinstance(d[secao][k], bool):
                    d[secao][k] = v.lower() in ('s', 'sim', 'true', '1')
                elif d[secao][k] is None:
                    try:
                        d[secao][k] = float(v.replace('.', '').replace(',', '.'))
                    except ValueError:
                        d[secao][k] = v
                else:
                    d[secao][k] = v
    docs = input('documentos recebidos (separados por ;): ').strip()
    d['documentos_recebidos'] = [x.strip() for x in docs.split(';') if x.strip()]
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dados', help='JSON do caso')
    ap.add_argument('--modelo', action='store_true', help='imprime o JSON em branco')
    ap.add_argument('--interativo', action='store_true')
    a = ap.parse_args()

    if a.modelo:
        print(json.dumps(MODELO, ensure_ascii=False, indent=2))
        return

    if a.interativo:
        dados = interativo()
    elif a.dados:
        with open(a.dados, encoding='utf-8') as f:
            dados = json.load(f)
    else:
        sys.exit('Use --dados <arquivo.json>, --interativo ou --modelo.')

    nome = slug(dados.get('cliente', {}).get('nome', ''))
    pasta = os.path.join(RAIZ, 'SAIDA', 'casos', nome)
    os.makedirs(pasta, exist_ok=True)
    md = os.path.join(pasta, f'DOSSIE_{nome}.md')
    with open(md, 'w', encoding='utf-8') as f:
        f.write(gerar_dossie(dados))
    with open(os.path.join(pasta, f'caso_{nome}.json'), 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f'Dossie: {md}')


if __name__ == '__main__':
    main()
