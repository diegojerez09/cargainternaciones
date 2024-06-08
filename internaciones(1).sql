-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 08-06-2024 a las 02:25:01
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `internaciones`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `afiliado`
--

CREATE TABLE `afiliado` (
  `id` int(11) NOT NULL,
  `dni` int(11) NOT NULL,
  `nombre` varchar(60) NOT NULL,
  `apellido` varchar(60) NOT NULL,
  `edad` int(11) NOT NULL,
  `sexo` varchar(20) NOT NULL,
  `fuerza` varchar(60) DEFAULT NULL,
  `estado` varchar(30) NOT NULL,
  `observaciones` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `afiliado`
--

INSERT INTO `afiliado` (`id`, `dni`, `nombre`, `apellido`, `edad`, `sexo`, `fuerza`, `estado`, `observaciones`) VALUES
(1, 34183274, 'DIEGO', 'JEREZ', 34, 'MASCULINO', 'GENDARMERIA', 'PENDIENTE', ''),
(4, 36123654, 'LUIS', 'CASTILLO', 32, 'MASCULINO', 'FUERZA AEREA', 'PENDIENTE', ''),
(16, 34657832, 'MARIANA', 'DANNA', 33, 'FEMENINO', 'PERSONAL CIVIL', 'CARGADO', ' PRUEBA DE ESTADO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `internacion`
--

CREATE TABLE `internacion` (
  `idinternacion` int(11) NOT NULL,
  `idafiliado` int(11) NOT NULL,
  `prestador` varchar(60) NOT NULL,
  `fechaingreso` date NOT NULL,
  `fechasalida` date NOT NULL,
  `diagnostico` varchar(60) NOT NULL,
  `totaldias` int(11) NOT NULL,
  `medico` varchar(60) DEFAULT NULL,
  `observaciones` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `internacion`
--

INSERT INTO `internacion` (`idinternacion`, `idafiliado`, `prestador`, `fechaingreso`, `fechasalida`, `diagnostico`, `totaldias`, `medico`, `observaciones`) VALUES
(17, 1, 'CLINICA YUNES', '2024-06-07', '2024-06-08', 'PREUBA DE FECHA', 1, 'ALVAREZ', ' '),
(18, 4, 'SANATORIO ALBERDI', '2024-06-03', '2024-06-07', 'PRUEBA', 4, 'A', 'PRUEBA DE FECHAS'),
(19, 4, 'SANATORIO ALBERDI', '2024-06-08', '2024-06-10', 'FEHCA', 2, 'ALVAREZ', 'PRUEBA FECHA INGRESO'),
(22, 16, 'SANATORIO ALBERDI', '2024-06-07', '2024-06-08', 'PRUEBA ESTADO', 1, 'GUTIERREZ', 'CAMBIO DE ESTADO');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `afiliado`
--
ALTER TABLE `afiliado`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `internacion`
--
ALTER TABLE `internacion`
  ADD PRIMARY KEY (`idinternacion`),
  ADD KEY `idafiliado` (`idafiliado`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `afiliado`
--
ALTER TABLE `afiliado`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `internacion`
--
ALTER TABLE `internacion`
  MODIFY `idinternacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `internacion`
--
ALTER TABLE `internacion`
  ADD CONSTRAINT `internacion_ibfk_1` FOREIGN KEY (`idafiliado`) REFERENCES `afiliado` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
