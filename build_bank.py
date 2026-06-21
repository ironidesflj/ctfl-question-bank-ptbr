# -*- coding: utf-8 -*-
"""
Gerador do banco de questões CTFL v4.0 (PT-BR).
Schema pronto para i18n: campos neutros no topo, texto traduzível em locales.{lang}.
Adicionar inglês depois = incluir locales["en"] em cada registro.
"""
import json, sys

DOMAINS = {1: "fund", 2: "proc", 3: "est", 4: "tec", 5: "mgmt", 6: "fer"}
DOMAIN_NAMES = {
    "fund": "Fundamentos do Teste",
    "proc": "Teste ao Longo do Ciclo de Desenvolvimento",
    "est": "Teste Estático",
    "tec": "Técnicas de Teste",
    "mgmt": "Gerenciamento das Atividades de Teste",
    "fer": "Ferramentas de Apoio ao Teste",
}
# Distribuição-alvo (proporcional ao exame: 8/5/5/11/9/2 x3 = 120)
TARGET = {1: 40, 2: 25, 3: 25, 4: 55, 5: 45, 6: 10}

# Cada questão: (capitulo, k_level, enunciado, [opcoes], indice_correto, explicacao)
Q = []
def add(ch, k, q, opts, ans, exp):
    Q.append((ch, k, q, opts, ans, exp))

# ============================================================
# CAPÍTULO 1 — FUNDAMENTOS (24)
# ============================================================
add(1,1,"Qual é a relação correta entre erro, defeito e falha?",
    ["Erro é do testador; defeito do desenvolvedor; falha do usuário",
     "Falha gera defeito, que gera erro",
     "Erro e defeito são sinônimos; falha só ocorre em produção",
     "Um erro (ação humana) introduz um defeito no artefato, que ao ser executado pode causar uma falha"],3,
    "A cadeia causal é erro humano → defeito no código/artefato → falha (comportamento incorreto em execução).")
add(1,1,"Qual NÃO é um objetivo típico do teste?",
    ["Encontrar defeitos","Reduzir o nível de risco","Verificar requisitos","Garantir matematicamente a ausência de defeitos"],3,
    "O teste não pode provar a ausência de defeitos; ele fornece informação e reduz risco, mas não garante perfeição.")
add(1,2,"Qual a diferença entre testar e depurar (debugging)?",
    ["São a mesma atividade, sem distinção entre encontrar e corrigir defeitos","A depuração só ocorre em produção, nunca durante o desenvolvimento",
     "A depuração encontra falhas e o teste corrige o defeito identificado","Teste encontra falhas; depuração localiza, analisa e corrige o defeito que as causou"],3,
    "Teste evidencia falhas causadas por defeitos; a depuração é a atividade de desenvolvimento que localiza, diagnostica e corrige o defeito.")
add(1,2,"Por que o teste é necessário?",
    ["Para substituir completamente a revisão de código e as inspeções","Porque é exigido por lei em todos os países e mercados",
     "Para garantir que o software fique completamente livre de defeitos","Para contribuir com o sucesso do projeto, reduzindo o risco de falhas em operação"],3,
    "O teste reduz o risco de falhas em operação e ajuda a entregar um produto com qualidade adequada às necessidades das partes interessadas.")
add(1,2,"Como se relacionam controle de qualidade (QC) e garantia da qualidade (QA)?",
    ["QC e QA são termos sinônimos usados indistintamente na prática","O teste faz parte apenas do QA, e nunca está dentro do QC",
     "QA é orientado ao produto testado; QC é orientado ao processo organizacional","QC é orientado ao produto (inclui o teste); QA é orientado ao processo"],3,
    "QC foca o produto e inclui atividades como o teste; QA foca a melhoria do processo para gerar confiança de que a qualidade será atingida.")
add(1,2,"A causa-raiz de um defeito é:",
    ["A falha observada pelo usuário final após o lançamento do sistema","O caso de teste específico que falhou durante a execução",
     "O ambiente de teste utilizado durante a execução dos casos","O evento mais antigo que, se corrigido, evita a recorrência do defeito"],3,
    "A análise de causa-raiz busca a origem fundamental, permitindo ações que previnem a reincidência de defeitos semelhantes.")
add(1,1,"Princípio: 'o teste mostra a presença de defeitos, não a sua ausência'. Isso significa que:",
    ["Testar prova que não há defeitos","O teste é inútil",
     "Defeitos sempre existem","Testar pode revelar defeitos, mas não provar que não existem"],3,
    "Encontrar defeitos não é prova de ausência deles; mesmo sem defeitos encontrados, não há garantia de correção total.")
add(1,1,"Princípio: 'o teste exaustivo é impossível'. A consequência prática é:",
    ["Não vale a pena testar","Automatizar tudo",
     "Testar apenas o caminho feliz","Usar análise de risco e prioridades para focar o esforço"],3,
    "Como não é viável testar todas as combinações, prioriza-se com base em risco e prioridades.")
add(1,2,"Princípio do 'teste antecipado' (early testing) afirma que:",
    ["Testes só devem começar após o código pronto","Só requisitos podem ser testados cedo",
     "Testar cedo aumenta os custos","Atividades de teste devem começar o mais cedo possível no ciclo"],3,
    "Iniciar cedo (inclusive com testes estáticos em requisitos) reduz custos, pois defeitos achados tarde são mais caros de corrigir.")
add(1,2,"O 'agrupamento de defeitos' (defect clustering) sugere que:",
    ["Defeitos se distribuem por igual","Defeitos só aparecem em código novo",
     "Cada módulo tem um defeito","Poucos módulos concentram a maioria dos defeitos"],3,
    "Geralmente uma minoria de módulos concentra a maioria dos defeitos, o que orienta a priorização do teste.")
add(1,2,"O 'paradoxo do pesticida' indica que:",
    ["Executar mais testes sempre gera mais defeitos no sistema","Pesticidas reais afetam o funcionamento do software testado",
     "Testes manuais são sempre melhores que os automatizados","Repetir os mesmos testes deixa de encontrar novos defeitos"],3,
    "Se os mesmos casos são repetidos, eles param de revelar defeitos novos; é preciso revisar e renovar os testes.")
add(1,2,"O princípio 'o teste depende do contexto' significa que:",
    ["Todo software deve ser testado exatamente da mesma forma sempre","Apenas sistemas críticos de segurança precisam ser testados",
     "O contexto do projeto nunca importa para o teste","A forma de testar varia conforme o domínio, risco e contexto"],3,
    "Sistemas diferentes (e.g., e-commerce vs. software médico) exigem abordagens, técnicas e rigor distintos.")
add(1,2,"A 'falácia da ausência de erros' (absence-of-errors fallacy) afirma que:",
    ["Um software sem defeitos conhecidos é sempre considerado bom","Os erros encontrados durante o teste nunca importam",
     "Não existem erros em nenhum sistema bem desenvolvido","Corrigir todos os defeitos é inútil se o sistema não atende às necessidades do usuário"],3,
    "Um produto pode estar livre de defeitos conhecidos e ainda assim ser inadequado se não atende às necessidades reais.")
add(1,2,"Um time decide priorizar o teste do módulo de pagamentos, onde historicamente surgem muitos defeitos. Qual princípio justifica isso?",
    ["Teste exaustivo","Paradoxo do pesticida","Falácia da ausência de erros","Agrupamento de defeitos"],3,
    "Concentrar esforço onde os defeitos historicamente se agrupam aplica o princípio do defect clustering.")
add(1,1,"Qual atividade do processo de teste define objetivos, abordagem e recursos?",
    ["Execução","Conclusão","Análise","Planejamento"],3,
    "O planejamento de teste define objetivos, escopo, abordagem, recursos e critérios.")
add(1,2,"O monitoramento e controle do teste serve para:",
    ["Escrever os casos de teste detalhados para o sistema","Encerrar formalmente o projeto antes do prazo final",
     "Executar diretamente os testes planejados no cronograma","Comparar o progresso real com o planejado e tomar ações corretivas"],3,
    "O monitoramento coleta métricas; o controle age (replanejar, realocar) quando há desvios em relação ao plano.")
add(1,2,"Na atividade de análise de teste, o que se produz principalmente?",
    ["Scripts automatizados prontos para execução imediata","Os dados de teste já preparados para a execução",
     "O relatório final de conclusão do ciclo de teste","Condições de teste a partir da base de teste e seus critérios"],3,
    "A análise identifica o que testar — as condições de teste — a partir da base de teste (requisitos, riscos, etc.).")
add(1,2,"Na modelagem de teste, o foco é:",
    ["Identificar apenas o que testar, sem definir como","Reportar os defeitos encontrados durante a execução",
     "Executar diretamente os casos de teste já prontos","Definir como testar: casos de teste e conjuntos a partir das condições"],3,
    "A modelagem (design) elabora como cobrir as condições de teste, produzindo casos e conjuntos de teste.")
add(1,2,"Qual é a saída principal da atividade de implementação de teste?",
    ["Apenas as condições de teste identificadas na análise","O relatório de progresso enviado às partes interessadas",
     "O plano de teste aprovado pelos stakeholders do projeto","Procedimentos, scripts e dados prontos para execução, com o ambiente preparado"],3,
    "A implementação organiza e prepara tudo o que é necessário para executar: procedimentos, dados, ambiente e agenda.")
add(1,2,"Durante a execução do teste, ao encontrar um resultado divergente, o testador deve primeiro:",
    ["Corrigir imediatamente o código-fonte sem registrar nada","Ignorar a divergência se ela parecer pouco relevante",
     "Encerrar o teste imediatamente sem informar ninguém","Registrar o resultado e, se for uma anomalia, criar um relatório de defeito"],3,
    "Resultados são comparados ao esperado; divergências (anomalias) são analisadas e, quando defeitos, registradas em relatório.")
add(1,2,"A atividade de conclusão do teste tipicamente inclui:",
    ["Escrever os primeiros casos de teste do próximo ciclo","Preparar o ambiente de teste para a próxima execução",
     "Definir os objetivos iniciais do esforço de teste","Arquivar testware, registrar lições aprendidas e produzir o relatório de conclusão"],3,
    "A conclusão consolida resultados, arquiva o testware reutilizável, registra lições aprendidas e emite o relatório de conclusão.")
add(1,1,"O que é 'testware'?",
    ["O hardware de teste","O sistema sob teste",
     "A ferramenta de automação","Os artefatos produzidos durante o processo de teste (planos, casos, dados, relatórios)"],3,
    "Testware engloba todos os artefatos do trabalho de teste: planos, condições, casos, dados, scripts, relatórios.")
add(1,2,"Qual o principal benefício da rastreabilidade entre a base de teste e o testware?",
    ["Reduzir automaticamente o número de testes necessários","Acelerar a execução do código em produção",
     "Eliminar completamente a necessidade de documentação","Permitir avaliar cobertura e o impacto de mudanças sobre os testes"],3,
    "A rastreabilidade liga requisitos/riscos a condições e casos, apoiando cobertura, análise de impacto e auditoria.")
add(1,2,"Sobre independência do teste, qual afirmação é correta?",
    ["Maior independência sempre encontra mais defeitos, sem nenhuma desvantagem associada","O grau de independência do testador não influencia em nada o teste",
     "O autor do código é sempre o melhor testador possível para o seu próprio trabalho","Independência pode reduzir o viés do autor, mas graus extremos têm desvantagens como menor conhecimento do contexto"],3,
    "Algum grau de independência reduz o viés cognitivo do autor, mas independência total pode afastar o testador do contexto e da comunicação.")

