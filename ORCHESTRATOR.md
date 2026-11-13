# Orquestrador de Questões (`orchestrate_bank.py`)

Pipeline determinístico (stdlib-only, custo zero de tokens) para analisar, validar e aplicar novos lotes de questões ou rodadas de manutenção no repositório canônico `ctfl-question-bank-ptbr`.

## Princípio de economia máxima de tokens

- Toda validação estrutural, anti-leak, duplicidade por Jaccard, alinhamento PT/EN, métricas psicométricas (`check_alignment.py`) e IDs Axon (`verify_axon_ids.py`) roda localmente em Python.
- A saída padrão imprime apenas um resumo compacto (contagens por rodada/certificação, status das guardas e até 10 falhas), evitando despejar os bancos inteiros no contexto de agentes.
- Use `--report relatorio.json` quando precisar inspecionar apenas os itens sinalizados.

## Comandos

### 1. Analisar (sem alterar arquivos)
Aceita arquivos `.json`, `.zip`, pastas extraídas ou um `--manifest` ordenado:

```bash
python3 orchestrate_bank.py analyze caminho/lote.zip --report /tmp/analyze.json
python3 orchestrate_bank.py analyze --manifest caminho/manifest.json
```

### 2. Validar (gate estrito / CI)
Retorna `exit 0` apenas se zero falhas estruturais/editoriais e todas as guardas do repositório (`check_alignment.py --threshold 0` em ambos os bancos + `verify_axon_ids.py`) passarem em sandbox isolada:

```bash
python3 orchestrate_bank.py validate caminho/lote.zip
```

### 3. Aplicar (fail-closed + backup automático)
Só grava em disco após aprovação completa em sandbox temporária. Cria backup antes de escrever em `.cache/orchestrator-backups/` (ignorado pelo git), atualiza `synapse-question-bank.json`, `ctfl-questions-ptbr.json` e as baselines auditadas, e reexecuta a suíte pós-aplicação (`unittest`, `verify_axon_ids.py`, `check_alignment.py`):

```bash
python3 orchestrate_bank.py apply --manifest caminho/manifest.json --version 1.8.0
python3 orchestrate_bank.py apply caminho/lote.zip --dry-run
```

## Formato de `--manifest`

```json
{
  "simulate_promote_live": ["CT-AI"],
  "ctfl_target_version": "1.5.0",
  "steps": [
    {
      "name": "r24",
      "mode": "add",
      "questions": "/caminho/synapse-new-questions-r24.json",
      "g1_additions": "/caminho/baseline-r24-guarda1-additions.json",
      "g2_additions": "/caminho/baseline-r24-guarda2-additions.json"
    },
    {
      "name": "m1",
      "mode": "replace",
      "questions": "/caminho/synapse-requalified-questions-m1.json",
      "g1_additions": "/caminho/check_alignment_baseline.synapse-question-bank.json",
      "g1_filter_prefix": "aitest-",
      "meta_cert_patches": {
        "CT-AI": { "kLevels": ["K1", "K2", "K3"] }
      }
    },
    {
      "name": "pool-rebalance",
      "mode": "pool_swap",
      "pool_swaps": [["ch1-96", "ch1-76"]],
      "ctfl_target_version": "1.5.1"
    }
  ]
}
```

- Também suporta `mode: "pool_swap"` (troca de `pool` entre questões na mesma célula `cert` × `chapter` × `kLevel`, sincronizando `ctfl-questions-ptbr.json` e recalculando automaticamente `meta.poolSplit.perCert`).
