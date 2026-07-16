-- ============================================================================
-- Booking Pace with Window Functions
-- ----------------------------------------------------------------------------
-- Purpose
--   Turn a flat daily bookings feed into a pace view: a running cumulative
--   total, day-over-day change, a 3-day moving average, and a within-region
--   rank of the strongest days. This is the shape a "how are we pacing?"
--   dashboard sits on top of, computed once in SQL instead of in the BI tool.
--
-- Demonstrates: SUM / AVG OVER (... ROWS BETWEEN ...), LAG, RANK, PARTITION BY.
-- Dialect: standard SQL. Verified on SQLite 3.45 via run_samples.py; portable
--          to Postgres, Snowflake, and Oracle unchanged.
-- ============================================================================

SELECT
    region,
    booking_date,
    bookings,

    -- Running cumulative bookings within each region, in date order.
    SUM(bookings) OVER (
        PARTITION BY region ORDER BY booking_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_bookings,

    -- Day-over-day change (NULL on each region's first day).
    bookings - LAG(bookings) OVER (
        PARTITION BY region ORDER BY booking_date
    ) AS day_over_day_change,

    -- Trailing 3-day moving average, smoothing daily noise.
    ROUND(
        AVG(bookings) OVER (
            PARTITION BY region ORDER BY booking_date
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 1
    ) AS moving_avg_3d,

    -- Rank of each day's volume within its region (1 = strongest day).
    RANK() OVER (
        PARTITION BY region ORDER BY bookings DESC
    ) AS rank_in_region
FROM bookings
ORDER BY region, booking_date;
