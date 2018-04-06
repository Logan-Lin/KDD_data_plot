create table bj_historical_meo_grid
(
	stationName varchar(128) not null,
	utctime datetime not null,
	temperature float null,
	pressure float null,
	humidity float null,
	wind_direction float null,
	wind_speed float null,
	primary key (stationName, utctime)
)