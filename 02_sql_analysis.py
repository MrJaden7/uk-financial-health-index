import sqlite3
import pandas as pd
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 120)
pd.set_option('display.float_format', '{:.2f}'.format)

# load the master dataset into an in-memory sqlite database
df = pd.read_csv('data/clean/uk_fhi_master_final.csv')
conn = sqlite3.connect(':memory:')
df.to_sql('financial_health', conn, index=False, if_exists='replace')
os.makedirs('outputs', exist_ok=True)

print(f"loaded {len(df)} rows into sqlite\n")


def run_query(label, sql, save_as=None):
    print(f"--- {label} ---")
    result = pd.read_sql_query(sql, conn)
    print(result.to_string(index=False))
    if save_as:
        result.to_csv(f'outputs/{save_as}', index=False)
    print()
    return result


# which regions are healthiest in 2024?
run_query("regional ranking 2024", """
    SELECT region,
        ROUND(AVG(financial_health_index), 1) AS avg_fhi,
        ROUND(MIN(financial_health_index), 1) AS worst_la,
        ROUND(MAX(financial_health_index), 1) AS best_la,
        ROUND(AVG(employment_rate), 1)         AS avg_employment_pct,
        ROUND(AVG(unemployment_rate), 1)       AS avg_unemployment_pct,
        ROUND(AVG(median_savings_gbp), 0)      AS avg_median_savings,
        COUNT(DISTINCT la_name)                AS num_las
    FROM financial_health
    WHERE year = 2024
    GROUP BY region
    ORDER BY avg_fhi DESC
""", "q1_regional_ranking_2024.csv")


# did the rate hike cycle hurt some regions more than others?
run_query("rate hike impact: 2020 vs 2023", """
    WITH pre AS (
        SELECT region,
            ROUND(AVG(financial_health_index), 2) AS fhi_2020,
            ROUND(AVG(median_savings_gbp), 0)      AS savings_2020
        FROM financial_health
        WHERE year = 2020
        GROUP BY region
    ),
    post AS (
        SELECT region,
            ROUND(AVG(financial_health_index), 2) AS fhi_2023,
            ROUND(AVG(median_savings_gbp), 0)      AS savings_2023
        FROM financial_health
        WHERE year = 2023
        GROUP BY region
    )
    SELECT
        p.region,
        p.fhi_2020,
        h.fhi_2023,
        ROUND(h.fhi_2023 - p.fhi_2020, 2)         AS fhi_change,
        p.savings_2020,
        h.savings_2023,
        ROUND(h.savings_2023 - p.savings_2020, 0)  AS savings_change
    FROM pre p
    JOIN post h ON p.region = h.region
    ORDER BY fhi_change ASC
""", "q2_rate_hike_impact.csv")


# top 10 healthiest local authorities
run_query("top 10 local authorities 2024", """
    SELECT la_name, region,
        ROUND(financial_health_index, 1) AS fhi,
        ROUND(employment_rate, 1)         AS employment_pct,
        ROUND(unemployment_rate, 1)       AS unemployment_pct,
        ROUND(median_savings_gbp, 0)      AS median_savings,
        ROUND(pct_zero_savings, 1)        AS pct_zero_savings
    FROM financial_health
    WHERE year = 2024
    ORDER BY financial_health_index DESC
    LIMIT 10
""", "q3a_top10_las_2024.csv")


# bottom 10 most stressed local authorities
run_query("bottom 10 local authorities 2024", """
    SELECT la_name, region,
        ROUND(financial_health_index, 1) AS fhi,
        ROUND(employment_rate, 1)         AS employment_pct,
        ROUND(unemployment_rate, 1)       AS unemployment_pct,
        ROUND(median_savings_gbp, 0)      AS median_savings,
        ROUND(pct_zero_savings, 1)        AS pct_zero_savings
    FROM financial_health
    WHERE year = 2024
      AND unemployment_rate IS NOT NULL
    ORDER BY financial_health_index ASC
    LIMIT 10
""", "q3b_bottom10_las_2024.csv")


