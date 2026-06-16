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
     "Um erro (ação humana) introduz um defeito no artefato, que ao ser executado pode causar uma falha",
     "Erro e defeito são sinônimos; falha só ocorre em produção",
     "Falha gera defeito, que gera erro"],1,
    "A cadeia causal é erro humano → defeito no código/artefato → falha (comportamento incorreto em execução).")
add(1,1,"Qual NÃO é um objetivo típico do teste?",
    ["Encontrar defeitos","Reduzir o nível de risco","Verificar requisitos","Garantir matematicamente a ausência de defeitos"],3,
    "O teste não pode provar a ausência de defeitos; ele fornece informação e reduz risco, mas não garante perfeição.")
add(1,2,"Qual a diferença entre testar e depurar (debugging)?",
    ["São a mesma atividade","Teste encontra falhas; depuração localiza, analisa e corrige o defeito que as causou",
     "Depuração encontra falhas; teste corrige o código","Depuração só ocorre em produção"],1,
    "Teste evidencia falhas causadas por defeitos; a depuração é a atividade de desenvolvimento que localiza, diagnostica e corrige o defeito.")
add(1,2,"Por que o teste é necessário?",
    ["Para substituir a revisão de código","Para contribuir com o sucesso do projeto, reduzindo o risco de falhas em operação",
     "Para garantir software sem defeitos","Porque é exigido por lei"],1,
    "O teste reduz o risco de falhas em operação e ajuda a entregar um produto com qualidade adequada às necessidades das partes interessadas.")
add(1,2,"Como se relacionam controle de qualidade (QC) e garantia da qualidade (QA)?",
    ["São sinônimos","QC é orientado ao produto (inclui o teste); QA é orientado ao processo",
     "QA é orientado ao produto; QC ao processo","O teste faz parte do QA, não do QC"],1,
    "QC foca o produto e inclui atividades como o teste; QA foca a melhoria do processo para gerar confiança de que a qualidade será atingida.")
add(1,2,"A causa-raiz de um defeito é:",
    ["A falha observada pelo usuário","O evento mais antigo que, se corrigido, evita a recorrência do defeito",
     "O ambiente de teste","O caso de teste que falhou"],1,
    "A análise de causa-raiz busca a origem fundamental, permitindo ações que previnem a reincidência de defeitos semelhantes.")
add(1,1,"Princípio: 'o teste mostra a presença de defeitos, não a sua ausência'. Isso significa que:",
    ["Testar prova que não há defeitos","Testar pode revelar defeitos, mas não provar que não existem",
     "Defeitos sempre existem","O teste é inútil"],1,
    "Encontrar defeitos não é prova de ausência deles; mesmo sem defeitos encontrados, não há garantia de correção total.")
add(1,1,"Princípio: 'o teste exaustivo é impossível'. A consequência prática é:",
    ["Não vale a pena testar","Usar análise de risco e prioridades para focar o esforço",
     "Testar apenas o caminho feliz","Automatizar tudo"],1,
    "Como não é viável testar todas as combinações, prioriza-se com base em risco e prioridades.")
add(1,2,"Princípio do 'teste antecipado' (early testing) afirma que:",
    ["Testes só devem começar após o código pronto","Atividades de teste devem começar o mais cedo possível no ciclo",
     "Testar cedo aumenta os custos","Só requisitos podem ser testados cedo"],1,
    "Iniciar cedo (inclusive com testes estáticos em requisitos) reduz custos, pois defeitos achados tarde são mais caros de corrigir.")
add(1,2,"O 'agrupamento de defeitos' (defect clustering) sugere que:",
    ["Defeitos se distribuem por igual","Poucos módulos concentram a maioria dos defeitos",
     "Cada módulo tem um defeito","Defeitos só aparecem em código novo"],1,
    "Geralmente uma minoria de módulos concentra a maioria dos defeitos, o que orienta a priorização do teste.")
add(1,2,"O 'paradoxo do pesticida' indica que:",
    ["Mais testes geram mais defeitos","Repetir os mesmos testes deixa de encontrar novos defeitos",
     "Testes manuais são melhores","Pesticidas afetam o software"],1,
    "Se os mesmos casos são repetidos, eles param de revelar defeitos novos; é preciso revisar e renovar os testes.")
add(1,2,"O princípio 'o teste depende do contexto' significa que:",
    ["Todo software é testado igual","A forma de testar varia conforme o domínio, risco e contexto",
     "Contexto não importa","Só sistemas críticos precisam de teste"],1,
    "Sistemas diferentes (e.g., e-commerce vs. software médico) exigem abordagens, técnicas e rigor distintos.")
add(1,2,"A 'falácia da ausência de erros' (absence-of-errors fallacy) afirma que:",
    ["Software sem defeitos é sempre bom","Corrigir todos os defeitos é inútil se o sistema não atende às necessidades do usuário",
     "Não existem erros","Erros não importam"],1,
    "Um produto pode estar livre de defeitos conhecidos e ainda assim ser inadequado se não atende às necessidades reais.")
add(1,2,"Um time decide priorizar o teste do módulo de pagamentos, onde historicamente surgem muitos defeitos. Qual princípio justifica isso?",
    ["Teste exaustivo","Agrupamento de defeitos","Falácia da ausência de erros","Paradoxo do pesticida"],1,
    "Concentrar esforço onde os defeitos historicamente se agrupam aplica o princípio do defect clustering.")
add(1,1,"Qual atividade do processo de teste define objetivos, abordagem e recursos?",
    ["Execução","Planejamento","Análise","Conclusão"],1,
    "O planejamento de teste define objetivos, escopo, abordagem, recursos e critérios.")
add(1,2,"O monitoramento e controle do teste serve para:",
    ["Escrever casos de teste","Comparar o progresso real com o planejado e tomar ações corretivas",
     "Executar os testes","Encerrar o projeto"],1,
    "O monitoramento coleta métricas; o controle age (replanejar, realocar) quando há desvios em relação ao plano.")
add(1,2,"Na atividade de análise de teste, o que se produz principalmente?",
    ["Scripts automatizados","Condições de teste a partir da base de teste e seus critérios",
     "O relatório final","Os dados de teste"],1,
    "A análise identifica o que testar — as condições de teste — a partir da base de teste (requisitos, riscos, etc.).")
add(1,2,"Na modelagem de teste, o foco é:",
    ["Identificar o que testar","Definir como testar: casos de teste e conjuntos a partir das condições",
     "Executar os casos","Reportar defeitos"],1,
    "A modelagem (design) elabora como cobrir as condições de teste, produzindo casos e conjuntos de teste.")
add(1,2,"Qual é a saída principal da atividade de implementação de teste?",
    ["Condições de teste","Procedimentos, scripts e dados prontos para execução, com o ambiente preparado",
     "O plano de teste","O relatório de progresso"],1,
    "A implementação organiza e prepara tudo o que é necessário para executar: procedimentos, dados, ambiente e agenda.")
add(1,2,"Durante a execução do teste, ao encontrar um resultado divergente, o testador deve primeiro:",
    ["Corrigir o código","Registrar o resultado e, se for uma anomalia, criar um relatório de defeito",
     "Encerrar o teste","Ignorar se for menor"],1,
    "Resultados são comparados ao esperado; divergências (anomalias) são analisadas e, quando defeitos, registradas em relatório.")
add(1,2,"A atividade de conclusão do teste tipicamente inclui:",
    ["Escrever os primeiros casos","Arquivar testware, registrar lições aprendidas e produzir o relatório de conclusão",
     "Definir os objetivos","Preparar o ambiente"],1,
    "A conclusão consolida resultados, arquiva o testware reutilizável, registra lições aprendidas e emite o relatório de conclusão.")
add(1,1,"O que é 'testware'?",
    ["O hardware de teste","Os artefatos produzidos durante o processo de teste (planos, casos, dados, relatórios)",
     "A ferramenta de automação","O sistema sob teste"],1,
    "Testware engloba todos os artefatos do trabalho de teste: planos, condições, casos, dados, scripts, relatórios.")
add(1,2,"Qual o principal benefício da rastreabilidade entre a base de teste e o testware?",
    ["Reduzir o número de testes","Permitir avaliar cobertura e o impacto de mudanças sobre os testes",
     "Eliminar a documentação","Acelerar o código"],1,
    "A rastreabilidade liga requisitos/riscos a condições e casos, apoiando cobertura, análise de impacto e auditoria.")
add(1,2,"Sobre independência do teste, qual afirmação é correta?",
    ["Maior independência sempre encontra mais defeitos","Independência pode reduzir o viés do autor, mas graus extremos têm desvantagens como menor conhecimento do contexto",
     "O autor é sempre o melhor testador do próprio código","Independência não influencia o teste"],1,
    "Algum grau de independência reduz o viés cognitivo do autor, mas independência total pode afastar o testador do contexto e da comunicação.")

# ============================================================
# CAPÍTULO 1 — FUNDAMENTOS (continuação, +16)
# ============================================================
add(1,2,"Qual habilidade cognitiva é considerada fundamental para um bom testador?",
    ["Velocidade de digitação",
     "Pensamento analítico e crítico para questionar suposições e identificar problemas",
     "Conhecimento exclusivo de linguagens de programação",
     "Capacidade de escrever código de produção"],1,
    "O pensamento analítico/crítico permite ao testador questionar suposições, identificar inconsistências e encontrar defeitos não óbvios.")

