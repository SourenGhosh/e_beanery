# App


## Flow

User has been categorized into four namely Resturant Manager, Customer, Chef and Waiter.
Meal Type and Table are two independent model; Table has a field booked to filter out table which are currently served on.

Order entity has direct mapping with user, table and mealtype, if two or more table are joined together so table is many to many field in order.Once an order has been placed, table associated with it will be automatically booked.

Billing Details and Address Reversal model are also there for billing and reversa;.

Apis two expose all data has been written in REST.Customer Can see only their prder but other role can see all order.Excluding customer other roles can change status so a permission decorator is used.




## Dependency
Celery and flower has been used to async order generation and monitoring failed tasks