# how big is the north-south gap and is it getting worse?
run_query("north south divide over time", """
    WITH grouped AS (
        SELECT year, la_name,
            CASE
                WHEN region IN ('London', 'South East', 'South West', 'East of England')
                    THEN 'South'
                WHEN region IN ('North East', 'North West', 'Yorkshire and The Humber')
                    THEN 'North'
                ELSE 'Midlands / Devolved'
            END AS area_group,
            financial_health_index,
            employment_rate,
            median_savings_gbp,
            pct_zero_savings
        FROM financial_health
    )
    SELECT
        year,
        area_group,
        ROUND(AVG(financial_health_index), 1) AS avg_fhi,
        ROUND(AVG(employment_rate), 1)         AS avg_employment_pct,
        ROUND(AVG(median_savings_gbp), 0)      AS avg_median_savings,
        ROUND(AVG(pct_zero_savings), 1)        AS avg_pct_zero_savings,
        COUNT(DISTINCT CASE WHEN financial_health_index < 25 THEN la_name END) AS deprived_las
    FROM grouped
    GROUP BY year, area_group
    ORDER BY year, avg_fhi DESC
""", "q4_north_south_divide.csv")


# where are people most exposed with no savings buffer?
run_query("zero savings rates by region", """
    SELECT region,
        ROUND(AVG(CASE WHEN year = 2020 THEN pct_zero_savings END), 1) AS pct_2020,
        ROUND(AVG(CASE WHEN year = 2022 THEN pct_zero_savings END), 1) AS pct_2022,
        ROUND(AVG(CASE WHEN year = 2024 THEN pct_zero_savings END), 1) AS pct_2024,
        ROUND(
            AVG(CASE WHEN year = 2024 THEN pct_zero_savings END) -
            AVG(CASE WHEN year = 2020 THEN pct_zero_savings END),
        1) AS change,
        ROUND(AVG(CASE WHEN year = 2024 THEN median_savings_gbp END), 0) AS median_savings_2024
    FROM financial_health
    GROUP BY region
    ORDER BY pct_2024 DESC
""", "q5_zero_savings_hotspots.csv")


# fhi vs bank rate - does the macro environment affect all regions equally?
run_query("fhi vs bank rate by region", """
    SELECT
        year,
        base_rate,
        ROUND(AVG(financial_health_index), 1) AS uk_avg,
        ROUND(AVG(CASE WHEN region = 'North East' THEN financial_health_index END), 1) AS north_east,
        ROUND(AVG(CASE WHEN region = 'London' THEN financial_health_index END), 1)     AS london,
        ROUND(AVG(CASE WHEN region = 'South East' THEN financial_health_index END), 1) AS south_east,
        ROUND(AVG(CASE WHEN region = 'Wales' THEN financial_health_index END), 1)      AS wales,
        ROUND(AVG(CASE WHEN region = 'Yorkshire and The Humber'
                       THEN financial_health_index END), 1)                            AS yorkshire
    FROM financial_health
    GROUP BY year, base_rate
    ORDER BY year
""", "q6_rate_sensitivity_timeline.csv")


# worst 3 local authorities within each region - uses window functions
run_query("worst 3 las per region", """
    WITH ranked AS (
        SELECT
            la_name,
            region,
            ROUND(financial_health_index, 1) AS fhi,
            ROUND(AVG(financial_health_index) OVER (PARTITION BY region), 1)    AS region_avg,
            ROUND(financial_health_index -
                  AVG(financial_health_index) OVER (PARTITION BY region), 1)    AS vs_avg,
            RANK() OVER (PARTITION BY region ORDER BY financial_health_index ASC) AS rnk
        FROM financial_health
        WHERE year = 2024
          AND financial_health_index IS NOT NULL
    )
    SELECT * FROM ranked
    WHERE rnk <= 3
    ORDER BY region, rnk
""", "q7_worst_per_region_2024.csv")


