import psycopg2

class functions():
    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)
    # rank number of new positive cases in a specified period
    def rank_new_positive(self, from_date, to_date, limit):        
        query = '''SELECT county, SUM(newpositives) 
        FROM covid19 WHERE testdate > '%s' AND testdate < '%s' 
        GROUP BY county 
        ORDER BY sum(newpositives) DESC LIMIT '%s';'''%(from_date,to_date,limit)
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    def positive_ratio(self, from_date, to_date, county):
        
        query = '''
        SELECT cast(sum(newpositives)::NUMERIC/sum(totalnumberoftestsperformed) as decimal(10,2))
        FROM covid19
        WHERE TestDATE > '%s' 
        AND TestDATE < '%s'
        AND County = '%s';       
        '''%(from_date,to_date,county)
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()[0][0]
        
    #rank crash factor frequencies   
    def rank_crash_factor(self,limit):        
        query = '''SELECT factor1,num1+num2+num3+num4+num5 num
        FROM
        (SELECT DISTINCT factor1,count(factor1) num1
        FROM factor
        GROUP BY factor1 
        ) a,
        (SELECT DISTINCT factor2,count(factor2) num2
        FROM factor
        GROUP BY factor2) b,
        (SELECT DISTINCT factor3,count(factor3) num3
        FROM factor
        GROUP BY factor3) c,
        (SELECT DISTINCT factor4,count(factor4) num4
        FROM factor
        GROUP BY factor4) d,
        (SELECT DISTINCT factor5,count(factor5) num5
        FROM factor
        GROUP BY factor5) e
        WHERE factor1 = factor2
        AND factor2 = factor3
        AND factor3 = factor4
        AND factor4 = factor5
        ORDER BY num DESC LIMIT '%s';'''%(limit)
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()    
        
    #crash per day in each weather
    def crash_weather(self, weather):
        query = '''SELECT num1/num2 ratio
        FROM(
        SELECT count(measure_date) num1
        FROM weatherType, occurence
        WHERE crashdate = measure_date
        AND %s = TRUE) a,
        (SELECT count(measure_date) num2
        FROM weatherType
        WHERE %s = TRUE) b;
        '''%(weather,weather)
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            self.conn.commit()
            return cursor.fetchone()[0]
 


if __name__ == '__main__':
    funcs = functions("host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'")
    L = funcs.rank_new_positive('2020-4-20','2020-4-25',5)
    print(L)
    L = funcs.positive_ratio('2020-3-2','2020-3-20','Albany')
    print('positive ratio: '+str(L))
    
    L = funcs.rank_crash_factor(10)
    print(L)
    print()
    L = funcs.crash_weather('is_snowy')
    print('average num of crash in a snowy day is:'+str(L))
    print()
    
    