add(1,2,"A 'abordagem de equipe completa' (whole-team approach) no teste ágil implica que:",
    ["Somente os testadores são responsáveis pela qualidade",
     "Toda a equipe compartilha a responsabilidade pela qualidade, com testadores colaborando com devs e stakeholders",
     "O gerente de testes toma todas as decisões",
     "Desenvolvedores não participam das atividades de teste"],1,
    "Na whole-team approach, qualidade é responsabilidade coletiva; testadores, devs e negócio colaboram desde o início.")

add(1,1,"Qual é o benefício principal de ter testadores com diferentes graus de independência?",
    ["Aumentar o custo do projeto",
     "Combinar o conhecimento do autor com a perspectiva imparcial de quem não escreveu o artefato",
     "Garantir que todos os testes sejam automatizados",
     "Eliminar a necessidade de revisões"],1,
    "Diferentes graus de independência equilibram conhecimento contextual e imparcialidade, melhorando a eficácia da detecção.")

add(1,2,"Um testador que revisa os próprios requisitos que escreveu terá dificuldade de encontrar defeitos porque:",
    ["Não tem tempo suficiente",
     "O viés do autor dificulta ver os próprios erros — o testador tende a confirmar o que escreveu",
     "Requisitos não podem ter defeitos",
     "Revisões não são parte do teste"],1,
    "O viés cognitivo do autor faz com que ele leia o que pretendia escrever, não o que realmente está escrito.")

add(1,1,"Em qual grau de independência o testador é externo à organização do desenvolvedor?",
    ["Testador que é o próprio autor",
     "Testador de outra equipe da mesma organização",
     "Testador de empresa especializada externa",
     "Testador da equipe de desenvolvimento"],2,
    "O grau mais alto de independência é representado por testadores de organizações externas — consultores ou laboratórios independentes.")

add(1,2,"A rastreabilidade bidirecional entre requisitos e casos de teste permite:",
    ["Executar testes automaticamente",
     "Verificar cobertura dos requisitos e analisar o impacto de mudanças nos testes",
     "Eliminar a necessidade de plano de teste",
     "Reduzir o número de defeitos automaticamente"],1,
    "Com rastreabilidade bidirecional, é possível saber quais testes cobrem cada requisito e quais testes serão afetados por mudanças.")

add(1,2,"Qual é o papel principal do gerente de testes (test manager) em um projeto?",
    ["Executar casos de teste manualmente",
     "Planejar, monitorar, controlar e liderar as atividades de teste e a equipe",
     "Desenvolver o código de produção",
     "Escrever requisitos de negócio"],1,
    "O gerente de testes é responsável pelo planejamento, monitoramento e controle do processo de teste e pela liderança da equipe.")

add(1,1,"O que é a 'base de teste' (test basis)?",
    ["O ambiente onde os testes são executados",
     "O conjunto de artefatos dos quais os testes são derivados (requisitos, código, modelos, etc.)",
     "O resultado dos testes executados",
     "O banco de dados de defeitos"],1,
    "A base de teste são os artefatos — requisitos, especificações, código, modelos — a partir dos quais condições e casos de teste são derivados.")

add(1,2,"Qual a diferença entre verificação e validação no contexto do teste?",
    ["São sinônimos",
     "Verificação: 'estamos construindo certo?' (conforme especificação); validação: 'estamos construindo a coisa certa?' (atende ao usuário)",
     "Verificação é dinâmica; validação é estática",
     "Validação só ocorre em produção"],1,
    "Verificação checa conformidade com a especificação; validação checa se o produto atende às necessidades reais do usuário.")

add(1,2,"A mentalidade do testador difere da do desenvolvedor porque o testador:",
    ["Foca em construir funcionalidades rapidamente",
     "Adota uma perspectiva crítica, buscando ativamente falhas e questionando suposições",
     "Evita questionar decisões de design",
     "Apenas confirma que o software funciona conforme esperado pelo dev"],1,
    "Testadores adotam mentalidade de questionamento e ceticismo construtivo para encontrar o que pode falhar, não para confirmar que funciona.")

add(1,1,"O que é um 'objeto de teste' (test object)?",
    ["A ferramenta usada para testar",
     "O item de trabalho (componente, sistema, requisito) que está sendo testado",
     "O caso de teste em si",
     "O ambiente de execução"],1,
    "O objeto de teste é o artefato que está sendo avaliado: um componente, sistema, requisito, modelo ou documento.")

add(1,2,"Como a comunicação eficaz de defeitos pelo testador contribui para o projeto?",
    ["Cria atrito desnecessário com o time de desenvolvimento",
     "Permite que defeitos sejam compreendidos, priorizados e corrigidos de forma eficiente",
     "Substitui a necessidade de cases de teste",
     "Aumenta o número de defeitos encontrados"],1,
    "Relatórios claros, objetivos e factuais facilitam a compreensão, reprodução e correção dos defeitos, além de preservar a colaboração.")

add(1,2,"Qual característica do teste antecipado (shift-left) o diferencia do teste tradicional?",
    ["Testa-se apenas em produção",
     "As atividades de teste (inclusive revisões estáticas) iniciam desde os requisitos, não só após o código",
     "Elimina o teste de sistema",
     "Só aplica-se a projetos ágeis"],1,
    "Shift-left significa começar a testar — inclusive com revisões de requisitos — nas fases iniciais, antes mesmo de qualquer código.")

add(1,2,"A 'análise de causa-raiz' (root cause analysis) de defeitos recorrentes beneficia o processo porque:",
    ["Apenas documenta os defeitos",
     "Identifica a origem dos problemas, permitindo melhorias de processo que previnam defeitos similares no futuro",
     "Substitui a execução de testes",
     "É necessária só em projetos críticos"],1,
    "Identificar a causa-raiz permite implementar melhorias de processo que evitam a reincidência de classes de defeitos semelhantes.")

add(1,2,"Um artefato de teste como um 'caso de teste' deve conter no mínimo:",
    ["Apenas o nome do testador",
     "Pré-condições, passos de execução, resultado esperado e pós-condições",
     "Somente o resultado esperado",
     "A data de criação e a versão do sistema"],1,
    "Um caso de teste completo define pré-condições, entradas, passos, resultado esperado e pós-condições, garantindo repetibilidade.")

add(1,2,"Qual o impacto de defeitos encontrados em produção comparado a defeitos encontrados em requisitos?",
    ["O custo é o mesmo",
     "Defeitos em produção são muito mais caros de corrigir — o custo cresce a cada fase que passa",
     "Defeitos em produção são mais fáceis de corrigir",
     "O impacto é irrelevante para o projeto"],1,
    "O custo de correção aumenta exponencialmente com a fase: defeitos em requisitos custam muito menos que em produção.")

# ============================================================
# CAPÍTULO 2 — TESTE AO LONGO DO CICLO (15)
# ============================================================
add(2,2,"Como o modelo de ciclo de desenvolvimento influencia o teste?",
    ["Não influencia","Influencia o momento, a abordagem e o nível de detalhe das atividades de teste",
     "Só muda a ferramenta","Apenas em projetos ágeis"],1,
    "Em sequenciais o teste tende a ser por fase; em ágeis/iterativos é contínuo e integrado a cada incremento.")
add(2,2,"O que significa 'shift-left' no teste?",
    ["Adiar o teste para o final","Antecipar atividades de teste para fases iniciais do ciclo",
     "Mover o teste para a direita","Testar só em produção"],1,
    "Shift-left antecipa o teste (inclusive estático) para fases iniciais, encontrando defeitos mais cedo e mais barato.")
add(2,1,"TDD, ATDD e BDD são exemplos de abordagens:",
    ["De automação de UI","De teste-primeiro (test-first), em que os testes guiam o desenvolvimento",
     "De gestão de configuração","De teste de carga"],1,
    "São abordagens test-first: os testes/critérios são definidos antes ou junto ao código e orientam a implementação.")
add(2,1,"Qual o benefício de retrospectivas para o teste?",
    ["Reduzir o número de testes","Promover melhoria contínua do processo a partir de lições aprendidas",
     "Substituir o planejamento","Eliminar defeitos"],1,
    "Retrospectivas identificam o que melhorar (processo, ferramentas, colaboração), apoiando a melhoria contínua.")
add(2,1,"O teste de componente (unidade) foca em:",
    ["A integração entre sistemas","Verificar componentes isoladamente, normalmente pelo desenvolvedor",
     "A aceitação do usuário","O sistema completo"],1,
    "O teste de componente verifica módulos/unidades de forma isolada, frequentemente com apoio de stubs/drivers.")
add(2,2,"Qual a diferença entre integração de componentes e integração de sistemas?",
    ["São iguais","Integração de componentes verifica interações dentro de um sistema; integração de sistemas verifica interações entre sistemas distintos",
     "Integração de sistemas é feita antes","Apenas a de componentes usa interfaces"],1,
    "A primeira foca interfaces internas entre componentes; a segunda, interfaces entre sistemas (e organizações) diferentes.")
add(2,1,"O teste de sistema avalia:",
    ["Apenas uma unidade","O comportamento e as capacidades do sistema como um todo",
     "Somente a interface","A aceitação contratual"],1,
    "O teste de sistema avalia o sistema integrado fim-a-fim, comportamento funcional e não funcional.")
add(2,2,"Quais são formas comuns de teste de aceitação?",
    ["Unitário e de integração","De usuário (UAT), operacional, contratual e regulatório",
     "Caixa-branca e caixa-preta","Estático e dinâmico"],1,
    "Aceitação inclui UAT, aceitação operacional (backup, segurança), e aceitação contratual/regulatória.")
