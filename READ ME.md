# 🧬 Pharmacovigilance Knowledge Graph Explorer

**Python Task 6 — Life Sciences Ontology & Knowledge Graph Explorer**

---

## 📖 Project Overview

This application explores a **Pharmacovigilance Knowledge Graph** built on a curated ontology with 6 entity types and 10 relationship types. It enables drug safety professionals and researchers to explore entities, discover relationships, run knowledge queries, generate insights, and apply discovery rules.

---

## 🗂️ Project Structure

```
knowledge_graph_explorer/
│
├── app.py                        # Main Streamlit application
├── entities.csv                  # Entity dataset (50+ entities)
├── relationships.csv             # Relationship dataset (75+ relationships)
├── ontology_definition.docx      # Task 3 — Ontology documentation
├── knowledge_graph_report.docx   # Task 10 — Knowledge graph report
└── README.md                     # This file
```

---

## ⚙️ Installation & Setup

### Step 1 — Install Python dependencies

```bash
pip install streamlit pandas networkx matplotlib scipy
```

> `scipy` is required for the **Kamada-Kawai** graph layout. All other layouts work without it.

### Step 2 — Ensure data files are present

Make sure `entities.csv` and `relationships.csv` are in the **same folder** as `app.py`.

**entities.csv format:**
```
Entity_Name,Entity_Type
Aspirin,Drug
Headache,Adverse_Event
PAT001,Patient
...
```

**relationships.csv format:**
```
Source,Target,Relationship
Aspirin,Headache,CAUSES
PAT001,Aspirin,TREATED_WITH
...
```

### Step 3 — Run the application

```bash
streamlit run app.py
```

Opens at `http://localhost:8501` in your browser.

---

## 🧩 Application Modules

| Module | Task | Description |
|--------|------|-------------|
| **Dashboard** | — | Overview: entity count, relationship count, entity distribution |
| **View Entities** | Task 1 & 2 | Browse entities filtered by type |
| **Search Entity** | — | Explore incoming & outgoing relationships for any entity |
| **Knowledge Queries** | Task 5 | 5 predefined graph queries |
| **Insights** | Task 6 | 5 automated graph-level insights |
| **Discovery Rules** | Task 7 | 4 custom scoring & classification rules |
| **Graph Visualization** | Task 8 | Color-coded, interactive NetworkX graph |
| **Screenshots** | Deliverables | Upload & track submission screenshots |

---

## 🧬 Ontology Design

### Entity Types (6)

| Entity Type | Description |
|-------------|-------------|
| `Drug` | Pharmaceutical compounds under safety monitoring |
| `Adverse_Event` | Harmful effects reported during drug use |
| `Patient` | Individuals in studies or treatment |
| `Researcher` | Scientists investigating safety signals |
| `Study` | Clinical or observational investigations |
| `Hospital` | Institutions conducting studies |

### Relationship Types (10)

| Relationship | Connects |
|-------------|----------|
| `CAUSES` | Drug → Adverse_Event |
| `TREATED_WITH` | Patient → Drug |
| `REPORTED` | Patient → Adverse_Event |
| `INVESTIGATES` | Researcher → Adverse_Event |
| `WORKS_AT` | Researcher → Hospital |
| `CONDUCTED_AT` | Study → Hospital |
| `PARTICIPATES_IN` | Patient → Study |
| `ASSOCIATED_WITH` | Drug → Study |
| `MONITORS` | Researcher → Drug |
| `OBSERVED_IN` | Adverse_Event → Patient |

---

## 🗃️ Knowledge Queries (Task 5)

| # | Query | Relationship |
|---|-------|-------------|
| 1 | Adverse Events caused by Drug | `CAUSES` |
| 2 | Researchers investigating Event | `INVESTIGATES` |
| 3 | Studies conducted at Hospital | `CONDUCTED_AT` |
| 4 | Patients treated with Drug | `TREATED_WITH` |
| 5 | Drugs associated with Study | `ASSOCIATED_WITH` |

---

## 💡 Insights (Task 6)

| # | Insight |
|---|---------|
| 1 | Most Connected Entity |
| 2 | Most Linked Adverse Event |
| 3 | Most Active Researcher |
| 4 | Hospital With Most Studies |
| 5 | Most Studied Drug |

---

## 🧪 Discovery Rules (Task 7)

### Rule 1 — High Risk Drug
```
Risk Score = (Adverse Events × 3) + (Linked Studies × 1)
```
- 🔴 > 10 → High Risk Drug
- 🟡 5–10 → Moderate Risk Drug
- 🟢 < 5 → Low Risk Drug

### Rule 2 — High Influence Researcher
```
Influence Score = (Investigations × 3) + (Studies × 2) + (Hospitals × 1)
```
- 🔴 > 10 → High Influence
- 🟡 5–10 → Moderate Influence
- 🟢 < 5 → Low Influence

### Rule 3 — Key Opinion Leader (KOL)
```
KOL Score = (Investigations × 2) + (Hospitals × 2) + (Graph Degree × 1)
```
- 🌟 > 12 → Key Opinion Leader
- 🔵 6–12 → Emerging Leader
- ⚪ < 6 → General Researcher

### Rule 4 — Critical Biomarker (Adverse Event)
```
Criticality Score = (Drugs × 3) + (Researchers × 2) + (Patients × 1)
```
- 🔴 > 10 → Critical Biomarker
- 🟡 5–10 → Moderate Signal
- 🟢 < 5 → Low Concern

---

## 📸 Screenshots (Submission Deliverables)

Minimum **3 screenshots** required for submission. Use the **Screenshots** module in the app to upload and track them.

| # | Screenshot | Module | Required |
|---|-----------|--------|----------|
| 1 | Ontology Design | Dashboard / View Entities | ✅ Yes |
| 2 | Graph Visualization | Graph Visualization | ✅ Yes |
| 3 | Query Results | Knowledge Queries | ✅ Yes |
| 4 | Insights Module | Insights | ⭐ Optional |
| 5 | Discovery Rules Table | Discovery Rules | ⭐ Optional |
| 6 | Deployment Screenshot | Streamlit Cloud | ⭐ Optional (Bonus) |

---

## 🚀 Deployment (Optional Bonus)

To deploy on **Streamlit Community Cloud**:

1. Push your project to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set the main file as `app.py`
4. Click **Deploy**

> Successful deployment may qualify for up to **50 bonus points** per the task evaluation criteria.

---

## 📦 Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| `streamlit` | Latest | Web UI framework |
| `pandas` | Latest | Data loading & manipulation |
| `networkx` | Latest | Knowledge graph construction |
| `matplotlib` | Latest | Graph visualization |
| `scipy` | Latest | Kamada-Kawai layout (optional) |

Install all at once:
```bash
pip install streamlit pandas networkx matplotlib scipy
```

---

## 📋 Deliverables Checklist

| Deliverable | File | Status |
|-------------|------|--------|
| Main Application | `app.py` | ✅ Complete |
| Ontology Definition | `ontology_definition.docx` | ✅ Complete |
| Knowledge Graph Report | `knowledge_graph_report.docx` | ✅ Complete |
| Dataset — Entities | `entities.csv` | ✅ Required |
| Dataset — Relationships | `relationships.csv` | ✅ Required |
| Screenshots (min 3) | Via Screenshots module | ✅ In App |
| README | `README.md` | ✅ This file |

---