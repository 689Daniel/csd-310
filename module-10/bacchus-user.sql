CREATE DATABASE bacchus;
CREATE USER 'bacchus_user'@'localhost' IDENTIFIED BY 'winery';
GRANT ALL PRIVILEGES ON bacchus.* TO 'bacchus_user'@'localhost';