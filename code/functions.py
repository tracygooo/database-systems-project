import psycopg2

class functions():
    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)
    # rank number of new positive cases in a specified period
    def rank_new_positive(self, from_date, to_date, limit):        
        query = '''SELECT county, SUM(newpositives) 
        FROM covid19 WHERE testdate > %s AND testdate < %s 
        GROUP BY county 
        ORDER BY sum(newpositives) DESC LIMIT %s;'''
        with self.conn.cursor() as cursor:
            cursor.execute(query,(str(from_date),str(to_date),str(limit)))
            return cursor.fetchall()
    def positive_ratio(self, from_date, to_date, county):
        query = '''
        SELECT cast(sum(newpositives)::NUMERIC/sum(totalnumberoftestsperformed) as decimal(10,2))
        FROM covid19
        WHERE TestDATE > %s 
        AND TestDATE < %s
        AND County = %s;       
        '''
        with self.conn.cursor() as cursor:
            cursor.execute(query,(str(from_date),str(to_date),str(county)))
            return cursor.fetchall()[0][0]
        
    #rank the most common crash factors    
    def rank_crash_factor(self,limit):        
        query = '''SELECT DISTINCT(a.factor),count(collision_id) rank
                    FROM factor,(
                    SELECT DISTINCT factor1 as factor
                    FROM factor
                    GROUP BY factor1
                    UNION
                    SELECT DISTINCT factor2
                    FROM factor
                    GROUP BY factor2
                    UNION
                    SELECT DISTINCT factor3
                    FROM factor
                    GROUP BY factor3
                    UNION   
                    SELECT DISTINCT factor4
                    FROM factor
                    GROUP BY factor4
                    UNION
                    SELECT DISTINCT factor5
                    FROM factor
                    GROUP BY factor5) a
                    WHERE a.factor = factor1
                    OR a.factor=factor2
                    OR a.factor=factor3
                    OR a.factor=factor4
                    OR a.factor=factor5
                    GROUP BY factor
                    ORDER BY rank DESC LIMIT %s;'''
        with self.conn.cursor() as cursor:
            cursor.execute(query,(str(limit),))
            return cursor.fetchall()   
        
    #crash per day in each weather
    def crash_weather(self, weather):
        l =['is_foggy','is_foggy_heavy','is_thunder','is_ice_pellets','is_glaze_rime','is_smoke_haze', 'is_damaging_wind','is_mist', 'is_drizzle', 'is_rainy', 'is_snowy', 'is_unknown_precipitation',  'is_freezing_foggy']
        for e in l:
            if weather in e:
                weather = e
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

    #crash number in different precipitation amount
    def crash_precipitation(self, bigger_than, smaller_than):
        query = '''
        SELECT count(COLLISION_ID)/tyw as ratio
        FROM occurence, precipitation,(
        SELECT count(measure_date) tyw
        FROM precipitation
        WHERE precipitation >%s
        AND precipitation < %s) wyt
        WHERE precipitation > %s
        AND precipitation < %s
        AND crashdate = measure_date
        GROUP BY tyw;
                '''
        with self.conn.cursor() as cursor:
            cursor.execute(query, (str(bigger_than),str(smaller_than), str(bigger_than),str(smaller_than)))
            return cursor.fetchall()[0][0]
     


if __name__ == '__main__':
    funcs = functions("host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'")
    L = funcs.rank_new_positive('2020-4-20','2020-4-25',5)
    print(L)
    L = funcs.positive_ratio('2020-3-2','2020-3-20','Albany')
    print('positive ratio: '+str(L))
    
    L = funcs.rank_crash_factor(10)
    print(L)
    print()
    L = funcs.crash_weather('snow')
    print('average num of crash in a snowy day is:'+str(L))
    print()
    L = funcs.crash_precipitation(0,1)
    print(L)
