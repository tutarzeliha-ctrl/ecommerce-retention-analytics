
    
    

with dbt_test__target as (

  select customer_id as unique_field
  from `project-505e76f5-40a4-4295-b57`.`ecom_staging`.`dim_customers`
  where customer_id is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


