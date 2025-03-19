CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    registration_date DATE,
    loyalty_status VARCHAR(20)
);

CREATE TABLE Products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    category_id INT,
    price DECIMAL(10, 2),
    stock_quantity INT,
    creation_date DATE
);

CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id),
    order_date TIMESTAMP,
    total_amount DECIMAL(10, 2),
    status VARCHAR(20),
    delivery_date DATE
);

CREATE TABLE OrderDetails (
    order_detail_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES Orders(order_id),
    product_id INT REFERENCES Products(product_id),
    quantity INT,
    price_per_unit DECIMAL(10, 2),
    total_price DECIMAL(10, 2)
);

CREATE TABLE ProductCategories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    parent_category_id INT
);

BEGIN;

INSERT INTO Users (first_name, last_name, email, phone, registration_date, loyalty_status)
VALUES
('John', 'Doe', 'john.doe@example.com', '1234567890', '2023-01-01', 'Gold'),
('Jane', 'Smith', 'jane.smith@example.com', '2345678901', '2023-01-02', 'Silver'),
('Alice', 'Brown', 'alice.brown@example.com', '3456789012', '2023-01-03', 'Bronze'),
('Bob', 'Jones', 'bob.jones@example.com', '4567890123', '2023-01-04', 'Gold'),
('Charlie', 'Johnson', 'charlie.johnson@example.com', '5678901234', '2023-01-05', 'Silver'),
('Emily', 'Davis', 'emily.davis@example.com', '6789012345', '2023-01-06', 'Bronze'),
('Frank', 'Wilson', 'frank.wilson@example.com', '7890123456', '2023-01-07', 'Gold'),
('Grace', 'Taylor', 'grace.taylor@example.com', '8901234567', '2023-01-08', 'Silver'),
('Hannah', 'Anderson', 'hannah.anderson@example.com', '9012345678', '2023-01-09', 'Bronze'),
('Ivy', 'Thomas', 'ivy.thomas@example.com', '1234567809', '2023-01-10', 'Gold'),
('Jack', 'Moore', 'jack.moore@example.com', '2233445566', '2023-01-11', 'Silver'),
('Karen', 'Martin', 'karen.martin@example.com', '3344556677', '2023-01-12', 'Bronze'),
('Larry', 'Clark', 'larry.clark@example.com', '4455667788', '2023-01-13', 'Gold'),
('Mona', 'Walker', 'mona.walker@example.com', '5566778899', '2023-01-14', 'Silver'),
('Nancy', 'Allen', 'nancy.allen@example.com', '6677889900', '2023-01-15', 'Bronze'),
('Oscar', 'King', 'oscar.king@example.com', '7788990011', '2023-01-16', 'Gold'),
('Paul', 'Scott', 'paul.scott@example.com', '8899001122', '2023-01-17', 'Silver'),
('Quincy', 'Adams', 'quincy.adams@example.com', '9900112233', '2023-01-18', 'Bronze'),
('Rachel', 'Baker', 'rachel.baker@example.com', '1112233445', '2023-01-19', 'Gold'),
('Steve', 'Harris', 'steve.harris@example.com', '1223344556', '2023-01-20', 'Silver');

INSERT INTO ProductCategories (name, parent_category_id)
VALUES
('Electronics', NULL),
('Home Appliances', NULL),
('Clothing', NULL),
('Smartphones', 1),
('Laptops', 1),
('Televisions', 1),
('Refrigerators', 2),
('Washing Machines', 2),
('Kitchen Appliances', 2),
('Mens Wear', 3),
('Womens Wear', 3),
('Kids Wear', 3),
('Accessories', 3),
('Sportswear', 3),
('Gaming', 1),
('Tablets', 1),
('Headphones', 1),
('Furniture', NULL),
('Bedding', 18),
('Outdoor', 18);

