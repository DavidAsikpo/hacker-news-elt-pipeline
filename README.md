# Hacker News Stories Analytics Pipeline

An end-to-end analytics engineering pipeline that ingests story data from the **Hacker News (Hack Stories) API**, lands it in **S3**, transforms it into analytics-ready marts using **dbt**, orchestrates the workflow with **Airflow**, and ships fully **containerized** with Docker for reproducible deployment and monitoring.

## Overview

This project simulates a production-grade analytics engineering workflow: pulling raw data from an external API, building a tested and documented transformation layer, and delivering trusted business-ready tables for visualization — all wrapped in CI/CD and containerization.

## Architecture

```
Hacker News API → Python Extractor → S3 (raw) → dbt (staging → marts) → Looker Studio
                                          ↑
                                      Airflow (orchestration)
                                          ↑
                                   Docker (containerized)
                                          ↑
                              GitHub Actions (CI on every PR)
```

## Key Features

**Data Ingestion**
- Custom Python extractor pulling raw story data from the Hacker News API
- Built-in error handling and retry logic to ensure ingestion reliability
- Structured data layout in S3 designed for efficient downstream consumption

**Transformation (dbt)**
- Staging, intermediate, and mart layers following dbt best practices
- Business logic marts built specifically to answer stakeholder questions and power Looker Studio dashboards
- Reusable macros to keep transformation logic DRY and consistent across models

**Data Quality & Testing**
- Generic dbt tests (`unique`, `not_null`, `relationships`) applied across all models
- Custom singular tests for business-specific data quality rules
- Tests run automatically via CI on every pull request, preventing bad data logic from merging

**Orchestration**
- Airflow DAG orchestrating the full pipeline: extraction → dbt run → dbt test
- Scheduled runs with task-level visibility into pipeline health and failures

**Documentation & Lineage**
- Auto-generated dbt docs with full column- and model-level lineage graphs
- Transformation logic made transparent and auditable for non-technical stakeholders

**Containerization**
- Entire codebase (extractor, dbt project, Airflow) containerized with Docker
- Enables consistent local development, testing, and deployment environments

## Tech Stack

| Layer | Tools |
|---|---|
| Ingestion | Python, Hacker News API |
| Storage | AWS S3 |
| Transformation | dbt |
| Orchestration | Apache Airflow |
| CI/CD | GitHub Actions |
| Containerization | Docker |
| Visualization | Looker Studio |

## Project Structure

```
.
├── extractor/          # Python scripts for API extraction & S3 loading
├── dbt_project/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   ├── macros/
│   └── tests/
├── dags/                # Airflow DAG definitions
├── docker/               # Dockerfiles & docker-compose
└── .github/workflows/    # CI pipeline running dbt tests on PRs
```

## What This Project Demonstrates

- Building a data pipeline end-to-end, from raw API ingestion through to business-ready marts
- Applying software engineering discipline (testing, CI/CD, version control) to analytics code
- Designing data models around actual stakeholder questions, not just raw table dumps
- Making pipelines observable and auditable through automated documentation and lineage
- Packaging and deploying the full stack reproducibly with Docker

## Getting Started

```bash
# Clone the repo
git clone <repo-url>
cd hacker-news-analytics-pipeline

# Spin up the containerized stack
docker-compose up -d

# Run dbt models
dbt build --profiles-dir ./dbt_project
```

## Future Improvements

- Migrate task-level dbt orchestration to Astronomer Cosmos for model-level lineage inside Airflow
- Add data observability/alerting (Slack notifications on test failures)
- Incremental models for high-volume story tables
