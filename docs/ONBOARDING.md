# Onboarding - Caroline Macedo Advocacia

Roteiro da implantacao: prevista em ate 7 dias, com acompanhamento de 90 dias.
(Condicoes comerciais ficam no contrato, nao neste repositorio.)

## O que o escritorio precisa entregar
| Item | Para que | Status |
|---|---|---|
| Timbrado .docx limpo (so cabecalho/rodape) | skill de formatacao das pecas | pendente |
| 1-2 pecas-modelo por tipo (revisional, contestacao em busca e apreensao, RMC) | calibrar o DNA de escrita | pendente |
| Modelos de contrato de honorarios, procuracao e declaracao | `macedo-contratacao` | pendente |
| Planilha de calculo atual (Excel semi-automatizada) | conferir o `CALCULO/calculo_revisional.py` | pendente |
| Chave da API do Asaas do escritorio | link da entrada | pendente |
| Token da API do Meta + ID da conta de anuncios | relatorio diario de trafego (bonificacao do contrato) | pendente |
| Corte de abusividade (razao contratada/media) e valor usual de dano moral | parametro dos pareceres | pendente |

## Reunioes de implantacao
1. **Plugar** - Asaas, Drive, Projects no Claude.ai, equipe com acesso. Rodar o link da entrada
   e o dossie com um caso real na frente deles.
2. **Calibrar** - subir timbrado e pecas-modelo; ajustar os agentes ao jeito de escrever do
   escritorio; conferir o calculo contra a planilha deles.
3. **Treinar** - Luysa, Vinicius, Gustavo e Ana Beatriz. Cada um sai sabendo rodar o que e dele.

## Como a equipe usa no dia a dia
- **Comercial (Vinicius, Gustavo, Ana Beatriz):** fecha -> `ENTRADA/gerar_entrada.py` gera o link
  e a mensagem -> envia -> preenche o JSON do caso -> `HANDOFF/passagem_bastao.py` -> manda o
  dossie para a Luysa. Fim do "espera o financeiro emitir".
- **Juridico (Luysa):** le o dossie, decide a via com a Dra. Caroline, aciona o agente da area,
  passa o resultado pelo `macedo-controladoria` e revisa. Nada sai sem ela.
- **Dra. Caroline:** palavra final em estrategia, tese, valores e protocolo.

## Limites ditos com clareza
- **Astrea nao tem API.** Lancamento de caso, tarefa e prazo continua manual; a automacao prepara
  o texto e lembra, nao lanca.
- A I.A. nao consulta o processo no PJe nem no sistema do banco sozinha: os documentos entram por
  link do Drive.
- A taxa media do BACEN e informada por quem roda o calculo, com mes e fonte. O sistema nao
  adivinha media de mercado.
