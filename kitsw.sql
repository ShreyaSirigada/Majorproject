-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 01, 2025 at 11:48 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kitsw`
--

-- --------------------------------------------------------

--
-- Table structure for table `traffic_data`
--

--CREATE TABLE `traffic_data` (
-- `id` int(11) NOT NULL,
-- `direction` text NOT NULL,
-- `vehicle_count` int(11) NOT NULL,
-- `timestamp` text NOT NULL
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `traffic_data`
--

-- INSERT INTO `traffic_data` (`id`, `direction`, `vehicle_count`, `timestamp`) VALUES
-- (1, 'North', 120, '08:00 AM - 09:00 AM'),
-- (2, 'South', 150, '09:00 AM - 10:00 AM'),
-- (3, 'East', 180, '10:00 AM - 11:00 AM'),
-- (4, 'West', 130, '11:00 AM - 12:00 PM');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

-- CREATE TABLE `user` (
  -- `id` int(11) NOT NULL,
  -- `name` varchar(100) NOT NULL,
  -- `username` varchar(100) NOT NULL,
  -- `email` varchar(100) NOT NULL,
  -- `password` text NOT NULL
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

-- INSERT INTO `user` (`id`, `name`, `username`, `email`, `password`) VALUES
-- (1, '101', 'user1', 'user1@gmail.com', 'pbkdf2:sha256:1000000$67gzb0DBEfJJFpah$9072db65306d4ed1e0c7d5c2b5ffbf03fdff32844062b333172fdaffab9a4df9'),
-- (3, '102', 'user2', 'user2@gmail.com', 'pbkdf2:sha256:1000000$RyR2RBXitA91xRS7$2335d638a7617e4a8bf70b37c6771c7d762978260e05d14460dfdf99052862cc');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `traffic_data`
--
-- ALTER TABLE `traffic_data`
-- ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
-- ALTER TABLE `user`
-- ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `traffic_data`
--
-- ALTER TABLE `traffic_data`
-- MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `user`
--
-- ALTER TABLE `user`
-- MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
-- COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
