# 🌌 BigQuery Data Lineage Explorer

> **Visualize table dependencies and data flows within your Google BigQuery environment.**

The **BigQuery Data Lineage Explorer** is a reverse engineering tool designed for data architects and engineers who need to map the origin and destination of information. It specifically analyzes **Scheduled Queries** to build a comprehensive dependency graph.

---

## 🎯 Objective

In complex data environments, Scheduled Queries often become decoupled from their documentation. This tool bridges that gap by parsing the SQL of each scheduled query to construct a bi-directional lineage graph, showing exactly where your data comes from and where it goes.

### Key Features
- **Bi-directional Lineage**: Discover both **Upstream** (sources) and **Downstream** (targets) dependencies.
- **Column-Level Extraction**: Identify identifying columns used in `JOIN` and `MERGE` operations.
- **Unified Search**: Filter the entire graph starting from a specific `project.dataset.table`.

---

## 🛠️ Architecture

- **Backend**: Python 3.10+ powered by **FastAPI**.
- **Parsing Engine**: **sqlglot** for robust SQL dialect decomposition.
- **Metadata**: Native integration with Google **BigQuery Data Transfer API**.
- **Visualization**: **Mermaid.js** for dynamic, client-side graph rendering.

---

## 🚀 Getting Started

### 1. Credentials Setup
1. Go to Google Cloud Console ➔ IAM & Admin ➔ Service Accounts.
2. Create a Service Account with:
   - `BigQuery Data Viewer`
   - `BigQuery Data Transfer Service Viewer`
3. Generate and download a **JSON** key.

### 2. Local Installation

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r backend/requirements.txt
```

### 3. Running the App
```bash
python backend/main.py
```
Open your browser at: **[http://localhost:8000](http://localhost:8000)**

---

## 💡 How to Use

1. **Upload**: Select your Service Account `.json` file.
2. **Location**: Choose the dataset region (e.g., `us` or `southamerica-east1`).
3. **Start Point**: Enter the table path (e.g., `my-project.prod.orders`).
4. **Generate**: Click "GENERATE LINEAGE" to visualize the dependencies.

---

## 📂 Project Structure
- `/backend`: Parsing logic and Google API services.
- `/frontend`: Responsive UI using React and Tailwind.
- `requirements.txt`: Project dependencies.

---
**Open Source Data Engineering Tool.**
