with source as (
    select * from {{ ref('raw_orders') }}
),

renamed as (
    select
        cast(order_id as string) as order_id,
        cast(user_id as string) as user_id,
        cast(order_date as timestamp) as order_timestamp,
        lower(status) as order_status
    from source
)

select * from renamed