add(2,2,"Qual a diferença entre teste alfa e beta?",
    ["Alfa é em produção; beta no desenvolvedor","Alfa ocorre no ambiente da organização desenvolvedora; beta no ambiente dos usuários reais",
     "São sinônimos","Beta vem antes do alfa"],1,
    "Alfa é realizado nas instalações do desenvolvedor (por usuários/equipe); beta é feito pelos usuários em seu próprio ambiente.")
add(2,1,"Teste funcional avalia:",
    ["Como o sistema se comporta (desempenho, usabilidade)","O que o sistema faz, conforme requisitos funcionais",
     "A estrutura interna do código","A documentação"],1,
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
    ["Confirmar a correção de um defeito específico","Detectar efeitos colaterais: mudanças que quebraram funcionalidades antes funcionais",
     "Avaliar desempenho","Testar requisitos novos apenas"],1,
    "A regressão verifica se alterações não introduziram defeitos em partes que antes funcionavam.")
add(2,2,"O que normalmente dispara o teste de manutenção?",
    ["Apenas o lançamento inicial","Modificações, migrações, atualizações ou aposentadoria do sistema",
     "Somente novos requisitos","A criação dos casos de teste"],1,
    "Gatilhos típicos: correções/melhorias (modificações), migração de ambiente, atualizações e descontinuação (aposentadoria).")

# ============================================================
# CAPÍTULO 2 — TESTE AO LONGO DO CICLO (continuação, +10)
# ============================================================
add(2,2,"No BDD (Behaviour-Driven Development), os cenários são escritos no formato:",
    ["Pseudo-código técnico",
     "Given/When/Then, descrevendo comportamento em linguagem próxima ao negócio",
     "XML de configuração",
     "Diagrama de estados"],1,
    "BDD usa Given/When/Then (ou equivalente) para descrever comportamentos em linguagem compreensível por negócio e técnicos.")

add(2,2,"Qual diferença essencial existe entre TDD e ATDD?",
    ["São idênticos",
     "TDD é guiado por testes unitários do desenvolvedor; ATDD usa testes de aceitação definidos com negócio",
     "ATDD só usa ferramentas de UI",
     "TDD só se aplica a projetos ágeis"],1,
    "TDD: dev escreve teste unitário antes do código. ATDD: equipe define testes de aceitação com stakeholders antes de implementar.")

add(2,2,"Em projetos ágeis com iterações curtas, qual nível de teste é mais desafiador de executar dentro do sprint?",
    ["Teste de componente (unitário)",
     "Teste de sistema e de aceitação completos, por exigirem integração e tempo maiores",
     "Revisões de código",
     "Testes de regressão unitários"],1,
    "Testes de sistema e aceitação requerem integração e cenários end-to-end, o que pode ser difícil de concluir dentro de um sprint curto.")

add(2,1,"O que é um 'stub' no contexto de teste de componente?",
    ["Uma ferramenta de automação",
     "Um componente substituto que simula a dependência do componente sob teste (chamado pelo componente)",
     "Um tipo de defeito",
     "Um relatório de teste"],1,
    "Stubs simulam dependências chamadas pelo componente testado (chamada descendente), permitindo isolamento do componente.")

add(2,2,"O teste de integração de sistemas avalia principalmente:",
    ["A lógica interna de cada módulo",
     "As interfaces e interações entre sistemas distintos, incluindo sistemas de terceiros e APIs externas",
     "A interface gráfica do usuário",
     "O desempenho de banco de dados"],1,
    "Testa as interfaces entre sistemas distintos — APIs, serviços externos, integrações — não a lógica interna de cada um.")

add(2,2,"Qual evento tipicamente NÃO é um gatilho de teste de manutenção?",
    ["Correção de um defeito crítico em produção",
     "Criação do planejamento inicial do projeto",
     "Migração de banco de dados para nova versão",
     "Aposentadoria/descontinuação de um sistema legado"],1,
    "Planejamento inicial é feito antes do sistema existir; os gatilhos de manutenção envolvem modificação, migração ou descontinuação.")

add(2,2,"O teste operacional (aceitação operacional) verifica aspectos como:",
    ["A lógica de negócio das funcionalidades",
     "Backup e recuperação, instalação, segurança operacional e procedimentos administrativos",
     "O código-fonte",
     "Os requisitos funcionais apenas"],1,
    "Aceitação operacional foca em aspectos de operação/suporte: backup, restore, instalação, configuração e segurança operacional.")

add(2,2,"Qual abordagem de integração combina componentes de baixo nível primeiro e vai adicionando componentes de nível mais alto?",
    ["Big-bang",
     "Bottom-up",
     "Top-down",
     "Sanduíche (sandwich)"],1,
    "Bottom-up integra de baixo para cima: começa pelos componentes de nível mais baixo, eliminando a necessidade de stubs mas exigindo drivers.")

add(2,2,"No contexto do teste de sistema, 'caso de uso' (use case) serve como:",
    ["Uma especificação de banco de dados",
     "Base para projetar cenários de teste que cobrem fluxos de interação ator-sistema",
     "Uma ferramenta de automação",
     "Um tipo de defeito"],1,
    "Casos de uso descrevem fluxos de interação, servindo de base para cenários de teste de sistema fim-a-fim.")

add(2,2,"A automação de testes de regressão em integração contínua (CI) tem como principal benefício:",
    ["Eliminar testes manuais para sempre",
     "Detectar rapidamente regressões introduzidas por novas mudanças, fornecendo feedback rápido à equipe",
     "Reduzir o número de requisitos",
     "Substituir o teste de aceitação"],1,
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
    ["Mede desempenho","Detecta defeitos cedo, inclusive em requisitos, antes de qualquer execução",
     "Substitui o teste dinâmico","Garante ausência de defeitos"],1,
    "Por agir cedo, encontra defeitos (ambiguidades, omissões) antes da execução, reduzindo custo de correção.")
add(3,2,"Qual a principal diferença entre teste estático e dinâmico?",
    ["Estático executa o código; dinâmico não","Dinâmico executa o software; estático examina artefatos sem executá-los",
     "São equivalentes","Estático só serve para código"],1,
    "O dinâmico requer execução e revela falhas; o estático examina artefatos e encontra defeitos diretamente.")
add(3,2,"Por que o feedback antecipado e frequente é valioso?",
    ["Aumenta o número de defeitos","Permite corrigir cedo, evitando que mal-entendidos se propaguem e fiquem caros",
     "Atrasolução o projeto","Elimina a necessidade de testes"],1,
    "Feedback cedo evita retrabalho caro e mantém o desenvolvimento alinhado às necessidades reais.")
add(3,1,"Qual a sequência geral das atividades de uma revisão?",
    ["Execução → planejamento → relatório","Planejamento → início → revisão individual → comunicação e análise → correção",
     "Análise → modelagem → execução","Início → execução → conclusão"],1,
    "Atividades: planejamento, início (kick-off), revisão individual, comunicação e análise dos resultados, correção e follow-up.")
add(3,1,"Qual papel lidera e modera uma revisão formal?",
    ["Autor","Moderador (facilitador)","Escriba","Gerente"],1,
    "O moderador/facilitador conduz a reunião, garante o processo e a objetividade.")
add(3,2,"Qual a responsabilidade do autor em uma revisão?",
    ["Moderar a reunião","Criar o artefato e, em geral, ser responsável por corrigi-lo",
     "Registrar as anomalias","Decidir o tipo de revisão"],1,
    "O autor é dono do artefato sob revisão e normalmente faz as correções identificadas.")
add(3,1,"Qual o papel do escriba (registrador) na revisão?",
    ["Liderar a discussão","Documentar as anomalias e decisões da reunião",
     "Corrigir o artefato","Aprovar a entrega"],1,
    "O escriba registra anomalias, decisões e novos achados durante a revisão.")
add(3,2,"Uma revisão informal caracteriza-se por:",
    ["Processo documentado e métricas","Ausência de processo formal, baixo custo e resultados não documentados formalmente",
     "Papéis rígidos","Preparação individual obrigatória"],1,
    "Revisão informal não segue processo definido nem produz documentação formal; é rápida e barata.")
add(3,2,"O principal objetivo de um walkthrough costuma ser:",
    ["Auditar conformidade","Permitir que o autor conduza os participantes pelo artefato para obter entendimento comum e feedback",
     "Medir cobertura de código","Aprovar formalmente o produto"],1,
    "No walkthrough o autor guia os participantes pelo documento, buscando entendimento comum, aprendizado e feedback.")
add(3,2,"A revisão técnica é conduzida principalmente para:",
    ["Treinar novatos","Obter consenso técnico e tomar decisões, conduzida por pares qualificados",
     "Documentar requisitos","Substituir o teste dinâmico"],1,
    "A revisão técnica reúne pares tecnicamente qualificados para avaliar qualidade e alcançar consenso/decisões técnicas.")
add(3,2,"A inspeção difere das demais revisões por ser:",
    ["A mais informal","A mais formal: papéis definidos, métricas e critérios de entrada/saída",
     "Conduzida pelo autor","Sem preparação"],1,
    "A inspeção é a mais formal: processo rígido, papéis, preparação individual, métricas e critérios de entrada/saída.")
add(3,2,"Ao escolher o tipo de revisão, o fator determinante deve ser:",
    ["A preferência do autor","O objetivo da revisão e o risco/criticidade do artefato",
     "O tamanho do time","A ferramenta disponível"],1,
    "O tipo é escolhido conforme o objetivo (consenso, conformidade, aprendizado) e a criticidade do artefato.")
