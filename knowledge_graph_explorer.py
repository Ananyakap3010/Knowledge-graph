# ==========================================================
# PROJECT : Life Sciences Ontology & Knowledge Graph Explorer
# DOMAIN  : Pharmacovigilance
#
# OBJECTIVE:
# To design a pharmacovigilance ontology and build a
# knowledge graph explorer that enables users to
# explore entities, relationships, queries, insights,
# and graph visualizations.
# ==========================================================

# ==========================================================
# IMPORT REQUIRED LIBRARIES
#
# streamlit  -> User Interface
# pandas     -> Data Handling
# networkx   -> Knowledge Graph Construction
# matplotlib -> Graph Visualization
# ==========================================================

import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import scipy as sp
# ==========================================================
# STREAMLIT PAGE CONFIGURATION
#
# Configure application title,
# icon and layout settings.
# ==========================================================

st.set_page_config(
    page_title="Pharmacovigilance Knowledge Graph Explorer",
    page_icon="🧬",
    layout="wide"
)

# ==========================================================
# TASK 4
# KNOWLEDGE GRAPH CONSTRUCTION
#
# Load pharmacovigilance dataset
# from CSV files.
#
# Files:
# - entities.csv
# - relationships.csv
#
# Build NetworkX Knowledge Graph
# using entities as nodes and
# relationships as edges.
# ==========================================================

@st.cache_data
def load_data():

    entities = pd.read_csv("entities.csv")
    relationships = pd.read_csv("relationships.csv")

    return entities, relationships

entities_df, relationships_df = load_data()

# ==========================================================
# GRAPH INITIALIZATION
#
# Create graph object and load all
# relationship connections into the
# knowledge graph.
# ==========================================================

G = nx.Graph()

for _, row in relationships_df.iterrows():
    G.add_edge(
        row["Source"],
        row["Target"],
        relationship=row["Relationship"]
    )

# Entity → Type lookup for visualization
entity_type_map = dict(
    zip(entities_df["Entity_Name"], entities_df["Entity_Type"])
)

# Color map for each entity type (used in graph visualization)
COLOR_MAP = {
    "Drug":          "#E74C3C",
    "Adverse_Event": "#E67E22",
    "Patient":       "#3498DB",
    "Researcher":    "#2ECC71",
    "Study":         "#9B59B6",
    "Hospital":      "#1ABC9C",
}

# ==========================================================
# SIDEBAR NAVIGATION
#
# Provides navigation between:
#
# Dashboard
# View Entities
# Search Entity
# Knowledge Queries
# Insights
# Discovery Rules
# Graph Visualization
# ==========================================================

st.sidebar.title("🧬 Knowledge Graph Explorer")
st.sidebar.markdown("---")
st.sidebar.markdown("**Navigate Modules**")

menu = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "View Entities",
        "Search Entity",
        "Knowledge Queries",
        "Insights",
        "Discovery Rules",
        "Graph Visualization"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "> 📌 *Pharmacovigilance Knowledge Graph — Life Sciences Ontology Explorer*"
)

# ==========================================================
# DASHBOARD MODULE
#
# PURPOSE:
# Provide an overview of the
# pharmacovigilance knowledge graph.
#
# Displays:
# - Total Entities
# - Total Relationships
# - Entity Type Count
# - Entity Distribution
# ==========================================================

