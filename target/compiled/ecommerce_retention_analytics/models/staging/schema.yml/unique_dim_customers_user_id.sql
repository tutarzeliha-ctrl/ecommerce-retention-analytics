
    
    

with dbt_test__target as (

  select user_id as unique_field
  from `project-505e76f5-40a4-4295-b57`.`ecom_staging`.`dim_customers`
  where user_id is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


