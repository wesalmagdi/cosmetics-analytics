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
└── results/ 


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

---


## **Dockerfile highlights:**
```markdown


```dockerfile
FROM python:3.11-slim

# Install dependencies
RUN pip install pandas numpy matplotlib seaborn scikit-learn scipy requests

# Set working directory
WORKDIR /app/pipeline

# Copy all scripts into container
COPY . /app/pipeline/

# Start interactive bash by default
CMD ["/bin/bash"]
```


### **🔄 Automated Execution Flow**
---
The project is designed to run as a continuous pipeline. By executing the `summary.sh` script, the following automated chain reaction occurs:

1. Initiation: `bash summary.sh` initiates the process from the host machine.
2. Container Trigger: `summary.sh` commands the Docker container to execute the first script.
3. The Python Chain:
    * `ingest.py` runs ➡️ calls `preprocess.py`.
    * `preprocess.py` runs ➡️ calls `analytics.py`.
    * `analytics.py` runs ➡️ calls `visualize.py`.
    * `visualize.py` runs ➡️ calls `cluster.py`.
4. Integrator Completion: `cluster.py` finishes the core machine learning computation and saves the final `clusters.txt` output.
5. Data Extraction: Once the Python chain is complete, `summary.sh` automatically reaches into the container, copies the generated `.txt`, `.csv`, and `.png` files, and saves them into the local `results/` folder on your computer.

---
## Sample Outputs

This section demonstrates the successful execution of the full analytics pipeline. All outputs were automatically extracted into the `results/` folder via the `summary.sh` automation script.

### 1. K-Means Clustering Results 
The `cluster.py` script successfully partitioned the cosmetics dataset into three distinct groups. The distribution below identifies a dominant mass-market category, a secondary formulation group, and a small set of specialized outliers.

| Category | Sample Count | Significance |
| :--- | :--- | :--- |
| **Cluster 0** | **48,191** | Standard mass-market formulations |
| **Cluster 1** | **20** | Outliers / Specialized niche products |
| **Cluster 2** | **15,873** | Secondary ingredient profile group |

Snippet from `results/clusters.txt`:
```text
Cluster 0: 48191 samples
Cluster 1: 20 samples
Cluster 2: 15873 samples
```

### 2. Statistical Insights (`insight1.txt`)
The `analytics.py` script  extracted a structural summary confirming that the data was successfully normalized via **Z-score scaling**. This ensures that the K-Means algorithm  treats all features with equal weight.

* Dataset Dimensions: 64,084 rows × 10 columns
* Target Features: `code`, `completeness`, `brand_popularity`, `brand`, `country`, etc.

**Data Distribution Summary:**

| Metric | `code` (Scaled) | `completeness` (Scaled) |
| :--- | :--- | :--- |
| **Count** | 64,084 | 64,084 |
| **Mean** | **~0.00** | **~0.00** |
| **Std Dev** | **1.00** | **1.00** |
| **Min** | -54.49 | -1.23 |
| **Max** | 53.31 | 3.88 |