# ============================================================
# CAPÍTULO 1 — FUNDAMENTOS (continuação, +16)
# ============================================================
add(1,2,"Qual habilidade cognitiva é considerada fundamental para um bom testador?",
    ["Velocidade de digitação e domínio de atalhos de teclado",
     "Capacidade de escrever código de produção em qualquer linguagem",
     "Conhecimento exclusivo e avançado de múltiplas linguagens de programação",
     "Pensamento analítico e crítico para questionar suposições e identificar problemas"],3,
    "O pensamento analítico/crítico permite ao testador questionar suposições, identificar inconsistências e encontrar defeitos não óbvios.")

add(1,2,"A 'abordagem de equipe completa' (whole-team approach) no teste ágil implica que:",
    ["Somente os testadores são responsáveis pela qualidade, nunca os desenvolvedores",
     "Os desenvolvedores nunca participam das atividades de teste do projeto",
     "O gerente de testes toma todas as decisões sozinho, sem consultar a equipe",
     "Toda a equipe compartilha a responsabilidade pela qualidade, com testadores colaborando com devs e stakeholders"],3,
    "Na whole-team approach, qualidade é responsabilidade coletiva; testadores, devs e negócio colaboram desde o início.")

add(1,1,"Qual é o benefício principal de ter testadores com diferentes graus de independência?",
    ["Aumentar o custo do projeto",
     "Eliminar a necessidade de revisões",
     "Garantir que todos os testes sejam automatizados",
     "Combinar o conhecimento do autor com a perspectiva imparcial de quem não escreveu o artefato"],3,
    "Diferentes graus de independência equilibram conhecimento contextual e imparcialidade, melhorando a eficácia da detecção.")

add(1,2,"Um testador que revisa os próprios requisitos que escreveu terá dificuldade de encontrar defeitos porque:",
    ["Não tem tempo suficiente disponível na agenda do projeto",
     "Revisões de requisitos não são consideradas parte do teste",
     "Requisitos bem escritos nunca podem conter nenhum tipo de defeito",
     "O viés do autor dificulta ver os próprios erros — o testador tende a confirmar o que escreveu"],3,
    "O viés cognitivo do autor faz com que ele leia o que pretendia escrever, não o que realmente está escrito.")

add(1,1,"Em qual grau de independência o testador é externo à organização do desenvolvedor?",
    ["Testador que é o próprio autor",
     "Testador de outra equipe da mesma organização",
     "Testador de empresa especializada externa",
     "Testador da equipe de desenvolvimento"],2,
    "O grau mais alto de independência é representado por testadores de organizações externas — consultores ou laboratórios independentes.")

add(1,2,"A rastreabilidade bidirecional entre requisitos e casos de teste permite:",
    ["Executar os testes automaticamente sem qualquer intervenção humana",
     "Reduzir automaticamente o número total de defeitos do sistema",
     "Eliminar totalmente a necessidade de um plano de teste formal",
     "Verificar cobertura dos requisitos e analisar o impacto de mudanças nos testes"],3,
    "Com rastreabilidade bidirecional, é possível saber quais testes cobrem cada requisito e quais testes serão afetados por mudanças.")

add(1,2,"Qual é o papel principal do gerente de testes (test manager) em um projeto?",
    ["Executar pessoalmente todos os casos de teste manualmente",
     "Escrever os requisitos de negócio junto com os stakeholders",
     "Desenvolver diretamente o código de produção do sistema",
     "Planejar, monitorar, controlar e liderar as atividades de teste e a equipe"],3,
    "O gerente de testes é responsável pelo planejamento, monitoramento e controle do processo de teste e pela liderança da equipe.")

add(1,1,"O que é a 'base de teste' (test basis)?",
    ["O ambiente onde os testes são executados",
     "O banco de dados de defeitos",
     "O resultado dos testes executados",
     "O conjunto de artefatos dos quais os testes são derivados (requisitos, código, modelos, etc.)"],3,
    "A base de teste são os artefatos — requisitos, especificações, código, modelos — a partir dos quais condições e casos de teste são derivados.")

add(1,2,"Qual a diferença entre verificação e validação no contexto do teste?",
    ["Verificação e validação são termos sinônimos e intercambiáveis",
     "A validação do sistema só pode ocorrer após o lançamento em produção",
     "A verificação é sempre dinâmica; a validação é sempre um processo estático",
     "Verificação: 'estamos construindo certo?' (conforme especificação); validação: 'estamos construindo a coisa certa?' (atende ao usuário)"],3,
    "Verificação checa conformidade com a especificação; validação checa se o produto atende às necessidades reais do usuário.")

add(1,2,"A mentalidade do testador difere da do desenvolvedor porque o testador:",
    ["Foca em construir funcionalidades rapidamente",
     "Apenas confirma que o software funciona conforme esperado pelo dev",
     "Evita questionar decisões de design",
     "Adota uma perspectiva crítica, buscando ativamente falhas e questionando suposições"],3,
    "Testadores adotam mentalidade de questionamento e ceticismo construtivo para encontrar o que pode falhar, não para confirmar que funciona.")

add(1,1,"O que é um 'objeto de teste' (test object)?",
    ["A ferramenta usada para testar",
     "O ambiente de execução",
     "O caso de teste em si",
     "O item de trabalho (componente, sistema, requisito) que está sendo testado"],3,
    "O objeto de teste é o artefato que está sendo avaliado: um componente, sistema, requisito, modelo ou documento.")

add(1,2,"Como a comunicação eficaz de defeitos pelo testador contribui para o projeto?",
    ["Cria atrito desnecessário com o time de desenvolvimento",
     "Aumenta o número de defeitos encontrados",
     "Substitui a necessidade de cases de teste",
     "Permite que defeitos sejam compreendidos, priorizados e corrigidos de forma eficiente"],3,
    "Relatórios claros, objetivos e factuais facilitam a compreensão, reprodução e correção dos defeitos, além de preservar a colaboração.")

add(1,2,"Qual característica do teste antecipado (shift-left) o diferencia do teste tradicional?",
    ["O teste só é realizado depois do sistema estar em produção",
     "O shift-left só pode ser aplicado em projetos totalmente ágeis",
     "O shift-left elimina por completo a necessidade do teste de sistema",
     "As atividades de teste (inclusive revisões estáticas) iniciam desde os requisitos, não só após o código"],3,
    "Shift-left significa começar a testar — inclusive com revisões de requisitos — nas fases iniciais, antes mesmo de qualquer código.")

add(1,2,"A 'análise de causa-raiz' (root cause analysis) de defeitos recorrentes beneficia o processo porque:",
    ["Apenas documenta os defeitos encontrados, sem investigar a causa",
     "É necessária apenas em projetos críticos de segurança ou saúde",
     "Substitui completamente a necessidade de executar testes dinâmicos",
     "Identifica a origem dos problemas, permitindo melhorias de processo que previnam defeitos similares no futuro"],3,
    "Identificar a causa-raiz permite implementar melhorias de processo que evitam a reincidência de classes de defeitos semelhantes.")

add(1,2,"Um artefato de teste como um 'caso de teste' deve conter no mínimo:",
    ["Apenas o nome do testador responsável pela execução",
     "Apenas a data de criação e a versão atual do sistema",
     "Somente o resultado esperado, sem nenhum passo de execução",
     "Pré-condições, passos de execução, resultado esperado e pós-condições"],3,
    "Um caso de teste completo define pré-condições, entradas, passos, resultado esperado e pós-condições, garantindo repetibilidade.")

add(1,2,"Qual o impacto de defeitos encontrados em produção comparado a defeitos encontrados em requisitos?",
    ["O custo de correção é exatamente o mesmo em qualquer fase",
     "O impacto financeiro é irrelevante para o sucesso do projeto",
     "Defeitos encontrados em produção são sempre mais fáceis de corrigir",
     "Defeitos em produção são muito mais caros de corrigir — o custo cresce a cada fase que passa"],3,
    "O custo de correção aumenta exponencialmente com a fase: defeitos em requisitos custam muito menos que em produção.")

# ============================================================
# CAPÍTULO 2 — TESTE AO LONGO DO CICLO (15)
# ============================================================
add(2,2,"Como o modelo de ciclo de desenvolvimento influencia o teste?",
    ["O modelo de ciclo de desenvolvimento nunca influencia o teste","Influencia o teste apenas em projetos exclusivamente ágeis",
     "O modelo de ciclo só muda a ferramenta de automação usada","Influencia o momento, a abordagem e o nível de detalhe das atividades de teste"],3,
    "Em sequenciais o teste tende a ser por fase; em ágeis/iterativos é contínuo e integrado a cada incremento.")
add(2,2,"O que significa 'shift-left' no teste?",
    ["Adiar todas as atividades de teste para o final do ciclo","Realizar o teste apenas depois do sistema estar em produção",
     "Mover as atividades de teste para mais tarde no cronograma","Antecipar atividades de teste para fases iniciais do ciclo"],3,
    "Shift-left antecipa o teste (inclusive estático) para fases iniciais, encontrando defeitos mais cedo e mais barato.")
add(2,1,"TDD, ATDD e BDD são exemplos de abordagens:",
    ["De automação de UI","De teste de carga",
     "De gestão de configuração","De teste-primeiro (test-first), em que os testes guiam o desenvolvimento"],3,
    "São abordagens test-first: os testes/critérios são definidos antes ou junto ao código e orientam a implementação.")
add(2,1,"Qual o benefício de retrospectivas para o teste?",
    ["Reduzir o número de testes","Eliminar defeitos",
     "Substituir o planejamento","Promover melhoria contínua do processo a partir de lições aprendidas"],3,
    "Retrospectivas identificam o que melhorar (processo, ferramentas, colaboração), apoiando a melhoria contínua.")
add(2,1,"O teste de componente (unidade) foca em:",
    ["A integração entre sistemas","O sistema completo",
     "A aceitação do usuário","Verificar componentes isoladamente, normalmente pelo desenvolvedor"],3,
    "O teste de componente verifica módulos/unidades de forma isolada, frequentemente com apoio de stubs/drivers.")
add(2,2,"Qual a diferença entre integração de componentes e integração de sistemas?",
    ["A integração de componentes e a integração de sistemas são processos exatamente iguais e intercambiáveis","Apenas a integração de componentes utiliza interfaces formais entre os módulos do mesmo sistema",
     "A integração de sistemas é sempre realizada antes da integração de componentes, nunca depois","Integração de componentes verifica interações dentro de um sistema; integração de sistemas verifica interações entre sistemas distintos"],3,
    "A primeira foca interfaces internas entre componentes; a segunda, interfaces entre sistemas (e organizações) diferentes.")
add(2,1,"O teste de sistema avalia:",
    ["Apenas uma unidade","A aceitação contratual",
     "Somente a interface","O comportamento e as capacidades do sistema como um todo"],3,
    "O teste de sistema avalia o sistema integrado fim-a-fim, comportamento funcional e não funcional.")
add(2,2,"Quais são formas comuns de teste de aceitação?",
    ["Apenas teste unitário e teste de integração de componentes","Somente teste estático e teste dinâmico do sistema",
     "Apenas técnicas de caixa-branca e de caixa-preta","De usuário (UAT), operacional, contratual e regulatório"],3,
    "Aceitação inclui UAT, aceitação operacional (backup, segurança), e aceitação contratual/regulatória.")
add(2,2,"Qual a diferença entre teste alfa e beta?",
    ["O teste alfa ocorre em produção; o beta no ambiente do desenvolvedor","O teste beta é sempre realizado antes do teste alfa",
     "Teste alfa e teste beta são termos sinônimos e equivalentes","Alfa ocorre no ambiente da organização desenvolvedora; beta no ambiente dos usuários reais"],3,
    "Alfa é realizado nas instalações do desenvolvedor (por usuários/equipe); beta é feito pelos usuários em seu próprio ambiente.")
