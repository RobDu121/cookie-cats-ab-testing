-- Question 1: How many players belong to each experimental group?
SELECT version, COUNT(version) AS [Number of players]
FROM cookie_cats
GROUP BY(version)

--Question 2: What is the average number of game rounds played by each group?
SELECT version, AVG(sum_gamerounds)
FROM cookie_cats 
GROUP BY(version)


--Question 3: What percentage of players in each group returned after one day?
SELECT version,
	ROUND(
		AVG(
			CASE
				WHEN LOWER(CAST(retention_1 AS TEXT)) IN ('true', '1') THEN 1.0
				ELSE 0.0
			END
			)*100
		) AS retention_percentage
FROM cookie_cats
GROUP BY(version)

--Question 4: What percentage of players in each group returned after seven days?
SELECT version,
	ROUND(
		AVG(
			CASE
				WHEN LOWER(CAST(retention_7 AS TEXT)) IN ('true', '1') THEN 1.0
				ELSE 0.0
			END
			)*100
		,2) AS retention_percentage
FROM cookie_cats
GROUP BY(version)

--Question 5: Write a querry that returns The experimental group (version),  
--the total number of players,
--the number of players who returned after 1 day,
--the number of players who returned after 7 days,
--The Day 1 retention percentage, rounded to two decimal places,
--The Day 7 retention percentage, rounded to two decimal places

SELECT version, 
	COUNT(version) AS [Total Number of Players],
--Change TRUE and FALSE into 1 and 0, sum to find # of trues, i.e the number that returned
	SUM(CASE 
		WHEN LOWER(CAST(retention_1 AS TEXT)) IN ('true', '1') THEN 1.0
		ELSE 0.0
	END) AS [Total Number of Players that Returned After 1 Day],
--Change TRUE and FALSE into 1 and 0, sum to find # of trues, i.e the number that returned
	SUM(CASE 
		WHEN LOWER(CAST(retention_7 AS TEXT)) IN ('true', '1') THEN 1.0
		ELSE 0.0
	END) AS [Total Number of Players that Returned After 7 Days],
--Change TRUE and FALSE into 1 and 0, AVG to find percent that returned
	ROUND(
		AVG(
			CASE
				WHEN LOWER(CAST(retention_1 AS TEXT)) IN ('true', '1') THEN 1.0
				ELSE 0.0
			END
			)*100
		,2) AS retention_percentage_1,
--Change TRUE and FALSE into 1 and 0, AVG to find percent that returned
	ROUND(
		AVG(
			CASE
				WHEN LOWER(CAST(retention_7 AS TEXT)) IN ('true', '1') THEN 1.0
				ELSE 0.0
			END
			)*100
		,2) AS retention_percentage_7
FROM cookie_cats
GROUP BY(version);

--Question 6: Calculate the difference in Day 7 retention between gate_30 and gate_40.

WITH retention_rates AS (
    SELECT
        AVG(
            CASE
                WHEN version = 'gate_30' THEN
                    CASE
                        WHEN LOWER(CAST(retention_7 AS TEXT))
                             IN ('true', '1') THEN 1.0
                        ELSE 0.0
                    END
                ELSE NULL
            END
        ) * 100 AS gate_30_retention,

        AVG(
            CASE
                WHEN version = 'gate_40' THEN
                    CASE
                        WHEN LOWER(CAST(retention_7 AS TEXT))
                             IN ('true', '1') THEN 1.0
                        ELSE 0.0
                    END
                ELSE NULL
            END
        ) * 100 AS gate_40_retention

    FROM cookie_cats
)

SELECT
    ROUND(gate_30_retention, 2) AS gate_30_retention,
    ROUND(gate_40_retention, 2) AS gate_40_retention,
    ROUND(
        gate_30_retention - gate_40_retention,
        2
    ) AS difference
FROM retention_rates;

--Question 7: Investigate game rounds
SELECT version,
	COUNT(*) AS [Number of Players], 
	ROUND(AVG(sum_gamerounds),2) AS [Average Gamerounds], 
	MAX(sum_gamerounds) AS [Max Rounds],
	SUM(CASE
			WHEN sum_gamerounds = 0 THEN 1
			ELSE 0
		END
		) AS [Total number of players that completed 0 rounds]
FROM cookie_cats
GROUP BY(version)

--Question 8: Find the top 5 players with the most games played
SELECT userid, version, sum_gamerounds
FROM cookie_cats
ORDER BY(sum_gamerounds) DESC 
LIMIT 5

--Question 9: Find the Average without the outlier
SELECT version, AVG(sum_gamerounds) AS [Average game rounds]
FROM cookie_cats
WHERE userid != 6390605
GROUP BY(version)
