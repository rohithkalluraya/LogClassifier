# Log Classification with Hybrid Classification Framework

A hybrid log classification system that combines rule-based matching, semantic classification, and language-model-assisted inference to handle logs with varying levels of complexity.

The framework is designed to balance speed, accuracy, and flexibility by routing log messages through different classification strategies depending on the nature of the input.

---

## Classification Approaches

### 1. Regular Expression (Regex)

Handles simple and predictable log patterns using predefined rules.

**Best suited for:**
- Standardized system logs
- Known error messages
- Repetitive operational events

### 2. Sentence Transformer + Logistic Regression

Uses sentence embeddings to capture semantic meaning and applies Logistic Regression for classification.

**Best suited for:**
- Logs with textual variations
- Domains with sufficient labeled training data
- Medium-complexity classification tasks

### 3. LLM-Based Classification

Provides contextual reasoning for logs that cannot be confidently classified by the previous methods.

**Best suited for:**
- Ambiguous log messages
- Rare or unseen patterns
- Poorly labeled datasets
- Long-tail classification scenarios

![architecture](resources/arch.png)

---

## Project Structure

### `training/`

Contains code for:

- Training Sentence Transformer + Logistic Regression models
- Creating and maintaining regex-based classifiers

### `models/`

Stores:

- Trained classification models
- Model artifacts
- Embedding-related files

### `resources/`

Contains:

- Sample datasets
- Test CSV files
- Output files
- Images and diagrams

### Root Directory

Includes:

- `server.py` – FastAPI application
- `classify.py` – Classification workflow
- `processor_llm.py` – LLM inference component

---

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure the Language Model

Download a compatible GGUF model and configure its path according to your environment.

Example:

```bash
export LLM_MODEL_PATH=/path/to/model.gguf
export LLM_NUM_THREADS=8
```

Depending on your hardware, additional runtime parameters may be configured for improved performance.

### 3. Start the API Server

```bash
uvicorn server:app --reload
```

API Endpoint:

```text
http://127.0.0.1:8000/
```

Interactive Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Usage

Upload a CSV file containing the following columns:

```csv
source,log_message
```

Example:

```csv
app-server,Connection timeout while contacting database
auth-service,User authentication failed
payment-service,Transaction completed successfully
```

The output CSV will include:

```csv
source,log_message,target_label
```

where `target_label` contains the predicted classification.

---

## Classification Workflow

```text
Incoming Log
      │
      ▼
Regex Classification
      │
      ├── Match Found → Return Label
      │
      ▼
Semantic Classification
      │
      ├── High Confidence → Return Label
      │
      ▼
LLM Classification
      │
      ▼
Final Prediction
```

This layered approach ensures that simple patterns are processed efficiently while more complex cases receive additional contextual analysis.

---

## Performance Notes

- Regex classification provides near-instant predictions.
- Semantic classification handles most operational logs efficiently.
- LLM inference is reserved for cases requiring deeper contextual understanding.
- Quantized models can significantly reduce memory usage and inference latency.
- GPU acceleration may improve throughput for larger workloads.

---

## Features

- Hybrid multi-stage classification pipeline
- Rule-based pattern matching
- Semantic log understanding
- Context-aware classification
- FastAPI deployment
- Modular architecture
- Extensible training workflow
- Local model support

---

## Future Improvements

- Confidence-based routing
- Active learning feedback loops
- Streaming log ingestion
- Classification explainability
- Anomaly detection integration
- Distributed inference support

---
