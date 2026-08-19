
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select customer_id
from `project-505e76f5-40a4-4295-b57`.`ecom_staging`.`dim_customers`
where customer_id is null



  
  
      
    ) dbt_internal_test