"""
Link da entrada de honorarios SEM depender do financeiro.

Este e o pedido numero 1 do escritorio para os primeiros 30 dias: hoje a emissao do
boleto/pix/link da entrada passa pelo financeiro e o cliente esfria esperando. Aqui o
proprio comercial (ou o Claude) gera o link na hora, com a mensagem pronta para enviar.

  python ENTRADA/gerar_entrada.py --cliente "Joao da Silva" --valor 1500 \
      --acao revisional [--parcelas 3] [--validade 7] [--dry-run]

Saida: link do checkout + mensagem pronta + registro em SAIDA/entradas/AAAA-MM.csv

Nada e enviado ao cliente por este script. Quem envia e a pessoa do comercial.
"""
import argparse
import csv
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.escritorio import ESCRITORIO  # noqa: E402

ACOES = {
    'revisional': 'Revisional de financiamento de veiculo',
    'busca': 'Defesa em busca e apreensao',
    'rmc': 'Cartao consignado (RMC/RCC)',
    'consignado': 'Emprestimo consignado',
    'superendividamento': 'Superendividamento',
    'outro': 'Honorarios advocaticios',
}

MENSAGEM = """Ola, {primeiro_nome}! Aqui e do escritorio {escritorio}.

Segue o link para a entrada dos honorarios do seu caso ({acao}):
{link}

Valor: R$ {valor}
{parcelamento}No link voce escolhe PIX, boleto ou cartao. O link vale por {validade} dias.

Assim que o pagamento cair, nossa equipe juridica inicia a analise do seu contrato.
Qualquer duvida, e so responder aqui."""


def brl(v):
    return f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def montar_mensagem(cliente, valor, acao_label, link, parcelas, validade):
    parc = ''
    if parcelas and parcelas > 1:
        parc = f'Pode dividir em ate {parcelas}x no cartao.\n'
    return MENSAGEM.format(
        primeiro_nome=cliente.split()[0],
        escritorio=ESCRITORIO['responsavel'].split()[0] + ' Macedo Advocacia',
        acao=acao_label,
        link=link,
        valor=brl(valor),
        parcelamento=parc,
        validade=validade,
    )


def registrar(linha):
    pasta = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         'SAIDA', 'entradas')
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, f'{datetime.now():%Y-%m}.csv')
    novo = not os.path.exists(caminho)
    with open(caminho, 'a', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, delimiter=';')
        if novo:
            w.writerow(['data', 'cliente', 'acao', 'valor', 'parcelas',
                        'link_id', 'url', 'situacao'])
        w.writerow(linha)
    return caminho


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cliente', required=True)
    ap.add_argument('--valor', type=float, required=True)
    ap.add_argument('--acao', default='outro', choices=sorted(ACOES))
    ap.add_argument('--parcelas', type=int, default=1, help='maximo no cartao')
    ap.add_argument('--validade', type=int, default=7, help='dias de validade do link')
    ap.add_argument('--dry-run', action='store_true',
                    help='nao chama o Asaas; mostra o que seria criado')
    a = ap.parse_args()

    if a.valor <= 0:
        sys.exit('Valor da entrada deve ser maior que zero.')

    acao_label = ACOES[a.acao]
    nome_link = f'Honorarios - {acao_label} - {a.cliente}'

    if a.dry_run:
        link_id, url = 'DRY_RUN', 'https://www.asaas.com/000/c/DRY_RUN'
    else:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                 'config', '.env'))
        from INTEGRACOES import asaas_integration as asaas
        resp = asaas.criar_link_pagamento(
            nome=nome_link,
            valor=a.valor,
            descricao=f'Entrada de honorarios - {acao_label}',
            max_parcelas=a.parcelas,
            dias_validade=a.validade,
        )
        if not resp or not resp.get('url'):
            sys.exit(f'Asaas nao devolveu link. Resposta: {json.dumps(resp, ensure_ascii=False)}')
        link_id, url = resp['id'], resp['url']

    msg = montar_mensagem(a.cliente, a.valor, acao_label, url, a.parcelas, a.validade)
    caminho = registrar([f'{datetime.now():%Y-%m-%d %H:%M}', a.cliente, acao_label,
                         brl(a.valor), a.parcelas, link_id, url,
                         'DRY_RUN' if a.dry_run else 'LINK_CRIADO'])

    print(f'\nLink: {url}')
    print(f'Registrado em: {caminho}')
    print('\n--- mensagem para enviar ao cliente (confira antes de mandar) ---\n')
    print(msg)
    print('\n----------------------------------------------------------------')
    print('Depois do pagamento: rodar HANDOFF/passagem_bastao.py para abrir o caso no juridico.')


if __name__ == '__main__':
    main()
