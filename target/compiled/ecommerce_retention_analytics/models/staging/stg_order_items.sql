with source as (
    select * from `project-505e76f5-40a4-4295-b57`.`ecom_raw`.`raw_order_items`
),

renamed as (
    select
        cast(order_id as string) as order_id,
        cast(product_id as string) as product_id,
        1 as quantity,
        1.0 as unit_price,
        0.0 as discount_rate
    from source
)

select * from renamed