with source as (
    select * from {{ ref('raw_order_items') }}
),

renamed as (
    select
        cast(item_id as string) as item_id,
        cast(order_id as string) as order_id,
        cast(product_id as string) as product_id,
        cast(quantity as integer) as quantity,
        cast(unit_price as numeric) as unit_price,
        cast(discount as numeric) as discount_rate
    from source
)

select * from renamed