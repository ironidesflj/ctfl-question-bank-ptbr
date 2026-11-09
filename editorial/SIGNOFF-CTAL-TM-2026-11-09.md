# Sign-off editorial — CTAL-TM 1.7.2

- **Data:** 2026-11-09
- **Escopo:** pool de estudo do CTAL-TM (101 questões publicadas no hub via Axon).
- **Revisão aplicada:** 16 itens do relatório `REVISAO-CTAL-TM` (6 P1: 121, 151, 155, 173, 183, 189; 6 P2: 02, 65, 66, 124, 168, 182; 2 P3: 125, 185), já presentes no banco desde 1.7.1; referências passaram a incluir o LO (`TM-x.y.z`).
- **Gabaritos:** nenhum alterado (0 answers modificados; conferido por diff).
- **Evidência:** guardas de alinhamento passam para os certs live (CTFL, CTAL-TA, CTAL-TM); manifesto público inalterado (SHA `1bdcde8e…`, igual ao do hub); app sincronizado (fatias de estudo/exame) no PR #31 do ctfl-app.
- **Aprovação:** mantenedor aprovou a aplicação em 2026-11-09.
- **Pendências registradas:** (a) cobertura K4 do estudo — aguarda novo pacote de questões; (b) revisão semântica integral das 101 não foi feita (amostra de 14 + guardas); (c) guards de certs não-live (CT-AI, CTFL-AT) são LATENT — não bloqueiam CI por desenho (`check_alignment.py`, LIVE_CERTS).

## Adendo — 1.7.3 (revisão semântica integral)

- **Revisão semântica integral das 101 questões do estudo concluída em 09/nov**: 62 itens corrigidos (14 do relatório inicial + 48 da leitura integral das 87 restantes), PT e EN, sem alterar gabaritos nem reordenar alternativas (0 answers alterados).
- **K4:** `ctaltm-121` remapeada para `TM-1.3.4 (K4)`, suprindo a lacuna de K4 do pool de estudo.
- **LO corrigidos:** `ctaltm-164` (TM-2.2.2), `ctaltm-82` (TM-2.1.2), `ctaltm-100` (TM-3.2.1, K2).
- **Guardas (7/7 PASS)** no banco 200 e na fatia de estudo 101 (incluindo BLUEPRINT_MATCH com K2/K3/K4); `verify_axon_ids.py`: 431 IDs de estudo, nenhum de simulado.
- **Efeito no contrato:** conteúdo do manifesto muda (checksums) → exige reingestão no hub e nova publicação do app; nada de gabarito/ID mudou.
- **Pendência:** novo pacote de questões para ampliar K4 além da única amostra (aguardando o mantenedor).
- **Baselines de heurística atualizadas:** as correções mudaram textos de opções/explicações e geraram 13 suspeitas novas nas guardas heurísticas (opção/exp e tema). Foram revisadas no parecer semântico e aceitas como falsos positivos; as baselines `check_alignment_baseline` e `check_alignment_topic_baseline` foram atualizadas (`--update-baseline` / `--update-topic-baseline`). Heurística é alerta, não prova de bug — CI segue bloqueando apenas certs live e guardas psicométricas.

## Adendo — 1.7.4 (CTAL-TA: 2 questões inconclusivas reescritas)

- `ctalta-106` (TA-1.2.2, K2, estudo): enunciado pedia "dois artefatos" enquanto a correta listava três itens e o passo já continha o dado 1500. Reescrito para "elementos de baixo nível (concreto)" com opção B e `exp` alinhadas; gabarito mantido (answer=1).
- `ctalta-120` (TA-2.1.1, K2, simulado): exigia classificação "por matriz padrão" sem dar a regra, gerando ambiguidade PT/EN. Enunciado agora explicita a regra da matriz (probabilidade baixa × impacto muito alto = risco "alto"); `answer=3` mantido e removida a exceção na baseline de tema (passa nativamente).
- Guardas: 0 suspeitas novas (opção/exp e tema) e 7/7 psicométricas PASS nos certs live; unittest 16/16; 431 IDs de estudo validados, 0 de simulado.
- Efeito: conteúdo de manifesto muda para 2 registros (1 de estudo) → exige reingestão no hub e publicação do app.
