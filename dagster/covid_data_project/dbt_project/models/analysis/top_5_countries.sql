{{ config(materialized='table') }}

SELECT
    country_region,
    COUNT(*) AS frequency
FROM {{ ref('cleaned_global_reports') }}
GROUP BY country_region
ORDER BY frequency DESC
LIMIT 5 