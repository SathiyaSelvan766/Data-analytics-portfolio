Create database copper_data1_db;

SELECT * FROM Copper;

SELECT
  AVG(Close) AS mean_close,
  STDDEV(Close) AS stddev_close
FROM Copper;

SELECT Close AS mode_close
FROM Copper
GROUP BY Close
ORDER BY COUNT(*) DESC
LIMIT 1;

SELECT COUNT(*) AS total_rows
FROM Copper;

SELECT 
    @rownum := @rownum + 1 AS row_num, 
    Close
FROM 
    Copper, (SELECT @rownum := 0) AS r
ORDER BY Close;

SELECT Close AS median
FROM (
    SELECT 
        @rownum := @rownum + 1 AS row_num, 
        Close
    FROM 
        Copper, (SELECT @rownum := 0) AS r
    ORDER BY Close
) AS ordered_rows
WHERE row_num = (SELECT FLOOR(COUNT(*) / 2) + 1 FROM Copper);

UPDATE Copper
SET 
    Open = COALESCE(Open, 3.40),
    High = COALESCE(High, 3.42),
    Low = COALESCE(Low, 3.37),
    Close = COALESCE(Close, 3.40)
WHERE 
    Open IS NULL OR High IS NULL OR Low IS NULL OR Close IS NULL;





SELECT VARIANCE(Close) AS variance
FROM Copper;

SELECT STDDEV(Close) AS standard_deviation
FROM Copper;

SELECT 
    VARIANCE(Close) AS variance,
    STDDEV(Close) AS standard_deviation,
    MAX(Close) - MIN(Close) AS `range`
FROM Copper;

SELECT 
    (COUNT(*) * SUM(POW(Close - (SELECT AVG(Close) FROM Copper), 3))) / 
    (POWER(STDDEV(Close), 3) * (COUNT(*) - 1) * (COUNT(*) - 2)) AS skewness
FROM Copper;

SELECT 
    (COUNT(*) * (COUNT(*) + 1) * SUM(POW(Close - (SELECT AVG(Close) FROM Copper), 4))) / 
    (POWER(STDDEV(Close), 4) * (COUNT(*) - 1) * (COUNT(*) - 2) * (COUNT(*) - 3)) - 
    (3 * POWER(COUNT(*) - 1, 2)) / ((COUNT(*) - 2) * (COUNT(*) - 3)) AS kurtosis
FROM Copper;

-- Create a new table to store the differenced data
CREATE TABLE copper_futures_diff AS
SELECT 
    date,
    close - LAG(close) OVER (ORDER BY date) AS diff_close
FROM Copper;

-- Check the differenced series
SELECT * FROM copper_futures_diff LIMIT 10;

-- Example to create a frequency distribution of 'close' price
SELECT 
    FLOOR(close / 10) * 10 AS price_range, -- Binning prices into 10's
    COUNT(*) AS frequency
FROM Copper
GROUP BY price_range
ORDER BY price_range;

-- Get position for the 25th percentile (Q1)
SELECT FLOOR(COUNT(*) * 0.25) AS Q1_position FROM Copper;

-- Get position for the 75th percentile (Q3)
SELECT FLOOR(COUNT(*) * 0.75) AS Q3_position FROM Copper;

-- Get Q1 (25th percentile) value
SELECT close
FROM Copper
ORDER BY close
LIMIT 1 OFFSET 10;  -- Replace 10 with the actual Q1 position

-- Get Q3 (75th percentile) value
SELECT close
FROM Copper
ORDER BY close
LIMIT 1 OFFSET 30;  -- Replace 30 with the actual Q3 position

-- Using the previously calculated Q1 and Q3 values, let's calculate IQR
WITH IQR AS (
    SELECT 
        -- Replace these with actual Q1 and Q3 values
        45 AS Q1,   -- Replace 45 with the actual Q1 value
        80 AS Q3    -- Replace 80 with the actual Q3 value
)
SELECT 
    date,
    close,
    CASE 
        WHEN close < (Q1 - 1.5 * (Q3 - Q1)) OR close > (Q3 + 1.5 * (Q3 - Q1)) THEN 'Outlier'
        ELSE 'Normal'
    END AS outlier_status
FROM Copper, IQR;



