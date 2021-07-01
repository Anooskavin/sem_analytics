-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 29, 2021 at 03:42 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 7.4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `school_mangement`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(50) NOT NULL,
  `admin_name` varchar(50) DEFAULT NULL,
  `admin_username` varchar(50) DEFAULT NULL,
  `admin_password` varchar(50) DEFAULT NULL,
  `admin_status` varchar(50) DEFAULT 'yes',
  `admin_usertype` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `admin_name`, `admin_username`, `admin_password`, `admin_status`, `admin_usertype`) VALUES
(1, 'kishore', 'kishore', '123', 'yes', 'data_entry'),
(3, 'Admin', '123', '123', 'yes', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `course_details`
--

CREATE TABLE `course_details` (
  `course_id` int(50) NOT NULL,
  `subject_id` int(50) DEFAULT NULL,
  `course_grade` int(50) DEFAULT NULL,
  `course_name` varchar(100) DEFAULT NULL,
  `course_description` varchar(900) DEFAULT NULL,
  `course_duration` int(100) DEFAULT NULL,
  `no_of_session` int(50) DEFAULT NULL,
  `course_status` varchar(100) DEFAULT 'open',
  `course_enroll_status` varchar(50) DEFAULT 'close',
  `course_timestamp` timestamp NULL DEFAULT current_timestamp(),
  `admin_id` int(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `course_details`
--

INSERT INTO `course_details` (`course_id`, `subject_id`, `course_grade`, `course_name`, `course_description`, `course_duration`, `no_of_session`, `course_status`, `course_enroll_status`, `course_timestamp`, `admin_id`) VALUES
(1, 1, 10, 'Trigonometry', 'a', 60, 3, 'open', 'close', '2021-05-27 05:31:54', 11),
(2, 2, 11, 'c++', '', 160, 3, 'close', 'close', '2021-06-01 10:57:36', 1),
(4, 1, 10, 'probability', 'Probability And Statistics are the two important concepts in Maths. Probability is all about chance. Whereas statistics is more about how we handle various data using different techniques.', 160, 2, 'open', 'close', '2021-06-19 06:16:50', 1);

-- --------------------------------------------------------

--
-- Table structure for table `course_enroll_details`
--

CREATE TABLE `course_enroll_details` (
  `course_enroll_id` int(50) NOT NULL,
  `course_id` int(50) DEFAULT NULL,
  `student_id` int(50) DEFAULT NULL,
  `course_enroll_timestamp` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `course_session_details`
--

CREATE TABLE `course_session_details` (
  `session_id` int(50) NOT NULL,
  `course_id` int(50) DEFAULT NULL,
  `session_duration` varchar(50) DEFAULT NULL,
  `faculty_id` int(50) DEFAULT NULL,
  `session_name` varchar(100) DEFAULT NULL,
  `session_discription` varchar(1000) DEFAULT NULL,
  `session_date` varchar(50) DEFAULT NULL,
  `session_starttime` varchar(50) DEFAULT NULL,
  `session_endtime` varchar(50) DEFAULT NULL,
  `session_timestamp` timestamp NULL DEFAULT current_timestamp(),
  `session_status` varchar(100) DEFAULT 'open'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `course_session_details`
--

INSERT INTO `course_session_details` (`session_id`, `course_id`, `session_duration`, `faculty_id`, `session_name`, `session_discription`, `session_date`, `session_starttime`, `session_endtime`, `session_timestamp`, `session_status`) VALUES
(1, 1, '120', 1, 'trignomenty session 1', 'introduction about trignomentry', '2021-05-27', '2.00 AM', '3.00 PM', '2021-05-27 05:35:12', 'open'),
(6, 1, '160', 4, 'session 3', 'con', '2021-06-11', '15:09', '15:10', '2021-06-11 09:38:38', 'close'),
(15, 2, '5', 1, 'session 2', 'asd', '2021-06-11', '20:07', '20:09', '2021-06-11 14:37:00', 'open'),
(16, 1, '2', 1, 'asd', 'asd', '2021-06-12', '21:07', '01:07', '2021-06-11 14:37:59', 'open'),
(17, 4, '120', 4, 'Introduction -1 ', 'about intro', '2021-06-19', '11:49', '13:49', '2021-06-19 06:19:35', 'open');

-- --------------------------------------------------------

--
-- Table structure for table `faculty_details`
--

CREATE TABLE `faculty_details` (
  `faculty_id` int(11) NOT NULL,
  `faculty_name` varchar(50) DEFAULT 'open',
  `faculty_email` varchar(50) DEFAULT NULL,
  `faculty_contact` varchar(50) DEFAULT NULL,
  `faculty_timestamp` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `faculty_details`
--

INSERT INTO `faculty_details` (`faculty_id`, `faculty_name`, `faculty_email`, `faculty_contact`, `faculty_timestamp`) VALUES
(1, 'anooshkavin', 'anooshkavin@gmail.com', '9562513517', '2021-05-27 05:54:05'),
(4, 'Kishore', 'kishoredurai7@gmail.com', '9787688154', '2021-06-02 04:29:48'),
(5, 'sad', 'asdasd@kflg.com', '97876881544', '2021-06-03 10:52:25');

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `notification_id` int(50) NOT NULL,
  `notification_msg` varchar(50) DEFAULT NULL,
  `notification_status` varchar(50) DEFAULT NULL,
  `notification_from` varchar(50) DEFAULT NULL,
  `admin_id` int(50) DEFAULT NULL,
  `notification_timestamp` date DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `notification`
--

INSERT INTO `notification` (`notification_id`, `notification_msg`, `notification_status`, `notification_from`, `admin_id`, `notification_timestamp`) VALUES
(1, 'testing msg', 'unread', '1', 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `school_details`
--

CREATE TABLE `school_details` (
  `school_id` int(50) NOT NULL,
  `school_name` varchar(100) DEFAULT NULL,
  `school_state` varchar(100) DEFAULT NULL,
  `school_district` varchar(100) DEFAULT NULL,
  `school_pincode` varchar(50) DEFAULT NULL,
  `school_board` varchar(100) DEFAULT NULL,
  `school_contact` varchar(50) DEFAULT NULL,
  `school_status` varchar(50) DEFAULT NULL,
  `school_timestamp` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `student_attendance`
--

CREATE TABLE `student_attendance` (
  `satt_id` int(100) NOT NULL,
  `student_id` int(100) DEFAULT NULL,
  `session_id` int(100) DEFAULT NULL,
  `satt_present` varchar(50) DEFAULT 'NO',
  `satt_timestamp` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student_attendance`
--

INSERT INTO `student_attendance` (`satt_id`, `student_id`, `session_id`, `satt_present`, `satt_timestamp`) VALUES
(1, 1, 1, 'YES', '2021-05-27 05:36:18'),
(2, 1, 6, 'YES', '2021-06-03 17:39:19'),
(3, 1, 6, 'YES', '2021-06-11 09:40:06'),
(6, 1, 16, 'NO', '2021-06-11 14:37:59'),
(7, 2, 16, 'NO', '2021-06-19 06:04:55'),
(8, 1, 17, 'NO', '2021-06-19 06:19:36'),
(9, 2, 17, 'NO', '2021-06-19 06:19:36'),
(11, 3, 1, 'NO', '2021-06-19 06:37:27');

-- --------------------------------------------------------

--
-- Table structure for table `student_details`
--

CREATE TABLE `student_details` (
  `student_id` int(50) NOT NULL,
  `school_id` int(11) DEFAULT NULL,
  `student_name` varchar(50) DEFAULT NULL,
  `student_contact` varchar(50) DEFAULT NULL,
  `student_email` varchar(50) NOT NULL,
  `student_password` varchar(50) DEFAULT NULL,
  `student_grade` varchar(50) DEFAULT NULL,
  `student_whatsapp` varchar(50) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT current_timestamp(),
  `account_status` varchar(50) DEFAULT 'yes'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student_details`
--

INSERT INTO `student_details` (`student_id`, `school_id`, `student_name`, `student_contact`, `student_email`, `student_password`, `student_grade`, `student_whatsapp`, `timestamp`, `account_status`) VALUES
(1, NULL, 'kishore D', '9787688154', 'kishore.ct19@bitsathy.ac.in', NULL, '10', '9787688154', '2021-05-26 18:30:00', 'yes'),
(2, NULL, 'Rameshraja r', '9562513517', 'rameshraja@gmail.com', NULL, '10', '9562513517', '2021-06-19 06:04:55', 'yes'),
(3, NULL, 'anooshkavin g', '9425786415', 'anooshkavin@gmail.com', NULL, '10', '9425786415', '2021-06-19 06:37:27', 'yes');

-- --------------------------------------------------------

--
-- Table structure for table `student_session_feedback`
--

CREATE TABLE `student_session_feedback` (
  `stu_feed_id` int(50) NOT NULL,
  `student_id` int(50) DEFAULT NULL,
  `session_id` int(50) DEFAULT NULL,
  `stu_session_feedback` varchar(10000) DEFAULT NULL,
  `stu_session_willingness` varchar(100) DEFAULT NULL,
  `stu_session_timestamp` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student_session_feedback`
--

INSERT INTO `student_session_feedback` (`stu_feed_id`, `student_id`, `session_id`, `stu_session_feedback`, `stu_session_willingness`, `stu_session_timestamp`) VALUES
(1, 1, 1, 'excellent', 'yes', '2021-05-27 05:44:07'),
(2, 1, 4, 'goods', 'yes', '2021-06-03 17:39:19'),
(3, 1, 6, 'GOOD', 'yes', '2021-06-11 09:40:06'),
(4, 2, 16, 'sdfs', 'yes', '2021-06-19 06:04:55'),
(5, 3, 1, 'good', 'yes', '2021-06-19 06:37:27');

-- --------------------------------------------------------

--
-- Table structure for table `subject`
--

CREATE TABLE `subject` (
  `subject_id` int(50) NOT NULL,
  `subject_name` varchar(50) DEFAULT NULL,
  `subject_description` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `subject`
--

INSERT INTO `subject` (`subject_id`, `subject_name`, `subject_description`) VALUES
(1, 'Mathematics', 'maths'),
(2, 'computer science', 'computer science');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `course_details`
--
ALTER TABLE `course_details`
  ADD PRIMARY KEY (`course_id`),
  ADD KEY `subject_forignkey` (`subject_id`);

--
-- Indexes for table `course_enroll_details`
--
ALTER TABLE `course_enroll_details`
  ADD PRIMARY KEY (`course_enroll_id`),
  ADD UNIQUE KEY `course_id` (`course_id`),
  ADD UNIQUE KEY `student_id` (`student_id`);

--
-- Indexes for table `course_session_details`
--
ALTER TABLE `course_session_details`
  ADD PRIMARY KEY (`session_id`),
  ADD KEY `course_table_foreignkey` (`course_id`),
  ADD KEY `faculty_forignkey` (`faculty_id`);

--
-- Indexes for table `faculty_details`
--
ALTER TABLE `faculty_details`
  ADD PRIMARY KEY (`faculty_id`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`notification_id`),
  ADD KEY `admin_id_forignkey` (`admin_id`);

--
-- Indexes for table `school_details`
--
ALTER TABLE `school_details`
  ADD PRIMARY KEY (`school_id`);

--
-- Indexes for table `student_attendance`
--
ALTER TABLE `student_attendance`
  ADD PRIMARY KEY (`satt_id`),
  ADD KEY `student_forignkey` (`student_id`),
  ADD KEY `session_forignkey` (`session_id`);

--
-- Indexes for table `student_details`
--
ALTER TABLE `student_details`
  ADD PRIMARY KEY (`student_id`),
  ADD UNIQUE KEY `student_email` (`student_email`),
  ADD KEY `school_forign_key` (`school_id`);

--
-- Indexes for table `student_session_feedback`
--
ALTER TABLE `student_session_feedback`
  ADD PRIMARY KEY (`stu_feed_id`);

--
-- Indexes for table `subject`
--
ALTER TABLE `subject`
  ADD PRIMARY KEY (`subject_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `course_details`
--
ALTER TABLE `course_details`
  MODIFY `course_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `course_enroll_details`
--
ALTER TABLE `course_enroll_details`
  MODIFY `course_enroll_id` int(50) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `course_session_details`
--
ALTER TABLE `course_session_details`
  MODIFY `session_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `faculty_details`
--
ALTER TABLE `faculty_details`
  MODIFY `faculty_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `notification`
--
ALTER TABLE `notification`
  MODIFY `notification_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `school_details`
--
ALTER TABLE `school_details`
  MODIFY `school_id` int(50) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `student_attendance`
--
ALTER TABLE `student_attendance`
  MODIFY `satt_id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `student_details`
--
ALTER TABLE `student_details`
  MODIFY `student_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `student_session_feedback`
--
ALTER TABLE `student_session_feedback`
  MODIFY `stu_feed_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `subject`
--
ALTER TABLE `subject`
  MODIFY `subject_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `course_details`
--
ALTER TABLE `course_details`
  ADD CONSTRAINT `subject_forignkey` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`subject_id`);

--
-- Constraints for table `course_enroll_details`
--
ALTER TABLE `course_enroll_details`
  ADD CONSTRAINT `course_foreignkey` FOREIGN KEY (`course_id`) REFERENCES `course_details` (`course_id`),
  ADD CONSTRAINT `student_foreignkey` FOREIGN KEY (`student_id`) REFERENCES `student_details` (`student_id`);

--
-- Constraints for table `course_session_details`
--
ALTER TABLE `course_session_details`
  ADD CONSTRAINT `course_table_foreignkey` FOREIGN KEY (`course_id`) REFERENCES `course_details` (`course_id`),
  ADD CONSTRAINT `faculty_forignkey` FOREIGN KEY (`faculty_id`) REFERENCES `faculty_details` (`faculty_id`);

--
-- Constraints for table `notification`
--
ALTER TABLE `notification`
  ADD CONSTRAINT `admin_id_forignkey` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`);

--
-- Constraints for table `student_attendance`
--
ALTER TABLE `student_attendance`
  ADD CONSTRAINT `session_forignkey` FOREIGN KEY (`session_id`) REFERENCES `course_session_details` (`session_id`),
  ADD CONSTRAINT `student_forignkey` FOREIGN KEY (`student_id`) REFERENCES `student_details` (`student_id`);

--
-- Constraints for table `student_details`
--
ALTER TABLE `student_details`
  ADD CONSTRAINT `school_forign_key` FOREIGN KEY (`school_id`) REFERENCES `school_details` (`school_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
