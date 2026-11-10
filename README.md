# 📊 Real-Time Live Poll App

> An end-to-end, event-driven streaming application built with **Apache Kafka**, **Python**, and **Streamlit** to ingest, process, and visualize live audience poll responses in real time[cite: 2].

---

## 🚀 Overview

This project simulates a live conference audience voting environment[cite: 2]. A decoupled Kafka Producer streams simulated survey responses[cite: 2], while an embedded Kafka Consumer within a Streamlit dashboard aggregates and renders the incoming data dynamically without requiring manual page reloads[cite: 2, 3].

### ✨ Key Features
- **⚡ Asynchronous Event Streaming:** High-throughput message queuing powered by Apache Kafka[cite: 2].
- **📈 Real-Time KPI Tracking:** Instant response counter updating dynamically with every submission using `st.metric()`.
- **📊 Dynamic Visualizations:** Question-wise bar charts maintaining natural logical order (e.g., ratings 1–5, sentiment scale).
- **📋 Live Feed Table:** Real-time DataFrame logging every recorded poll with unique submission IDs.
- **🔄 In-Place Dynamic Rerendering:** State-managed dashboard updates using session caching[cite: 3].

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Message Broker** | Apache Kafka | Real-time distributed event streaming[cite: 2] |
| **Coordination** | Apache ZooKeeper | Cluster state management for Kafka |
| **Frontend UI** | Streamlit | Real-time reactive data dashboard[cite: 2] |
| **Data Processing** | Python, Pandas | Payload transformation and aggregation |
| **Plotting Engine** | Plotly / Streamlit Native | Interactive categorical charts[cite: 3] |

---

## 📁 Repository Structure

```text
├── Screenshots/                          # Verification and demo evidence
│   ├── SS_1_KPI.png                      # Total responses KPI view
│   ├── SS_2_BarCharts.png                # Dynamic question-wise charts
│   └── SS_3_DataFrame.png                # Live response tabular feed
├── kafka_producer_Abdullah_khalid.py     # Kafka producer streaming poll data
├── streamlit_consumer_Abdullah_khalid.py # Embedded Kafka consumer & UI app
├── poll_response_api.py                  # Poll response generator & question schema
├── requirements.txt                      # Project dependencies
└── README.md                             # Documentation