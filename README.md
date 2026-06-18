# Banco de Questões — CTFL v4.0 (PT-BR + EN em progresso)

Banco de questões para preparação ao exame ISTQB CTFL v4.0.

## Estado atual
- 200 questões PT-BR
- 40 questões EN (Capítulo 1)
- Schema i18n-ready: `locales.pt` e `locales.en` por questão

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
- `build_bank.py` — gera e valida o JSON PT-BR
- `add_en.py` — injeta `locales.en` nas questões existentes por ID

## Como usar

```bash
python3 build_bank.py      # gera ctfl-questions-ptbr.json
python3 add_en.py          # injeta traduções EN
```

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
### v2.0.0
- Fix: rebalanceamento de posições (era 96% pos.1, agora 25%/25%/25%/25%)
- Fix: 399 distratores expandidos (133 questões K2/K3)
- feat: 40 questões EN — Capítulo 1

### v1.0.0
- 200 questões PT-BR, distribuição proporcional ao exame

## Aviso
Material independente, não afiliado ao ISTQB.