add(3,2,"Qual é um fator de sucesso para revisões?",
    ["Usar a revisão para avaliar o desempenho das pessoas","Focar no artefato (não na pessoa) e manter clima construtivo",
     "Não definir objetivos","Revisar tudo na maior formalidade possível"],1,
    "Revisões bem-sucedidas focam o produto, têm objetivos claros, escopo adequado e ambiente sem julgamento pessoal.")

# ============================================================
# CAPÍTULO 3 — TESTE ESTÁTICO (continuação, +10)
# ============================================================
add(3,2,"Qual é um tipo de defeito que o teste estático encontra mas o dinâmico dificilmente detecta?",
    ["Falha de desempenho em carga",
     "Requisito ambíguo ou contraditório antes de qualquer implementação",
     "Erro de runtime em módulo executado",
     "Falha de interface de usuário"],1,
    "Revisões estáticas encontram defeitos em requisitos (ambiguidades, omissões) antes que o código seja escrito.")

add(3,1,"Qual ferramenta apoia o teste estático por meio de análise automatizada do código-fonte?",
    ["Ferramenta de execução de testes de desempenho",
     "Ferramenta de análise estática (linter/analisador de código)",
     "Ferramenta de gravação e reprodução de UI",
     "Gerenciador de configuração"],1,
    "Ferramentas de análise estática examinam o código sem executá-lo, detectando padrões suspeitos, violações e vulnerabilidades.")

add(3,2,"O que é um critério de entrada (entry criterion) para uma revisão formal?",
    ["O número de participantes",
     "Uma condição que deve ser satisfeita antes de iniciar a revisão (ex.: artefato completo e disponível)",
     "A duração máxima da reunião",
     "O título do documento"],1,
    "Critérios de entrada garantem que a revisão só começa quando o artefato e os pré-requisitos estão prontos, evitando desperdício.")

add(3,2,"Um anti-padrão comum em revisões é:",
    ["Focar em defeitos do artefato",
     "Usar a revisão para avaliar o desempenho ou criticar o autor como pessoa",
     "Preparar-se individualmente antes da reunião",
     "Registrar as anomalias encontradas"],1,
    "Revisar a pessoa em vez do produto cria clima negativo, inibe participação e desvia do objetivo de melhorar o artefato.")

add(3,2,"Qual é o critério de saída típico de uma inspeção formal?",
    ["Todos os participantes concordarem com tudo",
     "Taxa de defeitos abaixo de um limite definido ou todos os defeitos abertos tratados",
     "Tempo de reunião encerrado",
     "Autor aprovar os comentários"],1,
    "Critérios de saída de inspeção incluem limites de densidade de defeitos e resolução de todos os problemas abertos identificados.")

add(3,1,"Qual papel na revisão é responsável por garantir que o processo seja seguido e o ambiente seja produtivo?",
    ["Autor","Moderador (facilitador)","Revisor","Gerente de testes"],1,
    "O moderador facilita a reunião, mantém o foco no artefato, garante o seguimento do processo e gerencia conflitos.")

add(3,2,"A 'revisão baseada em checklist' usa listas para:",
    ["Avaliar o desempenho dos revisores",
     "Guiar os revisores na busca de tipos específicos de defeitos conhecidos",
     "Medir cobertura de código",
     "Automatizar o processo de revisão"],1,
    "Checklists de revisão direcionam a atenção para defeitos típicos (clareza, consistência, completude), aumentando a eficácia.")

add(3,2,"A análise estática por ferramenta pode detectar automaticamente:",
    ["Falhas de usabilidade subjetivas",
     "Variáveis não inicializadas, código morto e violações de padrões de codificação",
     "Bugs que só aparecem sob carga",
     "Erros de lógica de negócio complexos"],1,
    "Ferramentas de análise estática detectam padrões problemáticos como variáveis não usadas, referências nulas potenciais e violações de estilo.")

add(3,2,"Qual é a principal diferença entre uma revisão técnica e uma inspeção?",
    ["A inspeção é menos formal que a revisão técnica",
     "A inspeção tem processo mais rígido com papéis definidos, métricas, entrada/saída e acompanhamento; a revisão técnica é menos formal",
     "A revisão técnica usa checklists; a inspeção não",
     "São equivalentes"],1,
    "A inspeção é a forma mais formal, com papéis, métricas, critérios de entrada/saída e follow-up rigoroso; a revisão técnica é menos rígida.")

add(3,2,"Por que é importante limitar o tamanho do artefato revisado em uma reunião de revisão?",
    ["Para reduzir o número de participantes",
     "Revisões longas causam fadiga, reduzindo a atenção e a taxa de detecção de defeitos",
     "O tamanho não influencia a qualidade",
     "Para economizar papel"],1,
    "Um artefato muito longo leva à fadiga dos revisores, diminuindo a concentração e a eficácia na detecção de defeitos.")

# ============================================================
# CAPÍTULO 4 — TÉCNICAS DE TESTE (33)
# ============================================================
add(4,2,"As técnicas de teste classificam-se principalmente em:",
    ["Manuais e automatizadas","Caixa-preta, caixa-branca e baseadas em experiência",
     "Funcionais e de carga","Estáticas e dinâmicas"],1,
    "As categorias do syllabus: caixa-preta (especificação), caixa-branca (estrutura) e baseadas em experiência.")
add(4,2,"O particionamento de equivalência (EP) baseia-se na ideia de que:",
    ["Cada valor deve ser testado","Valores de uma mesma partição são tratados igualmente, bastando um representante",
     "Só os limites importam","Não há partições inválidas"],1,
    "Em EP, valores de uma partição produzem comportamento equivalente; testa-se um representante por partição.")
add(4,3,"Um campo aceita 1 a 100. Quais partições de equivalência existem (incluindo inválidas)?",
    ["Apenas 1–100","≤0 (inválida), 1–100 (válida) e ≥101 (inválida)",
     "1–50 e 51–100","Somente 1 e 100"],1,
    "Há três partições: abaixo de 1 (inválida), 1–100 (válida) e acima de 100 (inválida).")
add(4,2,"Em EP, por que testar também partições inválidas?",
    ["Para aumentar a contagem de testes","Para verificar o tratamento de entradas fora do esperado",
     "Não é necessário","Para medir desempenho"],1,
    "Partições inválidas verificam se o sistema trata corretamente entradas indevidas (mensagens de erro, rejeição).")
add(4,2,"A análise de valor-fronteira (BVA) é eficaz porque:",
    ["Defeitos raramente ocorrem nos limites","Erros tendem a se concentrar nas fronteiras das partições",
     "Testa todos os valores","Ignora as partições"],1,
    "Defeitos frequentemente ocorrem nos limites; a BVA complementa o EP testando as fronteiras das partições.")
add(4,3,"Um campo aceita 18 a 65. Quais valores usar na BVA de 2 valores?",
    ["18 e 65","17, 18, 65, 66","0 e 100","17, 19, 64, 66"],1,
    "BVA de 2 valores testa, em cada limite, o valor da fronteira e o adjacente do outro lado: 17/18 e 65/66.")
add(4,2,"Na BVA de 3 valores, para o limite superior 65, quais valores são testados?",
    ["65 apenas","64, 65 e 66","63, 64, 65","65, 66, 67"],1,
    "A BVA de 3 valores testa o limite e os dois vizinhos: 64, 65 e 66 para a fronteira 65.")
add(4,3,"Senhas devem ter de 8 a 16 caracteres. Pela BVA de 2 valores, os tamanhos de teste no limite inferior são:",
    ["8 e 9","7 e 8","6, 7, 8","8 e 16"],1,
    "No limite inferior (8), a BVA de 2 valores testa 7 (inválido) e 8 (válido).")
add(4,2,"Uma tabela de decisão é mais indicada quando:",
    ["O sistema depende de estados","Há combinações de condições que levam a ações diferentes (regras de negócio)",
     "Há apenas uma entrada","O foco é desempenho"],1,
    "Tabelas de decisão modelam regras de negócio com combinações de condições e ações resultantes.")
add(4,3,"Uma regra concede frete grátis se (é assinante) E (compra > R$200). Com 2 condições binárias, quantas regras tem a tabela completa?",
    ["2","3","4","8"],2,
    "Duas condições binárias geram 2² = 4 combinações (regras) na tabela completa.")
add(4,3,"Numa tabela de decisão, um desconto é dado se 'cliente VIP' = Sim e 'cupom válido' = Sim. Para a combinação VIP=Sim, cupom=Não, a ação esperada é:",
    ["Conceder desconto","Não conceder desconto","Erro de sistema","Conceder meio desconto"],1,
    "A ação só ocorre quando ambas as condições são verdadeiras; com cupom=Não, não há desconto.")
add(4,2,"Em uma tabela de decisão, condições e ações representam, respectivamente:",
    ["Saídas e entradas","As entradas/causas e os resultados/efeitos esperados",
     "Estados e transições","Casos e dados"],1,
    "Condições são as causas (entradas); ações são os efeitos (resultados) esperados para cada regra.")
add(4,2,"O teste de transição de estados é apropriado para sistemas que:",
    ["Não têm memória de estado","Mudam de comportamento conforme o estado atual e os eventos recebidos",
     "Só processam lotes","Não têm interface"],1,
    "Modela estados, eventos, transições e ações — ideal para sessões, protocolos e workflows.")
add(4,2,"Em um diagrama de estados, uma 'transição inválida' é:",
    ["Uma transição permitida","Um evento que não deveria provocar mudança a partir do estado atual",
     "O estado inicial","Uma ação de saída"],1,
    "Transições inválidas são pares estado/evento sem transição definida; testá-las verifica robustez.")
