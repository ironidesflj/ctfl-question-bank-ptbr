# Synapse — Banco de Questões Multi-Certificação ISTQB (PT-BR + EN)

Banco de questões bilíngue para preparação a certificações ISTQB. Dois arquivos:
- `ctfl-questions-ptbr.json` — só CTFL v4.0 (300 questões), consumido pelo [`ctfl-app`](https://github.com/ironidesflj/ctfl-app)
- `synapse-question-bank.json` — todas as 5 certificações (1100 questões)

## IDs públicas Axon (em preparação)

`axon/ctfl-public-ids.json` reserva as primeiras 50 IDs `SYN-CTFL-*` para
questões CTFL do pool de estudo, em PT-BR. O registro liga cada ID pública à
ID interna existente; não altera o banco nem as chaves de progresso dos alunos.
`python3 verify_axon_ids.py` verifica sequência, unicidade e exclusão do pool
de simulado. No CI, `--against-parent` também impede remapear IDs já
reservadas. Este repositório ainda não publica snapshots ou manifesto;
referências por questão e revisão editorial são gates antes dessa etapa.
O rascunho das 50 referências e as dúvidas por item estão em
`editorial/axon-ctfl-reference-review.md`; nenhuma referência desse rascunho
foi aprovada para manifesto.

## Estado atual

**Release candidata:** 1.7.0-rc1, integrada ao app Synapse 3.18.0.
O CTAL-TM recebeu revisão editorial e 14 trocas estruturais auditadas, sem
alterar CTFL, CTAL-TA, CT-AI ou CTFL-AT.

As guardas bloqueantes do CTAL-TM PT/EN passam na release candidata
(comprimento, efeito de comprimento, qualificadores e runs test). CT-AI e
CTFL-AT continuam latentes e não bloqueiam o conteúdo publicado.

Proteção de sync: `verify_sync.py` rejeita downgrade e compara os dois bancos
e as fatias completas. `test_sync_protection.py` cobre as falhas que o sync
deve bloquear. O workflow valida qualidade antes de copiar/abrir PR, regenera
fatias e não usa auto-merge. Conteúdo diferente na mesma versão exige bump
na fonte. Verificações novas não estão ativas no GitHub até o envio autorizado.
O projeto evoluiu para o **Synapse**, englobando múltiplas certificações (total de 1.100 questões).

**Conteúdo no Ar (Lançado):**
- **CTFL v4.0:** 300 questões
- **CTAL-TA v4.0:** 200 itens
- **CTAL-TM v3.0:** 200 itens (release candidata 1.7.0-rc1; guardas live verdes)

**Roadmap de Lançamentos Futuros (Em Breve):**
- **CT-AI v2.0:** 200 itens (em breve)
- **CTAL-AT v2.0:** 200 itens (em breve - syllabus totalmente novo, a ser gerado)

**Conteúdo Legado:**
- **CTFL-AT (Agile Tester v2014):** 200 itens (adormecido/sunset pela ISTQB, substituído pelo CTAL-AT v2.0. O conteúdo é mantido por razões de arquivo e não está listado nos próximos lançamentos da UI).
- Schema i18n-ready: `locales.pt` e `locales.en` em todas as questões

## Formato do exame (CTFL v4.0)
| Item | Valor |
|------|-------|
| Questões | 40 |
| Nota de corte | 26/40 (65%) |
| Tempo | 60 min (75 min não-nativos) |

## Distribuição — CTFL v4.0 (300 questões no banco)
| Cap. | Domínio | Questões |
|------|---------|----------|
| 1 | Fundamentos | 60 |
| 2 | Teste no Ciclo | 38 |
| 3 | Teste Estático | 38 |
| 4 | Técnicas de Teste | 82 |
| 5 | Gerenciamento | 67 |
| 6 | Ferramentas | 15 |
| | **Total** | **300** |

Distribuição do **simulado** (proporcional à prova oficial, 40 questões):
1=8, 2=6, 3=4, 4=11, 5=9, 6=2 (fonte: ISTQB Exam Structures & Rules
tables v1.18). Corrigido nesta versão — `chapterWeights` gerava 8/5/5/11/9/2
antes do fix.

K-levels: K1=78 (26%), K2=180 (60%), K3=42 (14%)

## Formato do exame (CTAL-TA v4.0)
| Item | Valor |
|------|-------|
| Questões | 45 |
| Nota de corte | 29/45 (65%, 1 questão = 1 ponto) |
| Tempo | 120 min (150 min não-nativos) |

Nota: o exame oficial ISTQB pondera pontos por K-level (78 pontos, corte
51/78). O app pontua 1 questão = 1 ponto, sem peso por K-level — `passMark`
aqui reflete o modelo do app (`round(0.65*45)`), não o blueprint oficial de
pontos. Distribuição por capítulo segue a contagem oficial de questões
(Exam Structure Tables v1.18): cap.1=8, cap.2=3, cap.3=22, cap.4=4, cap.5=8.

`meta.chapterWeights`/`meta.examFormat` (v1.2.0) trazem esses números
prontos pro app, chaveados por `cert.id` (`ctfl`, `ctal-ta`).

## Distribuição — outras certificações (`synapse-question-bank.json`)
| Cert | Questões | Syllabus | Status |
|------|----------|----------|--------|
| CTAL-TA | 200 | Advanced Level Test Analyst v4.0 | **No ar** |
| CTAL-TM | 200 | Advanced Level Test Manager v3.0 | Release candidata; guardas live verdes |
| CT-AI | 200 | Certified Tester AI Testing v2.0 | Em breve |
| CTFL-AT | 200 | Agile Tester Extension v2014 | Legado / Adormecido |

## Scripts
- `build_bank.py` — gera e valida **só o bloco legado CTFL/300** a partir de `add()` no próprio script (⚠️ apaga `locales.en` se rodado sozinho — sempre seguido de `add_en.py`). **Não gera as questões novas do multi-cert** — desde a Fase 4, `ctfl-questions-ptbr.json` (300) e `synapse-question-bank.json` (1100) são editados/gerados fora deste pipeline e versionados diretamente. Migração de `build_bank.py` para uma fonte única (YAML) que cubra os 1100 é item pendente, ainda não construído.
- `add_en.py` — injeta `locales.en` nas questões existentes por ID (nunca sobrescreve EN já existente); cobre só o bloco legado de 300, mesma limitação acima.
- `check_alignment.py` — guardas estruturais, de alinhamento PT/EN e psicométricas
  (10–16), executadas no CI nos dois bancos. Suspeitas confirmadas como falso
  positivo ficam em baselines específicas; os dois casos inconclusivos
  (`ctalta-106` na guarda opção/exp e `ctalta-120` na guarda de tema) ficam fora
  das baselines e numa allowlist explícita por arquivo/guarda. Qualquer outro ID
  novo falha o CI (`threshold 0`). A ferramenta nunca corrige conteúdo
  automaticamente.

## Como usar

```bash
python3 build_all.py    # gera + injeta EN + valida alinhamento, em um passo
```

**Uso avançado / scripts individuais** (rodar `build_bank.py` isolado apaga `locales.en` — só use se souber o que está fazendo):

```bash
python3 build_bank.py        # gera ctfl-questions-ptbr.json (sem EN)
python3 add_en.py            # injeta traduções EN
python3 check_alignment.py   # verifica alinhamento PT/EN (heurística, não corrige nada)
```

**Ao expandir o banco** (novas questões/capítulos): depois de escrever o PT em `build_bank.py` e o EN em `add_en.py`, rode `check_alignment.py` antes de comitar. Se aparecerem suspeitas novas, leia PT e EN par a par para cada id sinalizado — não confie no índice "sugerido" pela heurística sem confirmar manualmente (ela já errou a sugestão em vários casos confirmados nesta sessão).

## Sincronização com ctfl-app

Push em `ctfl-questions-ptbr.json` ou `synapse-question-bank.json` na branch `main`
dispara a GitHub Action `sync-app.yml`. Ela detecta qual arquivo mudou, copia somente
os correspondentes para `ctfl-app/src/data/`, confere checksums e abre um Pull Request
no [`ctfl-app`](https://github.com/ironidesflj/ctfl-app). O merge é manual. Requer o
secret `CTFL_APP_SYNC_TOKEN` (token fine-grained com escrita em `ctfl-app`).

## Schema

```jsonc
{
  "id": "ch1-01",
  "chapter": 1,
  "domain": "fund",
  "kLevel": 1,
  "answer": 1,
  "locales": {
    "pt": { "q": "...", "options": [...], "exp": "..." },
    "en": { "q": "...", "options": [...], "exp": "..." }
  }
}
```

## Changelog

### synapse v1.5.0-pools / app v3.12.0 — 2026-10-14

- feat: partição determinística e reprodutível em pools exclusivos de estudo e
  simulado (`partition_pools.py`, seed fixa): CTFL 220+80; CTAL-TA 110+90.
- fix: metadados oficiais do CTAL-TA usam pontos ponderados por K-level
  (K2=1, K3=2, K4=3), total 78 e corte 51; CTFL mantém 26/40.
- docs: tempo nativo de prova no Brasil registrado como CTFL 60 min e CTAL-TA
  120 min; os 25% adicionais dependem da condição/solicitação aplicável.
- quality: conteúdo e índices das 1.100 questões permanecem inalterados; as
  guardas existentes continuam com `threshold 0` e allowlist explícita.

### synapse v1.4.0-e2e-round2 (QA r2 — 2026-10-14)

- fix: CTAL-TM rebalanceado de 124/26/25/25 para 50/50/50/50 posições de
  gabarito, preservando PT/EN e a ordem relativa dos distratores.
- fix: 98 reescritas auditadas de referência por letra, 110 correções de
  índice e cerca de 30 explicações adicionais reescritas por tema/snippet.
- quality: `aitest-177` revisada manualmente e registrada como falso positivo
  da heurística opção/exp: a resposta `40 / (40 + 10) = 0,80` aplica
  corretamente `precision = TP / (TP + FP)`.
- tooling: transformações reprodutíveis em `round2_bank_fixes.py` e
  `round2_bank_fixes_p2.py`; CI continua em `threshold 0`, com inconclusivos
  fora das baselines e em allowlist explícita.

### synapse v1.2.0 (P3 — multi-cert de verdade no app)
- feat: `meta.chapterWeights`/`meta.examFormat` adicionados ao
  `synapse-question-bank.json`, chaveados por `cert.id` (`ctfl`, `ctal-ta`).
  Sem isso o app quebrava (`TypeError`) ao montar o simulado multi-cert —
  o refactor `getBank()` do app já lia esse formato, só faltava o dado.
- fix: `passMark` do CTAL-TA calculado como `round(0.65*questions)` (29),
  não o 51/78 pontos ponderados do blueprint oficial ISTQB — o app pontua
  1 questão = 1 ponto, sem peso por K-level.
- nota histórica: o sync inicialmente cobria apenas o arquivo legado; hoje
  `sync-app.yml` cobre também `synapse-question-bank.json` e valida checksums.

### v4.0.0 / synapse v1.1.0 (Fase 4 — multi-certificação)
- feat: expansão multi-certificação ISTQB. `synapse-question-bank.json` (novo
  arquivo, 1100 questões): CTFL (300) + 4 certificações novas — CTFL-AT (200),
  CTAL-TA (200), CTAL-TM (200), CT-AI (200).
- feat: CTFL 200 → 300 questões (`ctfl-questions-ptbr.json`, capítulo 1
  expandido); as 200 originais preservadas intactas (validado byte-a-byte
  contra a v2.3.0).
- fix: 113 correções aplicadas às 800 questões novas das 4 certificações após
  auditoria cega (GLM 5.2, 5 bancos, 132 achados) + verificação cruzada manual
  — detalhamento completo em `FASE4_FIX_LEDGER.md`.
- fix: 9 questões com distratores EN conceitualmente divergentes do PT
  corrigidas antes da expansão (ch3-16, ch4-22, ch5-03, ch5-13, ch5-22,
  ch5-24, ch5-26, ch5-29, ch5-31).
- débito conhecido: `build_bank.py`/`add_en.py` ainda só cobrem o bloco legado
  de 200 questões CTFL — não geram as 100 novas nem o multi-cert (ver seção
  Scripts). As 100 questões novas do CTFL ainda não têm baseline própria em
  `check_alignment.py`.

### v2.3.0
- fix: corrige 87 questões com índice de resposta EN incorreto (bug de
  ordenação anterior ao desalinhamento de tema da v2.2.0). Nestas, o
  tema da pergunta EN já estava certo, mas a ordem das opções EN não
  espelhava a ordem PT (que tinha sido rebalanceada na v2.0.0 antes do
  EN existir) — então `answer` apontava para a opção errada em inglês.
  Afeta Cap.1 (21/24 originais), Cap.2 (10/15), Cap.4 (29/33, incl. o
  par ch4-11/ch4-12 que tinha o bloco EN inteiro trocado entre si) e a
  totalidade do Cap.5 original (27/27).
- feat: `check_alignment.py` — heurística permanente de verificação
  PT/EN, com baseline de falsos positivos conhecidos
  (`check_alignment_baseline.json`) e workflow de CI
  (`.github/workflows/check-alignment.yml`) que falha o build se
  aparecerem suspeitas NOVAS de desalinhamento em qualquer expansão
  futura do banco. Não corrige nada automaticamente — só alerta para
  revisão manual.

### v2.2.0
- fix: corrige desalinhamento PT/EN em 77 questões (38% do banco). A
  v2.1.0 criou o EN diretamente do syllabus oficial em vez de traduzir o
  PT existente; isso fez com que, em todos os 6 capítulos, as questões do
  bloco de expansão (120→200) ficassem com EN tratando de um tópico
  diferente do PT, embora compartilhando o mesmo `answer` index. Reescrito
  com tradução fiel do PT real para as 77 questões afetadas
  (ch1-25..40, ch2-16..25, ch3-18..25, ch4-34..55, ch5-28..45, ch6-07..09).

### v2.1.0
- Banco EN completo: Capítulos 2, 3, 4, 5 e 6 adicionados via add_en.py
  (Capítulo 1 já estava feito na v2.0.0)
- Total: 200/200 questões com locales.en
- Questões EN criadas diretamente do syllabus oficial em inglês, não traduzidas
  do PT-BR, para maior fidelidade terminológica

### v2.0.0
- Fix: rebalanceamento de posições (era 96% pos.1, agora 25%/25%/25%/25%)
- Fix: 399 distratores expandidos (133 questões K2/K3)
- feat: 40 questões EN — Capítulo 1

### v1.0.0
- 200 questões PT-BR, distribuição proporcional ao exame

## Guardas de qualidade

Qualquer alteração de conteúdo deve manter:

- as sete guardas do `check_alignment.py` verdes nos dois bancos;
- `threshold 0` no CI, sem absorver inconclusivos em baselines;
- zero referência nova a opção/alternativa A–D nas explicações;
- PT e EN alinhados em tema, opções e índice de resposta;
- certificações live abaixo dos limites psicométricos bloqueantes.

Execute antes de abrir PR:

```bash
python3 check_alignment.py --bank-file ctfl-questions-ptbr.json --threshold 0
python3 check_alignment.py --bank-file synapse-question-bank.json --threshold 0
```

## Aviso
Material independente, não afiliado ao ISTQB.
