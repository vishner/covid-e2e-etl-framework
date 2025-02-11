{{ config(materialized='table') }}

WITH deduplicated AS (
    SELECT DISTINCT ON (uid, report_date) *
    FROM {{ source('dlt_raw', 'csse_covid_19_daily_reports_us') }}
    ORDER BY uid, report_date DESC, last_update DESC
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
    fips,
    incident_rate,
    total_test_results,
    people_hospitalized,
    case_fatality_ratio,
    uid,
    iso3,
    testing_rate,
    hospitalization_rate,
    CAST("date" AS DATE) AS "date",
    people_tested,
    mortality_rate,
    CAST(report_date AS DATE) AS report_date
FROM deduplicated
WHERE confirmed IS NOT NULL 