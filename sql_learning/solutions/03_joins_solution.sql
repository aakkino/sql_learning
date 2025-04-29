-- solutions/03_joins_solution.sql
-- 表连接 (JOIN) 练习答案

-- 练习 1: 查询所有订单以及对应的客户信息
SELECT o.*, c.name, c.city
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;

-- 练习 2: 查询客户 '李四' 的所有订单信息 (包括订单ID, 日期, 金额)
SELECT o.order_id, o.order_date, o.amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE c.name = '李四';

-- 练习 3: 查询每个订单的订单ID (order_id) 和对应的客户姓名 (name)
SELECT o.order_id, c.name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;

-- 练习 4: 查询所有客户的信息，以及他们对应的订单信息。即使客户没有下过订单，也要显示客户信息。
SELECT c.*, o.order_id, o.order_date, o.amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- 练习 5: 查询来自 '北京' 的客户所下的所有订单的订单ID (order_id) 和订单金额 (amount)
SELECT o.order_id, o.amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE c.city = '北京';

-- 练习 6: 计算每个城市 (city) 的总销售额
SELECT c.city, SUM(o.amount) AS total_sales_per_city
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city; 