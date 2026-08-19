
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select user_id
from `project-505e76f5-40a4-4295-b57`.`ecom_staging`.`dim_customers`
where user_id is null



  
  
      
    ) dbt_internal_test