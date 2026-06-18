# -*- coding: utf-8 -*-
"""
add_en.py — injeta locales.en nas questões do banco CTFL.

USO:
  python3 add_en.py

Lê:  ctfl-questions-ptbr.json  (o banco atual)
Gera: ctfl-questions-ptbr.json  (mesmo arquivo, atualizado in-place)

Segurança:
  - Nunca altera id, chapter, domain, kLevel nem answer.
  - Nunca sobrescreve locales.pt.
  - Se uma questão já tiver locales.en, MANTÉM o existente (não sobrescreve).
  - Questões sem EN no dicionário abaixo ficam intactas.
  - Imprime relatório ao final.
"""

import json, sys

# Dicionário de traduções EN.
# Chave = question id.
# Valor = { "q": str, "options": [str x4], "exp": str }
# A ordem das options DEVE ser idêntica ao PT (answer index é compartilhado).

EN = {

# ============================================================
# CHAPTER 1 — FUNDAMENTALS OF TESTING (40 questions)
# ============================================================

"ch1-01": {
    "q": "Which correctly describes the relationship between error, defect, and failure?",
    "options": [
        "Error is caused by the tester; defect by the developer; failure by the user",
        "An error (human action) introduces a defect into an artifact, which when executed may cause a failure",
        "Error and defect are synonyms; failure only occurs in production",
        "A failure causes a defect, which causes an error"
    ],
    "exp": "The causal chain is: human error → defect in the artifact/code → failure (incorrect behavior at runtime)."
},
"ch1-02": {
    "q": "Which is NOT a typical objective of testing?",
    "options": [
        "Finding defects",
        "Reducing the level of risk",
        "Verifying requirements",
        "Mathematically proving the absence of all defects"
    ],
    "exp": "Testing cannot prove the absence of defects; it provides information and reduces risk, but cannot guarantee perfection."
},
"ch1-03": {
    "q": "What is the difference between testing and debugging?",
    "options": [
        "They are the same activity",
        "Testing finds failures; debugging locates, analyzes, and fixes the defect that caused them",
        "Debugging finds failures; testing fixes the code",
        "Debugging only occurs in production"
    ],
    "exp": "Testing reveals failures caused by defects; debugging is the development activity that locates, diagnoses, and corrects the defect."
},
"ch1-04": {
    "q": "Why is testing necessary?",
    "options": [
        "To replace code review",
        "To contribute to project success by reducing the risk of failures in operation",
        "To guarantee defect-free software",
        "Because it is required by law"
    ],
    "exp": "Testing reduces the risk of operational failures and helps deliver a product with quality adequate to stakeholder needs."
},
"ch1-05": {
    "q": "How do quality control (QC) and quality assurance (QA) relate?",
    "options": [
        "They are synonyms",
        "QC is product-oriented (includes testing); QA is process-oriented",
        "QA is product-oriented; QC is process-oriented",
        "Testing is part of QA, not QC"
    ],
    "exp": "QC focuses on the product and includes activities such as testing; QA focuses on process improvement to build confidence that quality will be achieved."
},
"ch1-06": {
    "q": "The root cause of a defect is:",
    "options": [
        "The failure observed by the user",
        "The earliest event that, if corrected, prevents the recurrence of the defect",
        "The test environment",
        "The test case that failed"
    ],
    "exp": "Root cause analysis seeks the fundamental origin, enabling actions that prevent similar defects from recurring."
},
"ch1-07": {
    "q": "The principle 'testing shows the presence of defects, not their absence' means that:",
    "options": [
        "Testing proves there are no defects",
        "Testing can reveal defects but cannot prove none exist",
        "Defects always exist",
        "Testing is useless"
    ],
    "exp": "Finding defects does not prove their absence; even when no defects are found, there is no guarantee of total correctness."
},
"ch1-08": {
    "q": "The principle 'exhaustive testing is impossible' has the practical consequence of:",
    "options": [
        "Not worth testing",
        "Using risk analysis and priorities to focus effort",
        "Testing only the happy path",
        "Automating everything"
    ],
    "exp": "Since testing all combinations is not feasible, effort is prioritized based on risk and business priorities."
},
"ch1-09": {
    "q": "The 'early testing saves time and money' principle states that:",
    "options": [
        "Tests should only start after the code is complete",
        "Testing activities should start as early as possible in the lifecycle",
        "Testing early increases costs",
        "Only requirements can be tested early"
    ],
    "exp": "Starting early (including static testing on requirements) reduces costs because defects found late are more expensive to fix."
},
"ch1-10": {
    "q": "The 'defect clustering' principle suggests that:",
    "options": [
        "Defects are evenly distributed",
        "A small number of modules contain the majority of defects",
        "Each module has exactly one defect",
        "Defects only appear in new code"
    ],
    "exp": "Typically a minority of modules concentrates most defects (Pareto principle), which guides test prioritization."
},
"ch1-11": {
    "q": "The 'pesticide paradox' indicates that:",
    "options": [
        "More testing generates more defects",
        "Repeating the same tests will eventually stop finding new defects",
        "Manual tests are better than automated",
        "Pesticides affect the software"
    ],
    "exp": "If the same test cases are repeated, they stop revealing new defects; tests must be reviewed and new ones created regularly."
},
"ch1-12": {
    "q": "The principle 'testing is context-dependent' means that:",
    "options": [
        "All software is tested the same way",
        "The way of testing varies according to domain, risk, and context",
        "Context does not matter",
        "Only critical systems need testing"
    ],
    "exp": "Different systems (e.g., e-commerce vs. medical software) require different approaches, techniques, and rigor."
},
"ch1-13": {
    "q": "The 'absence-of-errors fallacy' states that:",
    "options": [
        "Defect-free software is always good",
        "Fixing all known defects is useless if the system does not meet user needs",
        "Errors do not exist",
        "Errors do not matter"
    ],
    "exp": "A product may be free of known defects and still be inadequate if it does not meet real user needs."
},
"ch1-14": {
    "q": "A team decides to prioritize testing the payment module, where defects have historically clustered. Which principle justifies this?",
    "options": [
        "Exhaustive testing",
        "Defect clustering",
        "Absence-of-errors fallacy",
        "Pesticide paradox"
    ],
    "exp": "Concentrating effort where defects historically cluster applies the defect clustering principle."
},
"ch1-15": {
    "q": "Which test process activity defines objectives, approach, and resources?",
    "options": [
        "Test execution",
        "Test planning",
        "Test analysis",
        "Test completion"
    ],
    "exp": "Test planning defines objectives, scope, approach, resources, and criteria."
},
"ch1-16": {
    "q": "Monitoring and control of testing serves to:",
    "options": [
        "Write test cases",
        "Compare actual progress against the plan and take corrective actions",
        "Execute the tests",
        "Close the project"
    ],
    "exp": "Monitoring collects metrics; control acts (replan, reallocate) when there are deviations from the plan."
},
"ch1-17": {
    "q": "In the test analysis activity, what is primarily produced?",
    "options": [
        "Automated scripts",
        "Test conditions derived from the test basis and its criteria",
        "The final report",
        "Test data"
    ],
    "exp": "Analysis identifies what to test — the test conditions — from the test basis (requirements, risks, etc.)."
},
"ch1-18": {
    "q": "In test design, the focus is on:",
    "options": [
        "Identifying what to test",
        "Defining how to test: test cases and sets derived from the conditions",
        "Executing the cases",
        "Reporting defects"
    ],
    "exp": "Test design elaborates how to cover the test conditions, producing test cases and test sets."
},
"ch1-19": {
    "q": "What is the primary output of the test implementation activity?",
    "options": [
        "Test conditions",
        "Procedures, scripts, and data ready for execution, with the environment prepared",
        "The test plan",
        "The progress report"
    ],
    "exp": "Implementation organizes and prepares everything needed to execute: procedures, data, environment, and schedule."
},
"ch1-20": {
    "q": "During test execution, when a divergent result is found, the tester should first:",
    "options": [
        "Fix the code",
        "Record the result and, if it is an anomaly, create a defect report",
        "Stop testing",
        "Ignore it if it is minor"
    ],
    "exp": "Results are compared to expected; divergences (anomalies) are analyzed and, when defects are confirmed, logged in a defect report."
},
"ch1-21": {
    "q": "The test completion activity typically includes:",
    "options": [
        "Writing the first test cases",
        "Archiving testware, recording lessons learned, and producing the completion report",
        "Defining objectives",
        "Preparing the environment"
    ],
    "exp": "Completion consolidates results, archives reusable testware, records lessons learned, and issues the completion report."
},
"ch1-22": {
    "q": "What is 'testware'?",
    "options": [
        "Test hardware",
        "Artifacts produced during the test process (plans, cases, data, reports)",
        "The automation tool",
        "The system under test"
    ],
    "exp": "Testware encompasses all work products of the testing process: plans, conditions, cases, data, scripts, reports."
},
"ch1-23": {
    "q": "What is the main benefit of traceability between the test basis and testware?",
    "options": [
        "Reducing the number of tests",
        "Enabling coverage assessment and impact analysis of changes on the tests",
        "Eliminating documentation",
        "Speeding up the code"
    ],
    "exp": "Traceability links requirements/risks to conditions and cases, supporting coverage assessment, impact analysis, and auditing."
},
"ch1-24": {
    "q": "Regarding test independence, which statement is correct?",
    "options": [
        "Greater independence always finds more defects",
        "Independence can reduce author bias, but extreme degrees have disadvantages such as less context knowledge",
        "The author is always the best tester of their own code",
        "Independence does not influence testing"
    ],
    "exp": "Some degree of independence reduces the author's cognitive bias, but full independence can distance the tester from context and communication."
},

# Cap.1 questions added in the 200-question expansion (ch1-25 to ch1-40)
"ch1-25": {
    "q": "Which of the following best describes a 'test basis'?",
    "options": [
        "The test environment configuration",
        "Any artifact from which test conditions can be derived",
        "The set of all executed test cases",
        "The defect tracking system"
    ],
    "exp": "The test basis is any artifact (requirements, design, code, risk list) used to identify what needs to be tested."
},
"ch1-26": {
    "q": "What does 'testability' refer to?",
    "options": [
        "The number of test cases written",
        "The degree to which a work product facilitates testing",
        "The speed of test execution",
        "The coverage achieved"
    ],
    "exp": "Testability is a quality characteristic of a work product that indicates how easily it can be tested."
},
"ch1-27": {
    "q": "A tester finds that a critical module has never been tested. Which principle is most relevant?",
    "options": [
        "Pesticide paradox",
        "Early testing saves time and money",
        "Defect clustering",
        "Exhaustive testing is impossible"
    ],
    "exp": "Starting testing early — including identifying untested areas — reduces cost and risk of late defect discovery."
},
"ch1-28": {
    "q": "Which is an example of a failure?",
    "options": [
        "A developer misreads a requirement",
        "An incorrect line of code",
        "An application crash observed by the user during execution",
        "A missing test case"
    ],
    "exp": "A failure is the observable incorrect behavior of a system during execution, caused by a defect in the code."
},
"ch1-29": {
    "q": "Which is an example of a defect?",
    "options": [
        "A developer misunderstands a specification",
        "An incorrect statement in the source code",
        "An application returning a wrong result at runtime",
        "A missing test environment"
    ],
    "exp": "A defect is the manifestation of an error in an artifact (e.g., incorrect code statement) that may cause a failure."
},
"ch1-30": {
    "q": "Testing contributes to quality by:",
    "options": [
        "Replacing good development practices",
        "Providing information about quality and helping stakeholders make informed decisions",
        "Guaranteeing that all defects are found",
        "Eliminating the need for requirements"
    ],
    "exp": "Testing is an information-gathering activity; it provides data about quality to support decisions, not guarantee perfection."
},
"ch1-31": {
    "q": "Which statement best describes the relationship between testing and quality assurance?",
    "options": [
        "Testing and QA are the same thing",
        "Testing is a form of quality control and provides feedback that supports QA",
        "QA subsumes testing entirely",
        "Testing replaces QA in agile projects"
    ],
    "exp": "Testing (QC) provides product-level feedback on defects; QA uses that feedback alongside process improvements to build quality confidence."
},
"ch1-32": {
    "q": "A developer introduces an off-by-one error in a loop. This is an example of:",
    "options": [
        "A failure",
        "An error",
        "A defect",
        "A test condition"
    ],
    "exp": "The developer's mistake is an error; the resulting incorrect code is the defect. The failure occurs only when the defective code is executed."
},
"ch1-33": {
    "q": "Which activity does NOT belong to the test process?",
    "options": [
        "Test analysis",
        "Test design",
        "Code compilation",
        "Test completion"
    ],
    "exp": "Code compilation is a development activity. The test process activities are: planning, monitoring/control, analysis, design, implementation, execution, completion."
},
"ch1-34": {
    "q": "What is the purpose of a test completion report?",
    "options": [
        "To authorize the start of testing",
        "To summarize testing results, coverage, and lessons learned at the end of a test level or milestone",
        "To list all open defects only",
        "To replace the test plan"
    ],
    "exp": "The test completion report consolidates what was achieved, coverage attained, quality assessment, and lessons learned."
},
"ch1-35": {
    "q": "Which factor most directly influences the degree of test independence chosen for a project?",
    "options": [
        "The color scheme of the test management tool",
        "The level of risk and the need to reduce author cognitive bias",
        "The number of developers on the team",
        "The programming language used"
    ],
    "exp": "Independence level is chosen based on risk and the need to counteract author bias; higher risk typically warrants more independence."
},
"ch1-36": {
    "q": "In the context of testing, what is a 'test oracle'?",
    "options": [
        "An automated test generation tool",
        "A mechanism for determining whether a test has passed or failed",
        "A test case repository",
        "A type of specification-based technique"
    ],
    "exp": "A test oracle provides the expected result against which actual results are compared to determine pass or fail."
},
"ch1-37": {
    "q": "Which of the following is a generic skill expected of a tester?",
    "options": [
        "Expertise in network hardware",
        "Analytical thinking and attention to detail",
        "Ability to write production code only",
        "Sales and marketing experience"
    ],
    "exp": "Testers need analytical thinking, attention to detail, communication, and a systematic mindset among other generic skills."
},
"ch1-38": {
    "q": "The 'whole-team approach' to quality means:",
    "options": [
        "Only testers are responsible for quality",
        "Every team member shares responsibility for quality",
        "Developers never test",
        "Quality is only the concern of the QA manager"
    ],
    "exp": "In the whole-team approach, quality is a shared responsibility; everyone contributes, not just dedicated testers."
},
"ch1-39": {
    "q": "Continuous testing in DevOps pipelines is most closely associated with which testing principle?",
    "options": [
        "Exhaustive testing is impossible",
        "Early testing saves time and money",
        "Absence-of-errors fallacy",
        "Pesticide paradox"
    ],
    "exp": "Continuous testing embodies early and frequent testing throughout the pipeline, directly aligning with the early testing principle."
},
"ch1-40": {
    "q": "When a test case is executed and the actual result matches the expected result, the test:",
    "options": [
        "Has proven the software is correct",
        "Has passed, but this does not prove the absence of other defects",
        "Has found a defect",
        "Should be removed from the test suite"
    ],
    "exp": "A passing test increases confidence but does not prove correctness; other defects may exist in untested paths."
},
# ============================================================
# CHAPTER 2 — TESTING THROUGHOUT THE SDLC (25 questions)
# ============================================================

"ch2-01": {
    "q": "How does the software development lifecycle model influence testing?",
    "options": [
        "It has no influence; testing is always performed the same way regardless of the model",
        "It influences the scope, timing, approach, and level of detail of testing activities",
        "It only affects the choice of test automation tool",
        "It determines the number of testers required but not the testing approach"
    ],
    "exp": "The SDLC model shapes when, how, and how deeply testing is performed; sequential models tend to test by phase, while iterative/agile models integrate testing continuously."
},
"ch2-02": {
    "q": "What does 'shift-left' mean in the context of software testing?",
    "options": [
        "Moving test execution to a later phase to allow more development time",
        "Anticipating testing activities to earlier stages of the development lifecycle",
        "Shifting the testing team to the left side of the office floor plan",
        "Reducing the number of test levels by merging them into one phase"
    ],
    "exp": "Shift-left moves testing earlier in the lifecycle, enabling earlier defect detection and reducing the cost of fixing them."
},
"ch2-03": {
    "q": "TDD, ATDD, and BDD are examples of:",
    "options": [
        "Automated UI testing frameworks used in regression suites",
        "Test-first approaches where tests or acceptance criteria guide development",
        "Configuration management strategies for test environments",
        "Performance testing methodologies applied in load testing scenarios"
    ],
    "exp": "TDD, ATDD, and BDD are test-first approaches: tests or acceptance criteria are defined before or alongside the code, guiding implementation."
},
"ch2-04": {
    "q": "What is the primary benefit of retrospectives for the test process?",
    "options": [
        "They replace the need for test planning in agile projects",
        "They promote continuous process improvement based on lessons learned",
        "They provide a mechanism for assigning blame for defects found in production",
        "They eliminate the need for defect reports by resolving issues verbally"
    ],
    "exp": "Retrospectives identify what to improve (process, tools, collaboration), supporting continuous improvement across iterations."
},
"ch2-05": {
    "q": "Component testing (unit testing) focuses on:",
    "options": [
        "Verifying interactions between separately developed systems across organizational boundaries",
        "Testing individual components in isolation, typically performed by developers",
        "Validating the complete system against user acceptance criteria",
        "Evaluating system behavior under concurrent load from multiple users"
    ],
    "exp": "Component testing verifies individual modules/units in isolation, often using stubs and drivers, and is typically performed by developers."
},
"ch2-06": {
    "q": "What is the difference between component integration testing and system integration testing?",
    "options": [
        "They are identical; the terms are interchangeable in modern testing practice",
        "Component integration tests interactions within a system; system integration tests interactions between distinct systems",
        "System integration testing is always performed before component integration testing",
        "Only component integration testing uses interfaces; system integration testing uses only APIs"
    ],
    "exp": "Component integration focuses on internal interfaces between components of one system; system integration focuses on interfaces between different systems or organizations."
},
"ch2-07": {
    "q": "System testing evaluates:",
    "options": [
        "Individual components in isolation using drivers and stubs to simulate dependencies",
        "The behavior and capabilities of the complete integrated system as a whole",
        "Only the user interface layer of the application under test",
        "Contractual acceptance criteria defined between the customer and the supplier"
    ],
    "exp": "System testing evaluates the fully integrated system end-to-end, covering both functional and non-functional behavior."
},
"ch2-08": {
    "q": "Which are common forms of acceptance testing?",
    "options": [
        "Unit testing and integration testing performed by developers before handover",
        "User acceptance (UAT), operational, contractual, and regulatory acceptance testing",
        "White-box and black-box testing combined into a single acceptance phase",
        "Static and dynamic testing merged into a unified acceptance review process"
    ],
    "exp": "Acceptance testing includes UAT, operational acceptance (backup, security), contractual acceptance, and regulatory acceptance."
},
"ch2-09": {
    "q": "What is the difference between alpha and beta testing?",
    "options": [
        "Alpha testing is performed in production; beta testing is performed by the development team",
        "Alpha testing occurs at the developer's site; beta testing is performed by real users in their own environment",
        "Beta testing always precedes alpha testing in the release lifecycle",
        "Alpha and beta testing are synonyms for system and acceptance testing respectively"
    ],
    "exp": "Alpha is conducted at the developer's premises (by users or the team); beta is performed by users in their own environment."
},
"ch2-10": {
    "q": "Functional testing evaluates:",
    "options": [
        "How the system behaves under stress, including performance and resource consumption",
        "What the system does, based on its specified functional requirements and behavior",
        "The internal structure of the code, including statement and branch coverage",
        "The degree to which the system satisfies operational and regulatory constraints"
    ],
    "exp": "Functional testing verifies the functions and behavior of the system (what it does) against its functional requirements."
},
"ch2-11": {
    "q": "Which is an example of non-functional testing?",
    "options": [
        "Verifying that a discount calculation produces the correct monetary result",
        "Evaluating system response time under one thousand simultaneous users",
        "Confirming that the login workflow navigates to the correct dashboard",
        "Validating that a business rule correctly rejects an invalid date format"
    ],
    "exp": "Non-functional testing evaluates quality attributes such as performance, usability, security, and reliability — the 'how well' dimension."
},
"ch2-12": {
    "q": "White-box testing derives tests from:",
    "options": [
        "External specifications and user stories defined by the product owner",
        "The internal structure of the code, control flow, or system architecture",
        "The tester's experience and intuition about likely failure areas",
        "Acceptance criteria agreed between the development team and the customer"
    ],
    "exp": "White-box (structural) testing uses the internal structure (code, control flow, architecture) as the basis for designing and measuring tests."
},
"ch2-13": {
    "q": "Confirmation testing (re-testing) occurs when:",
    "options": [
        "A new feature is developed and needs to be validated against acceptance criteria",
        "A defect fix is verified to confirm the original failure no longer occurs",
        "The test environment is migrated to a new infrastructure platform",
        "The project reaches the end of an iteration and all stories are reviewed"
    ],
    "exp": "After a defect is fixed, the failing test case is re-executed to confirm the defect has been successfully resolved."
},
"ch2-14": {
    "q": "What is the objective of regression testing?",
    "options": [
        "To confirm that a specific defect fix has resolved the originally reported failure",
        "To detect unintended side effects: changes that have broken previously working functionality",
        "To evaluate system performance under gradually increasing load conditions",
        "To test new functionality that has never been tested in a previous iteration"
    ],
    "exp": "Regression testing verifies that changes have not introduced defects into previously working parts of the system."
},
"ch2-15": {
    "q": "What typically triggers maintenance testing?",
    "options": [
        "Only the initial system release after development is complete",
        "Modifications, migrations, upgrades, or retirement of an existing system",
        "Exclusively the addition of new functional requirements to the backlog",
        "The creation of test cases during the planning phase of a new project"
    ],
    "exp": "Maintenance testing is triggered by changes (fixes, enhancements), migrations to new environments, upgrades, and system retirement."
},
"ch2-16": {
    "q": "In a test-driven development (TDD) workflow, which sequence is correct?",
    "options": [
        "Write production code → run tests → write failing test → refactor",
        "Write a failing test → write minimal code to pass → refactor",
        "Write all tests upfront → implement the full feature → run tests once",
        "Deploy to production → monitor failures → write tests to reproduce them"
    ],
    "exp": "TDD follows the Red-Green-Refactor cycle: write a failing test, write just enough code to pass it, then refactor."
},
"ch2-17": {
    "q": "Which statement best describes the role of testing in DevOps?",
    "options": [
        "Testing is performed only at the end of the pipeline before production release",
        "Testing is integrated throughout the pipeline to provide fast feedback at every stage",
        "Testing in DevOps is fully automated and eliminates the need for manual testing entirely",
        "Testing responsibility shifts exclusively to operations engineers in a DevOps model"
    ],
    "exp": "In DevOps, testing is continuous and integrated at every pipeline stage to provide rapid feedback and support frequent safe deployments."
},
"ch2-18": {
    "q": "What distinguishes test levels from test types?",
    "options": [
        "Test levels and test types are synonyms used interchangeably in the CTFL syllabus",
        "Test levels relate to the degree of development completeness; test types relate to a specific quality characteristic being evaluated",
        "Test types are performed before test levels in every software development lifecycle",
        "Test levels apply only to waterfall projects; test types apply only to agile projects"
    ],
    "exp": "Test levels (component, integration, system, acceptance) relate to development completeness; test types (functional, non-functional, structural, change-related) relate to quality characteristics."
},
"ch2-19": {
    "q": "Which test type is most directly associated with evaluating security vulnerabilities?",
    "options": [
        "Functional testing, because security rules are part of the functional specification",
        "Non-functional testing, because security is a quality characteristic of the system",
        "White-box testing, because security flaws are always visible in the source code",
        "Confirmation testing, because security patches must be re-tested after each fix"
    ],
    "exp": "Security testing evaluates a quality attribute (resistance to unauthorized access), making it a non-functional test type."
},
"ch2-20": {
    "q": "In agile development, testing activities are:",
    "options": [
        "Deferred to a dedicated hardening sprint at the end of each release cycle",
        "Integrated into each iteration alongside development, with the whole team sharing quality responsibility",
        "Performed exclusively by a separate independent QA team after each sprint",
        "Limited to automated regression suites; exploratory testing is prohibited in agile"
    ],
    "exp": "In agile, testing is continuous within each iteration; the whole team shares quality responsibility rather than delegating it to a separate QA phase."
},
"ch2-21": {
    "q": "What is the primary purpose of a test environment?",
    "options": [
        "To store the final production build before it is released to end users",
        "To provide the infrastructure, tools, and configurations needed to execute tests",
        "To host the defect tracking system used by the development team",
        "To archive completed test cases for future audits and compliance reviews"
    ],
    "exp": "A test environment provides the hardware, software, network, and configurations necessary to execute test cases reliably."
},
"ch2-22": {
    "q": "Impact analysis in maintenance testing is used to:",
    "options": [
        "Determine the total cost of the maintenance project before work begins",
        "Identify which parts of the system may be affected by a change and need regression testing",
        "Assign severity ratings to all defects found during the maintenance phase",
        "Decide whether to retire the system or continue maintenance investment"
    ],
    "exp": "Impact analysis determines the scope of change and identifies areas requiring regression testing to prevent unintended side effects."
},
"ch2-23": {
    "q": "Which factor most directly determines the appropriate test level at which a defect should be detected?",
    "options": [
        "The personal preference of the test manager assigned to the project",
        "The origin of the defect: defects in components are best caught at component level; integration defects at integration level",
        "The severity of the defect, with high-severity defects always caught at system level",
        "The availability of automated tools at each level of the test hierarchy"
    ],
    "exp": "The appropriate test level aligns with the origin of the defect; catching defects at the level closest to their origin is most cost-effective."
},
"ch2-24": {
    "q": "A system passes all functional tests but fails to meet the response time SLA under peak load. This is a failure in:",
    "options": [
        "Functional testing, because SLAs are part of the functional specification",
        "Non-functional testing, because response time is a performance quality characteristic",
        "White-box testing, because performance bottlenecks are found by analyzing the code",
        "Acceptance testing only, because SLAs are contractual obligations"
    ],
    "exp": "Response time under load is a performance (non-functional) quality characteristic; its failure is detected through non-functional testing."
},
"ch2-25": {
    "q": "In the context of the CTFL v4.0 syllabus, which statement about the relationship between test activities and the SDLC is correct?",
    "options": [
        "Test activities are fixed and independent of the chosen development lifecycle model",
        "For every development activity there should be a corresponding test activity",
        "Test activities only begin after all development activities in a phase are complete",
        "Test planning is the only activity that occurs in parallel with development activities"
    ],
    "exp": "The CTFL v4.0 principle states that for every development activity there should be a corresponding test activity, ensuring testing is integrated throughout."
},
# ============================================================
# CHAPTER 3 — STATIC TESTING (25 questions)
# ============================================================

"ch3-01": {
    "q": "What characterizes static testing?",
    "options": [
        "Executing the software with controlled inputs to observe runtime behavior",
        "Examining work products without executing the software",
        "Measuring system response time and resource consumption under load",
        "Validating the user interface against approved design mockups"
    ],
    "exp": "Static testing evaluates artifacts (code, requirements, design) without executing them, through reviews and static analysis tools."
},
"ch3-02": {
    "q": "Which of the following can be a target of static testing?",
    "options": [
        "Only executable source code files that can be compiled",
        "Requirements, specifications, code, models, contracts, and user stories",
        "Only binary artifacts produced after the build process",
        "Exclusively test cases and test plans created by the testing team"
    ],
    "exp": "Almost any structured artifact can be reviewed: requirements, design documents, code, user stories, contracts, and test plans."
},
"ch3-03": {
    "q": "Which is a benefit of static testing?",
    "options": [
        "It measures system performance under simulated production load conditions",
        "It detects defects early, including in requirements, before any execution occurs",
        "It completely replaces dynamic testing by finding all possible defects",
        "It guarantees that the system will pass all subsequent dynamic tests"
    ],
    "exp": "By acting early, static testing finds defects (ambiguities, omissions) before execution, significantly reducing the cost of correction."
},
"ch3-04": {
    "q": "What is the key difference between static and dynamic testing?",
    "options": [
        "Static testing executes the code; dynamic testing examines artifacts without execution",
        "Dynamic testing executes the software; static testing examines artifacts without executing them",
        "Static and dynamic testing are equivalent approaches that find the same defect types",
        "Static testing applies only to source code; dynamic testing applies only to requirements"
    ],
    "exp": "Dynamic testing requires execution and reveals failures; static testing examines artifacts directly and finds defects without execution."
},
"ch3-05": {
    "q": "Why is early and frequent feedback from static testing valuable?",
    "options": [
        "It increases the total number of defects found by generating more test cases",
        "It enables early correction, preventing misunderstandings from propagating and becoming expensive",
        "It delays dynamic testing until the codebase is completely stable and reviewed",
        "It eliminates the need for regression testing by catching all defects before coding"
    ],
    "exp": "Early feedback prevents costly rework and keeps development aligned with real needs by catching misunderstandings at the source."
},
"ch3-06": {
    "q": "What is the general sequence of activities in a formal review?",
    "options": [
        "Execution → planning → individual review → report",
        "Planning → initiation → individual review → communication and analysis → fixing and follow-up",
        "Analysis → design → execution → completion report",
        "Initiation → execution → defect logging → planning"
    ],
    "exp": "Formal review activities: planning, kick-off/initiation, individual review, review meeting (communication and analysis), fixing and follow-up."
},
"ch3-07": {
    "q": "Which role leads and facilitates a formal review?",
    "options": [
        "The author of the work product under review",
        "The moderator (facilitator)",
        "The scribe who records the findings",
        "The development manager who commissioned the work"
    ],
    "exp": "The moderator/facilitator leads the meeting, ensures the process is followed, and maintains objectivity."
},
"ch3-08": {
    "q": "What is the responsibility of the author in a review?",
    "options": [
        "To moderate the review meeting and enforce the agenda",
        "To create the work product and be responsible for fixing the defects found",
        "To record all anomalies and decisions made during the review session",
        "To decide which review type is most appropriate for the artifact"
    ],
    "exp": "The author owns the artifact under review and is typically responsible for making the corrections identified during the review."
},
"ch3-09": {
    "q": "What is the role of the scribe (recorder) in a review?",
    "options": [
        "To lead the discussion and keep the review meeting on track",
        "To document anomalies, decisions, and new issues raised during the review",
        "To correct the work product based on review findings",
        "To approve the artifact for release after all defects are resolved"
    ],
    "exp": "The scribe records anomalies, decisions, and action items during the review to ensure nothing is lost."
},
"ch3-10": {
    "q": "An informal review is characterized by:",
    "options": [
        "A documented process with defined entry and exit criteria and mandatory metrics",
        "No formal process, low overhead, and results not formally documented",
        "Mandatory individual preparation before the review meeting takes place",
        "Strictly defined roles including moderator, author, scribe, and reviewers"
    ],
    "exp": "Informal reviews have no defined process and produce no formal documentation; they are fast, low-cost, and flexible."
},
"ch3-11": {
    "q": "The primary objective of a walkthrough is typically to:",
    "options": [
        "Audit the artifact for compliance against regulatory and contractual standards",
        "Allow the author to guide participants through the artifact to gain shared understanding and feedback",
        "Measure code coverage achieved by the existing automated test suite",
        "Formally approve the work product for entry into the next development phase"
    ],
    "exp": "In a walkthrough the author guides participants through the document seeking shared understanding, learning, and feedback."
},
"ch3-12": {
    "q": "A technical review is primarily conducted to:",
    "options": [
        "Train junior team members in the coding standards of the organization",
        "Achieve technical consensus and make decisions, led by technically qualified peers",
        "Produce formal documentation of all defects for the defect tracking system",
        "Replace dynamic testing for technically complex modules with high cyclomatic complexity"
    ],
    "exp": "A technical review brings technically qualified peers together to assess quality and reach consensus or decisions on technical matters."
},
"ch3-13": {
    "q": "How does an inspection differ from other review types?",
    "options": [
        "It is the most informal review type, with no defined roles or preparation required",
        "It is the most formal review type: defined roles, metrics, entry/exit criteria, and mandatory preparation",
        "It is conducted by the author alone without the involvement of other team members",
        "It focuses exclusively on code and cannot be applied to requirements or design artifacts"
    ],
    "exp": "Inspection is the most formal review: rigorous process, defined roles, individual preparation, metrics, and entry/exit criteria."
},
"ch3-14": {
    "q": "When selecting the review type, the primary determining factor should be:",
    "options": [
        "The personal preference of the author who created the work product",
        "The objective of the review and the risk or criticality of the artifact",
        "The size of the development team and the project timeline",
        "The availability of automated static analysis tools for the artifact type"
    ],
    "exp": "The review type is chosen based on the objective (consensus, compliance, learning) and the criticality/risk of the artifact."
},
"ch3-15": {
    "q": "Which is a success factor for reviews?",
    "options": [
        "Using reviews as a mechanism to formally evaluate individual developer performance",
        "Focusing on the artifact rather than the person, maintaining a constructive atmosphere",
        "Avoiding the definition of objectives to keep the review open-ended and flexible",
        "Always applying the most formal review type regardless of artifact criticality"
    ],
    "exp": "Successful reviews focus on the product, have clear objectives, appropriate scope, and maintain a blame-free, constructive environment."
},
"ch3-16": {
    "q": "Which defect type is most effectively found by static testing but is difficult to detect through dynamic testing?",
    "options": [
        "Race conditions that only manifest under specific concurrent execution timing",
        "Deviations from coding standards and unreachable (dead) code in the codebase",
        "Performance bottlenecks that only appear under high production load conditions",
        "Integration failures that occur only when two specific modules interact at runtime"
    ],
    "exp": "Static testing uniquely finds standard violations, dead code, and inconsistencies in requirements that may never cause a runtime failure."
},
"ch3-17": {
    "q": "Static analysis tools are most useful for:",
    "options": [
        "Executing test cases automatically and recording pass/fail results",
        "Detecting code defects such as security vulnerabilities, dead code, and standard violations without execution",
        "Generating realistic test data for use in performance and load testing scenarios",
        "Managing test case repositories and tracking defect resolution progress"
    ],
    "exp": "Static analysis tools examine code without executing it, finding issues like security flaws, unreachable code, and coding standard violations."
},
"ch3-18": {
    "q": "Which statement about the cost-effectiveness of static testing is correct?",
    "options": [
        "Static testing is always more expensive than dynamic testing due to the effort required for reviews",
        "Defects found through static testing are generally cheaper to fix than those found through dynamic testing",
        "Static testing has no impact on overall project cost because it duplicates dynamic testing effort",
        "Static testing is only cost-effective for safety-critical systems where defect cost is extremely high"
    ],
    "exp": "Defects found early through static testing cost significantly less to fix than those discovered later through dynamic testing or in production."
},
"ch3-19": {
    "q": "Which artifact would benefit most from static testing early in the project?",
    "options": [
        "Compiled binary files ready for deployment to the production environment",
        "Requirements specifications containing ambiguities, contradictions, or missing information",
        "Performance test results from the most recent load testing execution run",
        "Automated regression test scripts that have already been validated and baselined"
    ],
    "exp": "Reviewing requirements early catches ambiguities, contradictions, and omissions before they propagate into design and code."
},
"ch3-20": {
    "q": "In a review meeting, an issue is raised that is outside the scope of the current review. What should the moderator do?",
    "options": [
        "Stop the review immediately and reschedule once the scope issue is resolved",
        "Log it as a parking lot item and continue the review without derailing the agenda",
        "Assign it immediately to the author for correction before continuing",
        "Dismiss it entirely since out-of-scope items are not valid review findings"
    ],
    "exp": "The moderator manages scope; out-of-scope items are logged for later follow-up (parking lot) without derailing the current review."
},
"ch3-21": {
    "q": "Which metric is most useful for evaluating the effectiveness of an inspection?",
    "options": [
        "The number of lines of code reviewed per hour during the inspection session",
        "The defect density found (defects per page or per function point) compared to historical data",
        "The number of attendees present at the inspection meeting",
        "The total elapsed calendar time from inspection planning to final sign-off"
    ],
    "exp": "Defect density compared to historical baselines indicates whether the inspection found the expected number of issues and assesses artifact quality."
},
"ch3-22": {
    "q": "Entry criteria for a formal review typically include:",
    "options": [
        "Conditions that define when the review can be declared complete and closed",
        "Pre-conditions that must be satisfied before the review can begin, such as the artifact being stable",
        "The list of defects that must be fixed before the artifact is submitted for review",
        "The acceptance criteria that the final product must satisfy before release to users"
    ],
    "exp": "Entry criteria are pre-conditions for starting a review, e.g., the artifact is stable, reviewers have time allocated, and materials are distributed."
},
"ch3-23": {
    "q": "Which statement about checklist-based reviewing is correct?",
    "options": [
        "Checklists must be replaced entirely after each review to avoid the pesticide paradox",
        "Checklists help reviewers focus on common defect types and ensure consistent coverage",
        "Checklists are only appropriate for informal reviews and cannot be used in inspections",
        "Using a checklist guarantees that all defects in the artifact will be found"
    ],
    "exp": "Checklists provide structured guidance, helping reviewers focus on historically common defect types and ensuring consistent review coverage."
},
"ch3-24": {
    "q": "Perspective-based reading in reviews means that:",
    "options": [
        "Each reviewer reads the entire artifact from start to finish without any assigned focus",
        "Different reviewers adopt different stakeholder viewpoints to increase defect detection coverage",
        "The author reads the artifact aloud while other participants listen and take notes",
        "Reviewers focus exclusively on their own area of expertise and ignore other aspects"
    ],
    "exp": "Perspective-based reading assigns different stakeholder viewpoints (user, maintainer, tester) to different reviewers, increasing the variety of defects found."
},
"ch3-25": {
    "q": "Which of the following is an anti-pattern that reduces review effectiveness?",
    "options": [
        "Defining clear objectives and communicating them to all participants before the review",
        "Allowing the review to become a public critique of the author's skills and effort",
        "Limiting the review scope to a manageable artifact size within the session time",
        "Providing the artifact to reviewers in advance to allow adequate individual preparation"
    ],
    "exp": "Turning a review into personal criticism of the author destroys psychological safety, reduces participation quality, and undermines the review's effectiveness."
},
# ============================================================
# CHAPTER 4 — TEST TECHNIQUES (55 questions) — BLOCK 1/2 (ch4-01 to ch4-28)
# ============================================================

"ch4-01": {
    "q": "Test techniques are primarily classified into:",
    "options": [
        "Manual and automated techniques based on execution method",
        "Black-box, white-box, and experience-based techniques",
        "Functional and non-functional techniques based on quality characteristic",
        "Static and dynamic techniques based on whether code is executed"
    ],
    "exp": "The CTFL syllabus defines three technique categories: black-box (specification-based), white-box (structure-based), and experience-based."
},
"ch4-02": {
    "q": "Equivalence partitioning (EP) is based on the idea that:",
    "options": [
        "Every possible input value must be tested to ensure complete coverage",
        "Values within the same partition are treated equivalently by the system, so one representative suffices",
        "Only boundary values between partitions require testing for adequate coverage",
        "Invalid partitions do not need to be tested because the system should reject them automatically"
    ],
    "exp": "In EP, all values within a partition produce equivalent behavior; testing one representative value per partition is sufficient."
},
"ch4-03": {
    "q": "A field accepts integers from 1 to 100. Which equivalence partitions exist, including invalid ones?",
    "options": [
        "Only one valid partition: 1–100",
        "Three partitions: ≤0 (invalid), 1–100 (valid), ≥101 (invalid)",
        "Two partitions: 1–50 and 51–100",
        "Four partitions: negative, zero, 1–100, and above 100"
    ],
    "exp": "There are three partitions: below 1 (invalid), 1–100 (valid), and above 100 (invalid). Zero and negatives are part of the ≤0 invalid partition."
},
"ch4-04": {
    "q": "Why should invalid partitions also be tested in equivalence partitioning?",
    "options": [
        "To increase the total count of test cases and demonstrate thoroughness",
        "To verify that the system correctly handles out-of-range inputs with appropriate rejection or error messages",
        "Because invalid partitions are always more likely to contain defects than valid ones",
        "To satisfy regulatory requirements that mandate testing of all possible input combinations"
    ],
    "exp": "Invalid partitions verify that the system handles unexpected inputs correctly, such as displaying error messages or rejecting the input gracefully."
},
"ch4-05": {
    "q": "Boundary value analysis (BVA) is effective because:",
    "options": [
        "It guarantees 100% statement coverage of the source code under test",
        "Defects tend to cluster at the boundaries between partitions",
        "It eliminates the need for equivalence partitioning by subsumingg that technique",
        "Boundary values are always the easiest inputs for developers to implement correctly"
    ],
    "exp": "Defects frequently occur at partition boundaries; BVA complements EP by specifically targeting these error-prone boundary values."
},
"ch4-06": {
    "q": "A field accepts ages from 18 to 65. Which values are tested using 2-value BVA?",
    "options": [
        "18 and 65 only",
        "17, 18, 65, and 66",
        "17 and 66 only",
        "0, 18, 65, and 100"
    ],
    "exp": "2-value BVA tests each boundary and its adjacent invalid value: 17/18 at the lower boundary and 65/66 at the upper boundary."
},
"ch4-07": {
    "q": "Using 3-value BVA for the upper boundary of 65, which values are tested?",
    "options": [
        "65 only",
        "64, 65, and 66",
        "63, 64, and 65",
        "65, 66, and 67"
    ],
    "exp": "3-value BVA tests the boundary itself and both adjacent values: 64 (just below), 65 (the boundary), and 66 (just above)."
},
"ch4-08": {
    "q": "Passwords must be between 8 and 16 characters. Using 2-value BVA, which lengths are tested at the lower boundary?",
    "options": [
        "8 and 9",
        "7 and 8",
        "6, 7, and 8",
        "8 and 16"
    ],
    "exp": "At the lower boundary (8), 2-value BVA tests 7 (invalid, just below) and 8 (valid, the boundary itself)."
},
"ch4-09": {
    "q": "A decision table is most appropriate when:",
    "options": [
        "The system behavior depends on a sequence of states triggered by specific events",
        "There are combinations of conditions that lead to different actions (business rules)",
        "The focus is on measuring how thoroughly the source code has been exercised",
        "The tester needs to evaluate system performance under varying load conditions"
    ],
    "exp": "Decision tables model business rules with combinations of conditions and their resulting actions, making them ideal for complex logical rules."
},
"ch4-10": {
    "q": "A rule grants free shipping if (subscriber = Yes) AND (purchase > $100). With 2 binary conditions, how many rules does the full decision table contain?",
    "options": [
        "2",
        "3",
        "4",
        "8"
    ],
    "exp": "Two binary conditions produce 2² = 4 possible combinations (rules) in the complete decision table."
},
"ch4-11": {
    "q": "In a decision table, conditions and actions represent respectively:",
    "options": [
        "Outputs and inputs of the system under test",
        "The causes (inputs/conditions) and effects (resulting actions) for each rule",
        "States and transitions in the system's behavioral model",
        "Test cases and their associated expected test data values"
    ],
    "exp": "Conditions are the causes (inputs); actions are the effects (expected results) for each combination of conditions."
},
"ch4-12": {
    "q": "A discount is granted only when both 'VIP customer = Yes' AND 'valid coupon = Yes'. For the combination VIP=Yes, coupon=No, the expected action is:",
    "options": [
        "Grant the discount because the customer is VIP",
        "Do not grant the discount because not all conditions are satisfied",
        "Generate a system error requiring manual intervention",
        "Grant a partial discount proportional to the conditions satisfied"
    ],
    "exp": "The action (discount) only occurs when all required conditions are true; with coupon=No, the discount is not granted."
},
"ch4-13": {
    "q": "State transition testing is appropriate for systems that:",
    "options": [
        "Process purely numerical calculations without any dependency on previous inputs",
        "Change their behavior based on the current state and the events received",
        "Only have one possible state and respond identically to all inputs",
        "Are stateless REST APIs that process each request independently"
    ],
    "exp": "State transition testing models states, events, transitions, and actions — ideal for sessions, protocols, workflows, and any stateful system."
},
"ch4-14": {
    "q": "In a state diagram, an 'invalid transition' is:",
    "options": [
        "A transition that is permitted and should be exercised at least once",
        "An event that should not cause a state change from the current state",
        "The initial transition from the start state to the first operational state",
        "An exit action that executes when leaving a particular state"
    ],
    "exp": "Invalid transitions are state/event pairs for which no transition is defined; testing them verifies the system's robustness against unexpected events."
},
"ch4-15": {
    "q": "An ATM requires a card to be inserted before accepting a PIN. Attempting to enter a PIN without a card tests:",
    "options": [
        "A valid transition from the idle state",
        "An invalid transition (unexpected event for the current state)",
        "The terminal state of the ATM workflow",
        "An entry action for the PIN entry state"
    ],
    "exp": "Entering a PIN in the 'awaiting card' state is an event not defined for that state — an invalid transition testing system robustness."
},
"ch4-16": {
    "q": "0-switch coverage (valid transitions coverage) requires:",
    "options": [
        "Covering every pair of consecutive valid transitions at least once",
        "Exercising each individual valid transition at least once",
        "Covering all invalid transitions to verify system robustness",
        "Visiting every state at least twice during the test sequence"
    ],
    "exp": "0-switch (single transition) coverage requires each valid transition to be exercised at least once."
},
"ch4-17": {
    "q": "When choosing between EP, BVA, decision tables, and state transitions, the primary criterion is:",
    "options": [
        "The automation tool available to the test team",
        "The nature of the problem: ranges, rule combinations, or state-dependent behavior",
        "The personal preference and experience of the individual tester",
        "The size of the development team and the project deadline"
    ],
    "exp": "Technique selection depends on the problem structure: ranges (EP/BVA), combined rules (decision table), state-dependent behavior (state transition)."
},
"ch4-18": {
    "q": "White-box test techniques derive tests from:",
    "options": [
        "External requirements and user stories defined by the product owner",
        "The internal structure: code, control flow, and system architecture",
        "The tester's experience and intuition about likely failure modes",
        "Acceptance criteria agreed between the development team and stakeholders"
    ],
    "exp": "White-box techniques use the internal structure (statements, decisions, paths, architecture) as the basis for designing and measuring tests."
},
"ch4-19": {
    "q": "Statement coverage measures:",
    "options": [
        "The percentage of decision outcomes exercised by the test suite",
        "The percentage of executable statements that have been executed",
        "The total number of independent paths through the code",
        "The number of conditions that independently affect decision outcomes"
    ],
    "exp": "Statement coverage = executed executable statements ÷ total executable statements, expressed as a percentage."
},
"ch4-20": {
    "q": "A code segment has 10 executable statements; a test suite executed 7 of them. The statement coverage is:",
    "options": [
        "100%",
        "70%",
        "7%",
        "30%"
    ],
    "exp": "7 out of 10 executable statements executed = 70% statement coverage."
},
"ch4-21": {
    "q": "Decision coverage (branch coverage) requires:",
    "options": [
        "Executing every executable statement at least once",
        "Exercising each decision as both true and false at least once",
        "Covering every possible combination of condition values",
        "Testing all independent paths through the code under test"
    ],
    "exp": "Decision coverage requires each decision (e.g., if-statement) to evaluate to both true and false at least once."
},
"ch4-22": {
    "q": "For an 'if' statement without an 'else' branch, which coverage criterion ensures the false path is also tested?",
    "options": [
        "Statement coverage, because all statements must be executed",
        "Decision coverage, because each decision must evaluate to both true and false",
        "No standard coverage criterion requires testing the false path of an if without else",
        "Condition coverage, because each individual condition must be evaluated"
    ],
    "exp": "Without an else branch, 100% statement coverage can be achieved without testing the false path; decision coverage forces both true and false outcomes."
},
"ch4-23": {
    "q": "Which statement about the relative strength of coverage criteria is correct?",
    "options": [
        "Statement coverage is stronger than decision coverage",
        "100% decision coverage implies 100% statement coverage, but not vice versa",
        "Statement coverage and decision coverage are equally strong criteria",
        "Decision coverage does not subsume statement coverage in any circumstance"
    ],
    "exp": "Decision coverage is stronger: achieving 100% decision coverage guarantees 100% statement coverage, but the reverse does not hold."
},
"ch4-24": {
    "q": "What is the value of white-box testing?",
    "options": [
        "It completely replaces black-box testing by providing superior defect detection",
        "It reveals untested code segments and measures the thoroughness of the test suite",
        "It eliminates the need for requirements-based testing by focusing on implementation",
        "It guarantees that all defects will be found once 100% statement coverage is achieved"
    ],
    "exp": "White-box testing shows what the code actually exercises, revealing gaps that specification-based techniques alone cannot detect."
},
"ch4-25": {
    "q": "Error guessing consists of:",
    "options": [
        "Randomly selecting input values without any systematic approach or heuristic",
        "Anticipating likely defects based on experience, past defects, and knowledge of failure modes",
        "Generating test cases automatically using AI tools trained on historical defect data",
        "Measuring code coverage to identify gaps in the existing test suite"
    ],
    "exp": "Error guessing uses experience and knowledge of common failures to create tests likely to expose defects that formal techniques might miss."
},
"ch4-26": {
    "q": "In exploratory testing, the tester:",
    "options": [
        "Follows pre-defined test scripts step by step without deviation",
        "Simultaneously learns about the system, designs tests, and executes them",
        "Only measures performance metrics without evaluating functional behavior",
        "Documents all test cases in advance before executing any of them"
    ],
    "exp": "Exploratory testing combines learning, designing, and executing in real time, often guided by test charters and time-boxed sessions."
},
"ch4-27": {
    "q": "Checklist-based testing relies on:",
    "options": [
        "State diagrams showing all valid and invalid system transitions",
        "A list of items or conditions to verify, derived from experience and heuristics",
        "Code coverage metrics generated by automated instrumentation tools",
        "Decision tables enumerating all combinations of business rule conditions"
    ],
    "exp": "Checklists compile items to verify (heuristics, lessons learned), guiding testing without detailed scripts."
},
"ch4-28": {
    "q": "When are experience-based techniques most valuable?",
    "options": [
        "When a complete and stable specification is available for systematic technique application",
        "When documentation is scarce, time is short, or to complement formal techniques",
        "Only in safety-critical systems where formal techniques are mandatory by regulation",
        "Exclusively when automated testing tools are unavailable to the test team"
    ],
    "exp": "Experience-based techniques are valuable with limited documentation or tight timelines, and as complements to formal techniques to catch defects that escape them."
},
# CHAPTER 4 — BLOCK 2/2 (ch4-29 to ch4-55)

"ch4-29": {
    "q": "The '3 C's' of collaborative user story writing are:",
    "options": [
        "Code, Compile, and Commit — the three steps of test-driven development",
        "Card, Conversation, and Confirmation — the three elements of a well-formed user story",
        "Cost, Customer, and Contract — the three constraints of agile project management",
        "Create, Check, and Close — the three phases of the defect lifecycle"
    ],
    "exp": "The 3 C's: Card (brief summary), Conversation (detailed discussion), and Confirmation (acceptance criteria that define done)."
},
"ch4-30": {
    "q": "Acceptance criteria for a user story serve to:",
    "options": [
        "Estimate the development effort required to implement the story in story points",
        "Define the conditions the story must satisfy to be considered complete and accepted",
        "Measure the code coverage achieved by the automated tests for that story",
        "Replace the need for test cases by providing sufficient implementation guidance"
    ],
    "exp": "Acceptance criteria describe what makes a story 'done/accepted', providing the basis for deriving test cases."
},
"ch4-31": {
    "q": "In ATDD (Acceptance Test-Driven Development), acceptance tests are:",
    "options": [
        "Written after delivery to validate that the implemented feature works correctly",
        "Defined collaboratively before implementation, derived from acceptance criteria",
        "Only automated end-to-end UI tests executed by the continuous integration pipeline",
        "Optional artifacts that supplement but never replace traditional test planning"
    ],
    "exp": "In ATDD, the team (business, dev, test) collaboratively defines acceptance tests before coding, guiding implementation and confirming completion."
},
"ch4-32": {
    "q": "A requirement describes both value ranges and multi-field combination rules. The best test strategy is:",
    "options": [
        "Apply only BVA because it is the most comprehensive black-box technique available",
        "Combine techniques: EP/BVA for the ranges and decision tables for the combinations",
        "Apply only state transition testing because the system has multiple operational modes",
        "Use exploratory testing exclusively since the requirement is too complex for formal techniques"
    ],
    "exp": "Mixed problems need combined techniques: EP/BVA for ranges and decision tables for combined rules."
},
"ch4-33": {
    "q": "Coverage in test techniques measures:",
    "options": [
        "The total number of defects found by the test suite during execution",
        "The degree to which defined coverage items have been exercised by the tests",
        "The elapsed time taken to execute all test cases in the test suite",
        "The number of testers assigned to the project relative to its complexity"
    ],
    "exp": "Coverage expresses how much of the defined coverage items (partitions, decisions, transitions) the tests have exercised."
},
"ch4-34": {
    "q": "Which statement about black-box techniques is correct?",
    "options": [
        "Black-box techniques require full access to the source code to derive test cases",
        "Black-box techniques derive tests from specifications without knowledge of internal implementation",
        "Black-box techniques are less rigorous than white-box techniques in all circumstances",
        "Black-box techniques can only be applied at the system test level"
    ],
    "exp": "Black-box techniques (EP, BVA, decision tables, state transitions) derive tests from external specifications without examining the code."
},
"ch4-35": {
    "q": "Which of the following is an experience-based technique?",
    "options": [
        "Equivalence partitioning, because it requires experience to identify valid partitions",
        "Error guessing, because it relies on the tester's knowledge of likely failure modes",
        "Decision coverage, because testers use experience to select which paths to cover",
        "Boundary value analysis, because experienced testers know where defects cluster"
    ],
    "exp": "Error guessing, exploratory testing, and checklist-based testing are experience-based; the others are formal specification or structure-based techniques."
},
"ch4-36": {
    "q": "A system grants admin access if (role = admin) AND (MFA = enabled) AND (IP = whitelisted). With 3 binary conditions, how many rules does the full decision table contain?",
    "options": [
        "3",
        "6",
        "8",
        "16"
    ],
    "exp": "Three binary conditions produce 2³ = 8 possible combinations (rules) in the complete decision table."
},
"ch4-37": {
    "q": "Modified Condition/Decision Coverage (MC/DC) requires, beyond decision coverage, that:",
    "options": [
        "Every executable statement is covered at least once by the test suite",
        "Each condition independently demonstrates the ability to affect the decision outcome",
        "All possible combinations of condition values are tested exhaustively",
        "Only the true and false outcomes of each complete decision are exercised"
    ],
    "exp": "MC/DC requires each condition to independently affect the decision outcome, demonstrating that each condition matters individually."
},
"ch4-38": {
    "q": "MC/DC is required in which domain due to safety-critical certification standards?",
    "options": [
        "E-commerce platforms requiring high availability under peak shopping load",
        "Aviation software under DO-178C, where it is mandated for the highest criticality levels",
        "Social media applications requiring rapid feature deployment and A/B testing",
        "Database management systems requiring high transactional throughput"
    ],
    "exp": "MC/DC is required by DO-178C for Level A (catastrophic failure) aviation software and similar safety-critical standards like ISO 26262 in automotive."
},
"ch4-39": {
    "q": "A tester uses their knowledge of past defects to create tests targeting off-by-one errors and null pointer exceptions. This is an example of:",
    "options": [
        "Equivalence partitioning applied to boundary conditions",
        "Error guessing based on experience with common defect types",
        "White-box testing using statement coverage criteria",
        "Exploratory testing guided by a formal test charter"
    ],
    "exp": "Using past defect knowledge to target likely failure modes is the defining characteristic of error guessing."
},
"ch4-40": {
    "q": "A test charter in exploratory testing defines:",
    "options": [
        "The exact steps a tester must follow in a scripted test procedure",
        "The mission or focus area for a time-boxed exploratory test session",
        "The code coverage target that must be achieved before releasing the product",
        "The formal entry and exit criteria for a test level"
    ],
    "exp": "A test charter provides a mission or focus (what to explore, what to look for) for a time-boxed exploratory session without prescribing exact steps."
},
"ch4-41": {
    "q": "Which coverage criterion is achieved when both the true and false outcomes of every decision in the code have been exercised?",
    "options": [
        "Statement coverage",
        "Decision coverage",
        "Condition coverage",
        "Path coverage"
    ],
    "exp": "Decision coverage (branch coverage) is achieved when every decision evaluates to both true and false at least once."
},
"ch4-42": {
    "q": "For a valid partition of integers 1–100, which value is the LEAST appropriate representative to select?",
    "options": [
        "50, because it is in the middle of the partition",
        "1, because it is the lower boundary of the partition",
        "0, because it is outside the valid partition",
        "75, because it is in the upper quarter of the partition"
    ],
    "exp": "0 is outside the valid partition (≤0 is the invalid partition); selecting it as a representative of the valid partition violates EP principles."
},
"ch4-43": {
    "q": "State transition testing with 1-switch coverage requires:",
    "options": [
        "Every individual valid transition to be exercised at least once",
        "Every sequence of two consecutive valid transitions to be exercised at least once",
        "Every state to be visited at least once during the test sequence",
        "All invalid transitions to be exercised to verify system robustness"
    ],
    "exp": "1-switch (transition pair) coverage requires every valid sequence of two consecutive transitions to be exercised at least once — stronger than 0-switch."
},
"ch4-44": {
    "q": "A tester identifies that a module handles three independent discount types that can be combined. The most appropriate technique is:",
    "options": [
        "Boundary value analysis, because discounts involve numerical threshold values",
        "Decision table testing, because multiple conditions combine to determine the discount",
        "State transition testing, because discounts represent different system states",
        "Statement coverage, because the discount logic is implemented in code"
    ],
    "exp": "When multiple conditions combine to produce different outcomes (discount combinations), decision tables are the most systematic technique."
},
"ch4-45": {
    "q": "Which statement correctly describes the relationship between EP and BVA?",
    "options": [
        "BVA replaces EP entirely; there is no need to apply EP when BVA is used",
        "EP identifies partitions; BVA extends EP by specifically testing the boundaries between those partitions",
        "EP is only applicable to valid inputs; BVA handles both valid and invalid inputs",
        "BVA is a white-box technique; EP is a black-box technique"
    ],
    "exp": "EP defines the partitions; BVA complements EP by focusing test effort on the boundaries between partitions where defects commonly occur."
},
"ch4-46": {
    "q": "In black-box testing, test cases are derived from:",
    "options": [
        "The internal code structure, including loops, conditions, and data flows",
        "The specification, requirements, or expected behavior of the system",
        "The tester's intuition and experience with similar systems",
        "The code coverage report generated by the previous test execution"
    ],
    "exp": "Black-box techniques derive test cases from external specifications (requirements, user stories, models) without access to the internal implementation."
},
"ch4-47": {
    "q": "A login system has three states: Logged Out, Logged In, and Locked. From Logged Out, entering a correct password transitions to Logged In; three failed attempts transition to Locked. Entering a correct password while Locked should:",
    "options": [
        "Transition to Logged In, because the password is correct",
        "Remain in Locked state, because Locked → Logged In is an invalid transition",
        "Transition to Logged Out, because all locks expire automatically",
        "Generate a system crash, indicating a critical defect in the state machine"
    ],
    "exp": "If no transition from Locked to Logged In is defined, entering a correct password in the Locked state is an invalid transition; the system should stay Locked."
},
"ch4-48": {
    "q": "Which test technique is most appropriate for a system that processes insurance claims based on multiple eligibility conditions?",
    "options": [
        "Boundary value analysis, because insurance amounts have numerical thresholds",
        "Decision table testing, because multiple conditions combine to determine claim eligibility",
        "State transition testing, because claims move through different processing stages",
        "Statement coverage, because all code paths in the claims engine must be exercised"
    ],
    "exp": "Multiple eligibility conditions combining to determine an outcome is the ideal use case for decision table testing."
},
"ch4-49": {
    "q": "A code module has 5 decisions, each with a true and false branch. What is the minimum number of test cases required to achieve 100% decision coverage?",
    "options": [
        "2, because you need only one test for true and one for false across all decisions",
        "5, because each decision requires at least one test case",
        "2, provided the test cases collectively exercise every true and false outcome",
        "10, because each of the 5 decisions requires a separate true and false test case"
    ],
    "exp": "100% decision coverage requires every decision to evaluate true and false; with careful design, 2 test cases can cover all 5 decisions if paths are shared."
},
"ch4-50": {
    "q": "Which of the following best describes a 'coverage item' in the context of test techniques?",
    "options": [
        "A defect found during test execution that reduces overall product quality",
        "An attribute derived from a test condition that is used to measure test coverage",
        "A test case that has been executed and produced a definitive pass or fail result",
        "A requirement that has been traced to at least one executed test case"
    ],
    "exp": "A coverage item is a specific attribute (e.g., a partition, boundary value, decision outcome, transition) derived from conditions to measure how thoroughly testing covers the basis."
},
"ch4-51": {
    "q": "Collaborative user story testing (the 3 C's) helps testers by:",
    "options": [
        "Automating the generation of test cases directly from the user story card",
        "Involving testers early in story definition to identify testability issues and ambiguities",
        "Replacing formal test planning with informal conversations between developers",
        "Ensuring that user stories are always small enough to complete within one sprint"
    ],
    "exp": "Early tester involvement in story definition (Conversation + Confirmation) surfaces testability issues and ambiguities before implementation begins."
},
"ch4-52": {
    "q": "Which statement about applying multiple test techniques is correct?",
    "options": [
        "Only one technique should be applied per test level to avoid redundancy",
        "Combining techniques provides more thorough coverage than any single technique alone",
        "Experience-based techniques should never be combined with formal techniques",
        "White-box and black-box techniques are mutually exclusive and cannot be combined"
    ],
    "exp": "Combining techniques (e.g., EP + BVA + error guessing) provides broader and more thorough coverage than any single technique in isolation."
},
"ch4-53": {
    "q": "A field accepts a two-character country code (exactly 2 alphabetic characters). Which partitions should be defined?",
    "options": [
        "One valid partition only: all two-character alphabetic strings",
        "Valid: exactly 2 alpha chars; invalid: fewer than 2 chars, more than 2 chars, non-alpha chars",
        "Two partitions: uppercase codes and lowercase codes",
        "Four partitions based on the first and second character independently"
    ],
    "exp": "Correct partitioning includes the valid partition and multiple invalid partitions: too short, too long, and non-alphabetic characters."
},
"ch4-54": {
    "q": "Exploratory testing is most effectively structured using:",
    "options": [
        "Detailed step-by-step test scripts that define every action and verification point",
        "Time-boxed sessions with test charters that define the mission and scope",
        "Code coverage targets that guide which parts of the application to explore",
        "Decision tables that enumerate all conditions to investigate during the session"
    ],
    "exp": "Session-based exploratory testing uses time-boxed sessions guided by charters, balancing freedom with accountability."
},
"ch4-55": {
    "q": "Which of the following scenarios is BEST suited for state transition testing?",
    "options": [
        "A calculation engine that computes tax based on income brackets and filing status",
        "An order management system where orders move through states: New, Confirmed, Shipped, Delivered, Cancelled",
        "A search function that filters results based on multiple user-selected criteria",
        "A password field that enforces complexity rules on the characters entered"
    ],
    "exp": "An order moving through defined states (New → Confirmed → Shipped → Delivered/Cancelled) is a classic state machine — the ideal target for state transition testing."
},
# CHAPTER 5 — TEST MANAGEMENT (45 questions) — BLOCK 1/2 (ch5-01 to ch5-23)

"ch5-01": {
    "q": "What is the primary purpose of a test plan?",
    "options": [
        "To list every defect found during the testing phase of the project",
        "To document objectives, scope, approach, resources, schedule, and criteria for the test effort",
        "To replace test cases by providing sufficient guidance for ad hoc execution",
        "To formally approve the system for release to the production environment"
    ],
    "exp": "The test plan communicates objectives, scope, approach, resources, schedule, risks, and entry/exit criteria to all stakeholders."
},
"ch5-02": {
    "q": "What is the difference between a test strategy and a test approach?",
    "options": [
        "They are synonyms; both terms describe the same planning artifact",
        "A test strategy is a general organizational description; a test approach is its adaptation to a specific project",
        "A test approach is broader than a test strategy and supersedes it at the project level",
        "A test strategy applies only to agile projects; a test approach applies to waterfall projects"
    ],
    "exp": "The strategy describes the general organizational testing direction; the approach adapts the strategy to the context of a specific project."
},
"ch5-03": {
    "q": "Entry criteria define:",
    "options": [
        "The conditions that must be met before a test activity can begin",
        "The conditions under which a completed test activity can be declared finished",
        "The list of defects that must be resolved before testing can proceed",
        "The acceptance thresholds the final product must satisfy before user release"
    ],
    "exp": "Entry criteria are pre-conditions for starting a test activity, such as environment readiness, test cases approved, and test data available."
},
"ch5-04": {
    "q": "Exit criteria serve to:",
    "options": [
        "Authorize the commencement of the next test level or activity",
        "Determine when a test activity or level can be considered sufficiently complete",
        "Specify the defects that are acceptable to leave open at product release",
        "Define the skills required for testers assigned to the project"
    ],
    "exp": "Exit criteria define when to stop testing: coverage achieved, open defects below threshold, schedule met, or other agreed conditions."
},
"ch5-05": {
    "q": "In agile methods, the 'Definition of Done' (DoD) functions as:",
    "options": [
        "Entry criteria that must be satisfied before a sprint can begin",
        "A set of exit criteria defining when a work item is truly complete",
        "A formal test plan that replaces the need for traditional test documentation",
        "A defect report template used to track unresolved issues in the backlog"
    ],
    "exp": "The DoD is a set of exit criteria agreed by the team that defines when a work item (story, sprint, release) is genuinely complete."
},
"ch5-06": {
    "q": "The ratio-based estimation technique uses:",
    "options": [
        "Expert judgment from team members familiar with similar past projects",
        "Historical proportions (e.g., the ratio of test effort to development effort) to project the current estimate",
        "Function point analysis to derive test effort from system complexity metrics",
        "Monte Carlo simulation to generate probabilistic effort distributions"
    ],
    "exp": "Ratio-based estimation applies historical proportions from past projects (e.g., test effort = 30% of dev effort) to estimate the current project."
},
"ch5-07": {
    "q": "Metrics-based estimation (extrapolation) relies on:",
    "options": [
        "Intuitive judgment from the most experienced tester on the team",
        "Data and measurements from previous iterations or projects, extrapolated to the current work",
        "The project budget as the primary constraint for determining test scope",
        "Vendor-supplied benchmarks for the testing tools used on the project"
    ],
    "exp": "Metrics-based estimation uses historical data (velocity, defect rates, effort per test case) to extrapolate effort estimates for the current project."
},
"ch5-08": {
    "q": "Expert-based estimation is characterized by:",
    "options": [
        "Ignoring past experience in favor of objective measurement and data analysis",
        "Relying on the judgment of those experienced with the tasks, e.g., Planning Poker or Wideband Delphi",
        "Using only mathematical formulas derived from project size metrics",
        "Delegating estimation entirely to project managers rather than testers"
    ],
    "exp": "Expert-based estimation leverages the knowledge of experienced practitioners, using consensus techniques like Planning Poker or Wideband Delphi."
},
"ch5-09": {
    "q": "In risk-based prioritization, tests are executed first for:",
    "options": [
        "The shortest test cases to maximize the number of tests completed early",
        "The items with the highest risk level (highest probability × impact)",
        "The oldest test cases that have not been executed in recent cycles",
        "The test cases chosen randomly to avoid systematic bias in selection"
    ],
    "exp": "Risk-based prioritization executes tests covering the highest-risk items first, ensuring maximum risk reduction early in the test cycle."
},
"ch5-10": {
    "q": "Coverage-based prioritization orders test cases by:",
    "options": [
        "The estimated execution time, starting with the fastest cases",
        "The incremental coverage each test adds to what has not yet been covered",
        "Alphabetical order of the test case identifiers in the test management tool",
        "The severity of the defects each test case has found in previous cycles"
    ],
    "exp": "Coverage-based prioritization orders tests to maximize new coverage as quickly as possible, executing cases that cover uncovered items first."
},
"ch5-11": {
    "q": "The test pyramid suggests that a well-structured test suite should have:",
    "options": [
        "More end-to-end UI tests than unit tests, to maximize business-visible coverage",
        "Many unit tests at the base and few slow, fragile UI/E2E tests at the top",
        "An equal number of tests at every level to ensure balanced coverage",
        "Only automated tests; manual tests have no place in a mature test pyramid"
    ],
    "exp": "The pyramid recommends many fast, cheap unit tests at the base and few slow, expensive UI/E2E tests at the top for optimal ROI."
},
"ch5-12": {
    "q": "The testing quadrants help to:",
    "options": [
        "Calculate the exact number of test cases required for a given system",
        "Classify test types by whether they support the team or critique the product, and by technology vs. business focus",
        "Determine the sequence in which test levels should be executed",
        "Select the appropriate test automation tool for each test level"
    ],
    "exp": "The quadrants organize tests (supporting team vs. critiquing product; technology-facing vs. business-facing) to ensure balanced test planning coverage."
},
"ch5-13": {
    "q": "In test management, 'risk' is defined as:",
    "options": [
        "A defect that has been found but not yet fixed by the development team",
        "A potential future event with a negative consequence for the project or product",
        "A failed test case that blocks the continuation of the test cycle",
        "A test case that has been excluded from the scope of the current test plan"
    ],
    "exp": "Risk is the possibility of a future event with negative consequences; it combines the probability of occurrence with the magnitude of impact."
},
"ch5-14": {
    "q": "How is the risk level determined?",
    "options": [
        "Cost of fixing the defect multiplied by the remaining project timeline",
        "The likelihood of occurrence combined with the impact of the potential harm",
        "The severity rating multiplied by the priority assigned in the defect tracker",
        "The number of test cases that cover the area divided by total test cases"
    ],
    "exp": "Risk level = probability of occurrence × impact (magnitude of harm). This combination guides test prioritization."
},
"ch5-15": {
    "q": "What is the difference between product risk and project risk?",
    "options": [
        "They are the same; both refer to risks that affect software quality",
        "Product risk affects the quality of the product; project risk affects achieving project objectives",
        "Project risk is always technical; product risk is always business-related",
        "Product risk only applies to customer-facing features; project risk applies to internal processes"
    ],
    "exp": "Product risk affects the quality/fitness of the product; project risk (schedule, budget, resources, suppliers) affects the ability to achieve project goals."
},
"ch5-16": {
    "q": "Which of the following is an example of a PROJECT risk?",
    "options": [
        "An incorrect financial calculation in the billing module",
        "Key test personnel leaving the project mid-cycle, causing schedule delays",
        "A security vulnerability in the authentication component",
        "Poor performance of the search feature under concurrent user load"
    ],
    "exp": "Loss of key personnel causing delays is a project risk (affects project execution); the others are product risks (affect product quality)."
},
"ch5-17": {
    "q": "Which of the following is an example of a PRODUCT risk?",
    "options": [
        "The test environment not being available on the planned start date",
        "A data breach caused by a security defect in the user authentication module",
        "The project budget being exceeded due to unplanned scope additions",
        "A third-party supplier delivering a component later than contractually agreed"
    ],
    "exp": "A security defect causing a data breach directly affects product quality and user safety — a product risk. The others are project risks."
},
"ch5-18": {
    "q": "Risk-based testing uses the risk assessment to:",
    "options": [
        "Eliminate all identified risks before testing begins",
        "Decide what to test, how much to test, and in what order, allocating effort proportional to risk",
        "Determine the salary budget for the testing team",
        "Choose the programming language used to develop the system under test"
    ],
    "exp": "Risk-based testing uses risk levels to prioritize what to test first, how deeply to test, and where to concentrate the most experienced testers."
},
"ch5-19": {
    "q": "Risk assessment comprises:",
    "options": [
        "Only fixing the defects found during the risk identification workshop",
        "Identifying risks and analyzing them by estimating their probability and impact",
        "Executing test cases to verify that identified risks have been mitigated",
        "Approving the test plan after all risks have been reviewed by management"
    ],
    "exp": "Risk assessment includes risk identification followed by risk analysis (estimating probability and impact) to determine risk levels for prioritization."
},
"ch5-20": {
    "q": "How does risk level influence the depth of testing applied?",
    "options": [
        "Higher risk items receive less testing to preserve budget for lower-risk areas",
        "Higher risk items receive more rigorous testing, earlier execution, and more experienced testers",
        "Risk level has no influence on test depth; all items are tested equally",
        "Only items with risk level 'critical' are tested; lower-risk items are excluded"
    ],
    "exp": "Items with higher risk receive more thorough techniques, earlier testing, and more experienced testers to maximize risk reduction."
},
"ch5-21": {
    "q": "The purpose of test monitoring is:",
    "options": [
        "To write test cases that will be executed in the next test cycle",
        "To provide visibility of progress by comparing actual results against the test plan",
        "To fix defects found during the execution phase of testing",
        "To select the test tools that will be used throughout the project"
    ],
    "exp": "Monitoring collects information about test progress to compare against the plan and support informed control decisions."
},
"ch5-22": {
    "q": "Which of the following is a typical test metric?",
    "options": [
        "The color theme selected for the test management tool dashboard",
        "The percentage of test cases executed and the pass/fail ratio",
        "The team's preferred programming language for test automation",
        "The number of meetings held during the test planning phase"
    ],
    "exp": "Common metrics include: test cases planned/executed/passed/failed, defect density, coverage achieved, and defect trend over time."
},
"ch5-23": {
    "q": "A test progress report is primarily intended to:",
    "options": [
        "Replace the test plan when the project scope changes significantly",
        "Inform stakeholders about test status and support decisions during the test effort",
        "Document the final quality assessment at the end of the project",
        "List all requirements that have not yet been covered by any test case"
    ],
    "exp": "Progress reports communicate current status, risks, and results to stakeholders to support ongoing decisions during the test cycle."
},
# CHAPTER 5 — BLOCK 2/2 (ch5-24 to ch5-45)

"ch5-24": {
    "q": "A test completion report is produced:",
    "options": [
        "Before testing begins to communicate the planned approach to stakeholders",
        "At the end of a test level or milestone, summarizing results and lessons learned",
        "Daily during test execution to track the number of defects found each day",
        "Immediately after each individual test case is executed and evaluated"
    ],
    "exp": "The completion report summarizes results, coverage achieved, quality assessment, and lessons learned at the end of a test level or major milestone."
},
"ch5-25": {
    "q": "Configuration management supports testing by:",
    "options": [
        "Automatically generating test cases from configuration files",
        "Ensuring consistent identification and versioning of test items and testware with full traceability",
        "Replacing the test plan with version-controlled configuration documents",
        "Eliminating the need for defect reports by tracking changes to the codebase"
    ],
    "exp": "Configuration management maintains integrity and traceability of items under test and testware (versions, baselines) throughout the project."
},
"ch5-26": {
    "q": "What should a good defect report contain?",
    "options": [
        "Only the title and severity rating to keep reporting lightweight and efficient",
        "Identifier, description, steps to reproduce, expected vs actual result, severity, and priority",
        "Only the name of the developer responsible for the defective code",
        "A list of all test cases executed in the same session as the defect was found"
    ],
    "exp": "Effective defect reports include: ID, description, reproduction steps, expected vs. actual result, environment, severity, and priority."
},
"ch5-27": {
    "q": "What is the difference between defect severity and priority?",
    "options": [
        "They are the same; both measure how urgently a defect must be fixed",
        "Severity measures the technical impact on the system; priority measures the urgency of fixing from a business perspective",
        "Priority is determined by the development team; severity is determined by the business owner",
        "Severity only applies to critical defects; priority applies to all defect types"
    ],
    "exp": "Severity = technical impact on the system; priority = business urgency to fix. They can be independent: a cosmetic defect on the homepage may have low severity but high priority."
},
"ch5-28": {
    "q": "Which scenario best illustrates a defect with HIGH severity but LOW priority?",
    "options": [
        "A spelling mistake on the company homepage that is visible to all visitors",
        "A crash in a rarely used legacy report module that only two users access monthly",
        "A data loss bug in the primary checkout flow affecting all customers",
        "An incorrect currency symbol displayed on all invoices sent to customers"
    ],
    "exp": "A crash (high severity) in a rarely used module (low business impact = low priority) is the classic high-severity/low-priority scenario."
},
"ch5-29": {
    "q": "Which scenario best illustrates a defect with LOW severity but HIGH priority?",
    "options": [
        "A crash in the batch processing system that runs nightly for financial reconciliation",
        "A misspelling of the CEO's name on the company's public-facing homepage",
        "A calculation error in an internal report used only by the finance team quarterly",
        "A performance degradation affecting only users in a non-production test environment"
    ],
    "exp": "A misspelling (low technical severity) on the public homepage is highly visible and embarrassing, making it high priority for the business."
},
"ch5-30": {
    "q": "What is the purpose of test control in the test management process?",
    "options": [
        "To write and review test cases before execution begins",
        "To take corrective actions when monitoring reveals deviations from the test plan",
        "To approve the final product for release to the production environment",
        "To select testing tools and configure the test execution environment"
    ],
    "exp": "Test control acts on monitoring data by taking corrective measures (replanning, reallocating resources) when progress deviates from the plan."
},
"ch5-31": {
    "q": "Traceability between test cases and requirements supports:",
    "options": [
        "Automatic generation of production code from the test cases",
        "Coverage analysis, impact assessment of changes, and audit compliance",
        "Elimination of the need for a separate defect tracking system",
        "Automatic prioritization of test cases without tester involvement"
    ],
    "exp": "Traceability links requirements to test conditions and cases, enabling coverage assessment, change impact analysis, and regulatory audit trails."
},
"ch5-32": {
    "q": "When a change is made to a requirement after testing has begun, which test management activity is most immediately needed?",
    "options": [
        "Immediately halting all testing until the change is fully implemented",
        "Impact analysis to determine which test cases are affected and need updating",
        "Closing all open defects related to the changed requirement without resolution",
        "Discarding the existing test plan and starting the planning process from scratch"
    ],
    "exp": "Impact analysis identifies which existing tests are affected by the change, allowing targeted updates rather than a complete restart."
},
"ch5-33": {
    "q": "In agile projects, how is test planning typically different from traditional projects?",
    "options": [
        "Test planning is eliminated entirely; agile teams rely solely on exploratory testing",
        "Planning is continuous and lightweight, occurring at multiple levels (release, iteration, daily) rather than as a single upfront document",
        "Test planning in agile produces a more detailed document than in waterfall projects",
        "Only the Scrum Master performs test planning; testers focus exclusively on execution"
    ],
    "exp": "Agile test planning is continuous and multi-level (release, sprint, daily), adapting frequently rather than being defined once upfront."
},
"ch5-34": {
    "q": "What is the primary purpose of a risk register in test management?",
    "options": [
        "To track defects found during testing and their current resolution status",
        "To document identified risks, their probability, impact, level, and mitigation actions",
        "To list all test cases that have failed and require investigation",
        "To record the skills and availability of each tester assigned to the project"
    ],
    "exp": "A risk register documents identified risks with their probability, impact, risk level, owner, and planned mitigation or contingency actions."
},
"ch5-35": {
    "q": "A test manager notices that the defect detection rate has dropped significantly in the last three days despite continued testing. The most likely explanation is:",
    "options": [
        "The system has become completely defect-free due to effective testing",
        "The tests being run are repetitive and no longer finding new defects (pesticide paradox)",
        "The testers have become more efficient and are executing test cases faster",
        "The defect tracking tool is malfunctioning and not recording new defects"
    ],
    "exp": "A declining defect detection rate in stable testing conditions typically indicates the pesticide paradox: tests need to be diversified to find new defects."
},
"ch5-36": {
    "q": "Which estimation technique is most appropriate when detailed historical data from similar projects is available?",
    "options": [
        "Expert-based estimation using Planning Poker with the current team",
        "Metrics-based estimation (extrapolation) using historical project data",
        "Ratio-based estimation using industry-standard test-to-development effort ratios",
        "Three-point estimation using optimistic, most likely, and pessimistic scenarios"
    ],
    "exp": "When detailed historical data exists, metrics-based estimation provides the most objective and data-driven projections."
},
"ch5-37": {
    "q": "Test effort estimation should consider:",
    "options": [
        "Only the number of requirements, since each requirement maps to exactly one test case",
        "Product risk, system complexity, required coverage, team experience, and tool support",
        "Only the project deadline, working backward from the release date",
        "Exclusively the number of defects found in the previous project release"
    ],
    "exp": "Estimation considers multiple factors: risk levels, complexity, coverage targets, team skills, tool availability, environment stability, and process maturity."
},
"ch5-38": {
    "q": "What does 'risk mitigation' mean in the context of risk-based testing?",
    "options": [
        "Accepting the risk and proceeding without any testing of the affected area",
        "Taking actions to reduce the probability of a risk occurring or its impact if it does",
        "Transferring the risk entirely to the customer through contractual agreement",
        "Documenting the risk in the register and taking no further action"
    ],
    "exp": "Risk mitigation involves actions (more testing, earlier testing, design reviews) that reduce either the probability of the risk occurring or its impact."
},
"ch5-39": {
    "q": "A test manager is informed that two key testers will be unavailable for the next sprint. Which test management activity should be performed first?",
    "options": [
        "Cancel all testing planned for the sprint and reschedule for the following sprint",
        "Replan the test scope and priorities to account for the reduced capacity",
        "Replace both testers immediately with contractors regardless of cost",
        "Continue with the original plan and accept the resulting quality risk"
    ],
    "exp": "Test control responds to changed circumstances by replanning: adjusting scope, priorities, and assignments to match available capacity."
},
"ch5-40": {
    "q": "Which of the following best describes 'test basis' in the context of test planning?",
    "options": [
        "The team of testers assigned to execute the test cases in the plan",
        "Any documentation or knowledge used to derive test conditions and cases",
        "The baseline version of the software against which all tests are executed",
        "The test environment configuration documented in the test plan"
    ],
    "exp": "The test basis is any artifact (requirements, design, code, risk register) from which test conditions can be identified and test cases derived."
},
"ch5-41": {
    "q": "In risk-based testing, what happens to residual risk after testing is complete?",
    "options": [
        "It is automatically eliminated because all planned tests have been executed",
        "It is communicated to stakeholders so they can make an informed release decision",
        "It is transferred to the development team for resolution before release",
        "It is ignored because testing has already addressed the highest-priority risks"
    ],
    "exp": "Residual risk (untested or partially tested areas) must be communicated to stakeholders so they can make an informed go/no-go decision."
},
"ch5-42": {
    "q": "Which metric best indicates whether the test execution phase is on track?",
    "options": [
        "The total lines of code written by the development team per sprint",
        "The percentage of planned test cases executed versus the schedule to date",
        "The number of test team meetings held during the execution phase",
        "The total size of the test plan document in pages"
    ],
    "exp": "Comparing the percentage of test cases executed against the planned schedule is the most direct indicator of execution phase progress."
},
"ch5-43": {
    "q": "What is the relationship between test monitoring and test control?",
    "options": [
        "They are the same activity performed by different team members",
        "Monitoring collects progress data; control uses that data to take corrective actions",
        "Control precedes monitoring; actions are taken first, then progress is measured",
        "Monitoring is performed only at the end of testing; control occurs throughout"
    ],
    "exp": "Monitoring gathers and analyzes progress data; control acts on that data by adjusting plans, resources, or scope when deviations occur."
},
"ch5-44": {
    "q": "A product has been tested and 15 defects remain open at release. The test manager communicates this to stakeholders. This is an example of:",
    "options": [
        "Poor test management, because no defects should remain open at release",
        "Transparent risk communication, enabling stakeholders to make an informed release decision",
        "Test failure, because exit criteria require zero open defects before release",
        "Scope reduction, because untested features were excluded from the release"
    ],
    "exp": "Communicating known residual risk (open defects) is good practice; it gives stakeholders the information needed to make an informed release decision."
},
"ch5-45": {
    "q": "Which of the following best describes the role of a test manager versus a tester?",
    "options": [
        "Test managers write test cases; testers execute them and report results",
        "Test managers handle planning, monitoring, and stakeholder communication; testers handle analysis, design, and execution",
        "Test managers are responsible for automation; testers are responsible for manual testing",
        "Test managers work only in waterfall; testers work only in agile projects"
    ],
    "exp": "The test manager owns planning, monitoring, control, and stakeholder reporting; the tester owns test analysis, design, implementation, and execution."
},

}  # fim do dicionário EN

