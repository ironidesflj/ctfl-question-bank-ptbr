# Relatório de pendências editoriais — CTAL-TM

**Data:** 2026-10-24  
**Banco:** CTAL-TM v1.6.1-editorial.1  
**Aplicativo em produção:** Synapse 3.17.0  
**Status:** não aprovado para integração/publicação

## Resumo executivo

Foi feita uma revisão dos 188 itens CTAL-TM (`ctaltm-13` a `ctaltm-200`) em duas rodadas, com apoio de seis agentes e revisão principal independente.

Nenhuma proposta da segunda rodada foi integrada ao banco canônico. O aplicativo continua na versão 3.17.0 e não houve commit, push ou publicação desta revisão.

A primeira rodada não foi aprovada porque ainda havia distratores caricatos, alternativas corretas muito mais longas e pistas linguísticas. A segunda rodada melhorou muitos itens, mas ainda não pode ser integrada sem revisão semântica final.

## Verificação da segunda rodada

Arquivo analisado: `editorial/ctaltm-proposal-{2..7}-r2.json`.

- Cobertura: 188/188 IDs, sem duplicatas.
- Faixa: `ctaltm-13` até `ctaltm-200`.
- Índices de resposta preservados.
- Estados declarados pelos agentes:
  - 141 `REVISED`
  - 10 `UNCHANGED`
  - 26 `INCONCLUSIVO`
  - 11 `REPAIR_PROPOSED`
- Esses estados são propostas dos agentes, não aprovação editorial.
- Todos os itens possuem alternativas PT/EN estruturadas e quatro opções distintas.

## Resultado da simulação

Foi simulada a aplicação apenas das propostas `REVISED`, sem alterar o banco canônico.

As quatro guardas de qualidade do CTAL-TM continuam reprovadas:

| Guarda | PT | EN | Resultado |
|---|---:|---:|---|
| Pick-longest | 44,5% | 54,5% | Falha; máximo permitido: 40% |
| Efeito de comprimento, Cohen’s d | 0,648 | 0,679 | Falha; máximo permitido: 0,50 |
| Proporção de qualificadores | 0,278 | 0,218 | Falha; faixa permitida: 0,5–2,0 |
| Runs test | z = -6,71 | z = -6,71 | Falha; indica clustering |

Também foi detectada uma sequência máxima de 46 respostas com o mesmo índice de alternativa.

Os seguintes gates passaram na simulação:

- distribuição dos índices de resposta;
- blueprint e pesos de capítulos;
- consistência de K-levels;
- padrão de letras conhecido na baseline.

## Problemas que ainda precisam ser corrigidos

### 1. Distratores e pistas linguísticas

Os distratores precisam ser plausíveis para alguém que conhece parcialmente o conteúdo. Remover alternativas que:

- negam explicitamente uma prática essencial;
- usam palavras absolutas sem necessidade;
- descrevem ações obviamente absurdas;
- são muito mais curtas ou muito mais longas que a correta;
- revelam a resposta por vocabulário, estrutura ou detalhamento;
- trocam uma atividade central por uma caricatura;
- criam uma alternativa correta por interpretação diferente do enunciado.

Não corrigir as métricas apenas reordenando alternativas ou itens. A ordem precisa continuar compatível com progresso, respostas e rascunhos de simulados já salvos.

### 2. Preservação do nível cognitivo

Não transformar itens K3/K4 em perguntas de memorização apenas para torná-los factualmente corretos.

- K2: entendimento, explicação e distinção conceitual.
- K3: aplicação do conceito a um contexto.
- K4: análise de dados, restrições, alternativas e consequências.

Os reparos devem preservar o LO e o nível cognitivo declarados no banco, ou então alterar explicitamente LO, K-level, explicação, blueprint e cobertura — nunca somente as alternativas.

### 3. Alinhamento entre seção, LO e conteúdo

O número da seção não basta. O enunciado, a resposta, a explicação e o LO precisam tratar o mesmo assunto.

Exemplo: um item originalmente ligado a `TM-2.3.2` não deve ser convertido silenciosamente em uma pergunta de `TM-2.3.6` sobre melhoria de processo.

## Itens que exigem revisão prioritária

