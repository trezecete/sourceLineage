# 📝 Release Notes - IPNET BigQuery Lineage Explorer

## [1.0.0] - 2026-03-26

### 🚀 Lançamento Inicial
Esta é a primeira versão estável da ferramenta de engenharia reversa de linhagem de dados.

### ✨ Novas Funcionalidades
- **Parser SQL Inteligente**: Suporte completo para extração de linhagem de comandos `CREATE`, `INSERT`, `MERGE` e `UPDATE` dentro do BigQuery.
- **Visualização Mermaid**: Grafo dinâmico com auto-layout focado em fluxos de dados.
- **Identidade Visual IPNET**: Interface customizada com as cores roxo e lima, tipografia Exo e ícones modernos.
- **Relacionamento de Colunas**: Exibição automática das colunas de ligação extraídas de cláusulas `ON` e `USING`.
- **Filtro de Investigação**: Capacidade de buscar por tabelas específicas e isolar seus fluxos de dependência.
- **Segurança**: Processamento de credenciais via upload de arquivo JSON de Service Account.

### 🛠️ Melhorias Técnicas
- Implementação de algoritmo BFS para descoberta de linhagem bi-direcional (Upstream/Downstream).
- Tratamento de erros de sintaxe Mermaid para garantir que o grafo sempre tente renderizar mesmo com nomes de tabelas complexos.
- Backend modular seguindo princípios de separação de responsabilidades.

### 📦 Dependências Principais
- `fastapi` & `uvicorn` (Core API)
- `sqlglot` (SQL Analysis)
- `google-cloud-bigquery-datatransfer` (BQ Meta-data)
- `mermaid.js` v10 (Graph Rendering)

---
**IPNET Cloud Solutions** | *Inovação em Dados e Nuvem.*
