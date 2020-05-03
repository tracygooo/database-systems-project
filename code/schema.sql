DROP TABLE IF EXISTS covid19 ;
CREATE TABLE covid19 (
    TestDate DATE, 
    County VARCHAR(20), 
    NewPositives INTEGER, 
    CumulativeNumberOfPositives INTEGER, 
    TotalNumberOfTestsPerformed INTEGER,
    CumulativeNumberOfTestsPerformed INTEGER
);
