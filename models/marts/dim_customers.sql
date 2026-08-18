with users as (
    select * from {{ ref('stg_users') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

customer_orders as (
    select
        o.user_id,
        count(distinct o.order_id) as total_orders,
        min(o.order_timestamp) as first_order_at,
        max(o.order_timestamp) as most_recent_order_at,
        sum(i.quantity * i.unit_price * (1 - i.discount_rate)) as lifetime_value_ltv
    from orders o
    left join order_items i on o.order_id = i.order_id
    where o.order_status = 'completed'
    group by 1
)

select
    u.user_id,
    u.country_code,
    u.acquisition_channel,
    u.user_age,
    coalesce(co.total_orders, 0) as total_orders,
    co.first_order_at,
    co.most_recent_order_at,
    coalesce(co.lifetime_value_ltv, 0) as lifetime_value_ltv,
    case 
        when co.most_recent_order_at < timestamp_sub(current_timestamp(), interval 180 day) then true 
        else false 
    end as is_churned
from users u
left join customer_orders co on u.user_id = co.user_id