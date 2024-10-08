select * from information_schema.packages
where package_name like 'snowflake-snowpark%'
and runtime_version = '3.11';

create or replace stage mystage;



create view emp_dept
as
    select '(company)' as child, null as parent
    union
    select distinct department, '(company)'
    from employees
    union
    select employee_name, department
    from employees;

select * from emp_dept;

# ------------------
select repeat(' ', level - 1) || employee_name as name, 
    ltrim(sys_connect_by_path(employee_name, '.'), '.') as path
from employees
start with manager_name is null
connect by prior employee_name = manager_name
order by path
;

select repeat(' ', level - 1) || $1 as name, 
    ltrim(sys_connect_by_path($1, '.'), '.') as path
from employees
start with $2 is null
connect by prior $1 = $2
order by path
;

# -----------------
create or replace database deps_db;

create or replace table T1(id int, json variant);
create or replace table T2(id int, id_t1 int, name string);

create or replace view V1 as (
    select json, name from T1 join T2 on T1.id = T2.id_t1);
create or replace materialized view V2 as select id, id_t1 from T2;

create or replace function F1() returns variant
as 'select top 1 json from V1';

select * from snowflake.account_usage.object_dependencies limit 5;