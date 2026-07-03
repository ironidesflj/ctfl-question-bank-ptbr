# Fase 4 — Ledger de Correções (Mega Commit Multi-Cert)

Aplicado sobre o zip `synapse-question-bank.json` (1100 questões, 5 certificações)
antes da integração ao repositório. Fonte: auditoria cega via GLM 5.2 (5 bancos,
132 achados) + verificação cruzada manual (amostragem + heurístico determinístico).

## Resumo
- 110 fixes mecânicos de índice `answer` (CTFL-AT: 1, CTAL-TA: 1, CT-AI: 35, CTAL-TM: 73)
- 1 fix de tradução (`ctaltm-167`: "redemoinho" → "redesenho", PT)
- 1 reescrita de conteúdo (`ctaltm-15`: questão defeituosa, opção correta conflava
  teste de componente com teste de integração — corrigido pra alinhar com o syllabus)
- 1 achado novo durante validação final (`agile-195`: gabarito apontava pra
  distrator "Security, Failure, Defects..." em vez da opção correta "Structure,
  Function, Data, Interfaces, Platform, Operations, Time", que bate com a EXP)

**Total: 113 correções nesta passada.**

## Não incluído nesta passada (deferido, não bloqueante)
~6 distratores de baixa qualidade em CTAL-TM (gabarito já correto, só texto do
distrator é fraco/absurdo: ctaltm-44, 53, 64, 78, 87, 189) — cosmético, não afeta
pontuação. Revisar em uma passada futura de polish.

## Lista completa de IDs corrigidos (answer → novo índice)
CTFL-AT: agile-116→2, agile-195→0

CTAL-TA: ctalta-38→1

CT-AI (35): aitest-04→2, aitest-05→2, aitest-15→2, aitest-18→2, aitest-26→1,
aitest-29→2, aitest-30→1, aitest-34→2, aitest-36→1, aitest-38→3, aitest-42→3,
aitest-54→2, aitest-56→2, aitest-57→0, aitest-63→2, aitest-64→3, aitest-68→2,
aitest-72→3, aitest-75→1, aitest-76→1, aitest-80→2, aitest-82→1, aitest-84→1,
aitest-91→2, aitest-95→2, aitest-99→3, aitest-125→0, aitest-140→1, aitest-148→1,
aitest-159→2, aitest-163→0, aitest-171→1, aitest-182→0, aitest-194→0, aitest-198→1

CTAL-TM (73 → índice 0): ctaltm-102, 103, 104, 106, 107, 108, 110, 111, 112, 114,
115, 116, 118, 119, 120, 122, 123, 124, 126, 127, 128, 130, 131, 132, 134, 135,
138, 139, 140, 142, 143, 144, 146, 147, 148, 150, 151, 152, 154, 155, 156, 158,
159, 160, 162, 163, 164, 166, 167, 168, 170, 171, 172, 174, 175, 176, 178, 179,
180, 182, 183, 184, 186, 187, 188, 190, 191, 192, 194, 195, 196, 199, 200

CTAL-TM (conteúdo): ctaltm-15 (reescrita), ctaltm-167 (tradução PT)

## Falsos positivos confirmados (não tocar)
ctaltm-22 (heurístico apontou, verificado manualmente: answer=1 já está correto)
ch2-01, ch1-50, ch2-37, ch5-59 (CTFL), aitest-129 (CT-AI) — heurístico de
sobreposição lexical EXP-vs-opção deu falso positivo porque a EXP discute
todas as 4 opções em detalhe; verificado manualmente, gabarito já correto.

## Estado de origem
- Bloco CTFL (300): 200 originais = estado de produção atual (commit `6e473e7`,
  já com os 14 fixes anteriores desta sessão) + 100 novas do zip, sem alteração
  (nenhum problema encontrado nelas em amostragem nem na auditoria cega).
- Blocos CTFL-AT / CTAL-TA / CTAL-TM / CT-AI (800): conteúdo original do zip
  com os 113 fixes acima aplicados.

## Passada de verificação pós-Fase-4 (achados novos, fora dos 113)
Fonte: verificação cruzada em sessão de handoff (a explicação contradizia o
gabarito nas duas). Não apareciam na auditoria cega dos 132 achados.
CT-AI (2): aitest-13→2, aitest-22→1

## Auditoria P2.1 (418 suspeitas do banco multi-cert, pós-P2)
Metodologia: heurística (check_alignment.py, 2 guardas) → auditoria às cegas
por guarda (GLM em guarda_tema, Claude Code em guarda_opcao_exp — votação por
5 papéis) → verificação cruzada manual contra o dado bruto.
418 suspeitas processadas: 415 falso-positivo, 2 inconclusivo (não corrigidos,
ficam visíveis para revisão futura), 1 bug real.
CTAL-TM (1): ctaltm-136→0 (contradição direta com a explicação, SMART Time-bound;
confirmado FALSO_POSITIVO na guarda de tema — tradução correta, só o índice errado)
Inconclusivos não corrigidos, excluídos da baseline de propósito:
ctalta-106 (guarda_opcao_exp — falha de redação no enunciado, sem alternativa
defensável); ctalta-120 (guarda_tema — ambiguidade de matriz de risco)
