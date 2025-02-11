{{ config(materialized='table') }}

WITH deduplicated AS (
    SELECT DISTINCT ON (combined_key, report_date) *
    FROM {{ source('dlt_raw', 'csse_covid_19_daily_reports') }}
    ORDER BY combined_key, report_date DESC, last_update DESC
)

SELECT
    province_state,
    country_region,
    CAST(last_update AS DATE) AS last_update,
    lat,
    longx,
    confirmed,
    deaths,
    recovered,
    active,
    combined_key,
    CAST(report_date AS DATE) AS report_date
FROM deduplicated
WHERE confirmed IS NOT NULL 