if menu == "Dashboard":

    st.title("🧬 Pharmacovigilance Knowledge Graph Explorer")
    st.markdown(
        """
        Welcome to the **Pharmacovigilance Knowledge Graph Explorer** — a tool designed
        to help researchers, analysts, and safety professionals explore drug safety
        relationships, adverse events, and clinical study connections.

        ---
        ### 📖 About This Application

        Built on a curated ontology with **6 entity types** and **10 relationship types**,
        enabling structured navigation of pharmacovigilance data.

        | Entity Type      | Description                                       |
        |------------------|---------------------------------------------------|
        | 💊 Drug           | Pharmaceutical compounds under monitoring         |
        | ⚠️ Adverse Event  | Undesired effects reported during drug use        |
        | 🧑 Patient        | Individuals in studies or treatment               |
        | 🔬 Researcher     | Scientists investigating safety signals           |
        | 📋 Study          | Clinical or observational studies                 |
        | 🏥 Hospital       | Institutions conducting studies                   |

        ---
        """
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Entities",      len(entities_df))
    col2.metric("🔗 Total Relationships", len(relationships_df))
    col3.metric("🗂️ Entity Types",        entities_df["Entity_Type"].nunique())

    st.markdown("---")
    st.subheader("📊 Entity Distribution")
    st.dataframe(
        entities_df["Entity_Type"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Entity Type", "Entity_Type": "Count"}),
        use_container_width=True
    )

# ==========================================================
# ENTITY EXPLORATION MODULE
#
# PURPOSE:
# Allow users to browse ontology
# entities based on entity type.
#
# Supported Entity Types:
# - Drug
# - Adverse Event
# - Patient
# - Researcher
# - Study
# - Hospital
# ==========================================================

elif menu == "View Entities":

    st.title("📂 View Entities")
    st.markdown(
        """
        Browse all entities in the ontology by type.
        Select an **Entity Type** below to filter and explore the records.

        ---
        """
    )

    entity_type = st.selectbox(
        "Select Entity Type",
        sorted(entities_df["Entity_Type"].unique())
    )

    filtered = entities_df[entities_df["Entity_Type"] == entity_type]

    st.markdown(f"**Showing `{len(filtered)}` records for type: `{entity_type}`**")
    st.dataframe(filtered, use_container_width=True)

# ==========================================================
# RELATIONSHIP EXPLORATION MODULE
#
# PURPOSE:
# Explore incoming and outgoing
# relationships for a selected entity.
#
# Users can investigate how entities
# are connected within the graph.
# ==========================================================

elif menu == "Search Entity":

    st.title("🔍 Entity Relationship Explorer")
    st.markdown(
        """
        Select any entity to explore its **incoming** and **outgoing** relationships
        within the knowledge graph.

        ---
        """
    )

    entity = st.selectbox(
        "Select Entity",
        sorted(entities_df["Entity_Name"].unique())
    )

    source_matches = relationships_df[relationships_df["Source"] == entity]
    target_matches = relationships_df[relationships_df["Target"] == entity]

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### ➡️ Outgoing Relationships")
        st.markdown(f"*`{entity}` is the **source** in these relationships*")
        if source_matches.empty:
            st.info("No outgoing relationships found.")
        else:
            st.dataframe(source_matches, use_container_width=True)

    with col2:
        st.markdown(f"### ⬅️ Incoming Relationships")
        st.markdown(f"*`{entity}` is the **target** in these relationships*")
        if target_matches.empty:
            st.info("No incoming relationships found.")
        else:
            st.dataframe(target_matches, use_container_width=True)

# ==========================================================
# TASK 5
# KNOWLEDGE QUERY MODULE
#
# QUERY 1
# Show adverse events caused by a drug
#
# QUERY 2
# Show researchers investigating an event
#
# QUERY 3
# Show studies conducted at a hospital
#
# QUERY 4
# Show patients treated with a drug
#
# QUERY 5
# Show drugs associated with a study
#
# PURPOSE:
# Enable knowledge discovery using
# predefined graph queries.
# ==========================================================

elif menu == "Knowledge Queries":

    st.title("🗃️ Knowledge Queries")
    st.markdown(
        """
        Run predefined **graph queries** to discover structured knowledge
        from the pharmacovigilance dataset.

        > These queries traverse edges in the knowledge graph to return
        > targeted, relationship-filtered results.

        ---
        """
    )

    query = st.selectbox(
        "Choose Query",
        [
            "Adverse Events caused by Drug",
            "Researchers investigating Event",
            "Studies conducted at Hospital",
            "Patients treated with Drug",
            "Drugs associated with Study"
        ]
    )

    st.markdown("---")

    if query == "Adverse Events caused by Drug":
        st.markdown("#### 💊 → ⚠️  Query 1: Adverse Events caused by Drug")
        st.markdown("*Finds all adverse events linked via a `CAUSES` relationship from the selected drug.*")
        drug = st.selectbox(
            "Select Drug",
            entities_df[entities_df["Entity_Type"] == "Drug"]["Entity_Name"]
        )
        result = relationships_df[
            (relationships_df["Source"] == drug) &
            (relationships_df["Relationship"] == "CAUSES")
        ]
        st.dataframe(result, use_container_width=True)

    elif query == "Researchers investigating Event":
        st.markdown("#### 🔬 → ⚠️  Query 2: Researchers investigating an Adverse Event")
        st.markdown("*Finds researchers with an `INVESTIGATES` relationship pointing to the selected event.*")
        event = st.selectbox(
            "Select Event",
            entities_df[entities_df["Entity_Type"] == "Adverse_Event"]["Entity_Name"]
        )
        result = relationships_df[
            (relationships_df["Target"] == event) &
            (relationships_df["Relationship"] == "INVESTIGATES")
        ]
        st.dataframe(result, use_container_width=True)

    elif query == "Studies conducted at Hospital":
        st.markdown("#### 📋 → 🏥  Query 3: Studies conducted at a Hospital")
        st.markdown("*Finds studies with a `CONDUCTED_AT` relationship targeting the selected hospital.*")
        hospital = st.selectbox(
            "Select Hospital",
            entities_df[entities_df["Entity_Type"] == "Hospital"]["Entity_Name"]
        )
        result = relationships_df[
            (relationships_df["Target"] == hospital) &
            (relationships_df["Relationship"] == "CONDUCTED_AT")
        ]
        st.dataframe(result, use_container_width=True)

    elif query == "Patients treated with Drug":
        st.markdown("#### 🧑 → 💊  Query 4: Patients treated with a Drug")
        st.markdown("*Finds patients linked via a `TREATED_WITH` relationship to the selected drug.*")
        drug = st.selectbox(
            "Select Drug",
            entities_df[entities_df["Entity_Type"] == "Drug"]["Entity_Name"]
        )
        result = relationships_df[
            (relationships_df["Target"] == drug) &
            (relationships_df["Relationship"] == "TREATED_WITH")
        ]
        st.dataframe(result, use_container_width=True)

    elif query == "Drugs associated with Study":
        st.markdown("#### 💊 → 📋  Query 5: Drugs associated with a Study")
        st.markdown("*Finds drugs linked via an `ASSOCIATED_WITH` relationship to the selected study.*")
        study = st.selectbox(
            "Select Study",
            entities_df[entities_df["Entity_Type"] == "Study"]["Entity_Name"]
        )
        result = relationships_df[
            (relationships_df["Target"] == study) &
            (relationships_df["Relationship"] == "ASSOCIATED_WITH")
        ]
        st.dataframe(result, use_container_width=True)

# ==========================================================
# TASK 6
# KNOWLEDGE GRAPH INSIGHTS
#
# INSIGHT 1
# Most Connected Entity
#
# INSIGHT 2
# Most Linked Adverse Event
#
# INSIGHT 3
# Most Active Researcher
#
# INSIGHT 4
# Hospital Conducting Maximum Studies
#
# INSIGHT 5
# Most Studied Drug
#
# PURPOSE:
# Generate meaningful business
# insights from graph relationships.
# ==========================================================

elif menu == "Insights":

    st.title("💡 Knowledge Graph Insights")
    st.markdown(
        """
        Automatically computed **graph-level insights** derived from entity
        connections and relationship patterns.

        ---
        """
    )

    degree_dict = dict(G.degree())
    most_connected = max(degree_dict, key=degree_dict.get)

    event_count = relationships_df[
        relationships_df["Relationship"] == "CAUSES"
    ]["Target"].value_counts()

    researcher_count = relationships_df[
        relationships_df["Relationship"] == "INVESTIGATES"
    ]["Source"].value_counts()

    hospital_count = relationships_df[
        relationships_df["Relationship"] == "CONDUCTED_AT"
    ]["Target"].value_counts()

    drug_count = relationships_df[
        relationships_df["Relationship"] == "CAUSES"
    ]["Source"].value_counts()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🌐 Insight 1 — Most Connected Entity",      most_connected)
        st.metric("⚠️ Insight 2 — Most Linked Adverse Event",  event_count.idxmax())
        st.metric("🔬 Insight 3 — Most Active Researcher",     researcher_count.idxmax())

    with col2:
        st.metric("🏥 Insight 4 — Hospital With Most Studies", hospital_count.idxmax())
        st.metric("💊 Insight 5 — Most Studied Drug",          drug_count.idxmax())

    st.markdown(
        """
        ---
        > 📌 **Note:** Insights are computed dynamically from `relationships.csv`
        > and reflect the current state of the knowledge graph.
        """
    )

# ==========================================================
# TASK 7
# CUSTOM DISCOVERY RULE
#
# RULE NAME:
# High Risk Drug Identification
#
# PURPOSE:
# Identify drugs requiring additional
# pharmacovigilance monitoring.
#
# RISK SCORE FORMULA:
#
# Risk Score =
# (Number of Adverse Events × 3)
# + Number of Linked Studies
#
# CLASSIFICATION:
#
# Score > 10
# High Risk Drug
#
# Score 5 - 10
# Moderate Risk Drug
#
# Score < 5
# Low Risk Drug
# ==========================================================

elif menu == "Discovery Rules":

    st.title("🧪 Custom Discovery Rules")
    st.markdown(
        """
        Discovery rules are **algorithmic classification patterns** applied to the
        knowledge graph to surface entities that require special attention.

        Each rule combines graph-derived metrics into a **risk or influence score**,
        classified into meaningful tiers.

        ---
        """
    )

    rule = st.selectbox(
        "Select a Discovery Rule",
        [
            "High Risk Drug",
            "High Influence Researcher",
            "Key Opinion Leader",
            "Critical Biomarker (Adverse Event)"
        ]
    )

    st.markdown("---")

    # --------------------------------------------------
    # RULE 1 — HIGH RISK DRUG
    # --------------------------------------------------

    if rule == "High Risk Drug":

        st.markdown("### 💊 High Risk Drug Identification")

        with st.expander("📖 Why was this rule created?"):
            st.markdown(
                """
                Not all drugs carry the same pharmacovigilance concern.
                Drugs linked to **multiple adverse events** and **multiple clinical studies**
                represent a higher burden on safety monitoring systems.

                This rule helps safety teams **prioritize resources** — focusing deeper
                surveillance on drugs that show both wide adverse event coverage and
                broad study involvement.
                """
            )

        with st.expander("⚙️ How does the rule work?"):
            st.markdown(
                """
                For each **Drug** entity, the rule:

                1. Counts how many **Adverse Events** the drug causes (`CAUSES` relationships)
                2. Counts how many **Studies** the drug is associated with (`ASSOCIATED_WITH`)
                3. Combines both into a single **Risk Score**
                """
            )

        with st.expander("🧮 Score & Classification Formula"):
            st.markdown(
                """
                ```
                Risk Score = (Adverse Events × 3) + (Linked Studies × 1)
                ```

                | Score Range | Classification        |
                |-------------|----------------------|
                | > 10        | 🔴 High Risk Drug     |
                | 5 – 10      | 🟡 Moderate Risk Drug |
                | < 5         | 🟢 Low Risk Drug      |

                > Adverse events are weighted **3×** because they directly indicate patient harm.
                """
            )

        st.markdown("#### 📊 Results")
        drugs = entities_df[entities_df["Entity_Type"] == "Drug"]["Entity_Name"].tolist()
        records = []
        for drug in drugs:
            ae_count = len(relationships_df[
                (relationships_df["Source"] == drug) & (relationships_df["Relationship"] == "CAUSES")
            ])
            study_count = len(relationships_df[
                (relationships_df["Source"] == drug) & (relationships_df["Relationship"] == "ASSOCIATED_WITH")
            ])
            score = (ae_count * 3) + study_count
            label = "🔴 High Risk" if score > 10 else ("🟡 Moderate Risk" if score >= 5 else "🟢 Low Risk")
            records.append({"Drug": drug, "Adverse Events": ae_count, "Linked Studies": study_count, "Risk Score": score, "Classification": label})
        st.dataframe(pd.DataFrame(records).sort_values("Risk Score", ascending=False), use_container_width=True)

    # --------------------------------------------------
    # RULE 2 — HIGH INFLUENCE RESEARCHER
    # --------------------------------------------------

    elif rule == "High Influence Researcher":

        st.markdown("### 🔬 High Influence Researcher Identification")

        with st.expander("📖 Why was this rule created?"):
            st.markdown(
                """
                Certain researchers are deeply embedded in the pharmacovigilance network —
                they investigate multiple adverse events, work across several hospitals,
                and participate in numerous studies.

                This rule identifies **high-influence researchers** to recognize domain
                leaders and allocate collaboration opportunities.
                """
            )

        with st.expander("⚙️ How does the rule work?"):
            st.markdown(
                """
                For each **Researcher**, the rule counts:
                1. **Adverse Events** investigated (`INVESTIGATES`)
                2. **Studies** participated in (`PARTICIPATES_IN`)
                3. **Hospitals** worked at (`WORKS_AT`)
                """
            )

        with st.expander("🧮 Score & Classification Formula"):
            st.markdown(
                """
                ```
                Influence Score = (Investigations × 3) + (Studies × 2) + (Hospitals × 1)
                ```

                | Score Range | Classification               |
                |-------------|------------------------------|
                | > 10        | 🔴 High Influence Researcher  |
                | 5 – 10      | 🟡 Moderate Influence         |
                | < 5         | 🟢 Low Influence              |
                """
            )

        st.markdown("#### 📊 Results")
        researchers = entities_df[entities_df["Entity_Type"] == "Researcher"]["Entity_Name"].tolist()
        records = []
        for r in researchers:
            inv = len(relationships_df[(relationships_df["Source"] == r) & (relationships_df["Relationship"] == "INVESTIGATES")])
            stu = len(relationships_df[(relationships_df["Source"] == r) & (relationships_df["Relationship"] == "PARTICIPATES_IN")])
            hos = len(relationships_df[(relationships_df["Source"] == r) & (relationships_df["Relationship"] == "WORKS_AT")])
            score = (inv * 3) + (stu * 2) + hos
            label = "🔴 High Influence" if score > 10 else ("🟡 Moderate Influence" if score >= 5 else "🟢 Low Influence")
            records.append({"Researcher": r, "Investigations": inv, "Studies": stu, "Hospitals": hos, "Influence Score": score, "Classification": label})
        st.dataframe(pd.DataFrame(records).sort_values("Influence Score", ascending=False), use_container_width=True)

    # --------------------------------------------------
    # RULE 3 — KEY OPINION LEADER
    # --------------------------------------------------

    elif rule == "Key Opinion Leader":

        st.markdown("### 🏆 Key Opinion Leader (KOL) Identification")

        with st.expander("📖 Why was this rule created?"):
            st.markdown(
                """
                A **Key Opinion Leader** is a researcher who is strongly connected
                across hospitals and studies and actively investigates adverse events.

                Identifying KOLs helps find **trusted experts** for advisory boards,
                safety reviews, and regulatory policy guidance.
                """
            )

        with st.expander("⚙️ How does the rule work?"):
            st.markdown(
                """
                For each **Researcher**, the rule combines:
                1. Number of **Adverse Events** investigated
                2. Number of **Hospitals** associated with
                3. **Graph degree** (total connections in the knowledge graph)
                """
            )

        with st.expander("🧮 Score & Classification Formula"):
            st.markdown(
                """
                ```
                KOL Score = (Investigations × 2) + (Hospitals × 2) + (Graph Degree × 1)
                ```

                | Score Range | Classification        |
                |-------------|----------------------|
                | > 12        | 🌟 Key Opinion Leader |
                | 6 – 12      | 🔵 Emerging Leader    |
                | < 6         | ⚪ General Researcher  |
                """
            )

        st.markdown("#### 📊 Results")
        researchers = entities_df[entities_df["Entity_Type"] == "Researcher"]["Entity_Name"].tolist()
        records = []
        for r in researchers:
            inv = len(relationships_df[(relationships_df["Source"] == r) & (relationships_df["Relationship"] == "INVESTIGATES")])
            hos = len(relationships_df[(relationships_df["Source"] == r) & (relationships_df["Relationship"] == "WORKS_AT")])
            deg = G.degree(r) if r in G else 0
            score = (inv * 2) + (hos * 2) + deg
            label = "🌟 Key Opinion Leader" if score > 12 else ("🔵 Emerging Leader" if score >= 6 else "⚪ General Researcher")
            records.append({"Researcher": r, "Investigations": inv, "Hospitals": hos, "Graph Degree": deg, "KOL Score": score, "Classification": label})
        st.dataframe(pd.DataFrame(records).sort_values("KOL Score", ascending=False), use_container_width=True)

    # --------------------------------------------------
    # RULE 4 — CRITICAL BIOMARKER / ADVERSE EVENT
    # --------------------------------------------------

    elif rule == "Critical Biomarker (Adverse Event)":

        st.markdown("### 🧬 Critical Biomarker / Adverse Event Identification")

        with st.expander("📖 Why was this rule created?"):
            st.markdown(
                """
                Some adverse events appear across many drugs, are studied by multiple
                researchers, and are observed in many patients — these are **critical
                safety signals** requiring escalated regulatory reporting.

                This rule surfaces such events for priority monitoring.
                """
            )

        with st.expander("⚙️ How does the rule work?"):
            st.markdown(
                """
                For each **Adverse Event**, the rule counts:
                1. **Drugs** that cause it (`CAUSES`)
                2. **Researchers** investigating it (`INVESTIGATES`)
                3. **Patients** in whom it was observed (`OBSERVED_IN`)
                """
            )

        with st.expander("🧮 Score & Classification Formula"):
            st.markdown(
                """
                ```
                Criticality Score = (Drugs × 3) + (Researchers × 2) + (Patients × 1)
                ```

                | Score Range | Classification           |
                |-------------|--------------------------|
                | > 10        | 🔴 Critical Biomarker     |
                | 5 – 10      | 🟡 Moderate Signal        |
                | < 5         | 🟢 Low Concern Event      |

                > Drug linkage weighted highest — multiple drugs causing the same event
                > indicates a **class-wide safety concern**.
                """
            )

        st.markdown("#### 📊 Results")
        events = entities_df[entities_df["Entity_Type"] == "Adverse_Event"]["Entity_Name"].tolist()
        records = []
        for event in events:
            drugs = len(relationships_df[(relationships_df["Target"] == event) & (relationships_df["Relationship"] == "CAUSES")])
            res   = len(relationships_df[(relationships_df["Target"] == event) & (relationships_df["Relationship"] == "INVESTIGATES")])
            pat   = len(relationships_df[(relationships_df["Target"] == event) & (relationships_df["Relationship"] == "OBSERVED_IN")])
            score = (drugs * 3) + (res * 2) + pat
            label = "🔴 Critical Biomarker" if score > 10 else ("🟡 Moderate Signal" if score >= 5 else "🟢 Low Concern")
            records.append({"Adverse Event": event, "Linked Drugs": drugs, "Researchers": res, "Observed in Patients": pat, "Criticality Score": score, "Classification": label})
        st.dataframe(pd.DataFrame(records).sort_values("Criticality Score", ascending=False), use_container_width=True)

# ==========================================================
# TASK 8
# KNOWLEDGE GRAPH VISUALIZATION
#
# PURPOSE:
# Visualize ontology entities and
# relationships using NetworkX.
#
# BENEFITS:
# - Relationship Exploration
# - Pattern Identification
# - Knowledge Discovery
# - Graph Analysis
# ==========================================================

elif menu == "Graph Visualization":

    st.title("🕸️ Knowledge Graph Visualization")
    st.markdown(
        """
        Visual representation of the **pharmacovigilance knowledge graph**
        with entities **color-coded by type** and **sized by connection importance**.

        > Use the controls below to change layout or highlight a specific entity type.

        ---
        """
    )

    col_ctrl1, col_ctrl2 = st.columns([2, 2])
    with col_ctrl1:
        layout_choice = st.selectbox(
            "Graph Layout",
            ["Spring (Force-directed)", "Kamada-Kawai", "Circular", "Shell"]
        )
    with col_ctrl2:
        filter_type = st.selectbox(
            "Highlight Entity Type",
            ["All"] + sorted(entities_df["Entity_Type"].unique().tolist())
        )

    degree_dict = dict(G.degree())
    node_colors, node_sizes, edge_colors = [], [], []

    for node in G.nodes():
        etype = entity_type_map.get(node)
        if filter_type != "All" and etype != filter_type:
            node_colors.append("#DDDDDD")
            node_sizes.append(300)
        else:
            node_colors.append(COLOR_MAP.get(etype, "#95A5A6"))
            node_sizes.append(400 + degree_dict.get(node, 1) * 120)

    for u, v in G.edges():
        u_type = entity_type_map.get(u)
        v_type = entity_type_map.get(v)
        if filter_type != "All" and u_type != filter_type and v_type != filter_type:
            edge_colors.append("#EEEEEE")
        else:
            edge_colors.append("#AAAAAA")

    if layout_choice == "Spring (Force-directed)":
        pos = nx.spring_layout(G, seed=42, k=1.8)
    elif layout_choice == "Kamada-Kawai":
        pos = nx.kamada_kawai_layout(G)
    elif layout_choice == "Circular":
        pos = nx.circular_layout(G)
    else:
        pos = nx.shell_layout(G)

    fig, ax = plt.subplots(figsize=(18, 11))
    fig.patch.set_facecolor("#F8F9FA")
    ax.set_facecolor("#F8F9FA")

    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=0.8, alpha=0.6, ax=ax)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.92, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=7, font_color="#1A1A2E", font_weight="bold", ax=ax)

    ax.set_title(
        "Pharmacovigilance Knowledge Graph — Entity & Relationship Map",
        fontsize=15, fontweight="bold", color="#1A1A2E", pad=20
    )
    ax.axis("off")

    legend_elements = [
        Patch(facecolor=color, edgecolor="white", label=etype)
        for etype, color in COLOR_MAP.items()
    ]
    ax.legend(handles=legend_elements, loc="lower left", fontsize=9,
              title="Entity Types", title_fontsize=10, framealpha=0.85, edgecolor="#CCCCCC")

    st.pyplot(fig)

    st.markdown("---")
    st.markdown("#### 📊 Graph Summary")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔵 Total Nodes",         G.number_of_nodes())
    col2.metric("🔗 Total Edges",         G.number_of_edges())
    col3.metric("🌐 Graph Density",       f"{nx.density(G):.4f}")
    col4.metric("⭐ Most Connected Node", max(degree_dict, key=degree_dict.get))

    st.markdown("---")
    st.markdown("#### 🎨 Node Color Legend")

    legend_cols = st.columns(len(COLOR_MAP))
    for i, (etype, color) in enumerate(COLOR_MAP.items()):
        legend_cols[i].markdown(
            f"<div style='background:{color};padding:6px 10px;"
            f"border-radius:8px;text-align:center;"
            f"color:white;font-weight:bold;font-size:13px'>{etype}</div>",
            unsafe_allow_html=True
        )

# ==========================================================
# APPLICATION SUMMARY
#
# Ontology Designed           ✓
# Knowledge Graph Constructed ✓
# Knowledge Queries Executed  ✓
# Insights Generated          ✓
# Discovery Rules Applied     ✓
# Graph Visualized            ✓
#
# Pharmacovigilance Knowledge Graph
# Explorer Completed Successfully.
# ==========================================================
