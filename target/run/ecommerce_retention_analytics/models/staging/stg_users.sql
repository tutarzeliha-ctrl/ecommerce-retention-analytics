

  create or replace view `project-505e76f5-40a4-4295-b57`.`ecom_staging`.`stg_users`
  OPTIONS()
  as with source as (
    select * from `project-505e76f5-40a4-4295-b57`.`ecom_raw`.`raw_users`
),

renamed as (
    select
        cast(user_id as string) as user_id,
        cast(signup_date as timestamp) as signup_timestamp,
        upper(country) as country_code,
        lower(acquisition_channel) as acquisition_channel,
        cast(age as integer) as user_age
    from source
)

select * from renamed;

