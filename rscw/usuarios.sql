CREATE TABLE `rscw`.`usuarios` (`id` int(11) NOT NULL, `usuario` varchar(100) NOT NULL, `hash` varchar(150) NOT NULL `tema` varchar(20) SET DEFAULT 'claro') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario` (`usuario`);
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;
