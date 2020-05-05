select count(distinct COLLISION_ID)/bd
from（
	select count(measure_date) as bd
	from whetherType
	where whetherType.is_foggy_heavy = 1 or whetherType.is_ice_pellets = 1 or whetherType.is_smoke_haze = 1 or whetherType.is_damaging_wind = 1 or whetherType.is_snowy = 1
	）bad, whetherType join occurrence on occurence.crashdate = precipitation.measure_date
where whetherType.is_foggy_heavy = 1 or whetherType.is_ice_pellets = 1 or whetherType.is_smoke_haze = 1 or whetherType.is_damaging_wind = 1 or whetherType.is_snowy = 1