add(4,3,"Um caixa eletrônico exige cartão antes de aceitar a senha. Tentar digitar a senha sem inserir o cartão testa:",
    ["Uma transição válida","Uma transição inválida (evento inesperado para o estado)",
     "O estado final","Uma ação de entrada"],1,
    "Digitar a senha no estado 'aguardando cartão' é um evento inválido para aquele estado — uma transição inválida.")
add(4,2,"A cobertura de transições válidas (0-switch) exige:",
    ["Cobrir todos os pares de transições","Exercitar cada transição válida individual ao menos uma vez",
     "Cobrir transições inválidas","Cobrir todos os estados apenas"],1,
    "A cobertura 0-switch (de transições simples) cobre cada transição válida pelo menos uma vez.")
add(4,2,"Para escolher entre EP, BVA, tabela de decisão e transição de estados, o critério principal é:",
    ["A ferramenta disponível","A natureza do problema: faixas, combinações de regras ou comportamento por estado",
     "A preferência do testador","O tamanho do time"],1,
    "A técnica adequada depende da estrutura do problema: faixas (EP/BVA), regras (tabela), comportamento por estado (transição).")
add(4,1,"As técnicas de caixa-branca derivam testes a partir de:",
    ["Requisitos do usuário","A estrutura interna: código, fluxo de controle e arquitetura",
     "Experiência do testador","Critérios de aceitação"],1,
    "Caixa-branca usa a estrutura interna (instruções, decisões, fluxos) como base dos testes.")
add(4,2,"A cobertura de instruções (statement coverage) mede:",
    ["O percentual de decisões exercitadas","O percentual de instruções executáveis que foram executadas",
     "O número de caminhos","O número de condições"],1,
    "Cobertura de instruções = instruções executadas ÷ total de instruções executáveis.")
add(4,3,"Um trecho tem 10 instruções executáveis; um teste executou 7. A cobertura de instruções é:",
    ["100%","70%","7%","30%"],1,
    "7 de 10 instruções executadas = 70% de cobertura de instruções.")
add(4,2,"A cobertura de decisões (branch coverage) exige:",
    ["Executar cada instrução","Exercitar cada decisão como verdadeira e como falsa ao menos uma vez",
     "Cobrir todos os caminhos","Testar todas as condições isoladamente"],1,
    "Cobertura de decisões cobre os resultados V e F de cada decisão pelo menos uma vez.")
add(4,3,"Em um 'if' sem 'else', qual cobertura garante testar também o caminho em que a condição é falsa?",
    ["Cobertura de instruções","Cobertura de decisões","Nenhuma","Cobertura de funções"],1,
    "Com um if sem else, 100% de instruções pode ser atingido sem testar o ramo falso; a cobertura de decisões força os dois resultados.")
add(4,2,"Qual afirmação sobre a força das coberturas é correta?",
    ["Instruções é mais forte que decisões","100% de cobertura de decisões implica 100% de cobertura de instruções, mas não o contrário",
     "São equivalentes","Decisões não inclui instruções"],1,
    "Cobertura de decisões é mais forte: atingir 100% dela garante 100% de instruções; o inverso não vale.")
add(4,2,"Qual o valor do teste de caixa-branca?",
    ["Substituir o teste de caixa-preta","Revelar trechos de código não exercitados e medir a minúcia (thoroughness) dos testes",
     "Eliminar a necessidade de cobertura","Testar requisitos de negócio"],1,
    "Caixa-branca mostra o que o código realmente exercita, revelando lacunas que a especificação não evidencia.")
add(4,2,"A suposição de erro (error guessing) consiste em:",
    ["Adivinhar a senha","Antecipar defeitos prováveis com base em experiência, defeitos passados e intuição",
     "Gerar dados aleatórios","Medir cobertura"],1,
    "Error guessing usa experiência e conhecimento de falhas comuns para criar testes que exponham defeitos prováveis.")
add(4,2,"No teste exploratório, o testador:",
    ["Segue scripts pré-definidos","Aprende, projeta e executa testes simultaneamente, frequentemente com test charters",
     "Apenas mede desempenho","Não registra nada"],1,
    "O exploratório combina aprendizado, design e execução em tempo real, muitas vezes guiado por charters e em sessões cronometradas.")
add(4,2,"O teste baseado em checklist apoia-se em:",
    ["Diagramas de estado","Uma lista de itens/condições a verificar, derivada de experiência e heurísticas",
     "Cobertura de código","Tabelas de decisão"],1,
    "Checklists reúnem itens a verificar (heurísticas, lições aprendidas), guiando o teste sem scripts detalhados.")
add(4,2,"Quando as técnicas baseadas em experiência são mais úteis?",
    ["Quando há especificação completa e estável","Quando a documentação é escassa, o tempo é curto ou para complementar técnicas formais",
     "Apenas em sistemas críticos","Somente em testes automatizados"],1,
    "São valiosas com documentação limitada/tempo curto e como complemento às técnicas formais para achar defeitos que escapam.")
add(4,1,"Os '3 C's' da escrita colaborativa de user stories são:",
    ["Code, Compile, Commit","Card (cartão), Conversation (conversa) e Confirmation (confirmação)",
     "Cost, Customer, Contract","Create, Check, Close"],1,
    "Os 3 C's: Card (resumo), Conversation (detalhamento) e Confirmation (critérios de aceitação).")
add(4,2,"Critérios de aceitação de uma user story servem para:",
    ["Estimar custo","Definir as condições que a story deve satisfazer para ser aceita",
     "Medir cobertura de código","Substituir o teste"],1,
    "Critérios de aceitação descrevem o que torna a story 'pronta/aceita', servindo de base para casos de teste.")
add(4,2,"No ATDD (Acceptance Test-Driven Development), os testes de aceitação são:",
    ["Escritos após a entrega","Definidos colaborativamente antes da implementação, a partir dos critérios de aceitação",
     "Apenas automatizados de UI","Opcionais"],1,
    "No ATDD, equipe, negócio e teste definem juntos os testes de aceitação antes de codificar, guiando a implementação.")
add(4,2,"Um requisito descreve faixas de valores e também regras combinando vários campos. A melhor estratégia é:",
    ["Usar só BVA","Combinar técnicas: EP/BVA para as faixas e tabela de decisão para as combinações",
     "Usar só transição de estados","Usar somente exploratório"],1,
    "Problemas mistos pedem combinação de técnicas conforme cada aspecto: faixas (EP/BVA) e regras combinadas (tabela de decisão).")
add(4,2,"A cobertura, em técnicas de teste, mede:",
    ["A quantidade de defeitos","O grau em que itens de cobertura definidos foram exercitados pelos testes",
     "O tempo de execução","O número de testadores"],1,
    "Cobertura expressa quanto dos itens de cobertura (partições, decisões, transições) os testes exercitaram.")

# ============================================================
# CAPÍTULO 4 — TÉCNICAS DE TESTE (continuação, +22)
# ============================================================
add(4,3,"Um campo de temperatura aceita de -10 a 50°C. Pela BVA de 2 valores, quais são os 4 valores de fronteira a testar?",
    ["-10 e 50",
     "-11, -10, 50, 51",
     "-10, 0, 50, 100",
     "-9, -10, 49, 50"],1,
    "BVA de 2 valores testa o valor da fronteira e o imediatamente adjacente do lado inválido: -11/-10 (limite inferior) e 50/51 (limite superior).")

add(4,3,"Uma tabela de decisão tem 3 condições binárias. Quantas regras a tabela completa (sem colapso) possui?",
    ["3","6","8","9"],2,
    "Três condições binárias geram 2³ = 8 combinações (regras) na tabela de decisão completa.")

add(4,3,"Um sistema de desconto aplica desconto se: (cliente premium = Sim) OU (valor do pedido > R$500). Quantas regras distintas existem com 2 condições binárias?",
    ["2","4","6","8"],1,
    "Duas condições binárias geram 2² = 4 regras; a tabela completa tem 4 colunas independentemente do operador lógico.")

add(4,3,"Numa máquina de estados de conta bancária: estados = {Ativa, Bloqueada, Encerrada}. Quantas transições inválidas existem se há apenas 4 transições válidas definidas?",
    ["4","5","8","6"],2,
    "Com 3 estados, há 3×3 = 9 células na matriz (incluindo auto-transições); com 4 válidas, há 9-4 = 5 transições inválidas a verificar.")

add(4,3,"Um trecho de código tem 20 instruções executáveis. Um conjunto de testes executou 15. Qual é a cobertura de instruções?",
    ["75%","15%","85%","20%"],0,
    "Cobertura de instruções = executadas ÷ total = 15 ÷ 20 = 75%.")

add(4,3,"Um método tem 4 decisões (if/else). Para 100% de cobertura de decisões, quantos resultados de decisão precisam ser exercitados no mínimo?",
    ["4","8","2","16"],1,
    "Cada decisão tem 2 resultados (V/F); 4 decisões × 2 resultados = 8 resultados mínimos a exercitar para 100% de cobertura de decisões.")

add(4,3,"Um campo aceita idades de 0 a 120 anos (inteiros). Pela BVA de 3 valores, quais valores testar no limite inferior (0)?",
    ["0 e 1",
     "-1, 0 e 1",
     "0, 1 e 2",
     "-2, -1 e 0"],1,
    "BVA de 3 valores testa o limite e seus dois vizinhos: para o limite inferior 0, testam-se -1, 0 e 1.")

