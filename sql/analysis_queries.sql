-- SQL Analytical Queries for Diabetes Dataset
-- Run these queries on the diabetes_clean table in PostgreSQL

-- Query 1: Average glucose level by age groups
-- Shows how glucose levels vary across different age ranges
SELECT 
    CASE 
        WHEN age < 0.5 THEN '0-30'  -- Remember: age is normalized
        WHEN age < 1.0 THEN '30-50'
        WHEN age < 1.5 THEN '50-70'
        ELSE '70+'
    END AS age_group,
    COUNT(*) as patient_count,
    AVG(blood_glucose_level) as avg_glucose,
    AVG(hba1c_level) as avg_hba1c,
    SUM(CASE WHEN diabetes = 1 THEN 1 ELSE 0 END) as diabetes_cases
FROM diabetes_clean
GROUP BY age_group
ORDER BY age_group;

-- Query 2: BMI distribution by diabetes status
-- Analyzes BMI patterns between diabetic and non-diabetic patients
SELECT 
    diabetes,
    COUNT(*) as total_patients,
    AVG(bmi) as avg_bmi,
    MIN(bmi) as min_bmi,
    MAX(bmi) as max_bmi,
    STDDEV(bmi) as bmi_std_dev,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY bmi) as median_bmi
FROM diabetes_clean
GROUP BY diabetes
ORDER BY diabetes;

-- Query 3: Correlation analysis - Risk factors vs Diabetes
-- Shows percentage of diabetic patients for each risk factor
SELECT 
    'Hypertension' as risk_factor,
    hypertension as has_condition,
    COUNT(*) as total_patients,
    SUM(CASE WHEN diabetes = 1 THEN 1 ELSE 0 END) as diabetic_patients,
    ROUND(100.0 * SUM(CASE WHEN diabetes = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as diabetes_percentage
FROM diabetes_clean
GROUP BY hypertension

UNION ALL

SELECT 
    'Heart Disease' as risk_factor,
    heart_disease as has_condition,
    COUNT(*) as total_patients,
    SUM(CASE WHEN diabetes = 1 THEN 1 ELSE 0 END) as diabetic_patients,
    ROUND(100.0 * SUM(CASE WHEN diabetes = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as diabetes_percentage
FROM diabetes_clean
GROUP BY heart_disease

ORDER BY risk_factor, has_condition;

-- Query 4: Diabetes prevalence by age groups and gender
-- Percentage of diabetic patients segmented by age and gender
SELECT 
    gender,
    CASE 
        WHEN age < 0.5 THEN '0-30'
        WHEN age < 1.0 THEN '30-50'
        WHEN age < 1.5 THEN '50-70'
        ELSE '70+'
    END AS age_group,
    COUNT(*) as total_patients,
    SUM(CASE WHEN diabetes = 1 THEN 1 ELSE 0 END) as diabetic_count,
    ROUND(100.0 * SUM(CASE WHEN diabetes = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as diabetes_rate
FROM diabetes_clean
GROUP BY gender, age_group
ORDER BY gender, age_group;

-- Query 5: Extreme values and outliers detection
-- Identifies patients with extreme health metrics
SELECT 
    'High Glucose' as category,
    COUNT(*) as patient_count,
    AVG(age) as avg_age,
    AVG(bmi) as avg_bmi,
    SUM(CASE WHEN diabetes = 1 THEN 1 ELSE 0 END) as diabetic_patients
FROM diabetes_clean
WHERE blood_glucose_level > (SELECT AVG(blood_glucose_level) + 2 * STDDEV(blood_glucose_level) FROM diabetes_clean)

UNION ALL

SELECT 
    'High BMI' as category,
    COUNT(*) as patient_count,
    AVG(age) as avg_age,
    AVG(bmi) as avg_bmi,
    SUM(CASE WHEN diabetes = 1 THEN 1 ELSE 0 END) as diabetic_patients
FROM diabetes_clean
WHERE bmi > (SELECT AVG(bmi) + 2 * STDDEV(bmi) FROM diabetes_clean)

UNION ALL

SELECT 
    'High HbA1c' as category,
    COUNT(*) as patient_count,
    AVG(age) as avg_age,
    AVG(bmi) as avg_bmi,
    SUM(CASE WHEN diabetes = 1 THEN 1 ELSE 0 END) as diabetic_patients
FROM diabetes_clean
WHERE hba1c_level > (SELECT AVG(hba1c_level) + 2 * STDDEV(hba1c_level) FROM diabetes_clean);