add(2,1,"Teste funcional avalia:",
    ["Como o sistema se comporta (desempenho, usabilidade)","A documentação",
     "A estrutura interna do código","O que o sistema faz, conforme requisitos funcionais"],3,
    "Teste funcional verifica funções/comportamento (o que o sistema faz) frente aos requisitos.")
add(2,2,"Qual destes é um exemplo de teste não funcional?",
    ["Verificar o cálculo de um desconto","Avaliar o tempo de resposta sob 1000 usuários simultâneos",
     "Confirmar o fluxo de login","Validar uma regra de negócio"],1,
    "Não funcional avalia atributos de qualidade como desempenho, usabilidade, segurança e confiabilidade (o 'como').")
add(2,1,"Teste de caixa-branca baseia-se em:",
    ["Especificação externa","A estrutura interna do código ou da arquitetura",
     "Experiência do testador","Critérios de aceitação"],1,
    "Caixa-branca (estrutural) deriva e mede testes a partir da estrutura interna (código, fluxo, arquitetura).")
add(2,1,"O teste de confirmação (re-teste) ocorre quando:",
    ["Um novo recurso é criado","Verifica-se se a correção de um defeito realmente o resolveu",
     "Migra-se o ambiente","Encerra-se o projeto"],1,
    "Após corrigir um defeito, re-executa-se o caso que falhou para confirmar a correção.")
add(2,2,"Qual o objetivo do teste de regressão?",
    ["Confirmar exclusivamente a correção de um único defeito específico","Detectar efeitos colaterais: mudanças que quebraram funcionalidades antes funcionais",
     "Avaliar exclusivamente o desempenho do sistema sob carga","Testar apenas os requisitos completamente novos do sistema"],1,
    "A regressão verifica se alterações não introduziram defeitos em partes que antes funcionavam.")
add(2,2,"O que normalmente dispara o teste de manutenção?",
    ["Apenas o lançamento inicial do sistema em produção","Modificações, migrações, atualizações ou aposentadoria do sistema",
     "Somente o surgimento de requisitos completamente novos","A criação inicial dos casos de teste do projeto"],1,
    "Gatilhos típicos: correções/melhorias (modificações), migração de ambiente, atualizações e descontinuação (aposentadoria).")

# ============================================================
# CAPÍTULO 2 — TESTE AO LONGO DO CICLO (continuação, +10)
# ============================================================
add(2,2,"No BDD (Behaviour-Driven Development), os cenários são escritos no formato:",
    ["Pseudo-código técnico voltado exclusivamente para desenvolvedores",
     "Given/When/Then, descrevendo comportamento em linguagem próxima ao negócio",
     "Arquivos XML de configuração do ambiente de teste",
     "Um diagrama de estados representando o fluxo do sistema"],1,
    "BDD usa Given/When/Then (ou equivalente) para descrever comportamentos em linguagem compreensível por negócio e técnicos.")

add(2,2,"Qual diferença essencial existe entre TDD e ATDD?",
    ["TDD e ATDD são abordagens idênticas e intercambiáveis",
     "TDD é guiado por testes unitários do desenvolvedor; ATDD usa testes de aceitação definidos com negócio",
     "O ATDD só pode ser aplicado usando ferramentas de automação de UI",
     "O TDD só pode ser aplicado em projetos totalmente ágeis"],1,
    "TDD: dev escreve teste unitário antes do código. ATDD: equipe define testes de aceitação com stakeholders antes de implementar.")

add(2,2,"Em projetos ágeis com iterações curtas, qual nível de teste é mais desafiador de executar dentro do sprint?",
    ["Teste de componente (unitário), por ser o mais simples de todos",
     "Teste de sistema e de aceitação completos, por exigirem integração e tempo maiores",
     "Revisões de código realizadas pelos próprios desenvolvedores",
     "Testes de regressão unitários executados automaticamente no CI"],1,
    "Testes de sistema e aceitação requerem integração e cenários end-to-end, o que pode ser difícil de concluir dentro de um sprint curto.")

add(2,1,"O que é um 'stub' no contexto de teste de componente?",
    ["Uma ferramenta de automação",
     "Um componente substituto que simula a dependência do componente sob teste (chamado pelo componente)",
     "Um tipo de defeito",
     "Um relatório de teste"],1,
    "Stubs simulam dependências chamadas pelo componente testado (chamada descendente), permitindo isolamento do componente.")

add(2,2,"O teste de integração de sistemas avalia principalmente:",
    ["Apenas a lógica interna de cada módulo isoladamente",
     "As interfaces e interações entre sistemas distintos, incluindo sistemas de terceiros e APIs externas",
     "Somente a interface gráfica voltada para o usuário final",
     "Exclusivamente o desempenho do banco de dados utilizado"],1,
    "Testa as interfaces entre sistemas distintos — APIs, serviços externos, integrações — não a lógica interna de cada um.")

add(2,2,"Qual evento tipicamente NÃO é um gatilho de teste de manutenção?",
    ["Correção de um defeito crítico em produção",
     "Criação do planejamento inicial do projeto",
     "Migração de banco de dados para nova versão",
     "Aposentadoria/descontinuação de um sistema legado"],1,
    "Planejamento inicial é feito antes do sistema existir; os gatilhos de manutenção envolvem modificação, migração ou descontinuação.")

add(2,2,"O teste operacional (aceitação operacional) verifica aspectos como:",
    ["Apenas a lógica de negócio implementada nas funcionalidades",
     "Backup e recuperação, instalação, segurança operacional e procedimentos administrativos",
     "Diretamente o código-fonte da aplicação testada",
     "Exclusivamente os requisitos funcionais do sistema"],1,
    "Aceitação operacional foca em aspectos de operação/suporte: backup, restore, instalação, configuração e segurança operacional.")

add(2,2,"Qual abordagem de integração combina componentes de baixo nível primeiro e vai adicionando componentes de nível mais alto?",
    ["Big-bang",
     "Bottom-up",
     "Top-down",
     "Sanduíche (sandwich)"],1,
    "Bottom-up integra de baixo para cima: começa pelos componentes de nível mais baixo, eliminando a necessidade de stubs mas exigindo drivers.")

add(2,2,"No contexto do teste de sistema, 'caso de uso' (use case) serve como:",
    ["Uma especificação técnica do esquema de banco de dados",
     "Base para projetar cenários de teste que cobrem fluxos de interação ator-sistema",
     "Uma ferramenta de automação de testes de regressão",
     "Um tipo específico de defeito encontrado em produção"],1,
    "Casos de uso descrevem fluxos de interação, servindo de base para cenários de teste de sistema fim-a-fim.")

add(2,2,"A automação de testes de regressão em integração contínua (CI) tem como principal benefício:",
    ["Eliminar completamente a necessidade de testes manuais",
     "Detectar rapidamente regressões introduzidas por novas mudanças, fornecendo feedback rápido à equipe",
     "Reduzir diretamente o número de requisitos do projeto",
     "Substituir totalmente a necessidade do teste de aceitação"],1,
    "Em CI, a automação de regressão executa a cada integração, dando feedback imediato sobre o impacto das mudanças no código existente.")

# ============================================================
# CAPÍTULO 3 — TESTE ESTÁTICO (15)
# ============================================================
add(3,1,"O que caracteriza o teste estático?",
    ["Executar o software com dados","Examinar artefatos sem executar o software",
     "Medir desempenho em runtime","Testar a interface gráfica"],1,
    "Teste estático avalia artefatos (código, requisitos, design) sem executá-los, via revisões e análise estática.")
add(3,1,"Qual destes pode ser alvo de teste estático?",
    ["Apenas o código-fonte","Requisitos, especificações, código, modelos e até contratos",
     "Somente artefatos executáveis","Apenas casos de teste"],1,
    "Praticamente qualquer artefato com estrutura pode ser revisado: requisitos, design, código, user stories, contratos.")
add(3,2,"Qual é um benefício do teste estático?",
    ["Mede exclusivamente o desempenho do sistema em produção","Detecta defeitos cedo, inclusive em requisitos, antes de qualquer execução",
     "Substitui totalmente a necessidade do teste dinâmico","Garante matematicamente a ausência completa de defeitos"],1,
    "Por agir cedo, encontra defeitos (ambiguidades, omissões) antes da execução, reduzindo custo de correção.")
add(3,2,"Qual a principal diferença entre teste estático e dinâmico?",
    ["O teste estático executa o código; o dinâmico nunca executa nada","Dinâmico executa o software; estático examina artefatos sem executá-los",
     "Teste estático e teste dinâmico são completamente equivalentes","O teste estático só pode ser aplicado ao código-fonte"],1,
    "O dinâmico requer execução e revela falhas; o estático examina artefatos e encontra defeitos diretamente.")
add(3,2,"Por que o feedback antecipado e frequente é valioso?",
    ["Aumenta artificialmente o número de defeitos relatados","Permite corrigir cedo, evitando que mal-entendidos se propaguem e fiquem caros",
     "Sempre atrasa a conclusão do projeto, independentemente do contexto","Elimina completamente a necessidade de qualquer tipo de teste"],1,
    "Feedback cedo evita retrabalho caro e mantém o desenvolvimento alinhado às necessidades reais.")
add(3,1,"Qual a sequência geral das atividades de uma revisão?",
    ["Execução → planejamento → relatório","Planejamento → início → revisão individual → comunicação e análise → correção",
     "Análise → modelagem → execução","Início → execução → conclusão"],1,
    "Atividades: planejamento, início (kick-off), revisão individual, comunicação e análise dos resultados, correção e follow-up.")
add(3,1,"Qual papel lidera e modera uma revisão formal?",
    ["Autor","Moderador (facilitador)","Escriba","Gerente"],1,
    "O moderador/facilitador conduz a reunião, garante o processo e a objetividade.")
add(3,2,"Qual a responsabilidade do autor em uma revisão?",
    ["Moderar a reunião e garantir que o processo seja seguido","Criar o artefato e, em geral, ser responsável por corrigi-lo",
     "Registrar todas as anomalias encontradas durante a reunião","Decidir sozinho qual o tipo de revisão será utilizado"],1,
    "O autor é dono do artefato sob revisão e normalmente faz as correções identificadas.")
add(3,1,"Qual o papel do escriba (registrador) na revisão?",
    ["Liderar a discussão","Documentar as anomalias e decisões da reunião",
     "Corrigir o artefato","Aprovar a entrega"],1,
    "O escriba registra anomalias, decisões e novos achados durante a revisão.")
add(3,2,"Uma revisão informal caracteriza-se por:",
    ["Processo totalmente documentado, com métricas e papéis definidos","Ausência de processo formal, baixo custo e resultados não documentados formalmente",
     "Papéis rígidos e claramente definidos para cada participante","Preparação individual obrigatória antes da reunião formal"],1,
    "Revisão informal não segue processo definido nem produz documentação formal; é rápida e barata.")
add(3,2,"O principal objetivo de um walkthrough costuma ser:",
    ["Auditar formalmente a conformidade do artefato com normas","Permitir que o autor conduza os participantes pelo artefato para obter entendimento comum e feedback",
     "Medir precisamente a cobertura de código alcançada pelos testes","Aprovar formalmente o produto antes de seguir para produção"],1,
    "No walkthrough o autor guia os participantes pelo documento, buscando entendimento comum, aprendizado e feedback.")
add(3,2,"A revisão técnica é conduzida principalmente para:",
    ["Treinar exclusivamente novos membros da equipe de teste","Obter consenso técnico e tomar decisões, conduzida por pares qualificados",
     "Documentar formalmente os requisitos do sistema","Substituir totalmente a necessidade do teste dinâmico"],1,
    "A revisão técnica reúne pares tecnicamente qualificados para avaliar qualidade e alcançar consenso/decisões técnicas.")