add(4,3,"Um formulário tem campo 'quantidade' que aceita apenas 1, 2 ou 3. Pela EP, qual partição inválida existe acima do limite?",
    ["Não existe partição inválida superior",
     "Valores ≥ 4",
     "Valores = 0",
     "Valores negativos"],1,
    "A partição inválida superior inclui todos os valores ≥ 4 (acima do máximo 3); valores ≤ 0 formam a partição inválida inferior.")

add(4,2,"Em uma máquina de estados com cobertura de todas as transições (0-switch), qual cenário de login é mais adequado?",
    ["Testar apenas o login com sucesso",
     "Testar cada transição possível ao menos uma vez: login com sucesso, senha errada, bloqueio de conta, logout",
     "Testar somente o estado inicial",
     "Testar apenas transições inválidas"],1,
    "Cobertura 0-switch exige exercitar cada transição válida individualmente, cobrindo todos os arcos do diagrama de estados.")

add(4,2,"Ao testar um sistema de controle de semáforo (Verde → Amarelo → Vermelho → Verde), qual técnica é mais indicada?",
    ["Particionamento de equivalência",
     "Teste de transição de estados, pois o comportamento depende do estado atual",
     "Análise de valor-fronteira",
     "Tabela de decisão"],1,
    "Semáforos têm estados bem definidos e transições sequenciais — a técnica de transição de estados modela esse comportamento com precisão.")

add(4,3,"Em EP, ao testar um campo de nota de 0 a 10 (números inteiros), um testador usa apenas o valor 5. Qual é o problema dessa abordagem?",
    ["O valor 5 está correto; a abordagem é adequada",
     "Testa apenas a partição válida; as partições inválidas (< 0 e > 10) não são cobertas",
     "O EP exige testar todos os valores de 0 a 10",
     "O EP não se aplica a números inteiros"],1,
    "EP exige ao menos um representante de cada partição — válidas e inválidas; usar só valor 5 ignora as partições inválidas abaixo de 0 e acima de 10.")

add(4,3,"Um programa contém o trecho: if (x > 0) { y = x * 2; } z = y + 1; Com apenas um caso de teste onde x=5, qual cobertura é atingida?",
    ["100% de instruções e 100% de decisões",
     "100% de instruções executadas no caminho, mas não 100% de decisões (ramo falso não testado)",
     "0% de cobertura",
     "100% de decisões"],1,
    "Com x=5 (condição verdadeira), y=x*2 e z=y+1 são executados. O ramo falso (x≤0) não é testado, então cobertura de decisões < 100%.")

add(4,2,"O erro guessing (suposição de erro) é mais eficaz quando o testador:",
    ["Nunca viu o sistema antes",
     "Tem experiência com o domínio, conhece defeitos passados e entende erros comuns de implementação",
     "Usa apenas técnicas formais",
     "Não conhece o código"],1,
    "A eficácia do error guessing cresce com a experiência do testador: conhecimento de domínio e histórico de defeitos orientam a intuição.")

add(4,2,"O teste exploratório em sessões cronometradas (session-based testing) usa 'test charters' para:",
    ["Documentar todos os passos antes de executar",
     "Definir a missão da sessão: escopo, objetivo e área a explorar, sem detalhar cada passo",
     "Substituir o planejamento de teste",
     "Medir cobertura de código"],1,
    "Charters definem o foco da sessão exploratória (o que explorar e por quê) sem pré-determinar os passos exatos de execução.")

add(4,2,"Quando se usa uma checklist de teste em vez de casos de teste detalhados?",
    ["Quando há muito tempo disponível",
     "Quando se quer agilidade e experiência do testador para decidir como verificar cada item, sem scripts rígidos",
     "Somente em sistemas críticos",
     "Quando a automação não é possível"],1,
    "Checklists oferecem flexibilidade: o testador decide como verificar cada item, usando seu julgamento — adequado quando scripts detalhados seriam excessivos.")

add(4,2,"No ATDD, quem define os critérios de aceitação antes da implementação?",
    ["Apenas o testador",
     "Equipe de desenvolvimento, representantes de negócio e testadores colaborativamente",
     "Apenas o product owner",
     "O gerente de projetos"],1,
    "ATDD é colaborativo: negócio, dev e teste definem juntos os critérios/testes de aceitação antes de implementar a funcionalidade.")

add(4,3,"Qual técnica de caixa-preta seria mais indicada para testar regras de elegibilidade de empréstimo que combinam renda, histórico de crédito e tempo de emprego?",
    ["Análise de valor-fronteira",
     "Tabela de decisão, pois há múltiplas condições combinadas que levam a decisões diferentes",
     "Teste de transição de estados",
     "Cobertura de instruções"],1,
    "Quando o resultado depende de combinações de múltiplas condições (regras de negócio), a tabela de decisão é a técnica mais indicada.")

add(4,3,"Um campo aceita valores de R$1,00 a R$9.999,99. Na BVA de 2 valores, quais são os valores de teste para o limite inferior?",
    ["R$1,00 e R$9.999,99",
     "R$0,99 e R$1,00",
     "R$1,00 e R$1,01",
     "R$0,00 e R$1,00"],1,
    "No limite inferior R$1,00, a BVA de 2 valores testa o valor abaixo do limite (R$0,99, inválido) e o próprio limite (R$1,00, válido).")

add(4,2,"Em um diagrama de estados, o que a cobertura de 'switch-1' (transição de pares) garante além da cobertura 0-switch?",
    ["Nada de adicional",
     "Que pares de transições consecutivas (sequências de 2) são exercitados, aumentando a profundidade da cobertura",
     "Cobertura de todas as condições",
     "Cobertura de todas as instruções"],1,
    "Switch-1 cobre sequências de 2 transições (pares), detectando erros que só aparecem em combinações de transições, e é mais forte que 0-switch.")

add(4,2,"A combinação de EP e BVA é mais eficaz que usar cada técnica isoladamente porque:",
    ["EP e BVA são equivalentes",
     "EP reduz o espaço de teste; BVA complementa testando os pontos mais propensos a defeitos (fronteiras)",
     "BVA substitui completamente o EP",
     "EP testa apenas valores válidos; BVA apenas inválidos"],1,
    "EP define as partições, reduzindo o espaço; BVA aprofunda nos limites dessas partições, onde defeitos são mais frequentes.")

add(4,2,"Por que a cobertura de 100% de instruções não é suficiente como único critério de qualidade?",
    ["Porque é impossível de atingir",
     "Porque não garante que todos os ramos de decisão foram testados, podendo deixar caminhos sem teste",
     "Porque é muito cara de atingir",
     "Porque não é aceita pelo syllabus"],1,
    "100% de instruções pode ser atingido sem testar o ramo falso de um if sem else; a cobertura de decisões é mais forte e mais reveladora.")

add(4,2,"Qual é o objetivo principal do teste baseado em experiência (experience-based testing)?",
    ["Substituir técnicas formais em todos os casos",
     "Aproveitar o conhecimento e a intuição do testador para encontrar defeitos que técnicas formais podem perder",
     "Gerar casos de teste aleatórios",
     "Medir a cobertura de código"],1,
    "Técnicas baseadas em experiência complementam as formais, explorando o conhecimento do testador sobre defeitos comuns e comportamentos inesperados.")

# ============================================================
# CAPÍTULO 5 — GERENCIAMENTO (27)
# ============================================================
add(5,1,"O plano de teste tem como propósito principal:",
    ["Listar todos os defeitos","Documentar objetivos, escopo, abordagem, recursos e critérios do esforço de teste",
     "Substituir os casos de teste","Aprovar a entrega"],1,
    "O plano comunica objetivos, escopo, abordagem, recursos, cronograma, riscos e critérios de entrada/saída.")
add(5,2,"Qual a diferença entre estratégia de teste e abordagem de teste?",
    ["São sinônimos","A estratégia é uma descrição geral/organizacional; a abordagem é a aplicação adaptada a um projeto específico",
     "Abordagem é mais ampla que estratégia","Estratégia só existe em ágil"],1,
    "A estratégia descreve o nível geral/organizacional; a abordagem adapta a estratégia ao contexto do projeto.")
add(5,1,"Critérios de entrada (entry criteria) definem:",
    ["Quando parar o teste","As pré-condições para iniciar uma atividade de teste",
     "O número de defeitos aceitável","A cobertura final"],1,
    "Critérios de entrada são as condições necessárias para começar (ambiente pronto, casos aprovados, dados disponíveis).")
add(5,2,"Critérios de saída (exit criteria) servem para:",
    ["Iniciar o teste","Determinar quando uma atividade/nível de teste pode ser considerado concluído",
     "Estimar esforço","Selecionar ferramentas"],1,
    "Critérios de saída definem quando encerrar (cobertura atingida, defeitos abertos abaixo do limite, prazo cumprido).")
add(5,2,"Em métodos ágeis, 'Definition of Done' (DoD) funciona como:",
    ["Critério de entrada","Um conjunto de critérios de saída para considerar um item realmente concluído",
     "Um relatório de defeitos","Um plano de teste"],1,
    "A DoD é um conjunto de critérios de saída que define quando um item de trabalho está realmente pronto.")
add(5,2,"A estimativa baseada em ratios (proporções) usa:",
    ["Opinião de especialistas apenas","Proporções históricas (e.g., relação entre esforço de dev e de teste) para projetar o esforço",
     "Geração aleatória","Cobertura de código"],1,
    "A técnica de ratios aplica proporções de projetos passados (ex.: % do esforço destinado ao teste) para estimar.")
