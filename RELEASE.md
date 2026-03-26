# 📦 Notas de Release - IPNET Lineage Explorer

## [2.2.0] - 2026-03-26

### ✨ Novidades
- **Rebranding Completo**: Interface 100% alinhada com a identidade visual da IPNET Cloud (Roxo, Lima e fonte Exo).
- **Busca Unificada**: Implementada lógica de busca que aceita `projeto.dataset.tabela` em um único campo.
- **Relacionamento de Colunas**: Agora o sistema extrai e exibe nomes de colunas envolvidas em `JOINs` e `MERGEs` diretamente no grafo.

### 🛠️ Melhorias
- **Sintaxe Mermaid**: Corrigido bug de renderização que causava erro `Uncaught (in promise)` em tabelas com caracteres especiais.
- **Contraste de Cores**: Ajustado tema do gráfico para garantir legibilidade máxima (Textos Escuros sobre Nodes Claros).
- **Performance de Filtro**: Otimizada a busca bi-direcional no backend para grandes volumes de consultas agendadas.

### 🚀 Deploy
- Adicionado suporte a upload de arquivo JSON para autenticação simplificada.
- Adicionado arquivo `.gitignore` para segurança de credenciais.
- Configuração de ambiente virtual (`venv`) documentada.

---
*Versão Estável para uso em Engenharia de Dados.*
