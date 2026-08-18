with source as (
    select * from {{ ref('raw_users') }}
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

select * from renamed