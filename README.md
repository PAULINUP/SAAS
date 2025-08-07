# Q-Core AI System – Plataforma SaaS + API para Análise e Simulação Preditiva Multidocumental

## Visão Geral

Sistema corporativo híbrido, pronto para ingestão massiva de documentos, parsing inteligente, análise preditiva com força bruta de cálculo (CPU/GPU/quântico), resposta explicável e integração via API REST ou interface web.

- **Arquitetura modular**: Backend desacoplado, frontend MVP, núcleo preditivo flexível.
- **Pronto para produção**: Segurança, auditoria, escalabilidade, cloud-ready.
- **Documentação técnica completa em /docs**.

## Funcionalidades

- ✅ Predição com intervalo de confiança e variáveis explicativas
- ✅ Simulação de cenários "what-if"
- ✅ Análise simbólica-quântica (SANQ)
- ✅ Visualização gráfica dos impactos
- ✅ Feedback do usuário para correção contínua
- ✅ Geração automática de relatórios PDF
- ✅ API REST com FastAPI
- ✅ Interface web com Streamlit

## Estrutura do Projeto

Veja detalhes em `/docs/modelo_arquitetural_saas_api_qcore_ai.md`.

```bash
qcore_system/
├── app/                     # Núcleo da API FastAPI
├── web/                     # Interface Streamlit
├── qcore_intelligent_engine.py
├── feedback_module.py
├── explanation_view.py
├── quantum_bridge.py
├── api_gateway.py
├── presentation_mode.py
├── demo_runner.py
├── Dockerfile
├── setup.py
├── README.md
```

## Primeiros Passos

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Rode o backend:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

3. Rode o frontend MVP:
   ```bash
   streamlit run web/streamlit_app.py
   ```

4. Documentação interativa:
   ```
   http://localhost:8000/docs
   ```

## Diretórios

- `app/`: Backend FastAPI, núcleo Q-Core AI, ingestão, parsing, curadoria e simulação.
- `web/`: Interface MVP (Streamlit).
- `tests/`: Testes automatizados.
- `docs/`: Documentação técnica e de arquitetura.
- Raiz: Módulos principais do core e scripts utilitários (ex: demo, gateway, relatórios)

---

## Execução com Docker

```bash
docker build -t qcore-ai .
docker run -p 8000:8000 qcore-ai
```

---

## Instalação como pacote Python

```bash
pip install .
```

---

## Autor
Paulo Geovane da Silva Souza  
[paulobravo_23@hotmail.com](mailto:paulobravo_23@hotmail.com)

---

## Licença
MIT — Livre para uso, melhoria e distribuição.

---

> Q-Core: IA de verdade, explicável, simbiótica e poderosa. Não é mais uma promessa — é real.
