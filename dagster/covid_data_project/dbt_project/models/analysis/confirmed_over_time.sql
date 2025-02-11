{{ config(materialized='table') }}

SELECT
    report_date,
    SUM(confirmed) AS total_confirmed
FROM {{ ref('cleaned_global_reports') }}
GROUP BY report_date
ORDER BY report_date 