add(3,2,"A inspeção difere das demais revisões por ser:",
    ["A forma de revisão mais informal e menos estruturada","A mais formal: papéis definidos, métricas e critérios de entrada/saída",
     "Sempre conduzida pessoalmente pelo autor do artefato","Realizada sem qualquer tipo de preparação prévia"],1,
    "A inspeção é a mais formal: processo rígido, papéis, preparação individual, métricas e critérios de entrada/saída.")
add(3,2,"Ao escolher o tipo de revisão, o fator determinante deve ser:",
    ["Apenas a preferência pessoal do autor do artefato","O objetivo da revisão e o risco/criticidade do artefato",
     "Somente o tamanho disponível da equipe de revisão","Exclusivamente a ferramenta de revisão disponível"],1,
    "O tipo é escolhido conforme o objetivo (consenso, conformidade, aprendizado) e a criticidade do artefato.")
add(3,2,"Qual é um fator de sucesso para revisões?",
    ["Usar a revisão para avaliar o desempenho das pessoas","Focar no artefato (não na pessoa) e manter clima construtivo",
     "Não definir objetivos","Revisar tudo na maior formalidade possível"],1,
    "Revisões bem-sucedidas focam o produto, têm objetivos claros, escopo adequado e ambiente sem julgamento pessoal.")

# ============================================================
# CAPÍTULO 3 — TESTE ESTÁTICO (continuação, +10)
# ============================================================
add(3,2,"Qual é um tipo de defeito que o teste estático encontra mas o dinâmico dificilmente detecta?",
    ["Uma falha de desempenho detectada sob carga real",
     "Requisito ambíguo ou contraditório antes de qualquer implementação",
     "Um erro de runtime detectado em módulo já executado",
     "Uma falha visual na interface gráfica do usuário"],1,
    "Revisões estáticas encontram defeitos em requisitos (ambiguidades, omissões) antes que o código seja escrito.")

add(3,1,"Qual ferramenta apoia o teste estático por meio de análise automatizada do código-fonte?",
    ["Ferramenta de execução de testes de desempenho",
     "Ferramenta de análise estática (linter/analisador de código)",
     "Ferramenta de gravação e reprodução de UI",
     "Gerenciador de configuração"],1,
    "Ferramentas de análise estática examinam o código sem executá-lo, detectando padrões suspeitos, violações e vulnerabilidades.")

add(3,2,"O que é um critério de entrada (entry criterion) para uma revisão formal?",
    ["Apenas o número mínimo de participantes exigido para a reunião",
     "Uma condição que deve ser satisfeita antes de iniciar a revisão (ex.: artefato completo e disponível)",
     "Somente a duração máxima permitida para a realização da reunião",
     "Exclusivamente o título formal do documento submetido à revisão"],1,
    "Critérios de entrada garantem que a revisão só começa quando o artefato e os pré-requisitos estão prontos, evitando desperdício.")

add(3,2,"Um anti-padrão comum em revisões é:",
    ["Focar exclusivamente nos defeitos encontrados no artefato",
     "Usar a revisão para avaliar o desempenho ou criticar o autor como pessoa",
     "Preparar-se individualmente e com cuidado antes da reunião",
     "Registrar cuidadosamente todas as anomalias encontradas"],1,
    "Revisar a pessoa em vez do produto cria clima negativo, inibe participação e desvia do objetivo de melhorar o artefato.")

add(3,2,"Qual é o critério de saída típico de uma inspeção formal?",
    ["Todos os participantes concordarem totalmente com tudo discutido",
     "Taxa de defeitos abaixo de um limite definido ou todos os defeitos abertos tratados",
     "O tempo previsto para a reunião ter se encerrado",
     "O autor aprovar pessoalmente todos os comentários"],1,
    "Critérios de saída de inspeção incluem limites de densidade de defeitos e resolução de todos os problemas abertos identificados.")

add(3,1,"Qual papel na revisão é responsável por garantir que o processo seja seguido e o ambiente seja produtivo?",
    ["Autor","Moderador (facilitador)","Revisor","Gerente de testes"],1,
    "O moderador facilita a reunião, mantém o foco no artefato, garante o seguimento do processo e gerencia conflitos.")

add(3,2,"A 'revisão baseada em checklist' usa listas para:",
    ["Avaliar formalmente o desempenho individual dos revisores",
     "Guiar os revisores na busca de tipos específicos de defeitos conhecidos",
     "Medir precisamente a cobertura de código dos testes",
     "Automatizar completamente o processo de revisão"],1,
    "Checklists de revisão direcionam a atenção para defeitos típicos (clareza, consistência, completude), aumentando a eficácia.")

add(3,2,"A análise estática por ferramenta pode detectar automaticamente:",
    ["Falhas de usabilidade percebidas subjetivamente pelo usuário",
     "Variáveis não inicializadas, código morto e violações de padrões de codificação",
     "Bugs que só aparecem sob carga intensa de usuários",
     "Erros de lógica de negócio complexos e específicos do domínio"],1,
    "Ferramentas de análise estática detectam padrões problemáticos como variáveis não usadas, referências nulas potenciais e violações de estilo.")

add(3,2,"Qual é a principal diferença entre uma revisão técnica e uma inspeção?",
    ["A inspeção é sempre muito menos formal e rigorosa do que a revisão técnica",
     "A inspeção tem processo mais rígido com papéis definidos, métricas, entrada/saída e acompanhamento; a revisão técnica é menos formal",
     "Apenas a revisão técnica utiliza checklists formais; a inspeção nunca utiliza",
     "A inspeção e a revisão técnica são processos completamente equivalentes na prática"],1,
    "A inspeção é a forma mais formal, com papéis, métricas, critérios de entrada/saída e follow-up rigoroso; a revisão técnica é menos rígida.")

add(3,2,"Por que é importante limitar o tamanho do artefato revisado em uma reunião de revisão?",
    ["Apenas para reduzir o número de participantes convidados",
     "Revisões longas causam fadiga, reduzindo a atenção e a taxa de detecção de defeitos",
     "O tamanho do artefato nunca influencia a qualidade da revisão",
     "Apenas para economizar papel e recursos de impressão"],1,
    "Um artefato muito longo leva à fadiga dos revisores, diminuindo a concentração e a eficácia na detecção de defeitos.")

# ============================================================
# CAPÍTULO 4 — TÉCNICAS DE TESTE (33)
# ============================================================
add(4,2,"As técnicas de teste classificam-se principalmente em:",
    ["Caixa-preta, caixa-branca e baseadas em experiência","Apenas técnicas manuais e técnicas totalmente automatizadas",
     "Somente testes funcionais e testes de carga do sistema","Exclusivamente técnicas estáticas e técnicas dinâmicas"],0,
    "As categorias do syllabus: caixa-preta (especificação), caixa-branca (estrutura) e baseadas em experiência.")
add(4,2,"O particionamento de equivalência (EP) baseia-se na ideia de que:",
    ["Valores de uma mesma partição são tratados igualmente, bastando um representante","Cada valor individual da partição deve ser testado separadamente",
     "Apenas os valores nos limites das partições realmente importam","Não existem partições inválidas a serem consideradas no EP"],0,
    "Em EP, valores de uma partição produzem comportamento equivalente; testa-se um representante por partição.")
add(4,3,"Um campo aceita 1 a 100. Quais partições de equivalência existem (incluindo inválidas)?",
    ["≤0 (inválida), 1–100 (válida) e ≥101 (inválida)","Existe apenas a partição válida de 1 a 100",
     "Apenas as partições 1–50 e 51–100, ambas válidas","Somente os valores extremos 1 e 100 isoladamente"],0,
    "Há três partições: abaixo de 1 (inválida), 1–100 (válida) e acima de 100 (inválida).")
add(4,2,"Em EP, por que testar também partições inválidas?",
    ["Para verificar o tratamento de entradas fora do esperado","Apenas para aumentar artificialmente a contagem de testes",
     "Não é necessário testar partições inválidas em nenhum caso","Exclusivamente para medir o desempenho do sistema sob carga"],0,
    "Partições inválidas verificam se o sistema trata corretamente entradas indevidas (mensagens de erro, rejeição).")
add(4,2,"A análise de valor-fronteira (BVA) é eficaz porque:",
    ["Erros tendem a se concentrar nas fronteiras das partições","Defeitos raramente ocorrem nos limites das partições testadas",
     "Testa exaustivamente todos os valores possíveis da entrada","Ignora completamente as partições válidas e inválidas"],0,
    "Defeitos frequentemente ocorrem nos limites; a BVA complementa o EP testando as fronteiras das partições.")
add(4,3,"Um campo aceita 18 a 65. Quais valores usar na BVA de 2 valores?",
    ["17, 18, 65, 66","18 e 65","0 e 100","17, 19, 64, 66"],0,
    "BVA de 2 valores testa, em cada limite, o valor da fronteira e o adjacente do outro lado: 17/18 e 65/66.")
add(4,2,"Na BVA de 3 valores, para o limite superior 65, quais valores são testados?",
    ["64, 65 e 66","65 apenas","63, 64, 65","65, 66, 67"],0,
    "A BVA de 3 valores testa o limite e os dois vizinhos: 64, 65 e 66 para a fronteira 65.")
add(4,3,"Senhas devem ter de 8 a 16 caracteres. Pela BVA de 2 valores, os tamanhos de teste no limite inferior são:",
    ["7 e 8","8 e 9","6, 7, 8","8 e 16"],0,
    "No limite inferior (8), a BVA de 2 valores testa 7 (inválido) e 8 (válido).")
add(4,2,"Uma tabela de decisão é mais indicada quando:",
    ["Há combinações de condições que levam a ações diferentes (regras de negócio)","O comportamento do sistema depende apenas do estado atual",
     "Existe apenas uma única entrada simples a ser testada","O foco principal do teste é exclusivamente o desempenho"],0,
    "Tabelas de decisão modelam regras de negócio com combinações de condições e ações resultantes.")
add(4,3,"Uma regra concede frete grátis se (é assinante) E (compra > R$200). Com 2 condições binárias, quantas regras tem a tabela completa?",
    ["2","3","4","8"],2,
    "Duas condições binárias geram 2² = 4 combinações (regras) na tabela completa.")
add(4,3,"Numa tabela de decisão, um desconto é dado se 'cliente VIP' = Sim e 'cupom válido' = Sim. Para a combinação VIP=Sim, cupom=Não, a ação esperada é:",
    ["Não conceder desconto","Conceder desconto","Erro de sistema","Conceder meio desconto"],0,
    "A ação só ocorre quando ambas as condições são verdadeiras; com cupom=Não, não há desconto.")
add(4,2,"Em uma tabela de decisão, condições e ações representam, respectivamente:",
    ["As entradas/causas e os resultados/efeitos esperados","Apenas as saídas do sistema e as entradas do usuário",
     "Os estados do sistema e as transições entre eles","Os casos de teste e os dados utilizados na execução"],0,
    "Condições são as causas (entradas); ações são os efeitos (resultados) esperados para cada regra.")
add(4,2,"O teste de transição de estados é apropriado para sistemas que:",
    ["Mudam de comportamento conforme o estado atual e os eventos recebidos","Não possuem nenhuma memória de estado interno",
     "Processam exclusivamente dados em lote, sem interação","Não possuem nenhuma interface de interação com o usuário"],0,
    "Modela estados, eventos, transições e ações — ideal para sessões, protocolos e workflows.")
add(4,2,"Em um diagrama de estados, uma 'transição inválida' é:",
    ["Um evento que não deveria provocar mudança a partir do estado atual","Uma transição permitida e claramente definida no diagrama",
     "O estado inicial do diagrama de transições do sistema","Uma ação de saída executada ao deixar o estado atual"],0,
    "Transições inválidas são pares estado/evento sem transição definida; testá-las verifica robustez.")
