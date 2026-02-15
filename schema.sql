create table model_stats (
	id int primary key,
	name varchar(255) unique not null,
	size bigint not null
);

create table mesh_stats (
	model_id int primary key,
	vertices int not null,
	triangles int not null,
	surface double not null,
	volume double not null,
	bbox_x double not null,
	bbox_y double not null,
	bbox_z double not null,
	center_x double not null,
	center_y double not null,
	center_z double not null,
	foreign key (model_id) references model_stats(id)
);

create table quality_stats (
	model_id int primary key,
	uniformity double not null,
	water_tight boolean not null,
	degen_faces int not null,
	dup_vertices int not null,
	foreign key (model_id) references model_stats(id)
);

create table geometry_stats (
	model_id int primary key,
	edge_min double not null,
	edge_max double not null,
	dens_area double not null,
	dens_volume double not null,
	aspect_avg double not null,
	aspect_worst double not null,
	foreign key (model_id) references model_stats(id)
);

create table performance_stats (
	model_id int primary key,
	complexity double not null,
	memory_use double not null,
	load_time double not null,
	triangle_rate double not null,
	foreign key (model_id) references model_stats(id)
);

create table analysis_log (
	id int primary key,
	name varchar(255) not null,
	action varchar(255) not null,
	timestamp timestamp default current_timestamp,
	status ENUM('pending', 'success', 'failed') default 'pending'
);

delimiter //
create function log_id_update()
returns int
deterministic
begin
	declare new_id int;
	select ifnull(max(id), 0) + 1 into new_id from analysis_log;
	return new_id;
end //

delimiter //
create function model_id_update()
returns int
deterministic
begin
	declare new_id int;
	select ifnull(max(id), 0) + 1 into new_id from model_stats;
	return new_id;
end //

delimiter //
create trigger before_insert_model
before insert on model_stats
for each row
begin
	set new.id = model_id_update();
end //

delimiter //
create trigger after_insert_model
after insert on model_stats
for each row
begin
	insert into analysis_log (id, name, action, status)
	values (log_id_update(), new.name, 'insert', 'success');
end //

delimiter //
create trigger after_update_model
after update on model_stats
for each row
begin
	insert into analysis_log (id, name, action, status)
	values (log_id_update(), new.name, 'update', 'success');
end //

delimiter //
create trigger after_delete_model
after delete on model_stats
for each row
begin
	delete from mesh_stats where model_id = old.id;
	delete from quality_stats where model_id = old.id;
	delete from geometry_stats where model_id = old.id;
	delete from performance_stats where model_id = old.id;
	insert into analysis_log (id, name, action, status)
	values (log_id_update(), old.name, 'delete', 'success');
end //

create view full_stats as 
select model_stats.id, model_stats.name, model_stats.size,
mesh_stats.model_id, mesh_stats.vertices, mesh_stats.triangles, mesh_stats.surface, 
mesh_stats.volume, mesh_stats.bbox_x, mesh_stats.bbox_y, mesh_stats.bbox_z,
mesh_stats.center_x, mesh_stats.center_y, mesh_stats.center_z, 
quality_stats.uniformity, quality_stats.water_tight, quality_stats.degen_faces,
quality_stats.dup_vertices,  
geometry_stats.edge_min, geometry_stats.edge_max, geometry_stats.dens_area, 
geometry_stats.dens_volume, geometry_stats.aspect_avg, geometry_stats.aspect_worst,
performance_stats.complexity, performance_stats.memory_use, performance_stats.load_time, 
performance_stats.triangle_rate from model_stats
left join mesh_stats on model_stats.id = mesh_stats.model_id 
left join quality_stats on model_stats.id = quality_stats.model_id 
left join geometry_stats on model_stats.id = geometry_stats.model_id 
left join performance_stats on model_stats.id = performance_stats.model_id;