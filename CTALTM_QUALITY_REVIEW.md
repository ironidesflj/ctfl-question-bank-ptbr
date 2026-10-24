# Revisão CTAL TM e proteção da sincronização

Data: 2026-10-24. Estado: proteção técnica implementada localmente;
revisão editorial integral NÃO CONCLUÍDA. Não pronto para publicação.

## Primeiro lote editorial aplicado localmente

Candidato do banco: **1.6.1-editorial.1**; app continua **3.17.0**, sem push.
Leitura inicial de ctaltm-01 a ctaltm-12, com referência nas seções 1.1 e
1.2 do syllabus oficial v3.0. Oito questões receberam alternativas PT/EN
reformuladas: 02, 03, 04, 07, 08, 10, 11 e 12. A explicação da 02 foi
atualizada para acompanhar as alternativas. 01, 05, 06 e 09 ficaram intactas.

Registro reproduzível: `editorial/ctaltm-batch-01.json`; aplicação por
`python3 apply_editorial_batch.py editorial/ctaltm-batch-01.json`.
O teste `test_editorial_batch.py` protege campos de identidade, gabaritos,
pool, questões não selecionadas, ausência de mutação e idempotência.
Revisão independente do lote ainda pendente; 188 questões não receberam
revisão semântica nesta fase. A leitura de 12 questões não encerra o acervo.

Referência: https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTAL-TM_Syllabus_v3.0_zKjKsaN.pdf

Resultado do candidato: zero suspeitas NOVAS de alinhamento; quatro guardas
psicométricas ainda falham. Pick-longest caiu para 87,0% PT e 88,5% EN,
mas isso não representa aprovação do conteúdo. Sem permutação de índices,
mudança de gabaritos, alteração de threshold, baseline ou allowlist.

Fonte/app e fatias do candidato são idênticos. As evidências e o hash
da reconciliação original abaixo se referem à v1.6.0, antes deste lote.

## Reconciliação comprovada

Origem da entrega: app a5f664f, banco embarcado v1.6.0-ctaltm.
Base anterior da fonte: 32e6e7e, v1.5.0-pools.
O monólito canônico local agora é byte a byte idêntico ao publicado no app.
SHA-256: e7ce679001a64d9211b567f9f8130bcbce1a56eb0edd4cf35d76bc4d7c29e1f8.

O diff semântico contém 99 alterações de pool CTAL-TM, metadados da nova
certificação e alterações bilíngues dos distratores em seis questões:
ctaltm-44, ctaltm-53, ctaltm-64, ctaltm-78, ctaltm-87 e ctaltm-189.
IDs, gabaritos e conteúdo CTFL/CTAL-TA permanecem preservados. A cópia
legada CTFL também é idêntica nos dois repositórios.

## Achados das guardas

Executar na raiz da fonte:

```sh
python3 check_alignment.py --bank-file synapse-question-bank.json --threshold 0
```

Resultado real: exit 1; guardas antigas PASS; 3/7 guardas psicométricas PASS.
CTAL-TM agora bloqueia; CT-AI e CTFL-AT continuam latentes, sem promoção.

| Guarda CTAL-TM | PT | EN | Critério preservado |
| --- | --- | --- | --- |
| Alternativa mais longa | 91,0% | 91,5% | máximo 40% |
| Efeito do comprimento | d 2,271 | d 2,387 | máximo 0,50 |
| Qualificadores absolutistas | razão 0,275 | razão 0,243 | 0,5 a 2,0 |
| Clustering de gabaritos | z -6,71 | mesma sequência | mínimo -5,0 |

A maior sequência tem 46 respostas consecutivas no mesmo índice, embora
os índices globais estejam balanceados em 50/50/50/50. Balanceamento
global não elimina pistas locais.

Nenhuma baseline, allowlist ou threshold foi alterado para absorver os achados.
Corrigida também a resolução das baselines quando o CLI recebe caminho absoluto.

## Triagem de conteúdo e revisão humana parcial

`ctaltm-quality-triage.json` contém uma ficha para cada uma das 200 questões:
comprimento de alternativas, ocorrência dos qualificadores da guarda,
pool, capítulo e K-level. O relatório é gerado por `audit_ctaltm.py` e
identifica o hash do banco analisado. Todas as fichas permanecem
PENDING_REVIEW: heurística não substitui validação do syllabus ou do gabarito.

Leitura qualitativa inicial, sem alterar ou certificar os gabaritos:

- ctaltm-02: a alternativa correta acumula as condições de início e atualização;
  as erradas usam restrições absolutas. Revisar plausibilidade e extensão das
  alternativas conjuntamente, sem simplesmente remover palavras da lista.
- ctaltm-03: a correta combina o nome da atividade com a definição detalhada;
  os distratores são mais curtos. A formulação oferece pista de comprimento.
- ctaltm-44, 53 e 78: as mudanças importadas substituem distratores de café,
  escritório ou humor por termos do domínio. Isso melhora pertinência, mas
  ainda exige revisão da existência de uma única resposta defensável.
- ctaltm-64 e 87: os novos distratores mantêm "apenas" / "only" em série.
  Remover absurdos não resolve sozinho a pista de absolutismo.
- ctaltm-189: os distratores foram tornados mais próximos do domínio, mas
  a correção conceitual e a equivalência PT/EN ainda precisam de parecer.

Não foram feitas reformulações em massa, inserção de texto de enchimento,
permutação de alternativas ou mudanças de gabarito para forçar métricas verdes.
O relatório não constitui auditoria editorial completa das 200 questões.

## Proteções executadas

- `python3 -m unittest test_sync_protection.py -v`: 11 testes aprovados.
- `python3 verify_sync.py . '../ctfl-app 2'`: PASS, checksums e fatias completas.
- Mesmo comando com `--check-current`: PASS, anti-downgrade e cobertura LIVE.
- CTFL legado: exit 0, sete guardas aprovadas.
- App: formatação, lint, 443 testes, build e cinco E2E Chromium aprovados.

O sync agora verifica qualidade ANTES de copiar e abrir PR, rejeita downgrade,
perda de metadados LIVE, conteúdo diferente na mesma versão e remoção de IDs
sem migração. Depois da cópia, regenera as fatias e compara seu conteúdo inteiro.
O job de CI do app também compara com a fonte canônica e executa suas guardas.

## Publicação e pendências

Nenhum commit ou push nesta etapa. Os workflows foram inspecionados e testados
localmente; a execução hospedada não foi disparada. Para ativar as proteções,
as mudanças do banco-fonte precisam chegar ao remoto antes das mudanças do app.
Não se deve interpretar checks locais verdes como CI remoto aprovado.

O novo job de conteúdo continuará vermelho enquanto as quatro falhas CTAL-TM
permanecerem. É necessário revisar o acervo, registrar decisões por questão,
incrementar a versão canônica para qualquer nova alteração de conteúdo,
regenerar as fatias e repetir guardas e regressão. Só então preparar o envio.