add(4,3,"Um caixa eletrônico exige cartão antes de aceitar a senha. Tentar digitar a senha sem inserir o cartão testa:",
    ["Uma transição inválida (evento inesperado para o estado)","Uma transição válida e prevista no diagrama de estados",
     "O estado final alcançado após a transação completa","Uma ação de entrada executada ao chegar no estado"],0,
    "Digitar a senha no estado 'aguardando cartão' é um evento inválido para aquele estado — uma transição inválida.")
add(4,2,"A cobertura de transições válidas (0-switch) exige:",
    ["Exercitar cada transição válida individual ao menos uma vez","Cobrir todos os pares de transições",
     "Cobrir transições inválidas","Cobrir todos os estados apenas"],0,
    "A cobertura 0-switch (de transições simples) cobre cada transição válida pelo menos uma vez.")
add(4,2,"Para escolher entre EP, BVA, tabela de decisão e transição de estados, o critério principal é:",
    ["A natureza do problema: faixas, combinações de regras ou comportamento por estado","Exclusivamente a ferramenta de automação disponível no projeto",
     "Somente a preferência pessoal do testador responsável","Apenas o tamanho da equipe de teste disponível"],0,
    "A técnica adequada depende da estrutura do problema: faixas (EP/BVA), regras (tabela), comportamento por estado (transição).")
add(4,1,"As técnicas de caixa-branca derivam testes a partir de:",
    ["A estrutura interna: código, fluxo de controle e arquitetura","Requisitos do usuário",
     "Experiência do testador","Critérios de aceitação"],0,
    "Caixa-branca usa a estrutura interna (instruções, decisões, fluxos) como base dos testes.")
add(4,2,"A cobertura de instruções (statement coverage) mede:",
    ["O percentual de instruções executáveis que foram executadas","O percentual de decisões verdadeiras e falsas exercitadas",
     "O número total de caminhos possíveis no código","O número total de condições presentes no código"],0,
    "Cobertura de instruções = instruções executadas ÷ total de instruções executáveis.")
add(4,3,"Um trecho tem 10 instruções executáveis; um teste executou 7. A cobertura de instruções é:",
    ["70%","100%","7%","30%"],0,
    "7 de 10 instruções executadas = 70% de cobertura de instruções.")
add(4,2,"A cobertura de decisões (branch coverage) exige:",
    ["Exercitar cada decisão como verdadeira e como falsa ao menos uma vez","Executar cada instrução do código ao menos uma vez",
     "Cobrir absolutamente todos os caminhos possíveis do código","Testar todas as condições isoladamente, sem combiná-las"],0,
    "Cobertura de decisões cobre os resultados V e F de cada decisão pelo menos uma vez.")
add(4,3,"Em um 'if' sem 'else', qual cobertura garante testar também o caminho em que a condição é falsa?",
    ["Cobertura de decisões","Cobertura de instruções","Nenhuma","Cobertura de funções"],0,
    "Com um if sem else, 100% de instruções pode ser atingido sem testar o ramo falso; a cobertura de decisões força os dois resultados.")
add(4,2,"Qual afirmação sobre a força das coberturas é correta?",
    ["100% de cobertura de decisões implica 100% de cobertura de instruções, mas não o contrário","A cobertura de instruções é sempre mais forte que a de decisões",
     "Cobertura de instruções e cobertura de decisões são equivalentes","A cobertura de decisões nunca inclui a cobertura de instruções"],0,
    "Cobertura de decisões é mais forte: atingir 100% dela garante 100% de instruções; o inverso não vale.")
add(4,2,"Qual o valor do teste de caixa-branca?",
    ["Revelar trechos de código não exercitados e medir a minúcia (thoroughness) dos testes","Substituir completamente a necessidade do teste de caixa-preta",
     "Eliminar totalmente a necessidade de medir cobertura","Testar diretamente os requisitos de negócio do sistema"],0,
    "Caixa-branca mostra o que o código realmente exercita, revelando lacunas que a especificação não evidencia.")
add(4,2,"A suposição de erro (error guessing) consiste em:",
    ["Antecipar defeitos prováveis com base em experiência, defeitos passados e intuição","Adivinhar aleatoriamente a senha de acesso ao sistema",
     "Gerar dados de teste completamente aleatórios e sem critério","Medir exclusivamente a cobertura de código alcançada"],0,
    "Error guessing usa experiência e conhecimento de falhas comuns para criar testes que exponham defeitos prováveis.")
add(4,2,"No teste exploratório, o testador:",
    ["Aprende, projeta e executa testes simultaneamente, frequentemente com test charters","Segue rigorosamente scripts de teste pré-definidos e detalhados",
     "Apenas mede o desempenho do sistema sob diferentes cargas","Não registra absolutamente nada do que foi executado"],0,
    "O exploratório combina aprendizado, design e execução em tempo real, muitas vezes guiado por charters e em sessões cronometradas.")
add(4,2,"O teste baseado em checklist apoia-se em:",
    ["Uma lista de itens/condições a verificar, derivada de experiência e heurísticas","Diagramas de estado representando o comportamento do sistema",
     "A cobertura de código alcançada pelos testes executados","Tabelas de decisão com as regras de negócio combinadas"],0,
    "Checklists reúnem itens a verificar (heurísticas, lições aprendidas), guiando o teste sem scripts detalhados.")
add(4,2,"Quando as técnicas baseadas em experiência são mais úteis?",
    ["Quando a documentação é escassa, o tempo é curto ou para complementar técnicas formais","Apenas quando há especificação completa, detalhada e estável",
     "Apenas em sistemas críticos de segurança ou de saúde","Somente quando todos os testes já estão automatizados"],0,
    "São valiosas com documentação limitada/tempo curto e como complemento às técnicas formais para achar defeitos que escapam.")
add(4,1,"Os '3 C's' da escrita colaborativa de user stories são:",
    ["Card (cartão), Conversation (conversa) e Confirmation (confirmação)","Code, Compile, Commit",
     "Cost, Customer, Contract","Create, Check, Close"],0,
    "Os 3 C's: Card (resumo), Conversation (detalhamento) e Confirmation (critérios de aceitação).")
add(4,2,"Critérios de aceitação de uma user story servem para:",
    ["Definir as condições que a story deve satisfazer para ser aceita","Estimar o custo total de desenvolvimento da story",
     "Medir diretamente a cobertura de código alcançada","Substituir completamente a necessidade de qualquer teste"],0,
    "Critérios de aceitação descrevem o que torna a story 'pronta/aceita', servindo de base para casos de teste.")
add(4,2,"No ATDD (Acceptance Test-Driven Development), os testes de aceitação são:",
    ["Definidos colaborativamente antes da implementação, a partir dos critérios de aceitação","Sempre escritos somente após a entrega da funcionalidade",
     "Apenas testes automatizados executados na interface gráfica","Totalmente opcionais e dispensáveis em qualquer projeto"],0,
    "No ATDD, equipe, negócio e teste definem juntos os testes de aceitação antes de codificar, guiando a implementação.")
add(4,2,"Um requisito descreve faixas de valores e também regras combinando vários campos. A melhor estratégia é:",
    ["Combinar técnicas: EP/BVA para as faixas e tabela de decisão para as combinações","Usar apenas a análise de valor-fronteira para tudo",
     "Usar somente a técnica de transição de estados para tudo","Usar somente o teste exploratório, sem técnicas formais"],0,
    "Problemas mistos pedem combinação de técnicas conforme cada aspecto: faixas (EP/BVA) e regras combinadas (tabela de decisão).")
add(4,2,"A cobertura, em técnicas de teste, mede:",
    ["O grau em que itens de cobertura definidos foram exercitados pelos testes","A quantidade total de defeitos encontrados pelos testes",
     "O tempo total necessário para executar todos os testes","O número de testadores envolvidos na execução dos testes"],0,
    "Cobertura expressa quanto dos itens de cobertura (partições, decisões, transições) os testes exercitaram.")

# ============================================================
# CAPÍTULO 4 — TÉCNICAS DE TESTE (continuação, +22)
# ============================================================
add(4,3,"Um campo de temperatura aceita de -10 a 50°C. Pela BVA de 2 valores, quais são os 4 valores de fronteira a testar?",
    ["-11, -10, 50, 51",
     "-10 e 50",
     "-10, 0, 50, 100",
     "-9, -10, 49, 50"],0,
    "BVA de 2 valores testa o valor da fronteira e o imediatamente adjacente do lado inválido: -11/-10 (limite inferior) e 50/51 (limite superior).")

add(4,3,"Uma tabela de decisão tem 3 condições binárias. Quantas regras a tabela completa (sem colapso) possui?",
    ["3","6","8","9"],2,
    "Três condições binárias geram 2³ = 8 combinações (regras) na tabela de decisão completa.")

add(4,3,"Um sistema de desconto aplica desconto se: (cliente premium = Sim) OU (valor do pedido > R$500). Quantas regras distintas existem com 2 condições binárias?",
    ["4","2","6","8"],0,
    "Duas condições binárias geram 2² = 4 regras; a tabela completa tem 4 colunas independentemente do operador lógico.")

add(4,3,"Numa máquina de estados de conta bancária: estados = {Ativa, Bloqueada, Encerrada}. Quantas transições inválidas existem se há apenas 4 transições válidas definidas?",
    ["4","5","8","6"],1,
    "Com 3 estados, há 3×3 = 9 células na matriz (incluindo auto-transições); com 4 válidas, há 9-4 = 5 transições inválidas a verificar.")

add(4,3,"Um trecho de código tem 20 instruções executáveis. Um conjunto de testes executou 15. Qual é a cobertura de instruções?",
    ["75%","15%","85%","20%"],0,
    "Cobertura de instruções = executadas ÷ total = 15 ÷ 20 = 75%.")

add(4,3,"Um método tem 4 decisões (if/else). Para 100% de cobertura de decisões, quantos resultados de decisão precisam ser exercitados no mínimo?",
    ["8","4","2","16"],0,
    "Cada decisão tem 2 resultados (V/F); 4 decisões × 2 resultados = 8 resultados mínimos a exercitar para 100% de cobertura de decisões.")

add(4,3,"Um campo aceita idades de 0 a 120 anos (inteiros). Pela BVA de 3 valores, quais valores testar no limite inferior (0)?",
    ["-1, 0 e 1",
     "0 e 1",
     "0, 1 e 2",
     "-2, -1 e 0"],0,
    "BVA de 3 valores testa o limite e seus dois vizinhos: para o limite inferior 0, testam-se -1, 0 e 1.")

add(4,3,"Um formulário tem campo 'quantidade' que aceita apenas 1, 2 ou 3. Pela EP, qual partição inválida existe acima do limite?",
    ["Valores ≥ 4",
     "Não existe partição inválida superior",
     "Valores = 0",
     "Valores negativos"],0,
    "A partição inválida superior inclui todos os valores ≥ 4 (acima do máximo 3); valores ≤ 0 formam a partição inválida inferior.")

add(4,2,"Em uma máquina de estados com cobertura de todas as transições (0-switch), qual cenário de login é mais adequado?",
    ["Testar cada transição possível ao menos uma vez: login com sucesso, senha errada, bloqueio de conta, logout",
     "Testar apenas o cenário de login realizado com sucesso, ignorando os demais casos",
     "Testar somente o estado inicial do sistema de login, sem considerar as transições",
     "Testar apenas as transições inválidas entre os estados, ignorando as válidas"],0,
    "Cobertura 0-switch exige exercitar cada transição válida individualmente, cobrindo todos os arcos do diagrama de estados.")

