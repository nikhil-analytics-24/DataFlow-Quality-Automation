# DataFlow Quality Automation

An automated ETL pipeline built with Python for extracting data from a REST API, transforming and cleaning the data, performing data quality validation, and loading clean records into a database.

## 📌 Project Overview

DataFlow Quality Automation is an end-to-end ETL (Extract, Transform, Load) pipeline designed to automate the complete data processing workflow.

The pipeline takes raw data from a REST API, processes and cleans the data, performs validation and data quality checks, logs important activities, and finally loads the clean records into a database.

## 🔄 ETL Workflow

REST API
↓
Data Extraction
↓
JSON Flattening
↓
Data Cleaning & Transformation
↓
Type Casting & Validation
↓
Data Quality Check
↓
Audit Logging
↓
Database Loading
↓
Clean Production Data

## ✨ Key Features

- Automated ETL pipeline
- REST API data extraction
- Nested JSON flattening
- Data cleaning and transformation
- Data type casting
- Regular expression validation
- Data quality checks
- Anomaly detection
- Audit logging
- Database loading
- Modular Python architecture
- End-to-end pipeline execution
- Detailed execution logs

## 📂 Project Structure

DataFlow-Quality-Automation/
│
├── audit_logger.py
├── extractor.py
├── loader.py
├── main.py
├── transformer.py
└── README.md

## 🧩 Project Components

### extractor.py

Responsible for extracting data from the remote REST API.

It also handles nested JSON data and converts deeply nested structures into a more usable format.

### transformer.py

Responsible for:

- Data cleaning
- Type casting
- Regular expression validation
- Data transformation
- Data quality validation
- Detecting invalid or anomalous records

### loader.py

Responsible for connecting to the target database and loading validated and clean records.

### audit_logger.py

Responsible for maintaining audit logs and recording important pipeline events, execution status, and errors.

### main.py

Acts as the main controller of the ETL pipeline.

It coordinates all three major phases:

1. Extraction
2. Transformation and Validation
3. Database Loading

## 🛠️ Technologies Used

- Python
- REST API
- Requests
- JSON
- SQLite / SQL Database
- Python Logging
- Regular Expressions

## ⚙️ Installation

Clone the repository:

git clone https://github.com/nikhil-analytics-24/DataFlow-Quality-Automation.git

Open the project folder:

cd DataFlow-Quality-Automation

Install the required Python package:

pip install requests

## ▶️ How to Run

Run the main ETL pipeline using:

python main.py

The pipeline will automatically execute the complete workflow:

Phase 1 → Data Extraction

Phase 2 → Transformation and Quality Validation

Phase 3 → Database Loading

## 📊 Data Quality Process

Before loading data into the production database, the pipeline performs several validation steps.

These include:

- Data type validation
- Required field validation
- Regular expression validation
- Cleaning invalid values
- Detecting anomalous records
- Separating clean and rejected records

Only validated and clean records are loaded into the target database.

## 📝 Logging

The project uses Python logging to provide information about the pipeline execution.

Example:

[PHASE 1] Starting Data Extraction from Remote REST API

Extraction Phase Met. Processing records.

[PHASE 2] Starting Type Casting, Cleaning, and RegEx Validation

Quality Check: Records passed successfully

[PHASE 3] Initializing Database Target and Loading Clean Records

Successfully loaded production rows into database

[SUCCESS] End-to-End ETL Pipeline executed successfully

## 🎯 Project Objective

The main objective of this project is to demonstrate practical implementation of:

- Data Engineering
- ETL Pipeline Automation
- Data Quality Automation
- REST API Integration
- Data Transformation
- Data Validation
- Database Operations
- Python Automation
- Logging and Monitoring

## 🚀 Future Improvements

Some possible future improvements include:

- Adding automated scheduled execution
- Adding more data quality rules
- Adding email or notification alerts
- Adding dashboard-based monitoring
- Adding unit tests
- Adding Docker support
- Adding CI/CD automation
- Supporting multiple data sources and databases

## 👨‍💻 Author

Nikhil Singh

GitHub: nikhil-analytics-24

## 📄 License

This project is created for learning, portfolio, and educational purposes.
