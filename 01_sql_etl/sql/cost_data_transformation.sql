-- ============================================================================
-- Cost Data Transformation
-- ----------------------------------------------------------------------------
-- Purpose
--   Normalize raw, multi-row cost data into one enriched row per source record,
--   deriving the standard financial fields a reporting layer expects: gross
--   cost, net cost, cost adjustments, and cost discounts. Source-system quirks
--   (SYSTEM_A and SYSTEM_B encode discounts differently) are reconciled here so
--   the reporting layer never has to know about them.
--
-- Grain
--   Input:  many rows per service_no (one row per cost component).
--   Output: the same rows, enriched with derived measures and lookup labels.
--
-- Example (service_no 123)
--   | inventory_category | total_revenue |
--   | BASE               |   100         |
--   | ADJUSTMENT         |   -20         |
--   | PROMOTIONS         |   -10         |
--
-- Dialect: standard SQL. Verified on SQLite 3.45 via run_samples.py; the logic
--          below is portable to Postgres, Snowflake, and Oracle unchanged.
-- ============================================================================

WITH transformed_cost_data AS (
    SELECT
        base.*,

        -- Gross cost: positive contribution only.
        CASE WHEN base.total_revenue >= 0 THEN base.total_revenue ELSE 0 END
            AS gross_cost,

        -- Net cost: the signed value as-is.
        base.total_revenue AS net_cost,

        -- Cost adjustments: negative, non-promotional corrections.
        CASE
            WHEN base.total_revenue < 0
                 AND UPPER(base.inventory_category) NOT LIKE '%PROMOTIONS%'
            THEN base.total_revenue
            ELSE 0
        END AS cost_adjustments,

        -- Cost discounts: promotional reductions, reconciled across systems.
        --   SYSTEM_A carries the discount inline as a negative revenue row.
        --   SYSTEM_B carries it in a separate extracted_discount column.
        CASE
            WHEN base.source_system = 'SYSTEM_A'
                 AND base.total_revenue < 0
                 AND UPPER(base.inventory_category) LIKE '%PROMOTIONS%'
            THEN base.total_revenue
            WHEN base.source_system = 'SYSTEM_B'
                 AND UPPER(base.inventory_category) LIKE '%PROMOTIONS%'
                 AND base.extracted_discount IS NOT NULL
            THEN base.extracted_discount
            ELSE 0
        END AS cost_discounts,

        -- Standardized discount label. Defined here so the final COALESCE has a
        -- real column to fall back from. In the original script this column was
        -- referenced downstream but never created, so the query would not run.
        CASE
            WHEN UPPER(base.inventory_category) LIKE '%PROMOTIONS%' THEN 'DISCOUNT'
            ELSE NULL
        END AS discount_inventory_category
    FROM raw_cost_data base
)

SELECT
    tc.*,
    loc.location_print_name       AS service_location_name,
    emp.full_name,
    emp.team_name,
    -- Consolidated category: the standardized discount label when present,
    -- otherwise the row's own inventory category.
    COALESCE(tc.discount_inventory_category, tc.inventory_category)
        AS consolidated_inventory_category,
    home_loc.location_print_name  AS home_location_name
FROM transformed_cost_data tc
LEFT JOIN locations loc
    ON tc.location_code = loc.location_code
LEFT JOIN employee_info emp
    ON tc.inserted_by = emp.login_id
LEFT JOIN account_location acct
    ON tc.account_no = acct.account_no
LEFT JOIN locations home_loc
    ON acct.location_code = home_loc.location_code
WHERE
    UPPER(tc.inventory_category) NOT LIKE '%SETTLEMENT%'
    AND UPPER(tc.inventory_category) NOT LIKE '%SPECIAL PROMOTIONS%';
