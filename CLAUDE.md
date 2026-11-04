# Caroline Macedo Advocacia - Central de Automacoes

> Escritorio: **Caroline Macedo Sociedade Individual de Advocacia** (CNPJ 58.173.643/0001-17)
> Responsavel: **Dra. Caroline Neiva Christofano Macedo** - OAB/AL 15.766, OAB/SP 528.725, OAB/PE 70.091
> Sede Maceio/AL, filial Sorocaba/SP | caroline@carolinemacedoadv.com | (82) 9366-6565
> Area: **Direito Bancario do lado do consumidor**. Carro-chefe: revisional de financiamento
> de veiculo e defesa em busca e apreensao. Tambem RMC/RCC, consignado, CCB e superendividamento.
> Volume: 20 a 40 casos novos por mes.

## Regra de ouro (do briefing dela, inegociavel)

**A IA NUNCA define estrategia e NUNCA protocola.** Toda peca e todo parecer param para revisao
da **Luysa** (coordenadora juridica) e, por fim, da Dra. Caroline. Escolha de tese, valor de dano
moral, pedido de tutela e a decisao entre purgar a mora ou contestar sao da advogada: a IA
apresenta opcoes com riscos e numeros, nao decide. Nunca inventar CPF, taxa, valor, data, sumula,
tema ou precedente - onde faltar dado, `[CONFERIR]` ou `[PREENCHER]`.

## Equipe
| Papel | Quem |
|---|---|
| Titular / revisao final | Dra. Caroline Macedo |
| Coordenadora juridica (revisa TODA peca) | Luysa |
| Gerente comercial | Vinicius |
| Closer | Gustavo |
| SDR | Ana Beatriz |

## Stack do escritorio
- Processos: **Astrea** - sem kanban e **sem API**. Tudo que envolve Astrea e manual: o
  lancamento de caso e tarefa e feito por pessoa, a automacao so lembra e prepara o texto.
- Financeiro: **Asaas** (cobranca) + Conta Azul (contabil)
- Assinatura: **Autentique** (nao ZapSign)
- CRM: Proflow | Documentos: Google Drive (Workspace)
- Roda **na nuvem**, nao preso a uma maquina (Claude.ai Projects) - ver `agentes_claude/GUIA_INSTALACAO_CLAUDE_AI.md`

## Os dois gargalos que esta pasta resolve primeiro

### 1. Link da entrada sem depender do financeiro
```
python ENTRADA/gerar_entrada.py --cliente "Nome do Cliente" --valor 1500 --acao revisional [--parcelas 3] [--dry-run]
```
Cria o link de pagamento no Asaas e imprime a mensagem pronta para o comercial enviar.
Usa `POST /paymentLinks`, que **nao exige CPF/CNPJ** - o cliente preenche no checkout; e por isso
que o comercial consegue gerar na hora da venda. Registro em `SAIDA/entradas/AAAA-MM.csv`.
O script **nao envia** nada ao cliente.

### 2. Passagem de bastao comercial -> juridico
```
python HANDOFF/passagem_bastao.py --modelo > casos/novo.json   # JSON em branco
python HANDOFF/passagem_bastao.py --dados casos/novo.json      # gera o dossie
python HANDOFF/passagem_bastao.py --interativo
```
Gera `SAIDA/casos/<CLIENTE>/DOSSIE_<CLIENTE>.md`: ficha do cliente, numeros preliminares do
contrato, checklist de documentos que faltam, pendencias de cadastro que travam contrato e
procuracao, e qual agente acionar. E o que a Luysa le para abrir o caso.

## Calculo da revisao
```
python CALCULO/calculo_revisional.py --valor 50000 --parcela 1850 --prazo 48 --taxa-media-mensal 2.15 --pagas 14
```
Apura a taxa implicita do contrato (Price), compara com a **taxa media do BACEN** que VOCE informa
(serie SGS, mesmo mes e mesma modalidade - o script nao busca nem inventa a media) e devolve
diferenca por parcela, total e saldo devedor revisado. Testes: `python CALCULO/test_calculo_revisional.py`
(ou pytest). Resultado e subsidio ao revisor, nunca laudo final.

## Agentes (agentes_claude/ e .claude/agents/)
| Agente | Para que |
|---|---|
| `macedo-revisional` | viabilidade e inicial de revisional, RMC/RCC, consignado, CCB, superendividamento |
| `macedo-busca-apreensao` | triagem de prazo (5 dias purga / 15 dias contestacao), notificacao, opcoes e contestacao |
| `macedo-contratacao` | contrato, procuracao, declaracao a partir dos modelos do escritorio + resumo de handoff |
| `macedo-controladoria` | revisao adversarial antes da Luysa: numeros, citacoes, formatacao, como o banco rebate |

`agentes_claude/CLOUD_WEB_INSTRUCOES_CAROLINE.md` e a instrucao-mae dos Projects no Claude.ai.

## Formatacao das pecas (padrao do escritorio)
Garamond 11 no corpo, 12 no enderecamento/cabecalho; espacamento entre linhas 1,5; recuo de
paragrafo 2,5 cm; citacao de jurisprudencia com recuo 4 cm. Pecas **curtas**, tecnicas, **sem latim**.
Centralizado em `config/escritorio.py`.

## Regras que a IA nunca ignora
- Sem contrato e sem a taxa media BACEN do mes nao existe tese de juros abusivos: pedir os documentos.
- Abusividade nao e reconhecida de oficio (Sumula 381 STJ): tem de ser pedida expressamente.
- Capitalizacao: so atacar quando nao houver pactuacao expressa (Sumulas 539 e 541 STJ).
- Busca e apreensao: purga e **integral** em 5 dias (Tema 722 STJ); nunca prometer devolucao do
  veiculo por abusividade de juros; adimplemento substancial nao se aplica a alienacao fiduciaria.
- Dano moral so com fraude, desconto em beneficio alimentar, negativacao ou assedio.
- Arquivos entram por link do Drive, nao colados inteiros no chat.
- `SAIDA/`, `DOCS_MODELOS/` e `config/.env` nunca sao versionados: contem dado de cliente e segredo.

## Calibracao pendente (o que falta o escritorio enviar)
1. Timbrado em .docx limpo (so cabecalho e rodape) e 1-2 pecas-modelo por tipo, protocoladas.
2. Modelo de contrato de honorarios, procuracao e declaracao de hipossuficiencia.
3. Corte de abusividade que a Dra. Caroline usa (razao taxa contratada / media BACEN) e valor
   usual de dano moral pedido.
4. Planilha de calculo atual do escritorio (a semi-automatizada em Excel), para conferir o
   `CALCULO/calculo_revisional.py` contra ela.
5. Chave do Asaas do escritorio e, se quiserem o relatorio de trafego, token da API do Meta.
