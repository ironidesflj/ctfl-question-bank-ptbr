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
        "A failure causes a defect, which causes an error",
        "Error and defect are synonyms; failure only occurs in production",
        "An error (human action) introduces a defect into an artifact, which when executed may cause a failure"
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
        "Debugging only occurs in production",
        "Debugging finds failures; testing fixes the code",
        "Testing finds failures; debugging locates, analyzes, and fixes the defect that caused them"
    ],
    "exp": "Testing reveals failures caused by defects; debugging is the development activity that locates, diagnoses, and corrects the defect."
},
"ch1-04": {
    "q": "Why is testing necessary?",
    "options": [
        "To replace code review",
        "Because it is required by law",
        "To guarantee defect-free software",
        "To contribute to project success by reducing the risk of failures in operation"
    ],
    "exp": "Testing reduces the risk of operational failures and helps deliver a product with quality adequate to stakeholder needs."
},
"ch1-05": {
    "q": "How do quality control (QC) and quality assurance (QA) relate?",
    "options": [
        "They are synonyms",
        "Testing is part of QA, not QC",
        "QA is product-oriented; QC is process-oriented",
        "QC is product-oriented (includes testing); QA is process-oriented"
    ],
    "exp": "QC focuses on the product and includes activities such as testing; QA focuses on process improvement to build confidence that quality will be achieved."
},
"ch1-06": {
    "q": "The root cause of a defect is:",
    "options": [
        "The failure observed by the user",
        "The test case that failed",
        "The test environment",
        "The earliest event that, if corrected, prevents the recurrence of the defect"
    ],
    "exp": "Root cause analysis seeks the fundamental origin, enabling actions that prevent similar defects from recurring."
},
"ch1-07": {
    "q": "The principle 'testing shows the presence of defects, not their absence' means that:",
    "options": [
        "Testing proves there are no defects",
        "Testing is useless",
        "Defects always exist",
        "Testing can reveal defects but cannot prove none exist"
    ],
    "exp": "Finding defects does not prove their absence; even when no defects are found, there is no guarantee of total correctness."
},
"ch1-08": {
    "q": "The principle 'exhaustive testing is impossible' has the practical consequence of:",
    "options": [
        "Not worth testing",
        "Automating everything",
        "Testing only the happy path",
        "Using risk analysis and priorities to focus effort"
    ],
    "exp": "Since testing all combinations is not feasible, effort is prioritized based on risk and business priorities."
},
"ch1-09": {
    "q": "The 'early testing saves time and money' principle states that:",
    "options": [
        "Tests should only start after the code is complete",
        "Only requirements can be tested early",
        "Testing early increases costs",
        "Testing activities should start as early as possible in the lifecycle"
    ],
    "exp": "Starting early (including static testing on requirements) reduces costs because defects found late are more expensive to fix."
},
"ch1-10": {
    "q": "The 'defect clustering' principle suggests that:",
    "options": [
        "Defects are evenly distributed",
        "Defects only appear in new code",
        "Each module has exactly one defect",
        "A small number of modules contain the majority of defects"
    ],
    "exp": "Typically a minority of modules concentrates most defects (Pareto principle), which guides test prioritization."
},
"ch1-11": {
    "q": "The 'pesticide paradox' indicates that:",
    "options": [
        "More testing generates more defects",
        "Pesticides affect the software",
        "Manual tests are better than automated",
        "Repeating the same tests will eventually stop finding new defects"
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
        "Errors do not matter",
        "Errors do not exist",
        "Fixing all known defects is useless if the system does not meet user needs"
    ],
    "exp": "A product may be free of known defects and still be inadequate if it does not meet real user needs."
},
"ch1-14": {
    "q": "A team decides to prioritize testing the payment module, where defects have historically clustered. Which principle justifies this?",
    "options": [
        "Exhaustive testing",
        "Pesticide paradox",
        "Absence-of-errors fallacy",
        "Defect clustering"
    ],
    "exp": "Concentrating effort where defects historically cluster applies the defect clustering principle."
},
"ch1-15": {
    "q": "Which test process activity defines objectives, approach, and resources?",
    "options": [
        "Test execution",
        "Test completion",
        "Test analysis",
        "Test planning"
    ],
    "exp": "Test planning defines objectives, scope, approach, resources, and criteria."
},
"ch1-16": {
    "q": "Monitoring and control of testing serves to:",
    "options": [
        "Write test cases",
        "Close the project",
        "Execute the tests",
        "Compare actual progress against the plan and take corrective actions"
    ],
    "exp": "Monitoring collects metrics; control acts (replan, reallocate) when there are deviations from the plan."
},
"ch1-17": {
    "q": "In the test analysis activity, what is primarily produced?",
    "options": [
        "Automated scripts",
        "Test data",
        "The final report",
        "Test conditions derived from the test basis and its criteria"
    ],
    "exp": "Analysis identifies what to test — the test conditions — from the test basis (requirements, risks, etc.)."
},
"ch1-18": {
    "q": "In test design, the focus is on:",
    "options": [
        "Identifying what to test",
        "Reporting defects",
        "Executing the cases",
        "Defining how to test: test cases and sets derived from the conditions"
    ],
    "exp": "Test design elaborates how to cover the test conditions, producing test cases and test sets."
},
"ch1-19": {
    "q": "What is the primary output of the test implementation activity?",
    "options": [
        "Test conditions",
        "The progress report",
        "The test plan",
        "Procedures, scripts, and data ready for execution, with the environment prepared"
    ],
    "exp": "Implementation organizes and prepares everything needed to execute: procedures, data, environment, and schedule."
},
"ch1-20": {
    "q": "During test execution, when a divergent result is found, the tester should first:",
    "options": [
        "Fix the code",
        "Ignore it if it is minor",
        "Stop testing",
        "Record the result and, if it is an anomaly, create a defect report"
    ],
    "exp": "Results are compared to expected; divergences (anomalies) are analyzed and, when defects are confirmed, logged in a defect report."
},
"ch1-21": {
    "q": "The test completion activity typically includes:",
    "options": [
        "Writing the first test cases",
        "Preparing the environment",
        "Defining objectives",
        "Archiving testware, recording lessons learned, and producing the completion report"
    ],
    "exp": "Completion consolidates results, archives reusable testware, records lessons learned, and issues the completion report."
},
"ch1-22": {
    "q": "What is 'testware'?",
    "options": [
        "Test hardware",
        "The system under test",
        "The automation tool",
        "Artifacts produced during the test process (plans, cases, data, reports)"
    ],
    "exp": "Testware encompasses all work products of the testing process: plans, conditions, cases, data, scripts, reports."
},
"ch1-23": {
    "q": "What is the main benefit of traceability between the test basis and testware?",
    "options": [
        "Reducing the number of tests",
        "Speeding up the code",
        "Eliminating documentation",
        "Enabling coverage assessment and impact analysis of changes on the tests"
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
    "q": "Which cognitive skill is considered fundamental for a good tester?",
    "options": [
        "Typing speed and mastery of keyboard shortcuts",
        "Ability to write production code in any language",
        "Exclusive, advanced knowledge of multiple programming languages",
        "Analytical and critical thinking to question assumptions and identify problems"
    ],
    "exp": "Analytical/critical thinking allows the tester to question assumptions, identify inconsistencies, and find non-obvious defects."
},
"ch1-26": {
    "q": "The 'whole-team approach' in agile testing implies that:",
    "options": [
        "Only testers are responsible for quality, never developers",
        "Developers never participate in the project's testing activities",
        "The test manager makes all decisions alone, without consulting the team",
        "The whole team shares responsibility for quality, with testers collaborating with devs and stakeholders"
    ],
    "exp": "In the whole-team approach, quality is a collective responsibility; testers, devs, and business collaborate from the start."
},
"ch1-27": {
    "q": "What is the main benefit of having testers with different degrees of independence?",
    "options": [
        "Increasing project cost",
        "Eliminating the need for reviews",
        "Ensuring all tests are automated",
        "Combining the author's knowledge with the impartial perspective of someone who didn't write the artifact"
    ],
    "exp": "Different degrees of independence balance contextual knowledge and impartiality, improving detection effectiveness."
},
"ch1-28": {
    "q": "A tester who reviews the requirements they themselves wrote will have difficulty finding defects because:",
    "options": [
        "There isn't enough time available in the project schedule",
        "Requirements reviews aren't considered part of testing",
        "Well-written requirements can never contain any kind of defect",
        "Author bias makes it hard to see one's own mistakes — the tester tends to confirm what they wrote"
    ],
    "exp": "The author's cognitive bias causes them to read what they intended to write, not what is actually written."
},
"ch1-29": {
    "q": "At which degree of independence is the tester external to the developer's organization?",
    "options": [
        "A tester who is the author themselves",
        "A tester from another team in the same organization",
        "A tester from a specialized external company",
        "A tester from the development team"
    ],
    "exp": "The highest degree of independence is represented by testers from external organizations — consultants or independent labs."
},
"ch1-30": {
    "q": "Bidirectional traceability between requirements and test cases enables:",
    "options": [
        "Automatically executing tests without any human intervention",
        "Automatically reducing the total number of system defects",
        "Completely eliminating the need for a formal test plan",
        "Verifying requirements coverage and analyzing the impact of changes on tests"
    ],
    "exp": "With bidirectional traceability, you can know which tests cover each requirement and which tests will be affected by changes."
},
"ch1-31": {
    "q": "What is the main role of the test manager in a project?",
    "options": [
        "Personally executing all test cases manually",
        "Writing business requirements together with stakeholders",
        "Directly developing the system's production code",
        "Planning, monitoring, controlling, and leading test activities and the team"
    ],
    "exp": "The test manager is responsible for planning, monitoring, and controlling the test process and leading the team."
},
"ch1-32": {
    "q": "What is the 'test basis'?",
    "options": [
        "The environment where tests are executed",
        "The defect database",
        "The result of executed tests",
        "The set of artifacts from which tests are derived (requirements, code, models, etc.)"
    ],
    "exp": "The test basis is the artifacts — requirements, specifications, code, models — from which test conditions and cases are derived."
},
"ch1-33": {
    "q": "What is the difference between verification and validation in the context of testing?",
    "options": [
        "Verification and validation are synonymous and interchangeable terms",
        "System validation can only occur after release to production",
        "Verification is always dynamic; validation is always a static process",
        "Verification: 'are we building it right?' (per specification); validation: 'are we building the right thing?' (meets the user)"
    ],
    "exp": "Verification checks compliance with the specification; validation checks whether the product meets real user needs."
},
"ch1-34": {
    "q": "The tester's mindset differs from the developer's because the tester:",
    "options": [
        "Focuses on building features quickly",
        "Only confirms that the software works as the dev expects",
        "Avoids questioning design decisions",
        "Adopts a critical perspective, actively seeking failures and questioning assumptions"
    ],
    "exp": "Testers adopt a questioning mindset and constructive skepticism to find what might fail, not to confirm that it works."
},
"ch1-35": {
    "q": "What is a 'test object'?",
    "options": [
        "The tool used for testing",
        "The execution environment",
        "The test case itself",
        "The work item (component, system, requirement) being tested"
    ],
    "exp": "The test object is the artifact being evaluated: a component, system, requirement, model, or document."
},
"ch1-36": {
    "q": "How does effective defect communication by the tester contribute to the project?",
    "options": [
        "It creates unnecessary friction with the development team",
        "It increases the number of defects found",
        "It replaces the need for test cases",
        "It allows defects to be understood, prioritized, and fixed efficiently"
    ],
    "exp": "Clear, objective, and factual reports facilitate understanding, reproduction, and correction of defects, while preserving collaboration."
},
"ch1-37": {
    "q": "Which characteristic of early testing (shift-left) differentiates it from traditional testing?",
    "options": [
        "Testing is only carried out after the system is in production",
        "Shift-left can only be applied in fully agile projects",
        "Shift-left completely eliminates the need for system testing",
        "Test activities (including static reviews) start from requirements, not just after coding"
    ],
    "exp": "Shift-left means starting to test — including requirements reviews — in early phases, even before any code exists."
},
"ch1-38": {
    "q": "Root cause analysis of recurring defects benefits the process because it:",
    "options": [
        "Only documents the defects found, without investigating the cause",
        "Is only necessary in safety- or health-critical projects",
        "Completely replaces the need to run dynamic tests",
        "Identifies the origin of problems, enabling process improvements that prevent similar defects in the future"
    ],
    "exp": "Identifying the root cause enables process improvements that prevent the recurrence of similar classes of defects."
},
"ch1-39": {
    "q": "A test artifact such as a 'test case' must contain at minimum:",
    "options": [
        "Only the name of the tester responsible for execution",
        "Only the creation date and current system version",
        "Only the expected result, with no execution steps",
        "Preconditions, execution steps, expected result, and postconditions"
    ],
    "exp": "A complete test case defines preconditions, inputs, steps, expected result, and postconditions, ensuring repeatability."
},
"ch1-40": {
    "q": "What is the impact of defects found in production compared to defects found in requirements?",
    "options": [
        "The cost of fixing is exactly the same at any phase",
        "The financial impact is irrelevant to project success",
        "Defects found in production are always easier to fix",
        "Defects in production are much more expensive to fix — the cost grows with each phase that passes"
    ],
    "exp": "The cost of fixing increases exponentially by phase: defects in requirements cost much less than in production."
},
# ============================================================
# CHAPTER 2 — TESTING THROUGHOUT THE SDLC (25 questions)
# ============================================================

"ch2-01": {
    "q": "How does the software development lifecycle model influence testing?",
    "options": [
        "It has no influence; testing is always performed the same way regardless of the model",
        "It determines the number of testers required but not the testing approach",
        "It only affects the choice of test automation tool",
        "It influences the scope, timing, approach, and level of detail of testing activities"
    ],
    "exp": "The SDLC model shapes when, how, and how deeply testing is performed; sequential models tend to test by phase, while iterative/agile models integrate testing continuously."
},
"ch2-02": {
    "q": "What does 'shift-left' mean in the context of software testing?",
    "options": [
        "Moving test execution to a later phase to allow more development time",
        "Reducing the number of test levels by merging them into one phase",
        "Shifting the testing team to the left side of the office floor plan",
        "Anticipating testing activities to earlier stages of the development lifecycle"
    ],
    "exp": "Shift-left moves testing earlier in the lifecycle, enabling earlier defect detection and reducing the cost of fixing them."
},
"ch2-03": {
    "q": "TDD, ATDD, and BDD are examples of:",
    "options": [
        "Automated UI testing frameworks used in regression suites",
        "Performance testing methodologies applied in load testing scenarios",
        "Configuration management strategies for test environments",
        "Test-first approaches where tests or acceptance criteria guide development"
    ],
    "exp": "TDD, ATDD, and BDD are test-first approaches: tests or acceptance criteria are defined before or alongside the code, guiding implementation."
},
"ch2-04": {
    "q": "What is the primary benefit of retrospectives for the test process?",
    "options": [
        "They replace the need for test planning in agile projects",
        "They eliminate the need for defect reports by resolving issues verbally",
        "They provide a mechanism for assigning blame for defects found in production",
        "They promote continuous process improvement based on lessons learned"
    ],
    "exp": "Retrospectives identify what to improve (process, tools, collaboration), supporting continuous improvement across iterations."
},
"ch2-05": {
    "q": "Component testing (unit testing) focuses on:",
    "options": [
        "Verifying interactions between separately developed systems across organizational boundaries",
        "Evaluating system behavior under concurrent load from multiple users",
        "Validating the complete system against user acceptance criteria",
        "Testing individual components in isolation, typically performed by developers"
    ],
    "exp": "Component testing verifies individual modules/units in isolation, often using stubs and drivers, and is typically performed by developers."
},
"ch2-06": {
    "q": "What is the difference between component integration testing and system integration testing?",
    "options": [
        "They are identical; the terms are interchangeable in modern testing practice",
        "Only component integration testing uses interfaces; system integration testing uses only APIs",
        "System integration testing is always performed before component integration testing",
        "Component integration tests interactions within a system; system integration tests interactions between distinct systems"
    ],
    "exp": "Component integration focuses on internal interfaces between components of one system; system integration focuses on interfaces between different systems or organizations."
},
"ch2-07": {
    "q": "System testing evaluates:",
    "options": [
        "Individual components in isolation using drivers and stubs to simulate dependencies",
        "Contractual acceptance criteria defined between the customer and the supplier",
        "Only the user interface layer of the application under test",
        "The behavior and capabilities of the complete integrated system as a whole"
    ],
    "exp": "System testing evaluates the fully integrated system end-to-end, covering both functional and non-functional behavior."
},
"ch2-08": {
    "q": "Which are common forms of acceptance testing?",
    "options": [
        "Unit testing and integration testing performed by developers before handover",
        "Static and dynamic testing merged into a unified acceptance review process",
        "White-box and black-box testing combined into a single acceptance phase",
        "User acceptance (UAT), operational, contractual, and regulatory acceptance testing"
    ],
    "exp": "Acceptance testing includes UAT, operational acceptance (backup, security), contractual acceptance, and regulatory acceptance."
},
"ch2-09": {
    "q": "What is the difference between alpha and beta testing?",
    "options": [
        "Alpha testing is performed in production; beta testing is performed by the development team",
        "Alpha and beta testing are synonyms for system and acceptance testing respectively",
        "Beta testing always precedes alpha testing in the release lifecycle",
        "Alpha testing occurs at the developer's site; beta testing is performed by real users in their own environment"
    ],
    "exp": "Alpha is conducted at the developer's premises (by users or the team); beta is performed by users in their own environment."
},
"ch2-10": {
    "q": "Functional testing evaluates:",
    "options": [
        "How the system behaves under stress, including performance and resource consumption",
        "The degree to which the system satisfies operational and regulatory constraints",
        "The internal structure of the code, including statement and branch coverage",
        "What the system does, based on its specified functional requirements and behavior"
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
    "q": "In BDD (Behaviour-Driven Development), scenarios are written in the format:",
    "options": [
        "Technical pseudo-code aimed exclusively at developers",
        "Given/When/Then, describing behavior in language close to the business",
        "XML configuration files for the test environment",
        "A state diagram representing the system flow"
    ],
    "exp": "BDD uses Given/When/Then (or equivalent) to describe behaviors in language understandable by both business and technical people."
},
"ch2-17": {
    "q": "What is the essential difference between TDD and ATDD?",
    "options": [
        "TDD and ATDD are identical and interchangeable approaches",
        "TDD is driven by the developer's unit tests; ATDD uses acceptance tests defined with business",
        "ATDD can only be applied using UI automation tools",
        "TDD can only be applied in fully agile projects"
    ],
    "exp": "TDD: the dev writes a unit test before the code. ATDD: the team defines acceptance tests with stakeholders before implementing."
},
"ch2-18": {
    "q": "In agile projects with short iterations, which test level is most challenging to execute within the sprint?",
    "options": [
        "Component (unit) testing, as it is the simplest of all",
        "Complete system and acceptance testing, as they require more integration and time",
        "Code reviews carried out by the developers themselves",
        "Automated unit regression tests run in CI"
    ],
    "exp": "System and acceptance tests require integration and end-to-end scenarios, which can be hard to complete within a short sprint."
},
"ch2-19": {
    "q": "What is a 'stub' in the context of component testing?",
    "options": [
        "An automation tool",
        "A substitute component that simulates a dependency of the component under test (called by the component)",
        "A type of defect",
        "A test report"
    ],
    "exp": "Stubs simulate dependencies called by the tested component (downward call), allowing isolation of the component."
},
"ch2-20": {
    "q": "System integration testing mainly evaluates:",
    "options": [
        "Only the internal logic of each module in isolation",
        "The interfaces and interactions between distinct systems, including third-party systems and external APIs",
        "Only the graphical interface aimed at the end user",
        "Exclusively the performance of the database used"
    ],
    "exp": "It tests interfaces between distinct systems — APIs, external services, integrations — not the internal logic of each one."
},
"ch2-21": {
    "q": "Which event is typically NOT a trigger for maintenance testing?",
    "options": [
        "Fixing a critical defect in production",
        "Creating the project's initial planning",
        "Migrating a database to a new version",
        "Retirement/decommissioning of a legacy system"
    ],
    "exp": "Initial planning happens before the system exists; maintenance triggers involve modification, migration, or decommissioning."
},
"ch2-22": {
    "q": "Operational testing (operational acceptance) checks aspects such as:",
    "options": [
        "Only the business logic implemented in the features",
        "Backup and recovery, installation, operational security, and administrative procedures",
        "Directly the source code of the tested application",
        "Exclusively the system's functional requirements"
    ],
    "exp": "Operational acceptance focuses on operation/support aspects: backup, restore, installation, configuration, and operational security."
},
"ch2-23": {
    "q": "Which integration approach combines low-level components first and progressively adds higher-level components?",
    "options": [
        "Big-bang",
        "Bottom-up",
        "Top-down",
        "Sandwich"
    ],
    "exp": "Bottom-up integrates from the bottom up: it starts with the lowest-level components, eliminating the need for stubs but requiring drivers."
},
"ch2-24": {
    "q": "In the context of system testing, a 'use case' serves as:",
    "options": [
        "A technical specification of the database schema",
        "A basis for designing test scenarios that cover actor-system interaction flows",
        "A regression test automation tool",
        "A specific type of defect found in production"
    ],
    "exp": "Use cases describe interaction flows, serving as a basis for end-to-end system test scenarios."
},
"ch2-25": {
    "q": "The main benefit of automating regression tests in continuous integration (CI) is:",
    "options": [
        "Completely eliminating the need for manual testing",
        "Quickly detecting regressions introduced by new changes, providing fast feedback to the team",
        "Directly reducing the number of project requirements",
        "Completely replacing the need for acceptance testing"
    ],
    "exp": "In CI, regression automation runs on every integration, giving immediate feedback on the impact of changes to existing code."
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
    "q": "Which tool supports static testing through automated source code analysis?",
    "options": [
        "Performance test execution tool",
        "Static analysis tool (linter/code analyzer)",
        "UI record-and-playback tool",
        "Configuration management tool"
    ],
    "exp": "Static analysis tools examine code without executing it, detecting suspicious patterns, violations, and vulnerabilities."
},
"ch3-18": {
    "q": "What is an entry criterion for a formal review?",
    "options": [
        "Only the minimum number of participants required for the meeting",
        "A condition that must be satisfied before starting the review (e.g., artifact complete and available)",
        "Only the maximum duration allowed for the meeting",
        "Exclusively the formal title of the document submitted for review"
    ],
    "exp": "Entry criteria ensure the review only starts when the artifact and prerequisites are ready, avoiding wasted effort."
},
"ch3-19": {
    "q": "A common anti-pattern in reviews is:",
    "options": [
        "Focusing exclusively on the defects found in the artifact",
        "Using the review to evaluate performance or criticize the author as a person",
        "Preparing individually and carefully before the meeting",
        "Carefully recording all anomalies found"
    ],
    "exp": "Reviewing the person instead of the product creates a negative climate, inhibits participation, and diverts from the goal of improving the artifact."
},
"ch3-20": {
    "q": "What is a typical exit criterion for a formal inspection?",
    "options": [
        "All participants fully agreeing on everything discussed",
        "Defect rate below a defined threshold or all open defects addressed",
        "The time scheduled for the meeting having ended",
        "The author personally approving all comments"
    ],
    "exp": "Inspection exit criteria include defect density thresholds and resolution of all identified open issues."
},
"ch3-21": {
    "q": "Which role in a review is responsible for ensuring the process is followed and the environment is productive?",
    "options": [
        "Author",
        "Moderator (facilitator)",
        "Reviewer",
        "Test manager"
    ],
    "exp": "The moderator facilitates the meeting, keeps the focus on the artifact, ensures the process is followed, and manages conflicts."
},
"ch3-22": {
    "q": "'Checklist-based reviewing' uses lists to:",
    "options": [
        "Formally evaluate the individual performance of reviewers",
        "Guide reviewers in searching for specific known types of defects",
        "Precisely measure the code coverage of the tests",
        "Completely automate the review process"
    ],
    "exp": "Review checklists direct attention to typical defects (clarity, consistency, completeness), increasing effectiveness."
},
"ch3-23": {
    "q": "Tool-supported static analysis can automatically detect:",
    "options": [
        "Usability flaws perceived subjectively by the user",
        "Uninitialized variables, dead code, and coding standard violations",
        "Bugs that only appear under intense user load",
        "Complex, domain-specific business logic errors"
    ],
    "exp": "Static analysis tools detect problematic patterns such as unused variables, potential null references, and style violations."
},
"ch3-24": {
    "q": "What is the main difference between a technical review and an inspection?",
    "options": [
        "Inspection is always much less formal and rigorous than a technical review",
        "Inspection has a more rigid process with defined roles, metrics, entry/exit criteria, and follow-up; technical review is less formal",
        "Only the technical review uses formal checklists; inspection never does",
        "Inspection and technical review are completely equivalent in practice"
    ],
    "exp": "Inspection is the most formal form, with roles, metrics, entry/exit criteria, and rigorous follow-up; technical review is less rigid."
},
"ch3-25": {
    "q": "Why is it important to limit the size of the artifact reviewed in a review meeting?",
    "options": [
        "Only to reduce the number of participants invited",
        "Long reviews cause fatigue, reducing attention and defect detection rate",
        "Artifact size never influences review quality",
        "Only to save paper and printing resources"
    ],
    "exp": "An artifact that is too long leads to reviewer fatigue, decreasing concentration and effectiveness in defect detection."
},
# ============================================================
# CHAPTER 4 — TEST TECHNIQUES (55 questions) — BLOCK 1/2 (ch4-01 to ch4-28)
# ============================================================

"ch4-01": {
    "q": "Test techniques are primarily classified into:",
    "options": [
        "Black-box, white-box, and experience-based techniques",
        "Manual and automated techniques based on execution method",
        "Functional and non-functional techniques based on quality characteristic",
        "Static and dynamic techniques based on whether code is executed"
    ],
    "exp": "The CTFL syllabus defines three technique categories: black-box (specification-based), white-box (structure-based), and experience-based."
},
"ch4-02": {
    "q": "Equivalence partitioning (EP) is based on the idea that:",
    "options": [
        "Values within the same partition are treated equivalently by the system, so one representative suffices",
        "Every possible input value must be tested to ensure complete coverage",
        "Only boundary values between partitions require testing for adequate coverage",
        "Invalid partitions do not need to be tested because the system should reject them automatically"
    ],
    "exp": "In EP, all values within a partition produce equivalent behavior; testing one representative value per partition is sufficient."
},
"ch4-03": {
    "q": "A field accepts integers from 1 to 100. Which equivalence partitions exist, including invalid ones?",
    "options": [
        "Three partitions: ≤0 (invalid), 1–100 (valid), ≥101 (invalid)",
        "Only one valid partition: 1–100",
        "Two partitions: 1–50 and 51–100",
        "Four partitions: negative, zero, 1–100, and above 100"
    ],
    "exp": "There are three partitions: below 1 (invalid), 1–100 (valid), and above 100 (invalid). Zero and negatives are part of the ≤0 invalid partition."
},
"ch4-04": {
    "q": "Why should invalid partitions also be tested in equivalence partitioning?",
    "options": [
        "To verify that the system correctly handles out-of-range inputs with appropriate rejection or error messages",
        "To increase the total count of test cases and demonstrate thoroughness",
        "Because invalid partitions are always more likely to contain defects than valid ones",
        "To satisfy regulatory requirements that mandate testing of all possible input combinations"
    ],
    "exp": "Invalid partitions verify that the system handles unexpected inputs correctly, such as displaying error messages or rejecting the input gracefully."
},
"ch4-05": {
    "q": "Boundary value analysis (BVA) is effective because:",
    "options": [
        "Defects tend to cluster at the boundaries between partitions",
        "It guarantees 100% statement coverage of the source code under test",
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
        "64, 65, and 66",
        "65 only",
        "63, 64, and 65",
        "65, 66, and 67"
    ],
    "exp": "3-value BVA tests the boundary itself and both adjacent values: 64 (just below), 65 (the boundary), and 66 (just above)."
},
"ch4-08": {
    "q": "Passwords must be between 8 and 16 characters. Using 2-value BVA, which lengths are tested at the lower boundary?",
    "options": [
        "7 and 8",
        "8 and 9",
        "6, 7, and 8",
        "8 and 16"
    ],
    "exp": "At the lower boundary (8), 2-value BVA tests 7 (invalid, just below) and 8 (valid, the boundary itself)."
},
"ch4-09": {
    "q": "A decision table is most appropriate when:",
    "options": [
        "There are combinations of conditions that lead to different actions (business rules)",
        "The system behavior depends on a sequence of states triggered by specific events",
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
    "q": "A discount is granted only when both 'VIP customer = Yes' AND 'valid coupon = Yes'. For the combination VIP=Yes, coupon=No, the expected action is:",
    "options": [
        "Do not grant the discount because not all conditions are satisfied",
        "Grant the discount because the customer is VIP",
        "Generate a system error requiring manual intervention",
        "Grant a partial discount proportional to the conditions satisfied"
    ],
    "exp": "The action (discount) only occurs when all required conditions are true; with coupon=No, the discount is not granted."
},
"ch4-12": {
    "q": "In a decision table, conditions and actions represent respectively:",
    "options": [
        "The causes (inputs/conditions) and effects (resulting actions) for each rule",
        "Outputs and inputs of the system under test",
        "States and transitions in the system's behavioral model",
        "Test cases and their associated expected test data values"
    ],
    "exp": "Conditions are the causes (inputs); actions are the effects (expected results) for each combination of conditions."
},
"ch4-13": {
    "q": "State transition testing is appropriate for systems that:",
    "options": [
        "Change their behavior based on the current state and the events received",
        "Process purely numerical calculations without any dependency on previous inputs",
        "Only have one possible state and respond identically to all inputs",
        "Are stateless REST APIs that process each request independently"
    ],
    "exp": "State transition testing models states, events, transitions, and actions — ideal for sessions, protocols, workflows, and any stateful system."
},
"ch4-14": {
    "q": "In a state diagram, an 'invalid transition' is:",
    "options": [
        "An event that should not cause a state change from the current state",
        "A transition that is permitted and should be exercised at least once",
        "The initial transition from the start state to the first operational state",
        "An exit action that executes when leaving a particular state"
    ],
    "exp": "Invalid transitions are state/event pairs for which no transition is defined; testing them verifies the system's robustness against unexpected events."
},
"ch4-15": {
    "q": "An ATM requires a card to be inserted before accepting a PIN. Attempting to enter a PIN without a card tests:",
    "options": [
        "An invalid transition (unexpected event for the current state)",
        "A valid transition from the idle state",
        "The terminal state of the ATM workflow",
        "An entry action for the PIN entry state"
    ],
    "exp": "Entering a PIN in the 'awaiting card' state is an event not defined for that state — an invalid transition testing system robustness."
},
"ch4-16": {
    "q": "0-switch coverage (valid transitions coverage) requires:",
    "options": [
        "Exercising each individual valid transition at least once",
        "Covering every pair of consecutive valid transitions at least once",
        "Covering all invalid transitions to verify system robustness",
        "Visiting every state at least twice during the test sequence"
    ],
    "exp": "0-switch (single transition) coverage requires each valid transition to be exercised at least once."
},
"ch4-17": {
    "q": "When choosing between EP, BVA, decision tables, and state transitions, the primary criterion is:",
    "options": [
        "The nature of the problem: ranges, rule combinations, or state-dependent behavior",
        "The automation tool available to the test team",
        "The personal preference and experience of the individual tester",
        "The size of the development team and the project deadline"
    ],
    "exp": "Technique selection depends on the problem structure: ranges (EP/BVA), combined rules (decision table), state-dependent behavior (state transition)."
},
"ch4-18": {
    "q": "White-box test techniques derive tests from:",
    "options": [
        "The internal structure: code, control flow, and system architecture",
        "External requirements and user stories defined by the product owner",
        "The tester's experience and intuition about likely failure modes",
        "Acceptance criteria agreed between the development team and stakeholders"
    ],
    "exp": "White-box techniques use the internal structure (statements, decisions, paths, architecture) as the basis for designing and measuring tests."
},
"ch4-19": {
    "q": "Statement coverage measures:",
    "options": [
        "The percentage of executable statements that have been executed",
        "The percentage of decision outcomes exercised by the test suite",
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
        "Exercising each decision as both true and false at least once",
        "Executing every executable statement at least once",
        "Covering every possible combination of condition values",
        "Testing all independent paths through the code under test"
    ],
    "exp": "Decision coverage requires each decision (e.g., if-statement) to evaluate to both true and false at least once."
},
"ch4-22": {
    "q": "For an 'if' statement without an 'else' branch, which coverage criterion ensures the false path is also tested?",
    "options": [
        "Decision coverage, because each decision must evaluate to both true and false",
        "Statement coverage, because all statements must be executed",
        "No standard coverage criterion requires testing the false path of an if without else",
        "Condition coverage, because each individual condition must be evaluated"
    ],
    "exp": "Without an else branch, 100% statement coverage can be achieved without testing the false path; decision coverage forces both true and false outcomes."
},
"ch4-23": {
    "q": "Which statement about the relative strength of coverage criteria is correct?",
    "options": [
        "100% decision coverage implies 100% statement coverage, but not vice versa",
        "Statement coverage is stronger than decision coverage",
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
        "Anticipating likely defects based on experience, past defects, and knowledge of failure modes",
        "Randomly selecting input values without any systematic approach or heuristic",
        "Generating test cases automatically using AI tools trained on historical defect data",
        "Measuring code coverage to identify gaps in the existing test suite"
    ],
    "exp": "Error guessing uses experience and knowledge of common failures to create tests likely to expose defects that formal techniques might miss."
},
"ch4-26": {
    "q": "In exploratory testing, the tester:",
    "options": [
        "Simultaneously learns about the system, designs tests, and executes them",
        "Follows pre-defined test scripts step by step without deviation",
        "Only measures performance metrics without evaluating functional behavior",
        "Documents all test cases in advance before executing any of them"
    ],
    "exp": "Exploratory testing combines learning, designing, and executing in real time, often guided by test charters and time-boxed sessions."
},
"ch4-27": {
    "q": "Checklist-based testing relies on:",
    "options": [
        "A list of items or conditions to verify, derived from experience and heuristics",
        "State diagrams showing all valid and invalid system transitions",
        "Code coverage metrics generated by automated instrumentation tools",
        "Decision tables enumerating all combinations of business rule conditions"
    ],
    "exp": "Checklists compile items to verify (heuristics, lessons learned), guiding testing without detailed scripts."
},
"ch4-28": {
    "q": "When are experience-based techniques most valuable?",
    "options": [
        "When documentation is scarce, time is short, or to complement formal techniques",
        "When a complete and stable specification is available for systematic technique application",
        "Only in safety-critical systems where formal techniques are mandatory by regulation",
        "Exclusively when automated testing tools are unavailable to the test team"
    ],
    "exp": "Experience-based techniques are valuable with limited documentation or tight timelines, and as complements to formal techniques to catch defects that escape them."
},
# CHAPTER 4 — BLOCK 2/2 (ch4-29 to ch4-55)

"ch4-29": {
    "q": "The '3 C's' of collaborative user story writing are:",
    "options": [
        "Card, Conversation, and Confirmation — the three elements of a well-formed user story",
        "Code, Compile, and Commit — the three steps of test-driven development",
        "Cost, Customer, and Contract — the three constraints of agile project management",
        "Create, Check, and Close — the three phases of the defect lifecycle"
    ],
    "exp": "The 3 C's: Card (brief summary), Conversation (detailed discussion), and Confirmation (acceptance criteria that define done)."
},
"ch4-30": {
    "q": "Acceptance criteria for a user story serve to:",
    "options": [
        "Define the conditions the story must satisfy to be considered complete and accepted",
        "Estimate the development effort required to implement the story in story points",
        "Measure the code coverage achieved by the automated tests for that story",
        "Replace the need for test cases by providing sufficient implementation guidance"
    ],
    "exp": "Acceptance criteria describe what makes a story 'done/accepted', providing the basis for deriving test cases."
},
"ch4-31": {
    "q": "In ATDD (Acceptance Test-Driven Development), acceptance tests are:",
    "options": [
        "Defined collaboratively before implementation, derived from acceptance criteria",
        "Written after delivery to validate that the implemented feature works correctly",
        "Only automated end-to-end UI tests executed by the continuous integration pipeline",
        "Optional artifacts that supplement but never replace traditional test planning"
    ],
    "exp": "In ATDD, the team (business, dev, test) collaboratively defines acceptance tests before coding, guiding implementation and confirming completion."
},
"ch4-32": {
    "q": "A requirement describes both value ranges and multi-field combination rules. The best test strategy is:",
    "options": [
        "Combine techniques: EP/BVA for the ranges and decision tables for the combinations",
        "Apply only BVA because it is the most comprehensive black-box technique available",
        "Apply only state transition testing because the system has multiple operational modes",
        "Use exploratory testing exclusively since the requirement is too complex for formal techniques"
    ],
    "exp": "Mixed problems need combined techniques: EP/BVA for ranges and decision tables for combined rules."
},
"ch4-33": {
    "q": "Coverage in test techniques measures:",
    "options": [
        "The degree to which defined coverage items have been exercised by the tests",
        "The total number of defects found by the test suite during execution",
        "The elapsed time taken to execute all test cases in the test suite",
        "The number of testers assigned to the project relative to its complexity"
    ],
    "exp": "Coverage expresses how much of the defined coverage items (partitions, decisions, transitions) the tests have exercised."
},
"ch4-34": {
    "q": "A temperature field accepts -10 to 50°C. Using 2-value BVA, what are the 4 boundary values to test?",
    "options": [
        "-11, -10, 50, 51",
        "-10 and 50",
        "-10, 0, 50, 100",
        "-9, -10, 49, 50"
    ],
    "exp": "2-value BVA tests the boundary value and the one immediately adjacent on the invalid side: -11/-10 (lower boundary) and 50/51 (upper boundary)."
},
"ch4-35": {
    "q": "A decision table has 3 binary conditions. How many rules does the complete table (without collapsing) have?",
    "options": [
        "3",
        "6",
        "8",
        "9"
    ],
    "exp": "Three binary conditions generate 2³ = 8 combinations (rules) in the complete decision table."
},
"ch4-36": {
    "q": "A discount system applies a discount if: (premium customer = Yes) OR (order value > $500). How many distinct rules exist with 2 binary conditions?",
    "options": [
        "4",
        "2",
        "6",
        "8"
    ],
    "exp": "Two binary conditions generate 2² = 4 rules; the complete table has 4 columns regardless of the logical operator."
},
"ch4-37": {
    "q": "In a bank account state machine: states = {Active, Blocked, Closed}. How many invalid transitions exist if only 4 valid transitions are defined?",
    "options": [
        "4",
        "5",
        "8",
        "6"
    ],
    "exp": "With 3 states, there are 3×3 = 9 cells in the matrix (including self-transitions); with 4 valid ones, there are 9-4 = 5 invalid transitions to check."
},
"ch4-38": {
    "q": "A code segment has 20 executable statements. A test suite executed 15. What is the statement coverage?",
    "options": [
        "75%",
        "15%",
        "85%",
        "20%"
    ],
    "exp": "Statement coverage = executed ÷ total = 15 ÷ 20 = 75%."
},
"ch4-39": {
    "q": "A method has 4 decisions (if/else). For 100% decision coverage, how many decision outcomes must be exercised at minimum?",
    "options": [
        "8",
        "4",
        "2",
        "16"
    ],
    "exp": "Each decision has 2 outcomes (T/F); 4 decisions × 2 outcomes = 8 minimum outcomes to exercise for 100% decision coverage."
},
"ch4-40": {
    "q": "A field accepts ages from 0 to 120 years (integers). Using 3-value BVA, which values should be tested at the lower boundary (0)?",
    "options": [
        "-1, 0, and 1",
        "0 and 1",
        "0, 1, and 2",
        "-2, -1, and 0"
    ],
    "exp": "3-value BVA tests the boundary and its two neighbors: for the lower boundary 0, the values -1, 0, and 1 are tested."
},
"ch4-41": {
    "q": "A form has a 'quantity' field that only accepts 1, 2, or 3. Using EP, which invalid partition exists above the limit?",
    "options": [
        "Values ≥ 4",
        "There is no upper invalid partition",
        "Values = 0",
        "Negative values"
    ],
    "exp": "The upper invalid partition includes all values ≥ 4 (above the maximum of 3); values ≤ 0 form the lower invalid partition."
},
"ch4-42": {
    "q": "In a state machine with full transition coverage (0-switch), which login scenario is most appropriate?",
    "options": [
        "Testing every possible transition at least once: successful login, wrong password, account lockout, logout",
        "Testing only the successful login scenario, ignoring the others",
        "Testing only the initial state of the login system, without considering transitions",
        "Testing only the invalid transitions between states, ignoring the valid ones"
    ],
    "exp": "0-switch coverage requires exercising each valid transition individually, covering every arc of the state diagram."
},
"ch4-43": {
    "q": "When testing a traffic light control system (Green → Yellow → Red → Green), which technique is most suitable?",
    "options": [
        "State transition testing, since behavior depends on the current state",
        "Equivalence partitioning of the traffic light colors",
        "Boundary value analysis of the timing of each phase",
        "Decision table combining the traffic light colors"
    ],
    "exp": "Traffic lights have well-defined states and sequential transitions — state transition testing models this behavior precisely."
},
"ch4-44": {
    "q": "Using EP to test a grade field from 0 to 10 (integers), a tester uses only the value 5. What is the problem with this approach?",
    "options": [
        "It only tests the valid partition; the invalid partitions (< 0 and > 10) are not covered",
        "The value 5 is correct; the approach is adequate",
        "EP requires testing all values from 0 to 10",
        "EP does not apply to integers"
    ],
    "exp": "EP requires at least one representative from each partition — valid and invalid; using only value 5 ignores the invalid partitions below 0 and above 10."
},
"ch4-45": {
    "q": "A program contains the snippet: if (x > 0) { y = x * 2; } z = y + 1; With only one test case where x=5, which coverage is achieved?",
    "options": [
        "100% of statements executed on the path, but not 100% of decisions (false branch not tested)",
        "100% statement coverage and also 100% decision coverage",
        "No statement or decision coverage is achieved",
        "100% decision coverage, but not statement coverage"
    ],
    "exp": "With x=5 (true condition), y=x*2 and z=y+1 are executed. The false branch (x≤0) is not tested, so decision coverage < 100%."
},
"ch4-46": {
    "q": "Error guessing is most effective when the tester:",
    "options": [
        "Has experience with the domain, knows past defects, and understands common implementation errors",
        "Has never seen the system before and doesn't know the domain",
        "Only uses formal techniques, with no intuition at all",
        "Doesn't know the code or the system's architecture"
    ],
    "exp": "The effectiveness of error guessing grows with the tester's experience: domain knowledge and defect history guide intuition."
},
"ch4-47": {
    "q": "Exploratory testing in time-boxed sessions (session-based testing) uses 'test charters' to:",
    "options": [
        "Define the mission of the session: scope, objective, and area to explore, without detailing each step",
        "Document in detail every step before execution",
        "Completely replace formal test planning",
        "Exclusively measure the code coverage achieved"
    ],
    "exp": "Charters define the focus of the exploratory session (what to explore and why) without pre-determining the exact execution steps."
},
"ch4-48": {
    "q": "When is a test checklist used instead of detailed test cases?",
    "options": [
        "When agility and the tester's experience are wanted to decide how to verify each item, without rigid scripts",
        "Only when there is a lot of time available in the test project schedule",
        "Only when the system is extremely critical and requires heavy documentation",
        "Only when full automation of the tests is not technically possible"
    ],
    "exp": "Checklists offer flexibility: the tester decides how to verify each item using their judgment — suitable when detailed scripts would be excessive."
},
"ch4-49": {
    "q": "In ATDD, who defines the acceptance criteria before implementation?",
    "options": [
        "Development team, business representatives, and testers, collaboratively",
        "Only the tester, with no one else involved",
        "Only the product owner, in isolation, without the team",
        "Exclusively the project manager, alone"
    ],
    "exp": "ATDD is collaborative: business, dev, and test together define the acceptance criteria/tests before implementing the feature."
},
"ch4-50": {
    "q": "Which black-box technique would be most suitable for testing loan eligibility rules that combine income, credit history, and length of employment?",
    "options": [
        "Decision table, since there are multiple combined conditions leading to different decisions",
        "Boundary value analysis of the income range only",
        "State transition testing of the approval process",
        "Statement coverage of the credit approval system"
    ],
    "exp": "When the result depends on combinations of multiple conditions (business rules), the decision table is the most suitable technique."
},
"ch4-51": {
    "q": "A field accepts values from $1.00 to $9,999.99. Using 2-value BVA, what are the test values for the lower boundary?",
    "options": [
        "$0.99 and $1.00",
        "$1.00 and $9,999.99",
        "$1.00 and $1.01",
        "$0.00 and $1.00"
    ],
    "exp": "At the lower boundary $1.00, 2-value BVA tests the value below the boundary ($0.99, invalid) and the boundary itself ($1.00, valid)."
},
"ch4-52": {
    "q": "In a state diagram, what does 'switch-1' coverage (transition pairs) guarantee beyond 0-switch coverage?",
    "options": [
        "That consecutive pairs of transitions (sequences of 2) are exercised, increasing the depth of coverage",
        "Nothing additional beyond what basic 0-switch coverage already guarantees alone",
        "Complete coverage of all isolated conditions, without considering combinations",
        "Complete coverage of all executable statements present in the code"
    ],
    "exp": "Switch-1 covers sequences of 2 transitions (pairs), detecting errors that only appear in combinations of transitions, and is stronger than 0-switch."
},
"ch4-53": {
    "q": "Combining EP and BVA is more effective than using each technique in isolation because:",
    "options": [
        "EP and BVA are technically equivalent and interchangeable",
        "BVA completely replaces the need for EP",
        "EP reduces the test space; BVA complements it by testing the points most prone to defects (boundaries)",
        "EP only tests valid values; BVA only tests invalid values"
    ],
    "exp": "EP defines the partitions, reducing the space; BVA digs deeper into the boundaries of those partitions, where defects are more frequent."
},
"ch4-54": {
    "q": "Why isn't 100% statement coverage sufficient as the sole quality criterion?",
    "options": [
        "Because it is practically impossible to achieve in practice",
        "Because it is very expensive and time-consuming to achieve",
        "Because it does not guarantee that all decision branches were tested, potentially leaving paths untested",
        "Because this metric is not accepted by the official syllabus"
    ],
    "exp": "100% statement coverage can be achieved without testing the false branch of an if without else; decision coverage is stronger and more revealing."
},
"ch4-55": {
    "q": "What is the main objective of experience-based testing?",
    "options": [
        "Completely replacing formal techniques in all cases",
        "Generating completely random test cases with no criteria",
        "Leveraging the tester's knowledge and intuition to find defects that formal techniques might miss",
        "Exclusively measuring the system's code coverage"
    ],
    "exp": "Experience-based techniques complement formal ones, exploring the tester's knowledge of common defects and unexpected behaviors."
},
# CHAPTER 5 — TEST MANAGEMENT (45 questions) — BLOCK 1/2 (ch5-01 to ch5-23)

"ch5-01": {
    "q": "What is the primary purpose of a test plan?",
    "options": [
        "To list every defect found during the testing phase of the project",
        "To replace test cases by providing sufficient guidance for ad hoc execution",
        "To document objectives, scope, approach, resources, schedule, and criteria for the test effort",
        "To formally approve the system for release to the production environment"
    ],
    "exp": "The test plan communicates objectives, scope, approach, resources, schedule, risks, and entry/exit criteria to all stakeholders."
},
"ch5-02": {
    "q": "What is the difference between a test strategy and a test approach?",
    "options": [
        "They are synonyms; both terms describe the same planning artifact",
        "A test approach is broader than a test strategy and supersedes it at the project level",
        "A test strategy is a general organizational description; a test approach is its adaptation to a specific project",
        "A test strategy applies only to agile projects; a test approach applies to waterfall projects"
    ],
    "exp": "The strategy describes the general organizational testing direction; the approach adapts the strategy to the context of a specific project."
},
"ch5-03": {
    "q": "Entry criteria define:",
    "options": [
        "The list of defects that must be resolved before testing can proceed",
        "The conditions under which a completed test activity can be declared finished",
        "The conditions that must be met before a test activity can begin",
        "The acceptance thresholds the final product must satisfy before user release"
    ],
    "exp": "Entry criteria are pre-conditions for starting a test activity, such as environment readiness, test cases approved, and test data available."
},
"ch5-04": {
    "q": "Exit criteria serve to:",
    "options": [
        "Authorize the commencement of the next test level or activity",
        "Specify the defects that are acceptable to leave open at product release",
        "Determine when a test activity or level can be considered sufficiently complete",
        "Define the skills required for testers assigned to the project"
    ],
    "exp": "Exit criteria define when to stop testing: coverage achieved, open defects below threshold, schedule met, or other agreed conditions."
},
"ch5-05": {
    "q": "In agile methods, the 'Definition of Done' (DoD) functions as:",
    "options": [
        "Entry criteria that must be satisfied before a sprint can begin",
        "A formal test plan that replaces the need for traditional test documentation",
        "A set of exit criteria defining when a work item is truly complete",
        "A defect report template used to track unresolved issues in the backlog"
    ],
    "exp": "The DoD is a set of exit criteria agreed by the team that defines when a work item (story, sprint, release) is genuinely complete."
},
"ch5-06": {
    "q": "The ratio-based estimation technique uses:",
    "options": [
        "Expert judgment from team members familiar with similar past projects",
        "Function point analysis to derive test effort from system complexity metrics",
        "Historical proportions (e.g., the ratio of test effort to development effort) to project the current estimate",
        "Monte Carlo simulation to generate probabilistic effort distributions"
    ],
    "exp": "Ratio-based estimation applies historical proportions from past projects (e.g., test effort = 30% of dev effort) to estimate the current project."
},
"ch5-07": {
    "q": "Metrics-based (extrapolation) estimation is based on:",
    "options": [
        "Pure intuition and guesswork, ignoring any objective measurement",
        "Only on the budget available for the current project",
        "Data/measurements from previous iterations or projects, extrapolated to the current one",
        "Exclusively on the number of testers available"
    ],
    "exp": "The metrics-based approach uses historical data to extrapolate the expected effort."
},
"ch5-08": {
    "q": "Expert-based estimation is characterized by:",
    "options": [
        "Ignoring past experience in favor of objective measurement and data analysis",
        "Using only mathematical formulas derived from project size metrics",
        "Relying on the judgment of those experienced with the tasks, e.g., Planning Poker or Wideband Delphi",
        "Delegating estimation entirely to project managers rather than testers"
    ],
    "exp": "Expert-based estimation leverages the knowledge of experienced practitioners, using consensus techniques like Planning Poker or Wideband Delphi."
},
"ch5-09": {
    "q": "In risk-based prioritization, tests are executed first for:",
    "options": [
        "The shortest test cases to maximize the number of tests completed early",
        "The oldest test cases that have not been executed in recent cycles",
        "The items with the highest risk level (highest probability × impact)",
        "The test cases chosen randomly to avoid systematic bias in selection"
    ],
    "exp": "Risk-based prioritization executes tests covering the highest-risk items first, ensuring maximum risk reduction early in the test cycle."
},
"ch5-10": {
    "q": "Coverage-based prioritization orders test cases by:",
    "options": [
        "The estimated execution time, starting with the fastest cases",
        "Alphabetical order of the test case identifiers in the test management tool",
        "The incremental coverage each test adds to what has not yet been covered",
        "The severity of the defects each test case has found in previous cycles"
    ],
    "exp": "Coverage-based prioritization orders tests to maximize new coverage as quickly as possible, executing cases that cover uncovered items first."
},
"ch5-11": {
    "q": "The test pyramid suggests that a well-structured test suite should have:",
    "options": [
        "More end-to-end UI tests than unit tests, to maximize business-visible coverage",
        "An equal number of tests at every level to ensure balanced coverage",
        "Many unit tests at the base and few slow, fragile UI/E2E tests at the top",
        "Only automated tests; manual tests have no place in a mature test pyramid"
    ],
    "exp": "The pyramid recommends many fast, cheap unit tests at the base and few slow, expensive UI/E2E tests at the top for optimal ROI."
},
"ch5-12": {
    "q": "The testing quadrants help to:",
    "options": [
        "Calculate the exact number of test cases required for a given system",
        "Determine the sequence in which test levels should be executed",
        "Classify test types by whether they support the team or critique the product, and by technology vs. business focus",
        "Select the appropriate test automation tool for each test level"
    ],
    "exp": "The quadrants organize tests (supporting team vs. critiquing product; technology-facing vs. business-facing) to ensure balanced test planning coverage."
},
"ch5-13": {
    "q": "In test management, 'risk' is defined as:",
    "options": [
        "A defect that has been found but not yet fixed by the development team",
        "A failed test case that blocks the continuation of the test cycle",
        "A potential future event with a negative consequence for the project or product",
        "A test case that has been excluded from the scope of the current test plan"
    ],
    "exp": "Risk is the possibility of a future event with negative consequences; it combines the probability of occurrence with the magnitude of impact."
},
"ch5-14": {
    "q": "How is the risk level determined?",
    "options": [
        "Cost of fixing the defect multiplied by the remaining project timeline",
        "The severity rating multiplied by the priority assigned in the defect tracker",
        "The likelihood of occurrence combined with the impact of the potential harm",
        "The number of test cases that cover the area divided by total test cases"
    ],
    "exp": "Risk level = probability of occurrence × impact (magnitude of harm). This combination guides test prioritization."
},
"ch5-15": {
    "q": "What is the difference between product risk and project risk?",
    "options": [
        "They are the same; both refer to risks that affect software quality",
        "Project risk is always technical; product risk is always business-related",
        "Product risk affects the quality of the product; project risk affects achieving project objectives",
        "Product risk only applies to customer-facing features; project risk applies to internal processes"
    ],
    "exp": "Product risk affects the quality/fitness of the product; project risk (schedule, budget, resources, suppliers) affects the ability to achieve project goals."
},
"ch5-16": {
    "q": "Which of the following is an example of a PROJECT risk?",
    "options": [
        "An incorrect financial calculation in the billing module",
        "A security vulnerability in the authentication component",
        "Key test personnel leaving the project mid-cycle, causing schedule delays",
        "Poor performance of the search feature under concurrent user load"
    ],
    "exp": "Loss of key personnel causing delays is a project risk (affects project execution); the others are product risks (affect product quality)."
},
"ch5-17": {
    "q": "Which of the following is an example of a PRODUCT risk?",
    "options": [
        "The test environment not being available on the planned start date",
        "The project budget being exceeded due to unplanned scope additions",
        "A data breach caused by a security defect in the user authentication module",
        "A third-party supplier delivering a component later than contractually agreed"
    ],
    "exp": "A security defect causing a data breach directly affects product quality and user safety — a product risk. The others are project risks."
},
"ch5-18": {
    "q": "Risk-based testing uses the risk assessment to:",
    "options": [
        "Eliminate all identified risks before testing begins",
        "Determine the salary budget for the testing team",
        "Decide what to test, how much to test, and in what order, allocating effort proportional to risk",
        "Choose the programming language used to develop the system under test"
    ],
    "exp": "Risk-based testing uses risk levels to prioritize what to test first, how deeply to test, and where to concentrate the most experienced testers."
},
"ch5-19": {
    "q": "Risk assessment comprises:",
    "options": [
        "Only fixing the defects found during the risk identification workshop",
        "Executing test cases to verify that identified risks have been mitigated",
        "Identifying risks and analyzing them by estimating their probability and impact",
        "Approving the test plan after all risks have been reviewed by management"
    ],
    "exp": "Risk assessment includes risk identification followed by risk analysis (estimating probability and impact) to determine risk levels for prioritization."
},
"ch5-20": {
    "q": "How does risk level influence the depth of testing applied?",
    "options": [
        "Higher risk items receive less testing to preserve budget for lower-risk areas",
        "Risk level has no influence on test depth; all items are tested equally",
        "Higher risk items receive more rigorous testing, earlier execution, and more experienced testers",
        "Only items with risk level 'critical' are tested; lower-risk items are excluded"
    ],
    "exp": "Items with higher risk receive more thorough techniques, earlier testing, and more experienced testers to maximize risk reduction."
},
"ch5-21": {
    "q": "The purpose of test monitoring is:",
    "options": [
        "To write test cases that will be executed in the next test cycle",
        "To fix defects found during the execution phase of testing",
        "To provide visibility of progress by comparing actual results against the test plan",
        "To select the test tools that will be used throughout the project"
    ],
    "exp": "Monitoring collects information about test progress to compare against the plan and support informed control decisions."
},
"ch5-22": {
    "q": "Which of the following is a typical test metric?",
    "options": [
        "The color theme selected for the test management tool dashboard",
        "The team's preferred programming language for test automation",
        "The percentage of test cases executed and the pass/fail ratio",
        "The number of meetings held during the test planning phase"
    ],
    "exp": "Common metrics include: test cases planned/executed/passed/failed, defect density, coverage achieved, and defect trend over time."
},
"ch5-23": {
    "q": "A test progress report is primarily intended to:",
    "options": [
        "Replace the test plan when the project scope changes significantly",
        "Document the final quality assessment at the end of the project",
        "Inform stakeholders about test status and support decisions during the test effort",
        "List all requirements that have not yet been covered by any test case"
    ],
    "exp": "Progress reports communicate current status, risks, and results to stakeholders to support ongoing decisions during the test cycle."
},
# CHAPTER 5 — BLOCK 2/2 (ch5-24 to ch5-45)

"ch5-24": {
    "q": "A test completion report is produced:",
    "options": [
        "Before testing begins to communicate the planned approach to stakeholders",
        "Daily during test execution to track the number of defects found each day",
        "At the end of a test level or milestone, summarizing results and lessons learned",
        "Immediately after each individual test case is executed and evaluated"
    ],
    "exp": "The completion report summarizes results, coverage achieved, quality assessment, and lessons learned at the end of a test level or major milestone."
},
"ch5-25": {
    "q": "Configuration management supports testing by:",
    "options": [
        "Automatically generating test cases from configuration files",
        "Replacing the test plan with version-controlled configuration documents",
        "Ensuring consistent identification and versioning of test items and testware with full traceability",
        "Eliminating the need for defect reports by tracking changes to the codebase"
    ],
    "exp": "Configuration management maintains integrity and traceability of items under test and testware (versions, baselines) throughout the project."
},
"ch5-26": {
    "q": "What should a good defect report contain?",
    "options": [
        "Only the title and severity rating to keep reporting lightweight and efficient",
        "Only the name of the developer responsible for the defective code",
        "Identifier, description, steps to reproduce, expected vs actual result, severity, and priority",
        "A list of all test cases executed in the same session as the defect was found"
    ],
    "exp": "Effective defect reports include: ID, description, reproduction steps, expected vs. actual result, environment, severity, and priority."
},
"ch5-27": {
    "q": "What is the difference between defect severity and priority?",
    "options": [
        "They are the same; both measure how urgently a defect must be fixed",
        "Priority is determined by the development team; severity is determined by the business owner",
        "Severity measures the technical impact on the system; priority measures the urgency of fixing from a business perspective",
        "Severity only applies to critical defects; priority applies to all defect types"
    ],
    "exp": "Severity = technical impact on the system; priority = business urgency to fix. They can be independent: a cosmetic defect on the homepage may have low severity but high priority."
},
"ch5-28": {
    "q": "A risk has a 30% probability of occurrence and an impact rated 4 (scale 1-5). What is the risk level?",
    "options": [
        "0.3",
        "4.3",
        "1.2",
        "7"
    ],
    "exp": "Risk level = probability × impact = 0.30 × 4 = 1.2 (on the numeric scale)."
},
"ch5-29": {
    "q": "Two risks: Risk A (20% probability, impact 5) and Risk B (50% probability, impact 2). Which should be prioritized?",
    "options": [
        "Risk A, level 1.0 < Risk B 1.0 — tie; prioritize whichever is cheaper to mitigate",
        "Risk B due to higher probability",
        "Risk A (level 1.0) and Risk B (level 1.0) have the same level; other factors decide",
        "Risk A due to higher impact"
    ],
    "exp": "Level A = 0.20×5 = 1.0; Level B = 0.50×2 = 1.0 — tie in risk level; secondary criteria (mitigation cost, visibility) decide."
},
"ch5-30": {
    "q": "The 'Planning Poker' test estimation technique is a variant of:",
    "options": [
        "A variant of ratio-based historical estimation",
        "A variant of metrics-based extrapolation estimation",
        "Expert-based estimation (Wideband Delphi), using team consensus",
        "A formal function point analysis technique"
    ],
    "exp": "Planning Poker is a variation of Wideband Delphi: each member votes secretly and the team discusses until convergence, leveraging collective expertise."
},
"ch5-31": {
    "q": "A ratio-based test effort estimate uses the historical proportion that testing consumes 30% of total effort. If development is estimated at 1000h, the estimated test effort is:",
    "options": [
        "300h",
        "700h",
        "30h",
        "1300h"
    ],
    "exp": "30% ratio: test effort = 30% × 1000h = 300h."
},
"ch5-32": {
    "q": "The test pyramid places contract/API tests at the intermediate level because they:",
    "options": [
        "Are always slower than full UI tests",
        "Only visually check the system's graphical interface",
        "Are faster and more stable than E2E/UI tests, but validate more integration than unit tests",
        "Are completely equivalent to unit tests"
    ],
    "exp": "API/integration tests are intermediate: faster and less brittle than E2E, but with broader scope than unit tests."
},
"ch5-33": {
    "q": "Testing quadrant Q1 (team-supporting, technology-facing) mainly includes:",
    "options": [
        "Usability testing and manual exploratory testing",
        "Acceptance testing carried out by the end user",
        "Automated unit and component tests that guide development",
        "Load and performance testing of the system"
    ],
    "exp": "Q1 (technology-facing, team-support): automated unit and component tests that support development (TDD)."
},
"ch5-34": {
    "q": "Testing quadrant Q4 (product-critiquing, technology-facing) includes:",
    "options": [
        "Acceptance testing carried out directly by the user",
        "Automated unit tests for each component",
        "Performance, security, reliability, and other non-functional quality attribute testing",
        "Exploratory testing focused on business rules"
    ],
    "exp": "Q4 (technology-facing, product-critique): non-functional tests such as performance, security, and reliability, usually automated."
},
"ch5-35": {
    "q": "What is the difference between severity and priority of a defect in a practical scenario?",
    "options": [
        "Severity and priority are always exactly equal",
        "High severity always automatically implies high priority",
        "A cosmetic bug (low severity) can have high priority if it's on the marketing page of an upcoming launch",
        "Priority is always defined by the tester; severity, by the end customer"
    ],
    "exp": "Severity and priority are independent: a cosmetic bug can be urgent (high priority) for business reasons, even with low technical impact."
},
"ch5-36": {
    "q": "In configuration management, a 'baseline' is:",
    "options": [
        "A common error in the version control system",
        "The production environment where the system runs",
        "An approved and fixed version of one or more configuration items, used as a reference",
        "The test plan already approved by stakeholders"
    ],
    "exp": "A baseline is a stable, formally approved reference of configuration items, used to control subsequent changes."
},
"ch5-37": {
    "q": "Which of the following is a useful test progress metric for daily monitoring?",
    "options": [
        "Lines of code per developer",
        "Meeting hours per week",
        "Percentage of test cases executed and pass/fail rate",
        "Number of features requested"
    ],
    "exp": "Execution metrics (% executed, passed, failed) provide direct visibility of actual progress versus what was planned."
},
"ch5-38": {
    "q": "A quality defect report should avoid:",
    "options": [
        "Including detailed steps to reproduce the defect",
        "Correctly recording the severity of the defect found",
        "Subjective language, personal blame, or a vague title like 'system doesn't work'",
        "Clearly mentioning the environment where the test occurred"
    ],
    "exp": "Good reports are objective, descriptive, and factual; accusatory language and vague titles hinder efficient triage and correction."
},
"ch5-39": {
    "q": "What is the purpose of the test completion report?",
    "options": [
        "Listing only the defects that are still open",
        "Completely replacing the test plan for the next cycle",
        "Summarizing the test cycle results, communicating the quality achieved, and recording lessons learned",
        "Formally approving the final product's release"
    ],
    "exp": "The completion report consolidates results, coverage, defects, deviations from the plan, and lessons, serving as a reference for future cycles."
},
"ch5-40": {
    "q": "Risk-based testing affects planning by:",
    "options": [
        "Completely ignoring low-risk features",
        "Completely eliminating regression tests from the plan",
        "Allocating more effort, depth, and anticipation to the items of highest product risk",
        "Always reducing the total number of planned test cases"
    ],
    "exp": "Risk guides where to invest more (more rigorous techniques, earlier start) and allows reducing effort in low-risk areas."
},
"ch5-41": {
    "q": "When exit criteria are not met but the deadline has arrived, what is the most appropriate action?",
    "options": [
        "Ignore the defined criteria and end testing anyway",
        "Continue testing indefinitely, with no stopping criteria at all",
        "Report the status, the residual risks, and leave the decision to stop or continue to the stakeholders",
        "Formally fail the system without consulting anyone"
    ],
    "exp": "The test manager reports residual risks and status; the decision to stop or not is a business decision, made by stakeholders with full information."
},
"ch5-42": {
    "q": "Which prioritization technique is most suitable when time is very short and it's necessary to ensure the most critical items are tested first?",
    "options": [
        "Completely random prioritization of test cases",
        "Simple prioritization by alphabetical order of the module name",
        "Risk-based prioritization: test the highest risk level items first",
        "Testing only the shortest and fastest cases first"
    ],
    "exp": "With limited time, risk-based prioritization ensures the available effort covers what would cause the greatest impact if it failed."
},
"ch5-43": {
    "q": "'Impact analysis' in maintenance testing serves to:",
    "options": [
        "Exclusively estimate the total project cost",
        "Directly select the automation tool used",
        "Identify which parts of the system and which tests are affected by a change",
        "Plan the training needed for the team"
    ],
    "exp": "Impact analysis determines the scope of regression: which areas were affected by the change and which tests should be executed."
},
"ch5-44": {
    "q": "In agile projects, 'Definition of Ready' (DoR) for a user story means that:",
    "options": [
        "The story has already been fully implemented, tested, and is ready for delivery to the customer",
        "All automated and manual tests for the story have already been written and successfully executed",
        "The story meets the minimum criteria to enter the sprint (acceptance criteria defined, estimated, no blocking dependencies)",
        "The story's complete code has already been formally reviewed and approved by technical peers"
    ],
    "exp": "DoR defines when a story is sufficiently prepared to be worked on in the sprint, including clear acceptance criteria for testing."
},
"ch5-45": {
    "q": "In configuration management, what is a 'configuration item'?",
    "options": [
        "Only an individual test case stored separately in the test repository",
        "Only a defect report manually logged in the tracking system",
        "Only a single line of source code present in the compiled program",
        "Any artifact (component, document, environment) identified and managed as a unit in the configuration control system"
    ],
    "exp": "Configuration items are uniquely identified artifacts managed under configuration control: code, documents, environments, tools."
},
# CHAPTER 6 — TEST TOOLS (10 questions) — FINAL BLOCK

"ch6-01": {
    "q": "Test tools can support:",
    "options": [
        "Only test execution and result logging activities",
        "Multiple activities: management, static analysis, design, execution, performance, and more",
        "Exclusively automated UI testing and visual regression checks",
        "Only the generation of final test completion reports"
    ],
    "exp": "Tool categories exist for test management, static analysis, test design, execution, test data, performance testing, and monitoring."
},
"ch6-02": {
    "q": "Test automation typically provides the greatest return on investment for:",
    "options": [
        "One-off exploratory testing sessions on new, unstable features",
        "Repetitive, extensive regression testing executed across many cycles",
        "Usability evaluation requiring subjective human judgment",
        "Initial requirements review and static analysis of specifications"
    ],
    "exp": "Repetitive regression testing is the classic case for strong ROI: stable tests executed many times benefit most from automation."
},
"ch6-03": {
    "q": "What is a genuine risk when adopting test automation tools?",
    "options": [
        "Automation always reduces costs immediately upon implementation",
        "Underestimating the implementation effort and, especially, the ongoing maintenance cost of scripts",
        "Automation completely eliminates the need for any manual testing",
        "Automated tests always achieve higher coverage than manual tests"
    ],
    "exp": "Risks include unrealistic expectations, script maintenance costs, tool dependency, and brittle scripts that break with minor UI changes."
},
"ch6-04": {
    "q": "A general benefit of test tools is:",
    "options": [
        "Guaranteeing the complete absence of defects in the tested system",
        "Reducing repetitive manual work and increasing consistency and repeatability",
        "Completely replacing human judgment in all testing decisions",
        "Eliminating the need for test planning and risk assessment activities"
    ],
    "exp": "Tools reduce repetitive manual tasks, increase consistency and repeatability, and provide access to information such as coverage metrics."
},
"ch6-05": {
    "q": "When selecting a test tool, the organization should primarily consider:",
    "options": [
        "Only the purchase price compared to competing vendor offerings",
        "Organizational maturity, fit with context/process, and evaluation through a proof of concept",
        "The popularity of the tool on social media and developer forums",
        "Exclusively the visual appearance and user interface design of the tool"
    ],
    "exp": "Tool selection evaluates context, maturity, constraints, integration needs, and typically includes an evaluation or proof of concept (PoC) before full adoption."
},
"ch6-06": {
    "q": "Before broadly deploying a new tool across the organization, it is recommended to:",
    "options": [
        "Purchase enterprise licenses for the entire company immediately to lock in pricing",
        "Conduct a pilot project to evaluate fit, define usage guidelines, and measure benefits",
        "Train all staff on the tool after the full rollout has already been completed",
        "Skip evaluation entirely since most modern tools work well out of the box"
    ],
    "exp": "A pilot project allows evaluation of organizational fit, defines usage guidelines, and estimates costs/benefits before scaling to full adoption."
},
"ch6-07": {
    "q": "A project wants to automate API regression tests. Which tool category is most suitable?",
    "options": [
        "A requirements management and tracking tool",
        "An API test execution tool (e.g., a REST client with automated assertions)",
        "A static source code analysis tool",
        "A tool to support manual code review"
    ],
    "exp": "API testing tools (such as REST frameworks with assertions) are the appropriate category for automating service regression."
},
"ch6-08": {
    "q": "The ROI (return on investment) of test automation tends to be higher when:",
    "options": [
        "The automated tests are run very few times throughout the project",
        "The tests are stable, run frequently, and the maintenance cost is lower than that of repeated manual execution",
        "The system changes completely every sprint, with no backward compatibility at all",
        "The responsible team doesn't yet know the chosen tool well"
    ],
    "exp": "Positive ROI occurs when stable, frequent tests amortize the initial automation cost and maintenance cost over time."
},
"ch6-09": {
    "q": "What is the risk of 'brittle scripts' in UI test automation?",
    "options": [
        "The automation scripts run very fast",
        "Small interface changes break the scripts, generating high maintenance cost",
        "The automated scripts cover many test scenarios",
        "The automation starts detecting many more defects"
    ],
    "exp": "UI scripts that depend on brittle selectors (coordinates, literal text) break with any layout change, increasing maintenance."
},
"ch6-10": {
    "q": "Which factor is MOST important when evaluating whether to introduce a new tool into an existing test process?",
    "options": [
        "Whether the tool vendor offers the lowest price in the current market",
        "Whether the tool integrates well with existing tools, processes, and team skills",
        "Whether the tool has the largest number of features compared to competitors",
        "Whether the tool was recently released, ensuring access to the latest technology"
    ],
    "exp": "Successful tool adoption depends heavily on integration with the existing toolchain, process compatibility, and the team's ability to use it effectively."
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
