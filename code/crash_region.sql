SELECT region , count(region) FROM occurence
WHERE region NOT LIKE '' 
GROUP BY region
HAVING count(region) > 0
ORDER BY count(region) DESC
