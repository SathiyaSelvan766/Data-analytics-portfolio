CREATE DATABASE IF NOT EXISTS Garbha_IVF_DB;
USE Garbha_IVF_DB;




CREATE TABLE IVF_Treatments (
    Patient_ID INT PRIMARY KEY,
    Presentation_Date DATE,
    Age INT,
    Religion VARCHAR(50),
    Tribe VARCHAR(50),
    Parity INT,
    Menses_Regular VARCHAR(10),
    BMI DECIMAL(5,2),
    Serum_FSH DECIMAL(10,2),
    Serum_AMH DECIMAL(10,2),
    Antral_Follicle_Count INT,
    Oocytes_Retrieved INT,
    Method_of_Fertilization VARCHAR(50),
    Embryos_Transferred INT,
    Outcome VARCHAR(50), -- e.g., 'Pregnancy', 'No Pregnancy', 'Cancelled'
    Pregnancy_Outcome VARCHAR(50),
    Complications VARCHAR(255)
);


#Calculate Overall Success Rate (Pregnancy Rate)
SELECT 
    COUNT(*) AS Total_Cycles,
    SUM(CASE WHEN Outcome = 'Pregnancy' THEN 1 ELSE 0 END) AS Successes,
    (SUM(CASE WHEN Outcome = 'Pregnancy' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS Success_Rate_Percentage
FROM IVF_Treatments;


#Average Age and AMH for Success vs. Failure
SELECT 
    Outcome, 
    AVG(Age) AS Avg_Age, 
    AVG(Serum_AMH) AS Avg_AMH,
    COUNT(*) AS Total_Patients
FROM IVF_Treatments
WHERE Outcome IN ('Pregnancy', 'No Pregnancy')
GROUP BY Outcome;

#Success Rate by Age Group
SELECT 
    CASE 
        WHEN Age < 30 THEN 'Under 30'
        WHEN Age BETWEEN 30 AND 35 THEN '30-35'
        WHEN Age BETWEEN 36 AND 40 THEN '36-40'
        ELSE 'Over 40'
    END AS Age_Group,
    COUNT(*) AS Total_Cases,
    SUM(CASE WHEN Outcome = 'Pregnancy' THEN 1 ELSE 0 END) AS Successes
FROM IVF_Treatments
GROUP BY Age_Group;

#Handle Missing BMI Data (Imputation with Average)
UPDATE IVF_Treatments
SET BMI = (SELECT AVG(BMI) FROM IVF_Treatments WHERE BMI IS NOT NULL)
WHERE BMI IS NULL;

#Create a Success Flag
-- First, add the column
ALTER TABLE IVF_Treatments ADD COLUMN Success_Flag INT;

-- Then, update based on Outcome
UPDATE IVF_Treatments
SET Success_Flag = CASE WHEN Outcome = 'Pregnancy' THEN 1 ELSE 0 END;

#Categorize Ovarian Reserve
ALTER TABLE IVF_Treatments ADD COLUMN Ovarian_Reserve_Status VARCHAR(20);

UPDATE IVF_Treatments
SET Ovarian_Reserve_Status = CASE 
    WHEN Serum_AMH < 5 THEN 'Low'
    WHEN Serum_AMH BETWEEN 5 AND 15 THEN 'Normal'
    WHEN Serum_AMH > 15 THEN 'High/PCOS Risk'
    ELSE 'Unknown'
END;

#Complications Tracking
SELECT Complications, COUNT(*) as Occurrences
FROM IVF_Treatments
WHERE Complications IS NOT NULL AND Complications != 'None'
GROUP BY Complications
ORDER BY Occurrences DESC;