# ============================================================
# Script principal
# ============================================================
import pathlib

BANK_FILE = pathlib.Path(__file__).parent / "ctfl-questions-ptbr.json"

def main():
    bank = json.loads(BANK_FILE.read_text(encoding="utf-8"))
    questions = bank["questions"]

    injected = 0
    skipped_existing = 0
    not_found = []

    id_to_q = {q["id"]: q for q in questions}

    for qid, en_data in EN.items():
        if qid not in id_to_q:
            not_found.append(qid)
            continue
        q = id_to_q[qid]
        # Nunca sobrescreve EN existente
        if "en" in q.get("locales", {}):
            skipped_existing += 1
            continue
        # Validação básica
        assert len(en_data["options"]) == len(q["locales"]["pt"]["options"]), \
            f"Número de opções diferente em {qid}"
        q.setdefault("locales", {})["en"] = en_data
        injected += 1

    # Atualizar availableLanguages no meta
    if injected > 0 and "en" not in bank["meta"].get("availableLanguages", []):
        bank["meta"]["availableLanguages"].append("en")

    BANK_FILE.write_text(
        json.dumps(bank, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"\nResultado:")
    print(f"  Injetadas:          {injected}")
    print(f"  Já tinham EN:       {skipped_existing}")
    print(f"  IDs não encontrados: {len(not_found)}")
    if not_found:
        print(f"  IDs ausentes: {not_found}")

    total_en = sum(1 for q in questions if "en" in q.get("locales", {}))
    print(f"  Total com EN agora: {total_en} / {len(questions)}")

if __name__ == "__main__":
    main()
