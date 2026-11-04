# Caroline Macedo Advocacia - automacoes

Ecossistema de I.A. do escritorio **Caroline Macedo Sociedade Individual de Advocacia**
(Maceio/AL, filial Sorocaba/SP) - direito bancario na defesa do consumidor.

**Regra de ouro: a I.A. nunca define estrategia e nunca protocola.** Tudo para para revisao da
coordenadora juridica (Luysa) e da Dra. Caroline.

## Comecar

```bash
pip install -r requirements.txt
cp config/.env.example config/.env     # preencher a chave do Asaas
```

| O que | Comando |
|---|---|
| Link da entrada de honorarios | `python ENTRADA/gerar_entrada.py --cliente "Nome" --valor 1500 --acao revisional` |
| Dossie do caso (comercial -> juridico) | `python HANDOFF/passagem_bastao.py --interativo` |
| Calculo da revisao | `python CALCULO/calculo_revisional.py --valor 50000 --parcela 1850 --prazo 48 --taxa-media-mensal 2.15` |
| Relatorio do Meta Ads | `python MARKETING/relatorio_meta.py --dias 7` (ou `--exemplo`) |
| Testar sem tocar no Asaas | acrescentar `--dry-run` ao `gerar_entrada.py` |

Agentes juridicos para o Claude.ai: `agentes_claude/` (comece pelo `GUIA_INSTALACAO_CLAUDE_AI.md`).

## Estrutura

```
CALCULO/        calculo da revisao (Price x taxa media BACEN) + testes
ENTRADA/        link de pagamento da entrada, sem passar pelo financeiro
HANDOFF/        passagem de bastao do comercial para o juridico
MARKETING/      relatorio do Meta Ads (gasto, leads, custo por lead)
INTEGRACOES/    API Asaas e Meta Marketing API (somente leitura)
agentes_claude/ agentes juridicos (Claude.ai Projects / Claude Code)
.claude/        os mesmos agentes como subagentes do Claude Code
config/         dados do escritorio, formatacao e .env (nao versionado)
DOCS_MODELOS/   timbrado e pecas-modelo do escritorio (nao versionado)
SAIDA/          dossies, registros e pecas geradas (nao versionado)
docs/           plano do projeto e onboarding
```

Contexto completo em [CLAUDE.md](CLAUDE.md).

---
Implantacao: Casal da IA.
