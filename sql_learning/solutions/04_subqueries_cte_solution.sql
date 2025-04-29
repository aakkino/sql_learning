-- solutions/04_subqueries_cte_solution.sql
-- 子查询 (Subquery) 和 公用表表达式 (CTE) 练习答案

-- 练习 1: 查询订单金额大于平均订单金额的所有订单信息
SELECT *
FROM orders
WHERE amount > (SELECT AVG(amount) FROM orders);

-- 练习 2: 查询下过订单的客户的姓名和城市
-- 方法一: 使用 IN
SELECT name, city
FROM customers
WHERE customer_id IN (SELECT DISTINCT customer_id FROM orders);
-- 方法二: 使用 EXISTS (效率可能更高)
-- SELECT name, city
-- FROM customers c
-- WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

-- 练习 3: 查询没有下过订单的客户信息
-- 方法一: 使用 NOT IN
SELECT *
FROM customers
WHERE customer_id NOT IN (SELECT DISTINCT customer_id FROM orders);
-- 方法二: 使用 LEFT JOIN + WHERE IS NULL (通常推荐)
-- SELECT c.*
-- FROM customers c
-- LEFT JOIN orders o ON c.customer_id = o.customer_id
-- WHERE o.order_id IS NULL;

-- 练习 4: 使用 CTE 查询每个客户的总订单金额，并只显示总金额大于 150 的客户及其总金额
WITH CustomerTotal AS (
    SELECT customer_id, SUM(amount) as total_amount
    FROM orders
    GROUP BY customer_id
)
SELECT customer_id, total_amount
FROM CustomerTotal
WHERE total_amount > 150;

-- 练习 5: 查询订单金额最高的订单对应的客户姓名
-- 方法一: 子查询 + JOIN
SELECT c.name
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.amount = (SELECT MAX(amount) FROM orders);
-- 方法二: CTE + JOIN + ORDER BY + LIMIT
-- WITH MaxOrder AS (
--     SELECT customer_id, amount
--     FROM orders
--     ORDER BY amount DESC
--     LIMIT 1
-- )
-- SELECT c.name
-- FROM customers c
-- JOIN MaxOrder mo ON c.customer_id = mo.customer_id;

-- 练习 6: 使用 CTE 查询来自北京 (Beijing) 的客户，然后查询这些客户的订单总数
WITH BeijingCustomers AS (
    SELECT customer_id
    FROM customers
    WHERE city = '北京'
)
SELECT COUNT(*)
FROM orders o
WHERE o.customer_id IN (SELECT customer_id FROM BeijingCustomers);
-- 或者使用 JOIN
-- WITH BeijingCustomers AS (
--     SELECT customer_id
--     FROM customers
--     WHERE city = '北京'
-- )
-- SELECT COUNT(o.order_id)
-- FROM orders o
-- JOIN BeijingCustomers bc ON o.customer_id = bc.customer_id; 