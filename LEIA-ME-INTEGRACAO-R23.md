# LEIA-ME — Banco 1.7.0-rc1 (CTAL-TM editorial + trocas estruturais) · Rodada 23

**Data:** 2026-10-25 · **Origem:** execução completa das pendências da Fase A+B aqui no meu ambiente,
autorizada por você ("se tiver pendências, faça") após o relatório de vai-e-vem.

## O que é este pacote

O banco canônico **1.6.0-ctaltm** com as duas frentes aplicadas sobre as 200 questões do CTAL-TM:

1. **Editorial completo (Fase A)** — reescrita PT+EN dos distratores e explicações:
   - 1.265 opções reescritas (caricaturas → erros plausíveis de conteúdo);
   - ~430 tokens absolutistas removidos dos distratores ("apenas/only" 155×, "todos/all",
     "sempre/always", "nunca/never"...); "deve/must" normativo preservado onde natural;
   - corretas **intocadas em conteúdo** (compressão de verborragia ≤15% apenas);
   - enunciados **zero** alterados (PT e EN);
2. **Trocas estruturais (Fase B)** — as 14 trocas de índice do toolkit r20, re-simuladas
   contra o banco pós-editorial e aplicadas (ledger: `swap-ledger-r23.json`).

## Resultado das guardas (EVIDENCIA-GUARDAS-R23.txt — exit 0)

| Guarda | Antes (1.6.0) | Depois (1.7.0-rc1) |
|---|---|---|
| 10 length_bias (pick-longest) | PT 91,0% · EN 91,5% | **PT 22,5% · EN 22,5%** ✓ |
| 11 length_effect_size (Cohen's d) | PT 2,27 · EN 2,39 | **PT 0,05 · EN 0,02** ✓ |
| 12 hedge_ratio | PT 0,275 · EN 0,243 | **PT 0,78 · EN 0,61** ✓ |
| 14 runs_test (z / run máx) | −6,71 / 46 | **−3,02 / 5** ✓ |
| 13 chi² / 15 blueprint / 16 letter | passavam | **continuam passando** ✓ |
| Guards 0/1/2 (legados, baseline) | — | **0 suspeitas novas** ✓ |

Distribuição final de índices: [46, 51, 49, 54]. Integridade: 900 questões de
CTFL/CTAL-TA/CT-AI **byte-idênticas** ao canônico (nenhuma regressão possível nos certs verdes).

## Garantia de gabarito (o mais importante)

- Todos os 200 gabaritos **semânticos** auditados: a prática correta ORIGINAL está presente
  na posição do gabarito final — verificação automática por similaridade + **leitura manual
  das 19 divergências** que a auditoria apontou (17 reformulações legítimas, documentadas em
  `REVISAO-SUSPEITAS-R23.md`).
- **1 corrupção real foi encontrada e corrigida**: ctaltm-76 (lote 2 v1 havia invertido o
  gabarito — a própria Guarda 1 apontou; correta restaurada, distrator isolado na posição [1]).
- 14 trocas de índice = só posição, o conjunto de textos e o gabarito semântico preservados
  (validação embutida do applier + re-auditoria pós-troca).

## Como integrar (seu lado)

1. **Revisar por ID** (seu passo 1): `DIFF-RELATORIO-R23.json` lista, para cada uma das 200,
   opções alteradas (texto), comprimentos antes/depois, troca de índice e exp alterada.
2. **Commit no repo do banco**: substituir `synapse-question-bank.json` pelos deste pacote e
   os 3 arquivos `check_alignment_*baseline*.json` (a baseline opção/exp ganhou 19 ids
   revisados com justificativa — ver `REVISAO-SUSPEITAS-R23.md`).
3. **CI do banco deve passar** (as 4 guardas CTAL-TM estão verdes no meu ambiente, mesma
   suíte `check_alignment.py`, exit 0).
4. **Release 3.18.0 do app** (runbook completo no LEIA-ME-APLICACAO r2–r21): regenerar
   slices (split-bank) a partir deste monólito, `CERT_INDEX_EPOCHS['ctal-tm'] = 2` no
   **mesmo commit** (proteção de rascunhos v3.17.1 já em produção), 438 testes, build, E2E,
   bump 3.18.0 / banco 1.7.0.

## Arquivos do pacote

| Arquivo | Conteúdo |
|---|---|
| `synapse-question-bank.json` | o banco final (1.7.0-rc1) |
| `check_alignment.py` + 3 baselines | suíte de guardas (rodar: `python3 check_alignment.py synapse-question-bank.json`) |
| `EVIDENCIA-GUARDAS-R23.txt` | saída completa da suíte, exit 0 |
| `DIFF-RELATORIO-R23.json` | diff por ID para sua revisão |
| `REVISAO-SUSPEITAS-R23.md` | as 19 suspeitas lidas e justificadas + nota da 76 |
| `swap-ledger-r23.json` | ledger das 14 trocas |
