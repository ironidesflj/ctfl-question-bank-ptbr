# Banco de Questões — CTFL v4.0 (PT-BR + EN em progresso)

Banco de questões para preparação ao exame ISTQB CTFL v4.0.

## Estado atual
- 200 questões PT-BR
- 200 questões EN (banco 100% bilíngue, todos os 6 capítulos)
- Schema i18n-ready: `locales.pt` e `locales.en` em todas as questões

## Formato do exame
| Item | Valor |
|------|-------|
| Questões | 40 |
| Nota de corte | 26/40 (65%) |
| Tempo | 60 min (75 min não-nativos) |

## Distribuição
| Cap. | Domínio | Questões |
|------|---------|----------|
| 1 | Fundamentos | 40 |
| 2 | Teste no Ciclo | 25 |
| 3 | Teste Estático | 25 |
| 4 | Técnicas de Teste | 55 |
| 5 | Gerenciamento | 45 |
| 6 | Ferramentas | 10 |
| | **Total** | **200** |

K-levels: K1=~28%, K2=~58%, K3=~14%

## Scripts
- `build_bank.py` — gera e valida o JSON PT-BR (⚠️ apaga `locales.en` se rodado sozinho — sempre seguido de `add_en.py`)
- `add_en.py` — injeta `locales.en` nas questões existentes por ID (nunca sobrescreve EN já existente)
- `check_alignment.py` — heurística de verificação permanente de alinhamento PT/EN (rodada no CI a cada push). Sinaliza candidatos a revisão manual; nunca corrige nada automaticamente. Veja a docstring do arquivo para detalhes sobre a baseline de falsos positivos conhecidos.

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
