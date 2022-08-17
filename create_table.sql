-- Drop table

DROP TABLE public.modbus_plc_his;

CREATE TABLE public.modbus_plc_his (
	device_code varchar(30) NOT NULL,
	device_name varchar(50) NOT NULL,
	sensor_code varchar(30) NOT NULL,
	sensor_name varchar(50) NOT NULL,
	sensor_value varchar(64) NOT NULL,
	sensor_unit varchar(10) NULL,
	data_time timestamptz NOT NULL,
);

select create_hypertable('modbus_plc_his','data_time')


