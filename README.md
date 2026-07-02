# Synapse — Banco de Questões Multi-Certificação ISTQB (PT-BR + EN)

Banco de questões bilíngue para preparação a certificações ISTQB. Dois arquivos:
- `ctfl-questions-ptbr.json` — só CTFL v4.0 (300 questões), consumido pelo [`ctfl-app`](https://github.com/ironidesflj/ctfl-app)
- `synapse-question-bank.json` — todas as 5 certificações (1100 questões)

## Estado atual
- Total do projeto (5 certificações): 1.100 questões bilíngues (`locales.pt` + `locales.en`)
- CTFL (300) e CTFL-AT (200) já publicadas = 500 questões publicadas
- As outras três certificações (CTAL-TA, CTAL-TM, CT-AI) somam 600 questões (200 cada), geradas e no repositório, aguardando lançamento na Fase 5
- Schema i18n-ready: `locales.pt` e `locales.en` em todas as questões

## Formato do exame (CTFL v4.0)
| Item | Valor |
|------|-------|
| Questões | 40 |
| Nota de corte | 26/40 (65%) |
| Tempo | 60 min (75 min não-nativos) |

## Distribuição — CTFL v4.0 (300 questões)
| Cap. | Domínio | Questões |
|------|---------|----------|
| 1 | Fundamentos | 60 |
| 2 | Teste no Ciclo | 38 |
| 3 | Teste Estático | 38 |
| 4 | Técnicas de Teste | 82 |
| 5 | Gerenciamento | 67 |
| 6 | Ferramentas | 15 |
| | **Total** | **300** |

K-levels: K1=78 (26%), K2=180 (60%), K3=42 (14%)

## Distribuição — outras certificações (`synapse-question-bank.json`)
| Cert | Questões | Syllabus |
|------|----------|----------|
| CTFL-AT | 200 | Agile Tester Extension v2014 |
| CTAL-TA | 200 | Advanced Level Test Analyst v4.0 |
| CTAL-TM | 200 | Advanced Level Test Manager v3.0 |
| CT-AI | 200 | Certified Tester AI Testing v2.0 |

## Scripts
- `build_bank.py` — gera e valida **só o bloco legado CTFL/200** a partir de `add()` no próprio script (⚠️ apaga `locales.en` se rodado sozinho — sempre seguido de `add_en.py`). **Não gera as 100 questões novas nem o multi-cert** — desde a Fase 4, `ctfl-questions-ptbr.json` (300) e `synapse-question-bank.json` (1100) são editados/gerados fora deste pipeline e versionados diretamente. Migração de `build_bank.py` para uma fonte única (YAML) que cubra os 1100 é item pendente, ainda não construído.
- `add_en.py` — injeta `locales.en` nas questões existentes por ID (nunca sobrescreve EN já existente); cobre só o bloco legado de 200, mesma limitação acima.
- `check_alignment.py` — duas guardas de alinhamento PT/EN (rodadas no CI a cada push, sobre `ctfl-questions-ptbr.json`): (1) verifica se a opção correta tem maior similaridade à explicação EN do que as outras — guarda histórica com baseline em `check_alignment_baseline.json`; (2) verifica desalinhamento de **tema** comparando `pt.q` com `en.q` via z-score adaptativo (limiar = média − 1,5 × desvio da distribuição do banco) — baseline em `check_alignment_topic_baseline.json`. Sinaliza candidatos a revisão manual; nunca corrige nada automaticamente. As 100 questões novas da Fase 4 ainda não têm baseline própria — rodar com `--update-baseline --update-topic-baseline` após revisão manual dos alertas é trabalho pendente.

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

Push em `ctfl-questions-ptbr.json` na branch `main` deste repositório dispara a GitHub
Action `sync-app.yml`, que abre automaticamente um Pull Request no repositório
[`ctfl-app`](https://github.com/ironidesflj/ctfl-app) atualizando
`src/data/ctfl-questions-ptbr.json`. Não copie o arquivo manualmente — revise e faça o
merge do PR gerado. Requer o secret `CTFL_APP_SYNC_TOKEN` configurado neste repositório
(token fine-grained com escrita em `ctfl-app`).

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

## Aviso
Material independente, não afiliado ao ISTQB.