add(4,2,"Ao testar um sistema de controle de semáforo (Verde → Amarelo → Vermelho → Verde), qual técnica é mais indicada?",
    ["Teste de transição de estados, pois o comportamento depende do estado atual",
     "Particionamento de equivalência das cores do semáforo",
     "Análise de valor-fronteira dos tempos de cada fase",
     "Tabela de decisão combinando as cores do semáforo"],0,
    "Semáforos têm estados bem definidos e transições sequenciais — a técnica de transição de estados modela esse comportamento com precisão.")

add(4,3,"Em EP, ao testar um campo de nota de 0 a 10 (números inteiros), um testador usa apenas o valor 5. Qual é o problema dessa abordagem?",
    ["Testa apenas a partição válida; as partições inválidas (< 0 e > 10) não são cobertas",
     "O valor 5 está correto; a abordagem é adequada",
     "O EP exige testar todos os valores de 0 a 10",
     "O EP não se aplica a números inteiros"],0,
    "EP exige ao menos um representante de cada partição — válidas e inválidas; usar só valor 5 ignora as partições inválidas abaixo de 0 e acima de 10.")

add(4,3,"Um programa contém o trecho: if (x > 0) { y = x * 2; } z = y + 1; Com apenas um caso de teste onde x=5, qual cobertura é atingida?",
    ["100% de instruções executadas no caminho, mas não 100% de decisões (ramo falso não testado)",
     "100% de cobertura de instruções e também de decisões",
     "Nenhuma cobertura de instruções ou decisões é atingida",
     "100% de cobertura de decisões, mas não de instruções"],0,
    "Com x=5 (condição verdadeira), y=x*2 e z=y+1 são executados. O ramo falso (x≤0) não é testado, então cobertura de decisões < 100%.")

add(4,2,"O erro guessing (suposição de erro) é mais eficaz quando o testador:",
    ["Tem experiência com o domínio, conhece defeitos passados e entende erros comuns de implementação",
     "Nunca viu o sistema antes e não conhece o domínio",
     "Usa apenas técnicas formais, sem nenhuma intuição",
     "Não conhece o código nem a arquitetura do sistema"],0,
    "A eficácia do error guessing cresce com a experiência do testador: conhecimento de domínio e histórico de defeitos orientam a intuição.")

add(4,2,"O teste exploratório em sessões cronometradas (session-based testing) usa 'test charters' para:",
    ["Definir a missão da sessão: escopo, objetivo e área a explorar, sem detalhar cada passo",
     "Documentar detalhadamente todos os passos antes de executar",
     "Substituir totalmente o planejamento formal de teste",
     "Medir exclusivamente a cobertura de código alcançada"],0,
    "Charters definem o foco da sessão exploratória (o que explorar e por quê) sem pré-determinar os passos exatos de execução.")

add(4,2,"Quando se usa uma checklist de teste em vez de casos de teste detalhados?",
    ["Quando se quer agilidade e experiência do testador para decidir como verificar cada item, sem scripts rígidos",
     "Apenas quando há muito tempo disponível no cronograma do projeto de teste",
     "Somente quando o sistema é extremamente crítico e exige forte documentação",
     "Apenas quando a automação completa dos testes não é tecnicamente possível"],0,
    "Checklists oferecem flexibilidade: o testador decide como verificar cada item, usando seu julgamento — adequado quando scripts detalhados seriam excessivos.")

add(4,2,"No ATDD, quem define os critérios de aceitação antes da implementação?",
    ["Equipe de desenvolvimento, representantes de negócio e testadores colaborativamente",
     "Apenas o testador, sem participação de mais ninguém",
     "Apenas o product owner, isoladamente, sem a equipe",
     "Exclusivamente o gerente de projetos, sozinho"],0,
    "ATDD é colaborativo: negócio, dev e teste definem juntos os critérios/testes de aceitação antes de implementar a funcionalidade.")

add(4,3,"Qual técnica de caixa-preta seria mais indicada para testar regras de elegibilidade de empréstimo que combinam renda, histórico de crédito e tempo de emprego?",
    ["Tabela de decisão, pois há múltiplas condições combinadas que levam a decisões diferentes",
     "Análise de valor-fronteira da faixa de renda apenas",
     "Teste de transição de estados do processo de aprovação",
     "Cobertura de instruções do sistema de aprovação de crédito"],0,
    "Quando o resultado depende de combinações de múltiplas condições (regras de negócio), a tabela de decisão é a técnica mais indicada.")

add(4,3,"Um campo aceita valores de R$1,00 a R$9.999,99. Na BVA de 2 valores, quais são os valores de teste para o limite inferior?",
    ["R$0,99 e R$1,00",
     "R$1,00 e R$9.999,99",
     "R$1,00 e R$1,01",
     "R$0,00 e R$1,00"],0,
    "No limite inferior R$1,00, a BVA de 2 valores testa o valor abaixo do limite (R$0,99, inválido) e o próprio limite (R$1,00, válido).")

add(4,2,"Em um diagrama de estados, o que a cobertura de 'switch-1' (transição de pares) garante além da cobertura 0-switch?",
    ["Que pares de transições consecutivas (sequências de 2) são exercitados, aumentando a profundidade da cobertura",
     "Nada de adicional além do que a cobertura 0-switch básica já garante sozinha",
     "Cobertura completa de todas as condições isoladas, sem considerar combinações",
     "Cobertura completa de todas as instruções executáveis presentes no código"],0,
    "Switch-1 cobre sequências de 2 transições (pares), detectando erros que só aparecem em combinações de transições, e é mais forte que 0-switch.")

add(4,2,"A combinação de EP e BVA é mais eficaz que usar cada técnica isoladamente porque:",
    ["EP e BVA são tecnicamente equivalentes e intercambiáveis",
     "A BVA substitui completamente a necessidade do EP",
     "EP reduz o espaço de teste; BVA complementa testando os pontos mais propensos a defeitos (fronteiras)",
     "O EP testa apenas valores válidos; já a BVA testa apenas valores inválidos"],2,
    "EP define as partições, reduzindo o espaço; BVA aprofunda nos limites dessas partições, onde defeitos são mais frequentes.")

add(4,2,"Por que a cobertura de 100% de instruções não é suficiente como único critério de qualidade?",
    ["Porque é praticamente impossível de atingir na prática",
     "Porque é muito cara e demorada de se atingir",
     "Porque não garante que todos os ramos de decisão foram testados, podendo deixar caminhos sem teste",
     "Porque essa métrica não é aceita pelo syllabus oficial"],2,
    "100% de instruções pode ser atingido sem testar o ramo falso de um if sem else; a cobertura de decisões é mais forte e mais reveladora.")

add(4,2,"Qual é o objetivo principal do teste baseado em experiência (experience-based testing)?",
    ["Substituir totalmente as técnicas formais em todos os casos",
     "Gerar casos de teste completamente aleatórios e sem critério",
     "Aproveitar o conhecimento e a intuição do testador para encontrar defeitos que técnicas formais podem perder",
     "Medir exclusivamente a cobertura de código do sistema"],2,
    "Técnicas baseadas em experiência complementam as formais, explorando o conhecimento do testador sobre defeitos comuns e comportamentos inesperados.")

# ============================================================
# CAPÍTULO 5 — GERENCIAMENTO (27)
# ============================================================
add(5,1,"O plano de teste tem como propósito principal:",
    ["Listar todos os defeitos","Substituir os casos de teste",
     "Documentar objetivos, escopo, abordagem, recursos e critérios do esforço de teste","Aprovar a entrega"],2,
    "O plano comunica objetivos, escopo, abordagem, recursos, cronograma, riscos e critérios de entrada/saída.")
add(5,2,"Qual a diferença entre estratégia de teste e abordagem de teste?",
    ["Estratégia e abordagem de teste são termos completamente sinônimos","A abordagem de teste é sempre mais ampla que a estratégia",
     "A estratégia é uma descrição geral/organizacional; a abordagem é a aplicação adaptada a um projeto específico","A estratégia de teste só existe em projetos totalmente ágeis"],2,
    "A estratégia descreve o nível geral/organizacional; a abordagem adapta a estratégia ao contexto do projeto.")
add(5,1,"Critérios de entrada (entry criteria) definem:",
    ["Quando parar o teste","O número de defeitos aceitável",
     "As pré-condições para iniciar uma atividade de teste","A cobertura final"],2,
    "Critérios de entrada são as condições necessárias para começar (ambiente pronto, casos aprovados, dados disponíveis).")
add(5,2,"Critérios de saída (exit criteria) servem para:",
    ["Determinar exatamente quando o teste deve ser iniciado","Estimar o esforço total necessário para o teste",
     "Determinar quando uma atividade/nível de teste pode ser considerado concluído","Selecionar as ferramentas adequadas para o teste"],2,
    "Critérios de saída definem quando encerrar (cobertura atingida, defeitos abertos abaixo do limite, prazo cumprido).")
add(5,2,"Em métodos ágeis, 'Definition of Done' (DoD) funciona como:",
    ["Um critério de entrada para iniciar o desenvolvimento do item","Um relatório de defeitos encontrados durante a sprint",
     "Um conjunto de critérios de saída para considerar um item realmente concluído","Um plano de teste detalhado para toda a sprint"],2,
    "A DoD é um conjunto de critérios de saída que define quando um item de trabalho está realmente pronto.")
add(5,2,"A estimativa baseada em ratios (proporções) usa:",
    ["Apenas a opinião subjetiva de especialistas do time","Geração completamente aleatória de números de horas",
     "Proporções históricas (e.g., relação entre esforço de dev e de teste) para projetar o esforço","A cobertura de código já alcançada em projetos anteriores"],2,
    "A técnica de ratios aplica proporções de projetos passados (ex.: % do esforço destinado ao teste) para estimar.")
add(5,2,"A estimativa por extrapolação (metrics-based) baseia-se em:",
    ["Pura intuição e achismo, sem nenhum dado histórico","Apenas no orçamento disponível para o projeto atual",
     "Dados/medições de iterações ou projetos anteriores, extrapolando para o atual","Exclusivamente no número de testadores disponíveis"],2,
    "A abordagem baseada em métricas usa dados históricos para extrapolar o esforço esperado.")
add(5,2,"A estimativa baseada em especialistas (expert-based) caracteriza-se por:",
    ["Ignorar completamente a experiência de quem conhece as tarefas","Usar somente fórmulas matemáticas, sem nenhum julgamento humano",
     "Apoiar-se no julgamento de quem conhece as tarefas (ex.: Wideband Delphi/Planning Poker)","Dispensar totalmente a necessidade de consenso entre especialistas"],2,
    "A abordagem baseada em especialistas usa o conhecimento dos responsáveis pelas tarefas, e.g., Planning Poker/Delphi.")
add(5,2,"Na priorização de casos por risco, os testes executados primeiro são:",
    ["Os mais rápidos","Os mais antigos",
     "Os que cobrem os itens de maior risco","Os escolhidos aleatoriamente"],2,
    "A priorização baseada em risco executa antes os testes de maior risco (probabilidade × impacto).")
add(5,2,"Na priorização baseada em cobertura, a ordem é definida por:",
    ["Apenas o custo de execução de cada caso de teste","Somente o tamanho do código exercitado pelo teste",
     "Quanto cada teste adiciona de cobertura ainda não atingida","A ordem alfabética dos nomes dos casos de teste"],2,
    "A priorização por cobertura ordena para maximizar rapidamente a cobertura ainda não exercitada.")
add(5,2,"A 'pirâmide de testes' sugere que devemos ter:",
    ["Mais testes de UI no topo do que testes de unidade","Apenas testes manuais executados por pessoas, sem automação",
     "Muitos testes de unidade na base e poucos testes de UI/E2E no topo","Um número exatamente igual de testes em cada nível"],2,
    "A pirâmide recomenda muitos testes rápidos/baratos (unidade) na base e poucos lentos/frágeis (UI/E2E) no topo.")
