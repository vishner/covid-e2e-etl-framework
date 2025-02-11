### Running the Project

1. **Start Docker Containers**:
   ```bash
   docker-compose up
   ```

2. **Access Dagster UI**:
   Open your browser and go to `http://localhost:3000` to access the Dagster UI.

3. **Run the Pipeline**:
   - The `covid_etl` job is scheduled to run daily. You can also trigger it manually from the Dagster UI by clicking on the job and then clicking the
   Launchpad tab, and then clicking the "Launch Run" button.



## Design Decisions

- **Data Ingestion**: Handled by Dagster assets, ensuring data is loaded into PostgreSQL.
- **Data Processing**: dbt models clean and transform the data, handling inconsistencies.
- **Data Storage**: PostgreSQL is used for efficient querying and analysis.
- **Data Analysis**: dbt models provide insights through complex queries.

## Analysis Questions

1. **Top 5 Countries**: See `top_5_countries` model.
2. **Confirmed Cases Over Time**: See `confirmed_over_time` model.
3. **Correlation Analysis**: See `correlation_analysis` model.

## Technologies Used

- **Dagster**: For orchestration and data pipeline management.
- **dbt**: For data transformation and modeling.
- **PostgreSQL**: For relational data storage.
- **Docker**: For containerization and environment setup.

## Troubleshooting

- Ensure all environment variables are set correctly.
- Check Docker logs for any errors during container startup.
- Verify database connectivity and credentials.

## Future Improvements

- Implement more complex data analysis models.
- Explore additional data sources for richer analysis.