# areas with high employment but low savings - the working poor problem
run_query("working poor: high employment low savings", """
    SELECT
        la_name,
        region,
        ROUND(employment_rate, 1)        AS employment_pct,
        ROUND(unemployment_rate, 1)      AS unemployment_pct,
        ROUND(median_savings_gbp, 0)     AS median_savings,
        ROUND(pct_zero_savings, 1)       AS pct_zero_savings,
        ROUND(financial_health_index, 1) AS fhi,
        CASE
            WHEN employment_rate > 72 AND median_savings_gbp < 2500 THEN 'working poor risk'
            WHEN employment_rate > 72 AND median_savings_gbp >= 2500 THEN 'stable'
            WHEN employment_rate <= 72 AND median_savings_gbp < 2500 THEN 'high risk'
            ELSE 'employment gap'
        END AS risk_category
    FROM financial_health
    WHERE year = 2024
      AND unemployment_rate IS NOT NULL
    ORDER BY
        CASE
            WHEN employment_rate > 72 AND median_savings_gbp < 2500 THEN 0
            WHEN employment_rate <= 72 AND median_savings_gbp < 2500 THEN 1
            ELSE 2
        END,
        median_savings_gbp ASC
    LIMIT 20
""", "q8_working_poor_analysis.csv")


# year on year change using lag - which areas declined most consistently?
run_query("year on year fhi change", """
    WITH yoy AS (
        SELECT
            la_name,
            region,
            year,
            financial_health_index AS fhi,
            financial_health_index - LAG(financial_health_index)
                OVER (PARTITION BY la_name ORDER BY year) AS yoy_change
        FROM financial_health
        WHERE financial_health_index IS NOT NULL
    ),
    summary AS (
        SELECT
            la_name,
            region,
            ROUND(AVG(yoy_change), 2)  AS avg_annual_change,
            ROUND(SUM(yoy_change), 2)  AS total_change,
            COUNT(CASE WHEN yoy_change < 0 THEN 1 END) AS years_declined,
            COUNT(CASE WHEN yoy_change > 0 THEN 1 END) AS years_improved,
            ROUND(MIN(yoy_change), 2)  AS worst_year,
            ROUND(MAX(yoy_change), 2)  AS best_year
        FROM yoy
        WHERE yoy_change IS NOT NULL
        GROUP BY la_name, region
    )
    SELECT * FROM summary
    ORDER BY total_change ASC
    LIMIT 15
""", "q9_yoy_declining_las.csv")


# headline numbers
run_query("headline stats", """
    SELECT 'uk average fhi 2024' AS metric,
        ROUND(AVG(CASE WHEN year = 2024 THEN financial_health_index END), 1) AS value
    FROM financial_health
    UNION ALL SELECT 'uk average fhi 2020',
        ROUND(AVG(CASE WHEN year = 2020 THEN financial_health_index END), 1)
    FROM financial_health
    UNION ALL SELECT 'fhi change 2020 to 2024',
        ROUND(AVG(CASE WHEN year = 2024 THEN financial_health_index END) -
              AVG(CASE WHEN year = 2020 THEN financial_health_index END), 1)
    FROM financial_health
    UNION ALL SELECT 'las below fhi 25 in 2024',
        COUNT(DISTINCT CASE WHEN year = 2024 AND financial_health_index < 25 THEN la_name END)
    FROM financial_health
    UNION ALL SELECT 'las above fhi 75 in 2024',
        COUNT(DISTINCT CASE WHEN year = 2024 AND financial_health_index > 75 THEN la_name END)
    FROM financial_health
    UNION ALL SELECT 'gap best vs worst la 2024',
        ROUND(MAX(CASE WHEN year = 2024 THEN financial_health_index END) -
              MIN(CASE WHEN year = 2024 THEN financial_health_index END), 1)
    FROM financial_health
    UNION ALL SELECT 'median savings 2020',
        ROUND(AVG(CASE WHEN year = 2020 THEN median_savings_gbp END), 0)
    FROM financial_health
    UNION ALL SELECT 'median savings 2024',
        ROUND(AVG(CASE WHEN year = 2024 THEN median_savings_gbp END), 0)
    FROM financial_health
    UNION ALL SELECT 'pct zero savings 2020',
        ROUND(AVG(CASE WHEN year = 2020 THEN pct_zero_savings END), 1)
    FROM financial_health
    UNION ALL SELECT 'pct zero savings 2024',
        ROUND(AVG(CASE WHEN year = 2024 THEN pct_zero_savings END), 1)
    FROM financial_health
    UNION ALL SELECT 'peak bank rate 2023',
        MAX(CASE WHEN year = 2023 THEN base_rate END)
    FROM financial_health
    UNION ALL SELECT 'total local authorities',
        COUNT(DISTINCT la_name)
    FROM financial_health
""", "q10_executive_summary.csv")


conn.close()
print("done - results saved to outputs/")