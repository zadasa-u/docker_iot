CREATE DATABASE `rscw` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `rscw`;
CREATE TABLE `rscw`.`nodos` (`id` INT NOT NULL AUTO_INCREMENT , `alias` VARCHAR(100) NULL , `unique_id` INT NOT NULL, PRIMARY KEY (`id`)) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE USER 'rscw-usr'@'%'  IDENTIFIED BY 'espacio mira arma';
GRANT SELECT, INSERT, UPDATE, DELETE ON `rscw`.* TO 'rscw-usr'@'%';