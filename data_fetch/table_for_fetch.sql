create table bj_current_meo_grid
(
	stationName varchar(128) not null,
	utctime datetime not null,
	weather varchar(128) null,
	temperature float null,
	pressure float null,
	humidity float null,
	wind_direction float null,
	wind_speed float null,
	primary key (stationName, utctime)
);

create table bj_current_aq
(
	stationid varchar(128) not null,
	utctime datetime not null,
	`PM2.5` int null,
	PM10 int null,
	NO2 int null,
	CO double null,
	O3 int null,
	SO2 int null,
	primary key (stationid, utctime)
)