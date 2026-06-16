# Banco de Questões — CTFL v4.0 (PT-BR)

Banco de questões para preparação ao exame **ISTQB Certified Tester Foundation Level (CTFL) v4.0**.

- **120 questões** em português, distribuídas na mesma proporção do exame oficial.
- Schema **pronto para internacionalização** (i18n): adicionar inglês = incluir `locales.en` em cada registro, sem tocar na estrutura.
- Gerado e validado pelo script `build_bank.py` (distribuição, níveis K e índices de resposta conferidos automaticamente).

## Formato do exame (referência)

| Item | Valor |
|------|-------|
| Questões | 40 |
| Nota de corte | 26/40 (65%) |
| Tempo | 60 min (75 min para não-nativos) |

## Distribuição (proporcional ao exame oficial)

| Cap. | Domínio | Questões |
|------|---------|----------|
| 1 | Fundamentos do Teste | 24 |
| 2 | Teste ao Longo do Ciclo | 15 |
| 3 | Teste Estático | 15 |
| 4 | Técnicas de Teste | 33 |
| 5 | Gerenciamento das Atividades de Teste | 27 |
| 6 | Ferramentas de Apoio ao Teste | 6 |
| | **Total** | **120** |

Níveis cognitivos: K1 = 28, K2 = 84, K3 = 8 (mesma quantidade de K3 do exame real).

## Schema

```jsonc
{
  "meta": {
    "title": "Banco de Questões CTFL v4.0",
    "syllabus": "ISTQB Certified Tester Foundation Level v4.0",
    "version": "1.0.0",
    "defaultLanguage": "pt",
    "availableLanguages": ["pt"],
    "examFormat": { "questions": 40, "passMark": 26, "timeMinutes": 60, "timeMinutesNonNative": 75 },
    "chapterWeights": { "1": 24, "2": 15, "3": 15, "4": 33, "5": 27, "6": 6 },
    "total": 120
  },
  "questions": [
    {
      "id": "ch1-01",          // estável, único, não traduzível
      "chapter": 1,             // 1..6
      "domain": "fund",         // fund | proc | est | tec | mgmt | fer
      "kLevel": 1,              // 1 | 2 | 3
      "answer": 1,              // índice (0-based) da opção correta — igual em todos os idiomas
      "locales": {
        "pt": {
          "q": "enunciado...",
          "options": ["A", "B", "C", "D"],
          "exp": "explicação da resposta correta"
        }
        // "en": { ... }  <- adicionar aqui no futuro
      }
    }
  ]
}
```

### Por que esse formato

Os campos que **não mudam entre idiomas** (`id`, `chapter`, `domain`, `kLevel`, `answer`) ficam no topo.
O texto traduzível fica isolado em `locales.{lang}`. Assim, o inglês entra sem risco de desalinhar a resposta
correta, e o app pode trocar de idioma só lendo `locales[idiomaSelecionado]`.

> **Importante:** a ordem das opções deve ser idêntica entre idiomas, pois `answer` é um índice compartilhado.
> O embaralhamento de alternativas é responsabilidade do app, em tempo de execução.

## Como consumir no app

```js
import bank from "./ctfl-questions-ptbr.json";

const lang = "pt";
const q = bank.questions[0];
const { q: enunciado, options, exp } = q.locales[lang];
const correta = options[q.answer];

// filtrar por domínio
const tecnicas = bank.questions.filter(x => x.domain === "tec");

// simulado: amostra proporcional aos pesos do exame
```

## Regenerar / estender

```bash
python3 build_bank.py
```

O script valida automaticamente: contagem por capítulo vs. alvo, faixa do `kLevel`,
índice de `answer` dentro das opções e ausência de opções duplicadas. Para adicionar questões,
inclua novas chamadas `add(capitulo, kLevel, enunciado, [opcoes], indice, explicacao)` no bloco do capítulo.

## Roadmap

- [x] 120 questões PT-BR (3 simulados)
- [ ] Tradução EN (`locales.en`)
- [ ] Integração ao app (modo Estudo / Simulado já existentes)
- [ ] Persistência local + export/import JSON
- [ ] Deploy (PWA)

## Aviso

Material de estudo independente, **não afiliado ao ISTQB**. Baseado na estrutura pública do syllabus CTFL v4.0.
"Certified Tester Foundation Level" e "ISTQB" são marcas de seus respectivos detentores.
