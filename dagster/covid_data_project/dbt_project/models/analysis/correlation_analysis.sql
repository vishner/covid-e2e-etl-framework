{{ config(materialized='table') }}

SELECT
    CORR(confirmed, deaths) AS correlation_confirmed_deaths
FROM {{ ref('cleaned_us_reports') }} 