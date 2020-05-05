
import psycopg2
class query():
    def _init_(self,connection_string):
        self.conn = psycopg2.connect(connection_string)

    def accidentPerDayInRain(self, precipitation):
        query = "SELECT aibd/bd " \
                "FROM occurrence, (" \
                "SELECT measure_date, count(distinct measure_date) as bd " \
                "       FROM precipitation" \
                "       WHERE precipitation.precipitation > %s) rainDay," \
                "SELECT count(distinct occurrence.crashdate) as aibd" \
                "       FROM occurrence, precipitation" \
                "       WHERE occurrence.crashdate = precipitation.measure_date" \
                "       And precipitation.precipitation > %s) accInRainDay" \
                "WHERE occurrence.crashdate = rainDay.measure_date" \
                "GROUP BY occurrence.COLLISION_ID"

        with self.conn.cursor() as cursor:
            cursor.excute(query, (precipitation,precipitation, ))
            return cursor.fetchall()



    def accidentPerDayInBadWhether(self, precipitation):
            query = "select count(distinct COLLISION_ID)/bd" \
                    "from whetherType join occurrence on occurence.crashdate = precipitation.measure_date,（" \
                    "       select count(measure_date) as bd" \
                    "       from whetherType" \
                    "       where whetherType.is_foggy_heavy = 1 or whetherType.is_ice_pellets = 1 or " \
                    "       whetherType.is_smoke_haze = 1 or whetherType.is_damaging_wind = 1 or whetherType.is_snowy = 1）bad," \
                    "where whetherType.is_foggy_heavy = 1 or whetherType.is_ice_pellets = 1 or " \
                    "whetherType.is_smoke_haze = 1 or whetherType.is_damaging_wind = 1 or whetherType.is_snowy = 1" \
                    "GROUP BY occurrence.COLLISION_ID"

            with self.conn.cursor() as cursor:
                cursor.excute(query, (precipitation, precipitation,))
                return cursor.fetchall()
