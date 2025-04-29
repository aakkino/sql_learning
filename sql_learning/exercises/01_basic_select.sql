-- 基础 SELECT 练习
-- 文件: scripts/01_basic_select.sql

-- 练习 1: 查询 customers 表中的所有数据
-- 预期输出: 表中所有行和列



-- 练习 2: 查询 orders 表中 order_id 为 103 的订单信息
-- 预期输出: order_id = 103 的那一行数据



-- 练习 3: 查询 customers 表中城市为 '北京' 的客户姓名 (name) 和客户ID (customer_id)
-- 预期输出: 两列 (name, customer_id)，多行，对应城市为北京的客户



-- 练习 4: 查询 orders 表中订单金额 (amount) 大于 100 的所有订单信息
-- 预期输出: amount > 100 的所有行



-- 练习 5: 查询 orders 表中订单日期 (order_date) 为 '2023-10-28' 的订单ID (order_id) 和订单金额 (amount)
-- 预期输出: 两列 (order_id, amount)，对应日期为 2023-10-28 的订单



-- 练习 6: 查询 customers 表中的所有客户姓名，并按姓名升序排序
-- 预期输出: name 列，按字母/拼音顺序排列



-- 练习 7: 查询 orders 表中订单金额最高的前 3 个订单的所有信息
-- 提示: 使用 ORDER BY 和 LIMIT
-- 预期输出: 金额最高的 3 行订单数据 