INSERT INTO Products (name, description, category_id, price, stock_quantity, creation_date)
VALUES
('iPhone 14', 'Latest Apple smartphone', 4, 999.99, 50, '2023-01-01'),
('Galaxy S23', 'Latest Samsung smartphone', 4, 899.99, 60, '2023-01-02'),
('MacBook Pro', 'Apple laptop', 5, 1999.99, 30, '2023-01-03'),
('Dell XPS 15', 'High-performance laptop', 5, 1499.99, 40, '2023-01-04'),
('LG OLED TV', '55-inch OLED television', 6, 1299.99, 20, '2023-01-05'),
('Samsung Refrigerator', 'Double-door refrigerator', 7, 899.99, 25, '2023-01-06'),
('Whirlpool Washing Machine', 'Front-load washing machine', 8, 599.99, 30, '2023-01-07'),
('Mens Jacket', 'Winter jacket', 10, 89.99, 100, '2023-01-08'),
('Womens Dress', 'Summer dress', 11, 49.99, 80, '2023-01-09'),
('Kids T-shirt', 'Casual t-shirt', 12, 19.99, 150, '2023-01-10'),
('Gaming Console', 'Next-gen gaming console', 15, 499.99, 45, '2023-01-11'),
('Noise-canceling Headphones', 'High-quality headphones', 17, 199.99, 70, '2023-01-12'),
('Tablet Pro', 'Latest tablet', 16, 599.99, 35, '2023-01-13'),
('Outdoor Grill', 'Portable grill', 20, 149.99, 25, '2023-01-14'),
('Memory Foam Mattress', 'Queen-size mattress', 19, 499.99, 15, '2023-01-15'),
('Mens Sports Shoes', 'Comfortable running shoes', 14, 79.99, 120, '2023-01-16'),
('Womens Handbag', 'Leather handbag', 13, 99.99, 50, '2023-01-17'),
('Kids Sneakers', 'Stylish sneakers', 12, 39.99, 90, '2023-01-18'),
('Smartwatch', 'Fitness tracker', 1, 149.99, 60, '2023-01-19'),
('Gaming Chair', 'Ergonomic gaming chair', 15, 249.99, 20, '2023-01-20');

INSERT INTO Orders (user_id, order_date, total_amount, status, delivery_date)
VALUES
(1, '2023-02-01 10:00:00', 499.99, 'Shipped', '2023-02-05'),
(2, '2023-02-02 11:00:00', 599.99, 'Delivered', '2023-02-06'),
(3, '2023-02-03 12:00:00', 299.99, 'Cancelled', NULL),
(4, '2023-02-04 13:00:00', 199.99, 'Processing', NULL),
(5, '2023-02-05 14:00:00', 799.99, 'Shipped', '2023-02-09'),
(6, '2023-02-06 15:00:00', 1299.99, 'Delivered', '2023-02-10'),
(7, '2023-02-07 16:00:00', 89.99, 'Delivered', '2023-02-08'),
(8, '2023-02-08 17:00:00', 49.99, 'Delivered', '2023-02-09'),
(9, '2023-02-09 18:00:00', 999.99, 'Processing', NULL),
(10, '2023-02-10 19:00:00', 149.99, 'Shipped', '2023-02-14'),
(11, '2023-02-11 20:00:00', 89.99, 'Delivered', '2023-02-15'),
(12, '2023-02-12 21:00:00', 49.99, 'Processing', NULL),
(13, '2023-02-13 22:00:00', 1299.99, 'Shipped', '2023-02-17'),
(14, '2023-02-14 23:00:00', 99.99, 'Delivered', '2023-02-18'),
(15, '2023-02-15 08:00:00', 39.99, 'Processing', NULL),
(16, '2023-02-16 09:00:00', 149.99, 'Delivered', '2023-02-20'),
(17, '2023-02-17 10:00:00', 79.99, 'Shipped', '2023-02-21'),
(18, '2023-02-18 11:00:00', 999.99, 'Delivered', '2023-02-22'),
(19, '2023-02-19 12:00:00', 249.99, 'Processing', NULL),
(20, '2023-02-20 13:00:00', 199.99, 'Cancelled', NULL);

INSERT INTO OrderDetails (order_id, product_id, quantity, price_per_unit, total_price)
VALUES
(1, 1, 1, 499.99, 499.99),
(2, 2, 1, 599.99, 599.99),
(3, 3, 1, 299.99, 299.99),
(4, 4, 1, 199.99, 199.99),
(5, 5, 1, 799.99, 799.99),
(6, 6, 1, 1299.99, 1299.99),
(7, 8, 1, 89.99, 89.99),
(8, 9, 1, 49.99, 49.99),
(9, 10, 1, 999.99, 999.99),
(10, 14, 1, 149.99, 149.99),
(11, 15, 1, 89.99, 89.99),
(12, 16, 1, 49.99, 49.99),
(13, 17, 1, 1299.99, 1299.99),
(14, 18, 1, 99.99, 99.99),
(15, 19, 1, 39.99, 39.99),
(16, 20, 1, 149.99, 149.99),
(17, 11, 1, 79.99, 79.99),
(18, 12, 1, 999.99, 999.99),
(19, 13, 1, 249.99, 249.99),
(20, 7, 1, 199.99, 199.99);

COMMIT;
