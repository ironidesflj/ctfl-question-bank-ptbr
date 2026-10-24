# Parecer do revisor principal sobre os seis lotes

Data: 2026-10-24. Decisão: NÃO INTEGRAR esta primeira rodada.

## Cobertura e integridade

Conferidos os seis JSONs, intervalos, continuidade e índices de resposta:
188 IDs únicos, cobertura exata 13–200; 142 REVISED, 11 UNCHANGED e 35
INCONCLUSIVO. Todas as propostas REVISED têm quatro alternativas distintas
e não vazias em cada idioma. Índices de resposta coincidem com o banco.
Essas verificações não equivalem a aprovação semântica.

## Simulação das propostas sem alterar o banco

Aplicadas em memória somente as 142 entradas REVISED e suas explicações.
As 35 inconclusivas permaneceram intactas. Executadas as guardas existentes
sobre o candidato em diretório temporário, sem alterar baselines.

| Guarda CTAL-TM | PT | EN | Decisão |
| --- | --- | --- | --- |
| Pick-longest | 54,5% | 60,0% | Reprova máximo de 40% |
| Efeito do comprimento | 0,685 | 0,729 | Reprova máximo de 0,50 |
| Qualificadores | 0,136 | 0,148 | Reprova faixa 0,5–2,0 |
| Runs test | z -6,71 | mesma ordem | Reprova mínimo -5,0 |

O viés de comprimento melhora em relação ao banco atual, mas não é resolvido.
A pista de qualificadores piora. Não há aprovação baseada apenas em redução
de métricas. Nenhum conteúdo foi integrado a partir desta simulação.

## Problemas que exigem retrabalho

- Muitas alternativas erradas ainda negam explicitamente uma necessidade,
  substituem uma atividade essencial ou usam exclusividade sem contexto.
  Exemplo ctaltm-109: os distratores substituem análise de risco por votação,
  tornam cada stakeholder testador ou eliminam a análise de stakeholders.
  O aluno ainda pode acertar descartando caricaturas, sem dominar o conceito.
- ctaltm-174 e ctaltm-178: a correta continua muito mais extensa; a triagem
  encontrou três ocorrências acima de 1,5 vez a média dos distratores.
- As propostas inconclusivas incluem correções materiais de taxonomias,
  enunciados subespecificados e referências não sustentadas pelo syllabus.
  Preservar o número do índice não preserva o significado do gabarito.
- Alterar alternativas em ctaltm-39, 51, 69, 84, 125, 151, 170, 183 ou 195
  sem resolver também enunciado, explicação ou LO pode criar outra ambiguidade.
- Clustering é independente da revisão de texto. Exige uma decisão posterior
  sobre ordem das opções/itens e teste de compatibilidade com rascunhos salvos.
  Não será corrigido reordenando o banco só para obter estatística verde.

## Ação do revisor

Devolvidos os seis lotes aos mesmos agentes GPT-5.6, com escopos preservados.
Segunda rodada usa arquivos proposal-N-r2.json, mantendo a primeira como
evidência. Solicitação: distratores plausíveis, texto paralelo, correção
fundamentada de enunciados quando necessária e INCONCLUSIVO explícito quando
não houver solução demonstrável. Nenhuma mudança automática de gabarito.

## O que ainda falta

1. Receber e revisar a segunda rodada; não considerar um parecer de agente
   aprovação independente do revisor principal.
2. Resolver as 35 dúvidas conceituais com referência e contrato do item.
3. Conferir PT/EN e justificativa de cada alteração efetivamente aceita.
4. Tratar clustering com preservação de progresso e rascunhos.
5. Integrar somente o aprovado na fonte; regenerar fatias e repetir guardas,
   integridade, testes funcionais e E2E. Sem commit ou push nesta etapa.

Banco canônico permanece no candidato 1.6.1-editorial.1 com apenas o lote
inicial 01 previamente aplicado. App continua 3.17.0; produção inalterada.