add(5,2,"Os 'quadrantes de teste' (testing quadrants) ajudam a:",
    ["Medir diretamente a cobertura de código alcançada pelos testes automatizados","Estimar os custos totais do projeto de teste em todas as fases",
     "Classificar tipos de teste por foco em negócio/tecnologia e por apoiar a equipe ou criticar o produto","Definir formalmente o Definition of Done utilizado pela equipe ágil"],2,
    "Os quadrantes organizam os testes (apoio à equipe vs. crítica ao produto; foco negócio vs. tecnologia) para planejar a cobertura.")
add(5,1,"Em gestão de teste, 'risco' é definido como:",
    ["Um defeito encontrado","Uma falha em produção",
     "Um evento futuro possível com consequências negativas","Um caso de teste reprovado"],2,
    "Risco é a possibilidade de um evento futuro com efeito negativo; combina probabilidade e impacto.")
add(5,2,"Como se determina o nível de um risco?",
    ["Multiplicando o custo total pelo prazo do projeto","Multiplicando a severidade pela prioridade do defeito",
     "Probabilidade de ocorrência combinada ao impacto do dano","Pelo número total de defeitos já encontrados"],2,
    "Nível de risco = probabilidade de ocorrência × impacto (magnitude do dano).")
add(5,2,"Qual a diferença entre risco de produto e risco de projeto?",
    ["Risco de produto e risco de projeto são exatamente o mesmo conceito","O risco de projeto é sempre de natureza puramente técnica e nunca gerencial",
     "Risco de produto afeta a qualidade do produto; risco de projeto afeta a capacidade de atingir os objetivos do projeto","O risco de produto envolve apenas questões relacionadas ao prazo de entrega"],2,
    "Risco de produto: o produto pode falhar/insatisfazer. Risco de projeto: prazo, custo, recursos, fornecedores.")
add(5,2,"Qual destes é um exemplo de risco de PROJETO?",
    ["Um cálculo financeiro incorreto exibido no sistema","Uma falha de segurança detectada na tela de login",
     "Atraso na entrega por falta de pessoal qualificado","Lentidão do sistema sob carga elevada de usuários"],2,
    "Falta de recursos/atrasos são riscos de projeto; os demais são riscos de produto (qualidade).")
add(5,2,"Qual destes é um exemplo de risco de PRODUTO?",
    ["O orçamento total do projeto foi completamente estourado","Um fornecedor externo atrasou a entrega do componente",
     "Vazamento de dados por falha de segurança","A equipe de teste ficou sem treinamento adequado"],2,
    "Falha de segurança afeta a qualidade do produto; os demais são riscos de projeto.")
add(5,2,"O teste baseado em risco usa a avaliação de risco para:",
    ["Eliminar completamente a documentação do processo de teste","Definir os salários da equipe de teste do projeto",
     "Decidir o que testar, quanto e em que ordem, alocando esforço conforme o risco","Escolher a linguagem de programação usada no sistema"],2,
    "O risco orienta seleção, profundidade e priorização do teste, concentrando esforço onde o risco é maior.")
add(5,2,"A avaliação de risco (risk assessment) compreende:",
    ["Somente corrigir os defeitos já identificados no sistema","Executar diretamente os testes planejados no cronograma",
     "Identificar riscos e analisá-los (estimar probabilidade e impacto)","Aprovar formalmente a entrega final do produto"],2,
    "A avaliação inclui identificação dos riscos e sua análise (probabilidade e impacto) para priorização.")
add(5,2,"Como o nível de risco influencia o esforço de teste?",
    ["O nível de risco nunca influencia o esforço de teste","Riscos altos são sempre ignorados no planejamento do teste",
     "Maior risco implica testes mais minuciosos, mais cedo e por pessoal mais experiente","Sempre reduz a cobertura de teste necessária"],2,
    "Itens de maior risco recebem técnicas mais rigorosas, início mais cedo e, por vezes, revisão independente.")
add(5,2,"O propósito do monitoramento de teste é:",
    ["Escrever os casos de teste detalhados do projeto","Corrigir diretamente o código-fonte da aplicação",
     "Fornecer visibilidade do progresso comparando o real com o planejado","Selecionar as ferramentas de automação adequadas"],2,
    "O monitoramento coleta informações sobre o andamento para comparar com o plano e apoiar o controle.")
add(5,1,"Qual destas é uma métrica típica de teste?",
    ["Cor do tema da IDE","Salário do time",
     "Percentual de casos executados e taxa de aprovação","Número de reuniões"],2,
    "Métricas comuns: casos planejados/executados/aprovados/reprovados, cobertura, densidade e tendência de defeitos.")
add(5,2,"Um relatório de progresso de teste destina-se principalmente a:",
    ["Substituir completamente o plano de teste original","Encerrar formalmente o projeto antes do previsto",
     "Informar as partes interessadas sobre o andamento e apoiar decisões durante o teste","Listar todos os requisitos funcionais do sistema"],2,
    "O relatório de progresso comunica status, riscos e resultados às partes interessadas durante a execução.")
add(5,1,"O relatório de conclusão de teste é produzido:",
    ["Antes de iniciar o teste","Diariamente",
     "Ao final de uma atividade/marco, resumindo o que foi feito e os resultados","A cada defeito"],2,
    "O relatório de conclusão resume resultados, cobertura, qualidade alcançada e lições, ao fim de um nível/marco.")
add(5,2,"A gestão de configuração apoia o teste ao:",
    ["Aumentar artificialmente o número de defeitos relatados","Substituir completamente o plano de teste do projeto",
     "Garantir versões/identificação consistentes de itens de teste e testware, com rastreabilidade","Eliminar totalmente a necessidade de controle de versão"],2,
    "A gestão de configuração mantém integridade e rastreabilidade de itens sob teste e do testware (versões, baselines).")
add(5,1,"O que um bom relatório de defeito deve conter?",
    ["Apenas o título","Somente a severidade",
     "Identificação, descrição, passos para reproduzir, resultado esperado/obtido, severidade e prioridade","O nome do desenvolvedor culpado"],2,
    "Relatórios eficazes trazem id, descrição, passos, esperado vs. obtido, ambiente, severidade e prioridade.")
add(5,2,"Qual a diferença entre severidade e prioridade de um defeito?",
    ["Severidade e prioridade são exatamente o mesmo conceito","A prioridade é sempre definida exclusivamente pelo desenvolvedor",
     "Severidade mede o impacto técnico; prioridade mede a urgência de correção sob a ótica do negócio","A severidade depende diretamente do prazo de entrega"],2,
    "Severidade = impacto no sistema; prioridade = urgência de corrigir; podem ser independentes entre si.")

# ============================================================
# CAPÍTULO 5 — GERENCIAMENTO (continuação, +18)
# ============================================================
add(5,3,"Um risco tem probabilidade de ocorrência de 30% e impacto avaliado em 4 (escala 1–5). Qual é o nível de risco?",
    ["0,3","4,3","1,2","7"],2,
    "Nível de risco = probabilidade × impacto = 0,30 × 4 = 1,2 (em escala numérica).")

add(5,3,"Dois riscos: Risco A (probabilidade 20%, impacto 5) e Risco B (probabilidade 50%, impacto 2). Qual deve ser priorizado?",
    ["Risco A, nível 1,0 < Risco B 1,0 — empate; prioriza o que for mais barato de mitigar",
     "Risco B por ter maior probabilidade",
     "Risco A (nível 1,0) e Risco B (nível 1,0) têm o mesmo nível; outros fatores decidem",
     "Risco A por ter maior impacto"],2,
    "Nível A = 0,20×5 = 1,0; Nível B = 0,50×2 = 1,0 — empate em nível de risco; critérios secundários (custo de mitigação, visibilidade) decidem.")

add(5,2,"A técnica de estimativa de teste por 'Planning Poker' é uma variante de:",
    ["Uma variante da estimativa baseada em ratios históricos",
     "Uma variante da estimativa por extrapolação de métricas",
     "Estimativa baseada em especialistas (Wideband Delphi), usando consenso do time",
     "Uma técnica de análise formal de pontos de função"],2,
    "Planning Poker é uma variação do Wideband Delphi: cada membro vota secretamente e o time discute até convergir, aproveitando a expertise coletiva.")

add(5,2,"Uma estimativa de esforço de teste baseada em ratios usa a proporção histórica de que o teste consome 30% do esforço total. Se o desenvolvimento está estimado em 1000h, o esforço de teste estimado é:",
    ["300h","700h","30h","1300h"],0,
    "Ratio de 30%: esforço de teste = 30% × 1000h = 300h.")

add(5,2,"A pirâmide de testes coloca testes de contrato/API no nível intermediário porque:",
    ["São sempre mais lentos do que os testes de UI completos",
     "Apenas verificam visualmente a interface gráfica do sistema",
     "São mais rápidos e estáveis que testes E2E/UI, mas validam mais integração que testes unitários",
     "São completamente equivalentes aos testes unitários"],2,
    "Testes de API/integração são intermediários: mais rápidos e menos frágeis que E2E, mas com maior abrangência que unitários.")

add(5,2,"Os quadrantes de teste Q1 (que apoiam o time, orientados à tecnologia) incluem principalmente:",
    ["Testes de usabilidade e testes exploratórios manuais",
     "Testes de aceitação realizados pelo usuário final",
     "Testes unitários e de componente automatizados que guiam o desenvolvimento",
     "Testes de carga e de desempenho do sistema"],2,
    "Q1 (technology-facing, team-support): testes unitários e de componente automatizados que apoiam o desenvolvimento (TDD).")

add(5,2,"Os quadrantes de teste Q4 (que criticam o produto, orientados à tecnologia) incluem:",
    ["Testes de aceitação realizados diretamente pelo usuário",
     "Testes unitários automatizados de cada componente",
     "Testes de desempenho, segurança, confiabilidade e outros atributos de qualidade não funcionais",
     "Testes exploratórios focados nas regras de negócio"],2,
    "Q4 (technology-facing, product-critique): testes não funcionais como desempenho, segurança e confiabilidade, geralmente automatizados.")

add(5,2,"Qual é a diferença entre severidade e prioridade de um defeito em um cenário prático?",
    ["Severidade e prioridade são sempre exatamente iguais",
     "Alta severidade sempre implica automaticamente em alta prioridade",
     "Um bug cosmético (baixa severidade) pode ter alta prioridade se está na tela de marketing de um lançamento iminente",
     "A prioridade é sempre definida pelo testador; a severidade, pelo cliente final"],2,
    "Severidade e prioridade são independentes: um bug cosmético pode ser urgente (alta prioridade) por razões de negócio, mesmo com baixo impacto técnico.")

add(5,2,"Na gestão de configuração, um 'baseline' (linha de base) é:",
    ["Um erro comum no sistema de controle de versão",
     "O ambiente de produção onde o sistema é executado",
     "Uma versão aprovada e fixada de um ou mais itens de configuração, usada como referência",
     "O plano de teste já aprovado pelos stakeholders"],2,
    "Uma baseline é uma referência estável e formalmente aprovada de itens de configuração, usada para controlar mudanças subsequentes.")

add(5,1,"Qual das seguintes é uma métrica de progresso de teste útil para monitoramento diário?",
    ["Número de linhas de código por desenvolvedor",
     "Horas de reunião por semana",
     "Percentual de casos de teste executados e taxa de aprovação/reprovação",
     "Número de funcionalidades solicitadas"],2,
    "Métricas de execução (% executados, aprovados, reprovados) fornecem visibilidade direta do progresso real versus o planejado.")

