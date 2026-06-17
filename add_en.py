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
