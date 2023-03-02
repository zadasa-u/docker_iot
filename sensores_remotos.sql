--
-- Base de datos: `sensores_remotos`
--
CREATE DATABASE IF NOT EXISTS `sensores_remotos` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `sensores_remotos`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mediciones`
--

CREATE TABLE `mediciones` (
  `id` int(11) NOT NULL,
  `sensor_id` char(12) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `temperatura` decimal(3,1) NOT NULL,
  `humedad` decimal(3,1) NOT NULL   
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indices de la tabla `mediciones`
--
ALTER TABLE `mediciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `timestamp` (`timestamp`);

--
-- AUTO_INCREMENT de la tabla `mediciones`
--
ALTER TABLE `mediciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

CREATE USER 'mediciones'@'%' IDENTIFIED BY 'passworddeiot';GRANT USAGE ON *.* TO 'mediciones'@'%' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;
GRANT SELECT, INSERT ON `sensores\_remotos`.* TO 'mediciones'@'%';