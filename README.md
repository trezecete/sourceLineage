# 🌌 IPNET | BigQuery Data Lineage Explorer

> **Transforme o caos do seu Data Warehouse em uma árvore genealógica clara e visual.**

O **BigQuery Data Lineage Explorer** é uma ferramenta de engenharia reversa projetada para arquitetos de dados e engenheiros que precisam mapear a origem e o destino das informações dentro do Google BigQuery. Utilizando a identidade visual da **IPNET Cloud**, a ferramenta foca em transparência, inteligência e facilidade de uso.

---

## 🎯 Por que usar esta ferramenta?

Em ambientes de dados complexos, as **Scheduled Queries** (Consultas Agendadas) muitas vezes se tornam uma "caixa preta". Esta ferramenta abre essa caixa, analisando o SQL de cada consulta agendada para construir um grafo de dependências que mostra exatamente de onde os dados vêm e para onde vão.

### Diferenciais da v1.0
- **Branding IPNET**: Design moderno focado na experiência do usuário.
- **Linhagem Bi-direcional**: Veja quem alimenta uma tabela (**Upstream**) e quem ela alimenta (**Downstream**).
- **Mapeamento de Colunas**: Saiba quais colunas (`JOINs` e `MERGEs`) estão sendo usadas para relacionar as tabelas.

---

## 🛠️ O que tem "por baixo do capô"?

- **Backend**: Python 3.10+ com **FastAPI** para alta performance.
- **Motor de Parsing**: **sqlglot** (um dos parsers SQL mais avançados do mercado) para decompor dialetos nativos do BigQuery.
- **Visualização**: **Mermaid.js** para renderização de grafos dinâmicos diretamente no navegador.
- **Nuvem**: Integração nativa com a **Google BigQuery Data Transfer API**.

---

## 🚀 Guia Passo a Passo para Uso (Didático)

### 1. Preparação das Credenciais
Para que a ferramenta funcione, ela precisa de permissão para "ler" as configurações do seu BigQuery.
1. Vá ao Console do Google Cloud ➔ IAM & Admin ➔ Service Accounts.
2. Crie uma Service Account com as funções:
   - `BigQuery Data Viewer`
   - `BigQuery Data Transfer Service Viewer`
3. Gere uma chave em formato **JSON** e baixe-a.

### 2. Instalação Local
Se você recebeu este código agora, siga estes comandos no seu terminal:

```bash
# 1. Crie um ambiente isolado (para não bagunçar seu PC)
python -m venv venv

# 2. Ative o ambiente
# No Windows:
.\venv\Scripts\activate
# No Mac/Linux:
source venv/bin/activate

# 3. Instale os componentes necessários
pip install -r backend/requirements.txt
```

### 3. Iniciando a Aplicação
```bash
python backend/main.py
```
Agora, abra seu navegador em: **[http://localhost:8000](http://localhost:8000)**

---

## 💡 Como Investigar uma Tabela

1. **Upload**: Clique no botão de upload e selecione o arquivo `.json` que você baixou do Google Cloud.
2. **Localização**: Escolha a região onde suas consultas agendadas estão (ex: `us` ou `southamerica-east1`).
3. **Ponto de Partida**: No campo de busca, digite o caminho da tabela. Você pode usar o formato completo `projeto.dataset.tabela` ou apenas parte do nome.
4. **Gerar**: Clique em "VISUALIZAR LINHAGEM". O sistema filtrará todo o seu ambiente para mostrar apenas o que está conectado a essa tabela específica.

---

## 📂 Estrutura do Projeto
- `/backend`: Contém a inteligência de parsing (`lineage_parser.py`) e os serviços de conexão com a Google API (`bigquery_service.py`).
- `/frontend`: Contém a interface visual única em `index.html`.
- `venv/`: (Oculto) Onde as bibliotecas Python ficam instaladas.

---
**Desenvolvido com 💜 para IPNET Cloud Solutions.**