### Corrigir novamente antes de qualquer integração

| Item | Problema |
|---|---|
| `ctaltm-39` | O reparo diferencia Initiating e Establishing, mas ainda precisa garantir que o enunciado discrimine corretamente as fases do IDEAL. |
| `ctaltm-51` | A lista do ciclo de vida da ferramenta está correta, mas o item virou memorização; preservar TM-1.6.4 K2 com distinção contextual. |
| `ctaltm-52` | Evolução e aposentadoria precisam ser discriminadas por evidências do cenário, sem depender apenas de palavras-chave. |
| `ctaltm-64` | A taxonomia de fatores de estimativa foi corrigida; verificar que a alternativa correta não seja identificada por ser a única completa. |
| `ctaltm-65` | Não inferir direção universal do efeito de experiência/maturidade; exigir uso contextual dos fatores. |
| `ctaltm-66` | A resposta deve aplicar reestimativa, mudanças de base e retrabalho sem virar regra genérica. |
| `ctaltm-67` | Wideband Delphi está alinhado ao contexto sequencial, mas o cenário deve exigir análise, pois o item é K4. |
| `ctaltm-69` | O fluxo factual foi corrigido, mas TM-2.3.1 é K3; aplicar o fluxo a um contexto em vez de pedir a sequência decorada. |
| `ctaltm-70` | Evitar alternativa correta genérica; exigir desenho de processo com responsabilidades, transições, ferramenta e comunicação. |
| `ctaltm-77` | O reparo virou memorização de quatro campos; preservar K3 e a nuance de campos obrigatórios na maioria dos ambientes. |
| `ctaltm-82` | A tendência de defeitos reabertos não deve gerar ação automática; exigir investigação de causas e evidência. |
| `ctaltm-84` | Separar competência profissional de competência metodológica conforme o syllabus, sem classificação inventada. |
| `ctaltm-121` | A resposta depende de uma matriz de risco explicitamente fornecida; não presumir regra universal para alta probabilidade/baixo impacto. |
| `ctaltm-122` | Usar técnica de identificação de riscos realmente sustentada pelo syllabus; não chamar checklist de técnica não definida sem contextualização. |
| `ctaltm-124` | Fornecer a regra/matriz que produz risco alto; sem isso o cenário é subdeterminado. |
| `ctaltm-125` | Manter a distinção entre pontuação ordinal qualitativa e medida quantitativa; evitar cálculo com aparência estatística indevida. |
| `ctaltm-132` | Alinhar a integração de análise de riscos à estratégia sem atribuir taxonomia inexistente à seção 1.4.1. |
| `ctaltm-136` | Corrigir a terminologia `Timely`, mas preservar TM-1.4.3 K3 com aplicação de SMART, não mera identificação da letra T. |
| `ctaltm-139` | Corrigir as fases do IDEAL e manter o propósito de Diagnosing: avaliar o processo atual e identificar melhorias. |
| `ctaltm-150` | Diferenciar evolução de aposentadoria com evidências suficientes; o cenário original admitia as duas respostas. |
| `ctaltm-151` | Usar os quatro estágios oficiais do ciclo de vida da ferramenta e garantir distinção conceitual. |
| `ctaltm-155` | Não introduzir Kanban, WIP ou métricas que não estejam sustentados pelo syllabus; usar comparação válida entre modelos. |
| `ctaltm-161` | Separar percentual de execução, distribuição de resultados, testes restantes, defeitos críticos e critérios de saída; evitar dados aparentemente conflitantes. |
| `ctaltm-162` | Sem critérios de liberação e impacto dos defeitos, a resposta deve solicitar avaliação/autorização, não recomendar liberar ou adiar. |
| `ctaltm-168` | Não converter composição da equipe em multiplicador fixo de esforço; usar habilidades, experiência, alocação e premissas observáveis. |
| `ctaltm-170` | `CLOSED` é estado terminal; `DEFERRED`, `REOPENED` e `REJECTED` devem aparecer como ramos contextuais. |
| `ctaltm-173` | O reparo trata TM-2.3.6, mas o item está associado a TM-2.3.2; corrigir o conteúdo dentro do LO correto ou atualizar todo o contrato do item. |
| `ctaltm-175` | Não afirmar que planejamento substitui triagem; formalidade e cadência dependem de contexto, risco, tamanho e maturidade. |
| `ctaltm-182` | A proporção 80/10/10 não prova falha de contenção sem evidência adicional; manter a análise de causa. |
| `ctaltm-183` | Não usar ODC como se fosse conteúdo explícito do syllabus; usar dados de classificação previstos para definir melhoria. |
| `ctaltm-186` | A resposta é genérica e não demonstra K4; usar atividades, níveis, habilidades disponíveis, lacunas, risco e alternativas de aquisição/desenvolvimento. |
| `ctaltm-187` | Mesmo problema de K4: o cenário precisa discriminar planos de capacitação, contratação ou apoio especializado. |
| `ctaltm-188` | Usar uma técnica de avaliação explicitamente exemplificada no syllabus, com competência profissional/metodológica bem definida. |
| `ctaltm-189` | Não apresentar feedback 360 como técnica explicitamente citada; usar demonstração de tarefa ou outra técnica sustentada pelo syllabus. |
| `ctaltm-191` | Diferenciar treinamento/educação, coaching e autoestudo conforme a competência desenvolvida. |
| `ctaltm-195` | Com fatores de higiene atendidos, o cenário deve apontar claramente para motivadores: reconhecimento, autonomia, desafio, responsabilidade e desenvolvimento. |
| `ctaltm-200` | Cálculo candidato: `$1.500.000 - $400.000 - $200.000 = $900.000`. Manter todos os valores no enunciado e paridade PT/EN. |