add(5,2,"O 'relatório de defeito' (bug report) de qualidade deve evitar:",
    ["Incluir os passos detalhados para reproduzir o defeito",
     "Registrar corretamente a severidade do defeito encontrado",
     "Linguagem subjetiva, culpa pessoal ou título vago como 'sistema não funciona'",
     "Mencionar claramente o ambiente onde o teste ocorreu"],2,
    "Bons relatórios são objetivos, descritivos e factuais; linguagem acusatória e títulos vagos prejudicam a triagem e a correção eficiente.")

add(5,2,"Qual é o propósito do relatório de conclusão de teste (test completion report)?",
    ["Listar apenas os defeitos que ainda estão abertos",
     "Substituir completamente o plano de teste para o próximo ciclo",
     "Resumir os resultados do ciclo de teste, comunicar a qualidade atingida e registrar lições aprendidas",
     "Aprovar formalmente o lançamento do produto final"],2,
    "O relatório de conclusão consolida resultados, cobertura, defeitos, desvios do plano e lições, servindo de referência para ciclos futuros.")

add(5,3,"A abordagem de teste baseada em risco (risk-based testing) afeta o planejamento ao:",
    ["Ignorar completamente as funcionalidades de baixo risco",
     "Eliminar totalmente os testes de regressão do plano",
     "Alocar mais esforço, profundidade e antecipação aos itens de maior risco de produto",
     "Reduzir sempre o número total de casos de teste planejados"],2,
    "O risco orienta onde investir mais (técnicas mais rigorosas, início antecipado) e permite reduzir esforço em áreas de baixo risco.")

add(5,3,"Quando critérios de saída não são atingidos mas o prazo chegou ao fim, qual ação é mais adequada?",
    ["Ignorar os critérios definidos e encerrar o teste de qualquer forma",
     "Continuar o teste indefinidamente, sem nenhum critério de parada",
     "Relatar o status, os riscos residuais e deixar a decisão de encerrar ou continuar para os stakeholders",
     "Reprovar formalmente o sistema sem consultar ninguém"],2,
    "O gerente de testes reporta riscos residuais e status; a decisão de encerrar ou não é de negócio, tomada pelos stakeholders com informação completa.")

add(5,2,"Qual técnica de priorização é mais indicada quando o tempo é muito curto e é necessário garantir que o mais crítico seja testado primeiro?",
    ["Priorização totalmente aleatória dos casos de teste",
     "Priorização simples por ordem alfabética do nome do módulo",
     "Priorização baseada em risco: testa primeiro o que tem maior nível de risco",
     "Testar primeiro apenas os casos mais curtos e rápidos"],2,
    "Com tempo limitado, a priorização por risco garante que o esforço disponível cubra o que causaria maior impacto caso falhasse.")

add(5,2,"A 'análise de impacto' (impact analysis) em teste de manutenção serve para:",
    ["Estimar exclusivamente o custo total do projeto",
     "Selecionar diretamente a ferramenta de automação usada",
     "Identificar quais partes do sistema e quais testes são afetados por uma mudança",
     "Planejar os treinamentos necessários para a equipe"],2,
    "A análise de impacto determina o escopo da regressão: quais áreas foram afetadas pela mudança e quais testes devem ser executados.")

add(5,2,"Em projetos ágeis, o 'Definition of Ready' (DoR) para uma história de usuário significa que:",
    ["A história já foi totalmente implementada, testada e está pronta para entrega ao cliente",
     "Todos os testes automatizados e manuais da história já foram escritos e executados com sucesso",
     "A história atende aos critérios mínimos para entrar no sprint (critérios de aceitação definidos, estimada, sem dependências bloqueantes)",
     "O código completo da história já foi formalmente revisado e aprovado pelos pares técnicos"],2,
    "DoR define quando uma história está suficientemente preparada para ser trabalhada no sprint, incluindo critérios de aceitação claros para o teste.")

add(5,2,"Em gestão de configuração, o que é um 'item de configuração' (configuration item)?",
    ["Apenas um caso de teste individual armazenado isoladamente no repositório de testes",
     "Apenas um relatório de defeito registrado manualmente no sistema de rastreamento",
     "Apenas uma única linha de código-fonte presente no programa compilado",
     "Qualquer artefato (componente, documento, ambiente) identificado e gerenciado como unidade no sistema de controle de configuração"],3,
    "Itens de configuração são artefatos identificados unicamente e gerenciados sob controle de configuração: código, documentos, ambientes, ferramentas.")

# ============================================================
# CAPÍTULO 6 — FERRAMENTAS (6)
# ============================================================
add(6,1,"Ferramentas de teste podem apoiar:",
    ["Apenas a execução","Várias atividades: gestão, estática, modelagem, execução, desempenho e mais",
     "Somente a automação de UI","Apenas relatórios"],1,
    "Há categorias para gestão de teste, análise estática, modelagem, execução, dados, desempenho e monitoramento.")
add(6,1,"Para qual finalidade a automação traz maior retorno típico?",
    ["Teste exploratório","Teste de regressão repetitivo e extenso",
     "Avaliação de usabilidade","Revisão de requisitos"],1,
    "A regressão repetitiva é o caso clássico de bom ROI: testes estáveis executados muitas vezes.")
add(6,2,"Qual é um risco real ao adotar ferramentas de automação?",
    ["Reduzir os custos do projeto de forma totalmente imediata","Subestimar o esforço de implantação e, principalmente, de manutenção dos scripts",
     "Eliminar completamente a necessidade de teste manual","Aumentar a cobertura de testes sem nenhum esforço adicional"],1,
    "Riscos incluem expectativas irreais, custo de manutenção, dependência da ferramenta e scripts frágeis.")
add(6,2,"Um benefício geral das ferramentas de teste é:",
    ["Garantir matematicamente a ausência total de defeitos","Reduzir trabalho repetitivo e aumentar consistência e repetibilidade",
     "Substituir completamente o julgamento humano do testador","Dispensar totalmente a necessidade de planejamento de teste"],1,
    "Ferramentas reduzem tarefas manuais repetitivas, aumentam consistência e dão acesso a informações (ex.: cobertura).")
add(6,2,"Ao selecionar uma ferramenta de teste, deve-se considerar principalmente:",
    ["Apenas o preço de aquisição da licença da ferramenta","Maturidade da organização, ajuste ao contexto/processo e avaliação por meio de prova de conceito",
     "Apenas a popularidade da ferramenta nas redes sociais","Exclusivamente a cor e o visual da interface gráfica"],1,
    "A seleção avalia contexto, maturidade, restrições, integração e geralmente inclui uma avaliação/PoC antes de adotar.")
add(6,2,"Antes de implantar amplamente uma nova ferramenta, recomenda-se:",
    ["Comprar imediatamente a licença para toda a empresa","Conduzir um projeto piloto para avaliar ajuste, definir uso e medir benefícios",
     "Treinar a equipe somente depois da implantação total","Dispensar completamente a coleta de métricas de uso"],1,
    "Um piloto permite avaliar o ajuste à organização, definir diretrizes de uso e estimar custos/benefícios antes da escala.")

# ============================================================
# CAPÍTULO 6 — FERRAMENTAS (continuação, +4)
# ============================================================
add(6,2,"Um projeto deseja automatizar testes de regressão de API. Que categoria de ferramenta é mais adequada?",
    ["Uma ferramenta de gestão e rastreamento de requisitos",
     "Ferramenta de execução de testes de API (ex.: cliente REST com asserções automatizadas)",
     "Uma ferramenta de análise estática do código-fonte",
     "Uma ferramenta de apoio à revisão manual de código"],1,
    "Ferramentas de teste de API (como frameworks REST com asserções) são a categoria adequada para automatizar regressão de serviços.")

add(6,2,"O ROI (retorno sobre investimento) da automação de testes tende a ser maior quando:",
    ["Os testes automatizados são executados muito poucas vezes ao longo do projeto",
     "Os testes são estáveis, executados frequentemente e o custo de manutenção é menor que o de execução manual repetida",
     "O sistema muda completamente a cada sprint, sem nenhuma compatibilidade retroativa",
     "A equipe responsável ainda não conhece bem a ferramenta escolhida"],1,
    "ROI positivo ocorre quando testes estáveis e frequentes amortizam o custo inicial de automação e de manutenção ao longo do tempo.")

add(6,2,"Qual é o risco de 'scripts frágeis' (brittle scripts) na automação de testes de UI?",
    ["Os scripts de automação rodam de forma muito rápida",
     "Pequenas mudanças na interface quebram os scripts, gerando alto custo de manutenção",
     "Os scripts automatizados cobrem muitos cenários de teste",
     "A automação passa a detectar muito mais defeitos"],1,
    "Scripts de UI que dependem de seletores frágeis (coordenadas, textos literais) se quebram com qualquer mudança de layout, aumentando manutenção.")

add(6,2,"Ao avaliar uma ferramenta de automação de testes, qual critério é mais importante segundo boas práticas?",
    ["A quantidade total de funcionalidades oferecidas pela ferramenta",
     "O ajuste ao contexto da organização: tecnologia do sistema, habilidades da equipe, integração com o processo",
     "O número total de usuários da ferramenta no mercado global",
     "Apenas a data original de lançamento da ferramenta"],1,
    "A adequação ao contexto (tecnologia do produto, maturidade da equipe, integração ao processo) determina o sucesso da adoção mais que qualquer ranking.")

# ============================================================
# Montagem + validações
# ============================================================
counters = {d: 0 for d in DOMAINS}
questions = []
for (ch, k, q, opts, ans, exp) in Q:
    assert ch in DOMAINS, f"capítulo inválido: {ch}"
    assert 1 <= k <= 3, f"K-level inválido: {k}"
    assert 0 <= ans < len(opts), f"índice de resposta fora do intervalo em: {q[:40]}"
    assert len(opts) == len(set(opts)), f"opções duplicadas em: {q[:40]}"
    dom = DOMAINS[ch]
    counters[ch] += 1
    qid = f"ch{ch}-{counters[ch]:02d}"
    questions.append({
        "id": qid,
        "chapter": ch,
        "domain": dom,
        "kLevel": k,
        "answer": ans,
        "locales": {
            "pt": {"q": q, "options": opts, "exp": exp}
        }
    })

# Validar distribuição
print("Distribuição por capítulo (real / alvo):")
ok = True
for ch in sorted(DOMAINS):
    real = counters[ch]
    print(f"  Cap.{ch} {DOMAIN_NAMES[DOMAINS[ch]]:48s}: {real:3d} / {TARGET[ch]}")
    if real != TARGET[ch]:
        ok = False
print(f"TOTAL: {len(questions)} questões")

# Distribuição por K-level
from collections import Counter
kc = Counter(x["kLevel"] for x in questions)
print(f"K-levels -> K1: {kc[1]}  K2: {kc[2]}  K3: {kc[3]}")

if not ok:
    print("AVISO: distribuição diverge do alvo!", file=sys.stderr)

bank = {
    "meta": {
        "title": "Banco de Questões CTFL v4.0",
        "syllabus": "ISTQB Certified Tester Foundation Level v4.0",
        "version": "1.0.0",
        "defaultLanguage": "pt",
        "availableLanguages": ["pt"],
        "examFormat": {"questions": 40, "passMark": 26, "timeMinutes": 60, "timeMinutesNonNative": 75},
        "chapterWeights": {str(ch): TARGET[ch] for ch in TARGET},
        "domainNames": DOMAIN_NAMES,
        "total": len(questions)
    },
    "questions": questions
}

with open("ctfl-questions-ptbr.json", "w", encoding="utf-8") as f:
    json.dump(bank, f, ensure_ascii=False, indent=2)
print("\nArquivo gerado: ctfl-questions-ptbr.json")
