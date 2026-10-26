# Revisão manual das suspeitas NOVAS da Guarda 1 (opção/exp) — Rodada 23

Data: 2026-10-25 · Contexto: reescrita editorial CTAL-TM 1.7.0-rc1

19 suspeitas novas revisadas par a par (EN exp vs opções). Todas BENIGNAS:
a explicação justifica a correta e refuta os distratores, gerando overlap
lexical que a heurística SequenceMatcher detecta — padrão de falso-positivo
conhecido documentado no cabeçalho do check_alignment.py.

Uma corrupção REAL foi encontrada e CORRIGIDA antes desta revisão:
ctaltm-76 tinha o gabarito invertido pela v1 do lote 2 (a própria guarda
apontou; correta restaurada na posição [3], distrator isolado para [1]).

| ID | Justificativa da benignidade |
|---|---|
| aitest-177 | FALSO POSITIVO documentado na r21: exp cita as 4 opções verbatim para classificá-las (recall/acurácia/especificidade); precisão 40/50=0,80 é a resposta B |
| ctaltm-10 | exp define a matriz de stakeholders citando expertise/risk management — distrator reescrito deriva do mesmo vocabulário |
| ctaltm-111 | exp pede adaptação + coordenação de integração; distrator [1] propõe padronização — mesmo domínio de gerência híbrida |
| ctaltm-113 | exp descreve V-model; distrator [1] descreve o oposto ágil com o mesmo vocabulário de planejamento |
| ctaltm-125 | exp confirma multiplicação likelihood×impacto como método comum; distrator [2] descreve o mesmo método com erro adicional (thresholds padronizados) |
| ctaltm-130 | exp justifica técnica leve pelo contexto; distrator [1] escolhe a mesma técnica por razão errada (invenção de exigência do syllabus) |
| ctaltm-132 | exp lista abordagens típicas; distrator [2] nega a aplicabilidade da mesma abordagem analítica |
| ctaltm-15 | exp distingue os níveis de teste; distrator [3] menciona os mesmos níveis ao propor tratá-los como intercambiáveis |
| ctaltm-157 | exp define métrica de progresso; distrator [2] (satisfação com ferramentas) compartilha estrutura de frase |
| ctaltm-164 | exp lista fatores de estimativa; distrator [2] (calendário de férias de vendas) cita sizing/effort — derivado do lote com exemplo do próprio contrato |
| ctaltm-167 | exp explica instabilidade→esforço maior; distrator [3] propõe o inverso sobre o mesmo fator |
| ctaltm-28 | exp cita depth-first→breadth-first (texto do syllabus); distrator [0] discute a mesma estratégia errada |
| ctaltm-34 | exp exige abordagem rigorosa p/ contexto farmacêutico; distrator [2] propõe versão documental do mesmo contexto |
| ctaltm-50 | exp define ROI/TCO; distrator [2] (reputação de mercado) estrutura de lista similar |
| ctaltm-59 | exp lista ações de controle (causa raiz, replanejamento...); distrator [3] reatribuição é pseudo-ação do mesmo domínio |
| ctaltm-61 | distrator [1] é variação errada deliberada da correta (resumo executivo p/ ambos + Q&A) — vocabulário compartilhado por desenho |
| ctaltm-79 | exp explica phase containment; distrator [3] propõe arquivar as mesmas estatísticas |
| ctaltm-84 | exp classifica competências Professional/Methodological; distrator [2] usa a mesma taxonomia com conclusão errada |
| ctaltm-93 | exp lista motivadores E fatores de higiene (Herzberg) — overlap inevitável com distrator [0] (remuneração) |
