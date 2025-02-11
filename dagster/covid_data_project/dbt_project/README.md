# COVID-19 Data Analysis

## Setup Instructions
1. Ensure PostgreSQL is running and accessible.
2. Set environment variables for database connection.
3. Run Dagster to materialize assets.
4. Execute `dbt deps` and `dbt run` to build models.

## Design Decisions
- **Data Ingestion**: Handled by Dagster assets.
- **Data Processing**: dbt models clean and deduplicate data.
- **Data Storage**: PostgreSQL for relational data storage.
- **Data Analysis**: dbt models for complex queries.

## Analysis Questions
1. **Top 5 Countries**: See `top_5_countries` model.
2. **Confirmed Cases Over Time**: See `confirmed_over_time` model.
3. **Correlation Analysis**: See `correlation_analysis` model.

## Technologies Used
- Dagster for orchestration
- dbt for data transformation
- PostgreSQL for data storage
- Docker for containerization 