add(5,2,"A estimativa por extrapolação (metrics-based) baseia-se em:",
    ["Achismo","Dados/medições de iterações ou projetos anteriores, extrapolando para o atual",
     "Apenas no orçamento","No número de testadores"],1,
    "A abordagem baseada em métricas usa dados históricos para extrapolar o esforço esperado.")
add(5,2,"A estimativa baseada em especialistas (expert-based) caracteriza-se por:",
    ["Ignorar a experiência","Apoiar-se no julgamento de quem conhece as tarefas (ex.: Wideband Delphi/Planning Poker)",
     "Usar somente fórmulas","Dispensar consenso"],1,
    "A abordagem baseada em especialistas usa o conhecimento dos responsáveis pelas tarefas, e.g., Planning Poker/Delphi.")
add(5,2,"Na priorização de casos por risco, os testes executados primeiro são:",
    ["Os mais rápidos","Os que cobrem os itens de maior risco",
     "Os mais antigos","Os escolhidos aleatoriamente"],1,
    "A priorização baseada em risco executa antes os testes de maior risco (probabilidade × impacto).")
add(5,2,"Na priorização baseada em cobertura, a ordem é definida por:",
    ["Custo do caso","Quanto cada teste adiciona de cobertura ainda não atingida",
     "Tamanho do código","Ordem alfabética"],1,
    "A priorização por cobertura ordena para maximizar rapidamente a cobertura ainda não exercitada.")
add(5,2,"A 'pirâmide de testes' sugere que devemos ter:",
    ["Mais testes de UI que de unidade","Muitos testes de unidade na base e poucos testes de UI/E2E no topo",
     "Apenas testes manuais","Igual número em cada nível"],1,
    "A pirâmide recomenda muitos testes rápidos/baratos (unidade) na base e poucos lentos/frágeis (UI/E2E) no topo.")
add(5,2,"Os 'quadrantes de teste' (testing quadrants) ajudam a:",
    ["Medir cobertura de código","Classificar tipos de teste por foco em negócio/tecnologia e por apoiar a equipe ou criticar o produto",
     "Estimar custos","Definir o DoD"],1,
    "Os quadrantes organizam os testes (apoio à equipe vs. crítica ao produto; foco negócio vs. tecnologia) para planejar a cobertura.")
add(5,1,"Em gestão de teste, 'risco' é definido como:",
    ["Um defeito encontrado","Um evento futuro possível com consequências negativas",
     "Uma falha em produção","Um caso de teste reprovado"],1,
    "Risco é a possibilidade de um evento futuro com efeito negativo; combina probabilidade e impacto.")
add(5,2,"Como se determina o nível de um risco?",
    ["Custo × prazo","Probabilidade de ocorrência combinada ao impacto do dano",
     "Severidade × prioridade","Número de defeitos"],1,
    "Nível de risco = probabilidade de ocorrência × impacto (magnitude do dano).")
add(5,2,"Qual a diferença entre risco de produto e risco de projeto?",
    ["São o mesmo","Risco de produto afeta a qualidade do produto; risco de projeto afeta a capacidade de atingir os objetivos do projeto",
     "Risco de projeto é sempre técnico","Risco de produto envolve só prazo"],1,
    "Risco de produto: o produto pode falhar/insatisfazer. Risco de projeto: prazo, custo, recursos, fornecedores.")
add(5,2,"Qual destes é um exemplo de risco de PROJETO?",
    ["Cálculo financeiro incorreto","Atraso na entrega por falta de pessoal qualificado",
     "Falha de segurança no login","Lentidão sob carga"],1,
    "Falta de recursos/atrasos são riscos de projeto; os demais são riscos de produto (qualidade).")
add(5,2,"Qual destes é um exemplo de risco de PRODUTO?",
    ["Orçamento estourado","Vazamento de dados por falha de segurança",
     "Fornecedor atrasado","Equipe sem treinamento"],1,
    "Falha de segurança afeta a qualidade do produto; os demais são riscos de projeto.")
add(5,2,"O teste baseado em risco usa a avaliação de risco para:",
    ["Eliminar a documentação","Decidir o que testar, quanto e em que ordem, alocando esforço conforme o risco",
     "Definir salários","Escolher a linguagem"],1,
    "O risco orienta seleção, profundidade e priorização do teste, concentrando esforço onde o risco é maior.")
add(5,2,"A avaliação de risco (risk assessment) compreende:",
    ["Somente corrigir defeitos","Identificar riscos e analisá-los (estimar probabilidade e impacto)",
     "Executar os testes","Aprovar a entrega"],1,
    "A avaliação inclui identificação dos riscos e sua análise (probabilidade e impacto) para priorização.")
add(5,2,"Como o nível de risco influencia o esforço de teste?",
    ["Não influencia","Maior risco implica testes mais minuciosos, mais cedo e por pessoal mais experiente",
     "Riscos altos são ignorados","Reduz a cobertura"],1,
    "Itens de maior risco recebem técnicas mais rigorosas, início mais cedo e, por vezes, revisão independente.")
add(5,2,"O propósito do monitoramento de teste é:",
    ["Escrever casos","Fornecer visibilidade do progresso comparando o real com o planejado",
     "Corrigir o código","Selecionar ferramentas"],1,
    "O monitoramento coleta informações sobre o andamento para comparar com o plano e apoiar o controle.")
add(5,1,"Qual destas é uma métrica típica de teste?",
    ["Cor do tema da IDE","Percentual de casos executados e taxa de aprovação",
     "Salário do time","Número de reuniões"],1,
    "Métricas comuns: casos planejados/executados/aprovados/reprovados, cobertura, densidade e tendência de defeitos.")
add(5,2,"Um relatório de progresso de teste destina-se principalmente a:",
    ["Substituir o plano","Informar as partes interessadas sobre o andamento e apoiar decisões durante o teste",
     "Encerrar o projeto","Listar requisitos"],1,
    "O relatório de progresso comunica status, riscos e resultados às partes interessadas durante a execução.")
add(5,1,"O relatório de conclusão de teste é produzido:",
    ["Antes de iniciar o teste","Ao final de uma atividade/marco, resumindo o que foi feito e os resultados",
     "Diariamente","A cada defeito"],1,
    "O relatório de conclusão resume resultados, cobertura, qualidade alcançada e lições, ao fim de um nível/marco.")
add(5,2,"A gestão de configuração apoia o teste ao:",
    ["Aumentar o número de defeitos","Garantir versões/identificação consistentes de itens de teste e testware, com rastreabilidade",
     "Substituir o plano","Eliminar o controle de versão"],1,
    "A gestão de configuração mantém integridade e rastreabilidade de itens sob teste e do testware (versões, baselines).")
add(5,1,"O que um bom relatório de defeito deve conter?",
    ["Apenas o título","Identificação, descrição, passos para reproduzir, resultado esperado/obtido, severidade e prioridade",
     "Somente a severidade","O nome do desenvolvedor culpado"],1,
    "Relatórios eficazes trazem id, descrição, passos, esperado vs. obtido, ambiente, severidade e prioridade.")
add(5,2,"Qual a diferença entre severidade e prioridade de um defeito?",
    ["São o mesmo","Severidade mede o impacto técnico; prioridade mede a urgência de correção sob a ótica do negócio",
     "Prioridade é definida pelo desenvolvedor","Severidade depende do prazo"],1,
    "Severidade = impacto no sistema; prioridade = urgência de corrigir; podem ser independentes entre si.")

# ============================================================
# CAPÍTULO 5 — GERENCIAMENTO (continuação, +18)
# ============================================================
add(5,3,"Um risco tem probabilidade de ocorrência de 30% e impacto avaliado em 4 (escala 1–5). Qual é o nível de risco?",
    ["0,3","1,2","4,3","7"],1,
    "Nível de risco = probabilidade × impacto = 0,30 × 4 = 1,2 (em escala numérica).")

add(5,3,"Dois riscos: Risco A (probabilidade 20%, impacto 5) e Risco B (probabilidade 50%, impacto 2). Qual deve ser priorizado?",
    ["Risco A, nível 1,0 < Risco B 1,0 — empate; prioriza o que for mais barato de mitigar",
     "Risco A (nível 1,0) e Risco B (nível 1,0) têm o mesmo nível; outros fatores decidem",
     "Risco B por ter maior probabilidade",
     "Risco A por ter maior impacto"],1,
    "Nível A = 0,20×5 = 1,0; Nível B = 0,50×2 = 1,0 — empate em nível de risco; critérios secundários (custo de mitigação, visibilidade) decidem.")

add(5,2,"A técnica de estimativa de teste por 'Planning Poker' é uma variante de:",
    ["Estimativa baseada em ratios",
     "Estimativa baseada em especialistas (Wideband Delphi), usando consenso do time",
     "Estimativa por extrapolação de métricas",
     "Análise de pontos de função"],1,
    "Planning Poker é uma variação do Wideband Delphi: cada membro vota secretamente e o time discute até convergir, aproveitando a expertise coletiva.")

add(5,2,"Uma estimativa de esforço de teste baseada em ratios usa a proporção histórica de que o teste consome 30% do esforço total. Se o desenvolvimento está estimado em 1000h, o esforço de teste estimado é:",
    ["300h","700h","30h","1300h"],0,
    "Ratio de 30%: esforço de teste = 30% × 1000h = 300h.")

add(5,2,"A pirâmide de testes coloca testes de contrato/API no nível intermediário porque:",
    ["São mais lentos que testes de UI",
     "São mais rápidos e estáveis que testes E2E/UI, mas validam mais integração que testes unitários",
     "Apenas verificam a interface gráfica",
     "São equivalentes a testes unitários"],1,
    "Testes de API/integração são intermediários: mais rápidos e menos frágeis que E2E, mas com maior abrangência que unitários.")

