# Nile University — CSCI461: Introduction to Big Data  
## Assignment #1 — Spring 2026  

**Team Members:**  
1. Member 1 – Wesal Magdy
2. Member 2 – Rana Osman
3. Member 3 – Raneem Khaled
4. Member 4 – Rama Mousa  

---

## **Project Overview**

This project demonstrates a **data analytics pipeline** using Python and Docker.  
The pipeline processes a raw dataset (`en.openbeautyfacts.org.products.csv`) and performs the following tasks:

1. **Ingestion:** Load raw dataset from CSV/ZIP and save as `data_raw.csv`.  
2. **Preprocessing:** Clean, transform, and reduce features; output `data_preprocessed.csv`.  
3. **Analytics:** Generate textual insights from processed data (`insight1.txt`, `insight2.txt`).  
4. **Visualization:** Create plots (`summary_plot.png`) to summarize data patterns.  
5. **Clustering:** Apply K-Means clustering on selected features (`clusters.txt`).  
6. **Summary:** Copy all generated files to host results folder.

---

## **Folder Structure**
customer-analytics/
├── Dockerfile
├── ingest.py
├── preprocess.py
├── analytics.py
├── visualize.py
├── cluster.py
├── summary.sh
├── README.md
└── results/ # Generated outputs


---

## **Docker Setup**

We use **Python 3.11-slim** as the base image and install all necessary packages:

- pandas  
- numpy  
- matplotlib  
- seaborn  
- scikit-learn  
- scipy  
- requests  

**Dockerfile highlights:**

```dockerfile
FROM python:3.11-slim

# Install dependencies
RUN pip install pandas numpy matplotlib seaborn scikit-learn scipy requests

# Set working directory
WORKDIR /app/pipeline

# Copy all scripts into container
COPY . /app/pipeline/

# Start interactive bash by default
CMD ["bash"]