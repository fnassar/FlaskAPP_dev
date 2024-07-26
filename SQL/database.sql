-- Create Database
-- CREATE DATABASE sample_db;

-- -- Use Database
-- USE sample_db;

-- Create Tables
-- CREATE TABLE users (
--     user_id INT AUTO_INCREMENT,
--     username VARCHAR(50) NOT NULL,
--     email VARCHAR(100) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     PRIMARY KEY (user_id)
-- );

-- CREATE TABLE products (
--     product_id INT AUTO_INCREMENT,
--     name VARCHAR(100) NOT NULL,
--     description TEXT,
--     price DECIMAL(10, 2) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     PRIMARY KEY (product_id)
-- );

-- CREATE TABLE orders (
--     order_id INT AUTO_INCREMENT,
--     user_id INT,
--     product_id INT,
--     quantity INT NOT NULL,
--     order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     PRIMARY KEY (order_id),
--     FOREIGN KEY (user_id) REFERENCES users(user_id),
--     FOREIGN KEY (product_id) REFERENCES products(product_id)
-- );

-- Insert Sample Data
INSERT INTO users (username, email) VALUES
('john_doe', 'john@example.com'),
('jane_smith', 'jane@example.com'),
('alice_jones', 'alice@example.com');

INSERT INTO products (name, description, price) VALUES
('Laptop', 'A high-performance laptop', 999.99),
('Smartphone', 'A latest model smartphone', 699.99),
('Headphones', 'Noise-cancelling headphones', 199.99);

INSERT INTO orders (user_id, product_id, quantity) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 1);

-- Verify Data
SELECT * FROM users;
SELECT * FROM products;
SELECT * FROM orders;