add(5,2,"Os quadrantes de teste Q1 (que apoiam o time, orientados à tecnologia) incluem principalmente:",
    ["Testes de usabilidade e exploratórios",
     "Testes unitários e de componente automatizados que guiam o desenvolvimento",
     "Testes de aceitação de usuário",
     "Testes de carga e desempenho"],1,
    "Q1 (technology-facing, team-support): testes unitários e de componente automatizados que apoiam o desenvolvimento (TDD).")

add(5,2,"Os quadrantes de teste Q4 (que criticam o produto, orientados à tecnologia) incluem:",
    ["Testes de aceitação do usuário",
     "Testes de desempenho, segurança, confiabilidade e outros atributos de qualidade não funcionais",
     "Testes unitários",
     "Testes exploratórios de negócio"],1,
    "Q4 (technology-facing, product-critique): testes não funcionais como desempenho, segurança e confiabilidade, geralmente automatizados.")

add(5,2,"Qual é a diferença entre severidade e prioridade de um defeito em um cenário prático?",
    ["São sempre iguais",
     "Um bug cosmético (baixa severidade) pode ter alta prioridade se está na tela de marketing de um lançamento iminente",
     "Alta severidade implica sempre alta prioridade",
     "A prioridade é definida pelo testador; a severidade pelo cliente"],1,
    "Severidade e prioridade são independentes: um bug cosmético pode ser urgente (alta prioridade) por razões de negócio, mesmo com baixo impacto técnico.")

add(5,2,"Na gestão de configuração, um 'baseline' (linha de base) é:",
    ["Um erro no sistema de controle de versão",
     "Uma versão aprovada e fixada de um ou mais itens de configuração, usada como referência",
     "O ambiente de produção",
     "O plano de teste aprovado"],1,
    "Uma baseline é uma referência estável e formalmente aprovada de itens de configuração, usada para controlar mudanças subsequentes.")

add(5,1,"Qual das seguintes é uma métrica de progresso de teste útil para monitoramento diário?",
    ["Número de linhas de código por desenvolvedor",
     "Percentual de casos de teste executados e taxa de aprovação/reprovação",
     "Horas de reunião por semana",
     "Número de funcionalidades solicitadas"],1,
    "Métricas de execução (% executados, aprovados, reprovados) fornecem visibilidade direta do progresso real versus o planejado.")

add(5,2,"O 'relatório de defeito' (bug report) de qualidade deve evitar:",
    ["Incluir passos para reproduzir",
     "Linguagem subjetiva, culpa pessoal ou título vago como 'sistema não funciona'",
     "Registrar a severidade",
     "Mencionar o ambiente de teste"],1,
    "Bons relatórios são objetivos, descritivos e factuais; linguagem acusatória e títulos vagos prejudicam a triagem e a correção eficiente.")

add(5,2,"Qual é o propósito do relatório de conclusão de teste (test completion report)?",
    ["Listar apenas os defeitos abertos",
     "Resumir os resultados do ciclo de teste, comunicar a qualidade atingida e registrar lições aprendidas",
     "Substituir o plano de teste para o próximo ciclo",
     "Aprovar o lançamento do produto"],1,
    "O relatório de conclusão consolida resultados, cobertura, defeitos, desvios do plano e lições, servindo de referência para ciclos futuros.")

add(5,3,"A abordagem de teste baseada em risco (risk-based testing) afeta o planejamento ao:",
    ["Ignorar funcionalidades de baixo risco",
     "Alocar mais esforço, profundidade e antecipação aos itens de maior risco de produto",
     "Eliminar testes de regressão",
     "Reduzir o número total de casos de teste sempre"],1,
    "O risco orienta onde investir mais (técnicas mais rigorosas, início antecipado) e permite reduzir esforço em áreas de baixo risco.")

add(5,3,"Quando critérios de saída não são atingidos mas o prazo chegou ao fim, qual ação é mais adequada?",
    ["Ignorar os critérios e encerrar o teste",
     "Relatar o status, os riscos residuais e deixar a decisão de encerrar ou continuar para os stakeholders",
     "Continuar o teste indefinidamente",
     "Reprovar formalmente o sistema"],1,
    "O gerente de testes reporta riscos residuais e status; a decisão de encerrar ou não é de negócio, tomada pelos stakeholders com informação completa.")

add(5,2,"Qual técnica de priorização é mais indicada quando o tempo é muito curto e é necessário garantir que o mais crítico seja testado primeiro?",
    ["Priorização aleatória",
     "Priorização baseada em risco: testa primeiro o que tem maior nível de risco",
     "Priorização por ordem alfabética de módulo",
     "Testar primeiro os casos mais curtos"],1,
    "Com tempo limitado, a priorização por risco garante que o esforço disponível cubra o que causaria maior impacto caso falhasse.")

add(5,2,"A 'análise de impacto' (impact analysis) em teste de manutenção serve para:",
    ["Estimar o custo do projeto",
     "Identificar quais partes do sistema e quais testes são afetados por uma mudança",
     "Selecionar a ferramenta de automação",
     "Planejar treinamentos da equipe"],1,
    "A análise de impacto determina o escopo da regressão: quais áreas foram afetadas pela mudança e quais testes devem ser executados.")

add(5,2,"Em projetos ágeis, o 'Definition of Ready' (DoR) para uma história de usuário significa que:",
    ["A história já foi implementada",
     "A história atende aos critérios mínimos para entrar no sprint (critérios de aceitação definidos, estimada, sem dependências bloqueantes)",
     "Todos os testes da história foram escritos",
     "O código foi revisado"],1,
    "DoR define quando uma história está suficientemente preparada para ser trabalhada no sprint, incluindo critérios de aceitação claros para o teste.")

add(5,2,"Em gestão de configuração, o que é um 'item de configuração' (configuration item)?",
    ["Um caso de teste individual",
     "Qualquer artefato (componente, documento, ambiente) identificado e gerenciado como unidade no sistema de controle de configuração",
     "Uma linha de código",
     "Um relatório de defeito"],1,
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
    ["Reduzir custos imediatamente","Subestimar o esforço de implantação e, principalmente, de manutenção dos scripts",
     "Eliminar o teste manual","Aumentar a cobertura sem esforço"],1,
    "Riscos incluem expectativas irreais, custo de manutenção, dependência da ferramenta e scripts frágeis.")
add(6,2,"Um benefício geral das ferramentas de teste é:",
    ["Garantir ausência de defeitos","Reduzir trabalho repetitivo e aumentar consistência e repetibilidade",
     "Substituir o julgamento humano","Dispensar o planejamento"],1,
    "Ferramentas reduzem tarefas manuais repetitivas, aumentam consistência e dão acesso a informações (ex.: cobertura).")
add(6,2,"Ao selecionar uma ferramenta de teste, deve-se considerar principalmente:",
    ["Apenas o preço","Maturidade da organização, ajuste ao contexto/processo e avaliação por meio de prova de conceito",
     "A popularidade nas redes","A cor da interface"],1,
    "A seleção avalia contexto, maturidade, restrições, integração e geralmente inclui uma avaliação/PoC antes de adotar.")
add(6,2,"Antes de implantar amplamente uma nova ferramenta, recomenda-se:",
    ["Comprar a licença para toda a empresa","Conduzir um projeto piloto para avaliar ajuste, definir uso e medir benefícios",
     "Treinar depois da implantação total","Dispensar métricas"],1,
    "Um piloto permite avaliar o ajuste à organização, definir diretrizes de uso e estimar custos/benefícios antes da escala.")

# ============================================================
# CAPÍTULO 6 — FERRAMENTAS (continuação, +4)
# ============================================================
add(6,2,"Um projeto deseja automatizar testes de regressão de API. Que categoria de ferramenta é mais adequada?",
    ["Ferramenta de gestão de requisitos",
     "Ferramenta de execução de testes de API (ex.: cliente REST com asserções automatizadas)",
     "Ferramenta de análise estática",
     "Ferramenta de revisão de código"],1,
    "Ferramentas de teste de API (como frameworks REST com asserções) são a categoria adequada para automatizar regressão de serviços.")

add(6,2,"O ROI (retorno sobre investimento) da automação de testes tende a ser maior quando:",
    ["Os testes são executados poucas vezes",
     "Os testes são estáveis, executados frequentemente e o custo de manutenção é menor que o de execução manual repetida",
     "O sistema muda a cada sprint sem compatibilidade retroativa",
     "A equipe ainda não conhece a ferramenta"],1,
    "ROI positivo ocorre quando testes estáveis e frequentes amortizam o custo inicial de automação e de manutenção ao longo do tempo.")

add(6,2,"Qual é o risco de 'scripts frágeis' (brittle scripts) na automação de testes de UI?",
    ["Scripts rodam muito rápido",
     "Pequenas mudanças na interface quebram os scripts, gerando alto custo de manutenção",
     "Os scripts cobrem muitos cenários",
     "A automação detecta mais defeitos"],1,
    "Scripts de UI que dependem de seletores frágeis (coordenadas, textos literais) se quebram com qualquer mudança de layout, aumentando manutenção.")

add(6,2,"Ao avaliar uma ferramenta de automação de testes, qual critério é mais importante segundo boas práticas?",
    ["A quantidade de funcionalidades da ferramenta",
     "O ajuste ao contexto da organização: tecnologia do sistema, habilidades da equipe, integração com o processo",
     "O número de usuários da ferramenta no mercado",
     "A data de lançamento da ferramenta"],1,
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
