# Retomada e revisão independente da rodada 2

Data: 2026-10-24. Estado: EM REVISÃO, NÃO LIBERADO.

## Interrupção identificada

A consulta aos seis agentes encontrou cinco encerramentos por limite de uso
e um encerramento concluído. Apesar disso, os seis arquivos `*-r2.json`
estão presentes e puderam ser analisados. Não se deve confundir arquivo
entregue, execução concluída e aprovação editorial.

## Verificação reproduzível realizada pelo revisor

Executar `python3 editorial/review_round2.py` na raiz deste repositório.
O resultado está em `editorial/round2-validation.json`. O script não altera
o banco canônico nem os arquivos dos agentes.

- Cobertura exata: 188 IDs únicos, 13–200, sem mudança dos índices de resposta.
- Estados declarados: 141 REVISED, 10 UNCHANGED, 26 INCONCLUSIVO,
  11 REPAIR_PROPOSED. Esses estados NÃO são aprovações do revisor.
- Simulação aplica somente REVISED; mantém os 37 reparos pendentes intactos.
- CTAL-TM: pick-longest PT 44,5%, EN 54,5%; efeito de comprimento
  PT 0,648, EN 0,679; qualificadores PT 0,278, EN 0,218;
  runs z -6,71, sequência máxima de 46 respostas iguais.
- As quatro guardas continuam reprovadas. Nenhum limiar foi alterado.
- Os 12 testes Python de proteção editorial/sincronização passaram novamente.

## Parecer individual inicial sobre reparos críticos

Referência primária consultada pelo revisor:
[Syllabus CTAL-TM v3.0](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTAL-TM_Syllabus_v3.0_zKjKsaN.pdf).
Lidos os enunciados, quatro alternativas e explicações em PT/EN dos itens
abaixo. Esta lista explicita o escopo, sem alegar revisão semântica completa
dos 188 itens.

| Item | Parecer do revisor | Trabalho necessário |
| --- | --- | --- |
| 51 | Taxonomia proposta coincide com 1.6.4, mas pergunta somente uma lista | Cobrar distinção entre estágios para sustentar TM-1.6.4 K2, não mera recordação |
| 69 | Bloqueado: sequência factual corrigida, demanda cognitiva reduzida | TM-2.3.1 é K3; exigir aplicar o fluxo a um contexto, não reconhecer sua ordem |
| 77 | Bloqueado: pergunta passa a recordar uma lista apesar de K3 | Aplicar seleção de informações a um relatório; não tornar reprodução universalmente obrigatória se a explicação diz preferencial |
| 136 | Bloqueado: reconhecer o T de SMART não demonstra aplicação K3 | Exigir selecionar ou construir um objetivo adequado às restrições do contexto |
| 161 | Ainda não aprovado | Explicitar denominador de 95/3/2% versus 90% de execução; evitar aparente soma de 100% do plano já classificado |
| 162 | Ainda não aprovado | Não pedir que se relate atendimento a critérios que o enunciado diz não fornecer; alternativa deve solicitar os critérios e declarar limite da avaliação |
| 173 | Bloqueado por rastreabilidade | Proposta avalia 2.3.6, mas item mantém TM-2.3.2. Corrigir apenas texto cria atribuição falsa de LO; preferir reparo dentro do LO original |
| 186 | Bloqueado por K4 não demonstrado | Resposta descreve método genérico; analisar lacunas concretas, recursos e alternativas viáveis do cenário |
| 187 | Bloqueado por K4 não demonstrado | Mesma receita genérica de 186; explicitar evidências que permitam discriminar planos de capacitação |
| 200 | Cálculo e paridade PT/EN aceitos para candidato, integração pendente | 1.500.000 − 400.000 − 200.000 = 900.000. Dados agora constam do enunciado; preservar premissas e executar validação completa antes de integrar |

## Compatibilidade investigada no app

`src/components/Quiz.jsx` salva `questionIds`, `optOrder` com `origIndex` e
respostas; `resumeExam()` reconstrói opções e correção consultando o banco
atual. Portanto reordenar alternativas/alterar gabaritos pode reinterpretar
respostas salvas. Mesmo conservar o índice não garante preservar o conteúdo
que a pessoa respondeu, quando se reescreve semanticamente o item.

Não foi aplicada permutação para corrigir clustering. Antes da integração
é preciso definir e testar identificação de revisão do banco/rascunho ou
migração explícita; não descartar silenciosamente rascunhos nem progresso.

## Pendências objetivas

1. Concluir revisão independente dos demais itens e registrar decisões por ID.
2. Refazer os reparos acima preservando LO e nível cognitivo; não simplesmente
   diminuir K-level ou alterar blueprint para fazer o gate passar.
3. Avaliar os outros reparos propostos, incluindo 121 (seção proposta 1.3.3
   versus LO original TM-1.3.1), sem aprovação automática.
4. Resolver pistas textuais e clustering sem enfraquecer guardas.
5. Testar rascunhos anteriores à atualização e somente então integrar,
   regenerar fatias e repetir regressão do app.

Nenhum conteúdo da rodada 2 foi aplicado ao banco. App permanece 3.17.0,
sem commit, push ou publicação nesta retomada.
