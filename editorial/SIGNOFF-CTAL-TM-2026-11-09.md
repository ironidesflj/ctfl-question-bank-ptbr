# Sign-off editorial — CTAL-TM 1.7.2

- **Data:** 2026-11-09
- **Escopo:** pool de estudo do CTAL-TM (101 questões publicadas no hub via Axon).
- **Revisão aplicada:** 16 itens do relatório `REVISAO-CTAL-TM` (6 P1: 121, 151, 155, 173, 183, 189; 6 P2: 02, 65, 66, 124, 168, 182; 2 P3: 125, 185), já presentes no banco desde 1.7.1; referências passaram a incluir o LO (`TM-x.y.z`).
- **Gabaritos:** nenhum alterado (0 answers modificados; conferido por diff).
- **Evidência:** guardas de alinhamento passam para os certs live (CTFL, CTAL-TA, CTAL-TM); manifesto público inalterado (SHA `1bdcde8e…`, igual ao do hub); app sincronizado (fatias de estudo/exame) no PR #31 do ctfl-app.
- **Aprovação:** mantenedor aprovou a aplicação em 2026-11-09.
- **Pendências registradas:** (a) cobertura K4 do estudo — aguarda novo pacote de questões; (b) revisão semântica integral das 101 não foi feita (amostra de 14 + guardas); (c) guards de certs não-live (CT-AI, CTFL-AT) são LATENT — não bloqueiam CI por desenho (`check_alignment.py`, LIVE_CERTS).