## Itens de maior risco estatístico

Na primeira revisão, foram observados como especialmente problemáticos:

- `ctaltm-109`: distratores substituíam análise de risco por votação, tornavam todos os stakeholders testadores ou eliminavam análise de stakeholders.
- `ctaltm-174`: alternativa correta excessivamente longa.
- `ctaltm-178`: alternativa correta excessivamente longa.

Esses itens precisam de revisão manual adicional mesmo que tenham recebido proposta `REVISED`.

## Critérios para aceitar uma correção

Para cada item alterado, entregar:

1. enunciado PT e EN semanticamente equivalente;
2. quatro alternativas PT e EN paralelas;
3. índice de resposta preservado ou justificativa formal para mudança;
4. explicação PT e EN que justifique o gabarito;
5. seção e LO compatíveis com o conteúdo;
6. K-level preservado;
7. fonte no syllabus CTAL-TM v3.0;
8. ausência de distrator caricatural, absoluto desnecessário ou pista textual;
9. confirmação de que a mudança não quebra rascunhos de simulados e progresso;
10. teste das guardas completas após integrar.

## Regras de integração

- Não alterar thresholds das guardas.
- Não remover CTAL-TM de `LIVE_CERTS`.
- Não alterar baselines para esconder regressão.
- Não corrigir clustering por simples reordenação.
- Não alterar gabaritos automaticamente.
- Não publicar enquanto qualquer guarda bloqueante falhar.
- Integrar primeiro no banco canônico.
- Regenerar as fatias do app a partir da fonte canônica.
- Executar testes do banco, testes do app, build e E2E.
- Confirmar que CTFL, CTAL-TA e funcionalidades existentes permanecem idênticos.

## Estado dos arquivos

- Propostas dos agentes: preservadas em `editorial/ctaltm-proposal-2.json` até `editorial/ctaltm-proposal-7.json`.
- Segunda rodada: preservada em `editorial/ctaltm-proposal-2-r2.json` até `editorial/ctaltm-proposal-7-r2.json`.
- Validação estrutural/simulação: `editorial/round2-validation.json`.
- Parecer da primeira rodada: `editorial/PARENT_REVIEW_ROUND_1.md`.
- Parecer desta retomada: `editorial/PARENT_REVIEW_ROUND_2.md`.
- Banco canônico: sem propostas da segunda rodada integradas.
- Aplicativo: Synapse 3.17.0, produção inalterada.

## Fonte oficial

[ISTQB CTAL-TM Syllabus v3.0](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTAL-TM_Syllabus_v3.0_zKjKsaN.pdf)
