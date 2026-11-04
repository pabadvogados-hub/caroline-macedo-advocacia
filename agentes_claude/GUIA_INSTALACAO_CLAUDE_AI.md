# Guia - agentes Macedo no Claude.ai (nuvem)

A Dra. Caroline quer rodar na nuvem, sem prender a uma maquina. Um Project por frente.

1. Claude.ai > Projects > New project: "Macedo - Revisional", "Macedo - Busca e Apreensao", "Macedo - Contratacao", "Macedo - Controladoria".
2. Em Custom instructions cole `CLOUD_WEB_INSTRUCOES_CAROLINE.md` seguido do conteudo do agente (sem o bloco `---` do topo).
3. Project knowledge: timbrado, 1-2 pecas-modelo por tipo, modelos de contrato/procuracao/declaracao, planilha de calculo.
4. Teste com um caso real anonimizado; a saida deve terminar com "PRONTA PARA REVISAO".
5. Arquivos entram por link do Drive, nao colados inteiros.

Claude Code (opcional): copie os `.md` para `.claude/agents/`.
Calculo local: `python CALCULO/calculo_revisional.py --valor ... --parcela ... --prazo ... --taxa-media-mensal ...`
