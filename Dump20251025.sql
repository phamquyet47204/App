CREATE DATABASE  IF NOT EXISTS `university_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `university_db`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: university_db
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add user',1,'add_user'),(2,'Can change user',1,'change_user'),(3,'Can delete user',1,'delete_user'),(4,'Can view user',1,'view_user'),(5,'Can add academic year',2,'add_academicyear'),(6,'Can change academic year',2,'change_academicyear'),(7,'Can delete academic year',2,'delete_academicyear'),(8,'Can view academic year',2,'view_academicyear'),(9,'Can add department',3,'add_department'),(10,'Can change department',3,'change_department'),(11,'Can delete department',3,'delete_department'),(12,'Can view department',3,'view_department'),(13,'Can add document type',4,'add_documenttype'),(14,'Can change document type',4,'change_documenttype'),(15,'Can delete document type',4,'delete_documenttype'),(16,'Can view document type',4,'view_documenttype'),(17,'Can add major',5,'add_major'),(18,'Can change major',5,'change_major'),(19,'Can delete major',5,'delete_major'),(20,'Can view major',5,'view_major'),(21,'Can add notification',6,'add_notification'),(22,'Can change notification',6,'change_notification'),(23,'Can delete notification',6,'delete_notification'),(24,'Can view notification',6,'view_notification'),(25,'Can add semester',7,'add_semester'),(26,'Can change semester',7,'change_semester'),(27,'Can delete semester',7,'delete_semester'),(28,'Can view semester',7,'view_semester'),(29,'Can add admin',8,'add_admin'),(30,'Can change admin',8,'change_admin'),(31,'Can delete admin',8,'delete_admin'),(32,'Can view admin',8,'view_admin'),(33,'Can add student',9,'add_student'),(34,'Can change student',9,'change_student'),(35,'Can delete student',9,'delete_student'),(36,'Can view student',9,'view_student'),(37,'Can add subject',10,'add_subject'),(38,'Can change subject',10,'change_subject'),(39,'Can delete subject',10,'delete_subject'),(40,'Can view subject',10,'view_subject'),(41,'Can add password reset token',11,'add_passwordresettoken'),(42,'Can change password reset token',11,'change_passwordresettoken'),(43,'Can delete password reset token',11,'delete_passwordresettoken'),(44,'Can view password reset token',11,'view_passwordresettoken'),(45,'Can add notification recipient',12,'add_notificationrecipient'),(46,'Can change notification recipient',12,'change_notificationrecipient'),(47,'Can delete notification recipient',12,'delete_notificationrecipient'),(48,'Can view notification recipient',12,'view_notificationrecipient'),(49,'Can add course class',13,'add_courseclass'),(50,'Can change course class',13,'change_courseclass'),(51,'Can delete course class',13,'delete_courseclass'),(52,'Can view course class',13,'view_courseclass'),(53,'Can add tuition fee',14,'add_tuitionfee'),(54,'Can change tuition fee',14,'change_tuitionfee'),(55,'Can delete tuition fee',14,'delete_tuitionfee'),(56,'Can view tuition fee',14,'view_tuitionfee'),(57,'Can add teacher',15,'add_teacher'),(58,'Can change teacher',15,'change_teacher'),(59,'Can delete teacher',15,'delete_teacher'),(60,'Can view teacher',15,'view_teacher'),(61,'Can add student class',16,'add_studentclass'),(62,'Can change student class',16,'change_studentclass'),(63,'Can delete student class',16,'delete_studentclass'),(64,'Can view student class',16,'view_studentclass'),(65,'Can add grade',17,'add_grade'),(66,'Can change grade',17,'change_grade'),(67,'Can delete grade',17,'delete_grade'),(68,'Can view grade',17,'view_grade'),(69,'Can add document request',18,'add_documentrequest'),(70,'Can change document request',18,'change_documentrequest'),(71,'Can delete document request',18,'delete_documentrequest'),(72,'Can view document request',18,'view_documentrequest'),(73,'Can add course registration',19,'add_courseregistration'),(74,'Can change course registration',19,'change_courseregistration'),(75,'Can delete course registration',19,'delete_courseregistration'),(76,'Can view course registration',19,'view_courseregistration'),(77,'Can add log entry',20,'add_logentry'),(78,'Can change log entry',20,'change_logentry'),(79,'Can delete log entry',20,'delete_logentry'),(80,'Can view log entry',20,'view_logentry'),(81,'Can add permission',21,'add_permission'),(82,'Can change permission',21,'change_permission'),(83,'Can delete permission',21,'delete_permission'),(84,'Can view permission',21,'view_permission'),(85,'Can add group',22,'add_group'),(86,'Can change group',22,'change_group'),(87,'Can delete group',22,'delete_group'),(88,'Can view group',22,'view_group'),(89,'Can add content type',23,'add_contenttype'),(90,'Can change content type',23,'change_contenttype'),(91,'Can delete content type',23,'delete_contenttype'),(92,'Can view content type',23,'view_contenttype'),(93,'Can add session',24,'add_session'),(94,'Can change session',24,'change_session'),(95,'Can delete session',24,'delete_session'),(96,'Can view session',24,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_academicyear`
--

DROP TABLE IF EXISTS `core_academicyear`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_academicyear` (
  `yearId` varchar(20) NOT NULL,
  `yearCode` varchar(20) NOT NULL,
  `yearName` varchar(100) NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `status` varchar(10) NOT NULL,
  PRIMARY KEY (`yearId`),
  UNIQUE KEY `yearCode` (`yearCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_academicyear`
--

LOCK TABLES `core_academicyear` WRITE;
/*!40000 ALTER TABLE `core_academicyear` DISABLE KEYS */;
INSERT INTO `core_academicyear` VALUES ('AY2024','2024-2025','Academic Year 2024-2025','2024-09-01','2025-06-30','active');
/*!40000 ALTER TABLE `core_academicyear` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_admin`
--

DROP TABLE IF EXISTS `core_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_admin` (
  `user_id` bigint NOT NULL,
  `adminId` varchar(20) NOT NULL,
  `adminCode` varchar(20) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `adminId` (`adminId`),
  UNIQUE KEY `adminCode` (`adminCode`),
  CONSTRAINT `core_admin_user_id_8bc0cb90_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_admin`
--

LOCK TABLES `core_admin` WRITE;
/*!40000 ALTER TABLE `core_admin` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_admin_permissions`
--

DROP TABLE IF EXISTS `core_admin_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_admin_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `admin_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_admin_permissions_admin_id_permission_id_8e9c9579_uniq` (`admin_id`,`permission_id`),
  KEY `core_admin_permissio_permission_id_00d0b670_fk_auth_perm` (`permission_id`),
  CONSTRAINT `core_admin_permissio_permission_id_00d0b670_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `core_admin_permissions_admin_id_37494980_fk_core_admin_user_id` FOREIGN KEY (`admin_id`) REFERENCES `core_admin` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_admin_permissions`
--

LOCK TABLES `core_admin_permissions` WRITE;
/*!40000 ALTER TABLE `core_admin_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_admin_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_courseclass`
--

DROP TABLE IF EXISTS `core_courseclass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_courseclass` (
  `courseClassId` varchar(20) NOT NULL,
  `courseCode` varchar(20) NOT NULL,
  `courseName` varchar(100) NOT NULL,
  `room` varchar(50) NOT NULL,
  `schedule` datetime(6) DEFAULT NULL,
  `maxStudents` int NOT NULL,
  `currentStudents` int NOT NULL,
  `status` tinyint(1) NOT NULL,
  `semester_id` varchar(20) NOT NULL,
  `subject_id` varchar(20) NOT NULL,
  `teacher_id` bigint DEFAULT NULL,
  PRIMARY KEY (`courseClassId`),
  UNIQUE KEY `courseCode` (`courseCode`),
  KEY `core_courseclass_teacher_id_a7abbef5_fk_core_teacher_user_id` (`teacher_id`),
  KEY `core_courseclass_semester_id_df1ed1d6_fk_core_seme` (`semester_id`),
  KEY `core_courseclass_subject_id_6f3fd2bf_fk_core_subject_subjectId` (`subject_id`),
  CONSTRAINT `core_courseclass_semester_id_df1ed1d6_fk_core_seme` FOREIGN KEY (`semester_id`) REFERENCES `core_semester` (`semesterId`),
  CONSTRAINT `core_courseclass_subject_id_6f3fd2bf_fk_core_subject_subjectId` FOREIGN KEY (`subject_id`) REFERENCES `core_subject` (`subjectId`),
  CONSTRAINT `core_courseclass_teacher_id_a7abbef5_fk_core_teacher_user_id` FOREIGN KEY (`teacher_id`) REFERENCES `core_teacher` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_courseclass`
--

LOCK TABLES `core_courseclass` WRITE;
/*!40000 ALTER TABLE `core_courseclass` DISABLE KEYS */;
INSERT INTO `core_courseclass` VALUES ('CC001','CS101-01','Programming Fundamentals - Class 1','Room 471',NULL,25,0,1,'SEM001','SUB001',2),('CC002','CS102-01','Data Structures - Class 1','Room 498',NULL,25,0,1,'SEM001','SUB002',3),('CC003','CS103-01','Database Systems - Class 1','Room 545',NULL,25,0,1,'SEM001','SUB003',2),('CC004','CS104-01','Web Development - Class 1','Room 247',NULL,25,0,1,'SEM001','SUB004',3);
/*!40000 ALTER TABLE `core_courseclass` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_courseregistration`
--

DROP TABLE IF EXISTS `core_courseregistration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_courseregistration` (
  `registrationId` varchar(20) NOT NULL,
  `registrationDate` date NOT NULL,
  `status` varchar(20) NOT NULL,
  `courseClass_id` varchar(20) NOT NULL,
  `semester_id` varchar(20) NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`registrationId`),
  KEY `core_courseregistrat_courseClass_id_f81fe4a9_fk_core_cour` (`courseClass_id`),
  KEY `core_courseregistrat_semester_id_3fdaddd3_fk_core_seme` (`semester_id`),
  KEY `core_courseregistrat_student_id_c46c0892_fk_core_stud` (`student_id`),
  CONSTRAINT `core_courseregistrat_courseClass_id_f81fe4a9_fk_core_cour` FOREIGN KEY (`courseClass_id`) REFERENCES `core_courseclass` (`courseClassId`),
  CONSTRAINT `core_courseregistrat_semester_id_3fdaddd3_fk_core_seme` FOREIGN KEY (`semester_id`) REFERENCES `core_semester` (`semesterId`),
  CONSTRAINT `core_courseregistrat_student_id_c46c0892_fk_core_stud` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_courseregistration`
--

LOCK TABLES `core_courseregistration` WRITE;
/*!40000 ALTER TABLE `core_courseregistration` DISABLE KEYS */;
INSERT INTO `core_courseregistration` VALUES ('REG000000','2024-08-20','registered','CC001','SEM001',4),('REG000001','2024-08-20','registered','CC002','SEM001',4),('REG001000','2024-08-20','registered','CC001','SEM001',5),('REG001001','2024-08-20','registered','CC002','SEM001',5),('REG002000','2024-08-20','registered','CC001','SEM001',6),('REG002001','2024-08-20','registered','CC002','SEM001',6),('REG003000','2024-08-20','registered','CC001','SEM001',10),('REG003001','2024-08-20','registered','CC002','SEM001',10),('REG004000','2024-08-20','registered','CC001','SEM001',11),('REG004001','2024-08-20','registered','CC002','SEM001',11),('REG005000','2024-08-20','registered','CC001','SEM001',12),('REG005001','2024-08-20','registered','CC002','SEM001',12),('REG006000','2024-08-20','registered','CC001','SEM001',13),('REG006001','2024-08-20','registered','CC002','SEM001',13),('REG007000','2024-08-20','registered','CC001','SEM001',14),('REG007001','2024-08-20','registered','CC002','SEM001',14),('REG008000','2024-08-20','registered','CC001','SEM001',15),('REG008001','2024-08-20','registered','CC002','SEM001',15),('REG009000','2024-08-20','registered','CC001','SEM001',16),('REG009001','2024-08-20','registered','CC002','SEM001',16);
/*!40000 ALTER TABLE `core_courseregistration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_department`
--

DROP TABLE IF EXISTS `core_department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_department` (
  `departmentId` varchar(20) NOT NULL,
  `departmentCode` varchar(20) NOT NULL,
  `departmentName` varchar(100) NOT NULL,
  `status` varchar(10) NOT NULL,
  `createdAt` datetime(6) NOT NULL,
  `headTeacher_id` bigint DEFAULT NULL,
  PRIMARY KEY (`departmentId`),
  UNIQUE KEY `departmentCode` (`departmentCode`),
  KEY `core_department_headTeacher_id_ae4fdda1_fk_core_teacher_user_id` (`headTeacher_id`),
  CONSTRAINT `core_department_headTeacher_id_ae4fdda1_fk_core_teacher_user_id` FOREIGN KEY (`headTeacher_id`) REFERENCES `core_teacher` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_department`
--

LOCK TABLES `core_department` WRITE;
/*!40000 ALTER TABLE `core_department` DISABLE KEYS */;
INSERT INTO `core_department` VALUES ('DEPT001','IT','Information Technology','active','2025-10-21 11:26:22.175793',NULL),('DEPT002','BUS','Business Administration','active','2025-10-21 11:51:39.474448',NULL),('DEPT002323','ITu','Information Technology','active','2025-10-22 03:48:43.853327',NULL),('DEPT003','ENG','Engineering','active','2025-10-21 11:51:39.585635',NULL);
/*!40000 ALTER TABLE `core_department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_documentrequest`
--

DROP TABLE IF EXISTS `core_documentrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_documentrequest` (
  `requestId` varchar(20) NOT NULL,
  `requestDate` datetime(6) NOT NULL,
  `purpose` longtext NOT NULL,
  `status` varchar(10) NOT NULL,
  `approvedDate` datetime(6) DEFAULT NULL,
  `completedDate` datetime(6) DEFAULT NULL,
  `rejectionReason` longtext,
  `documentType_id` varchar(20) NOT NULL,
  `semester_id` varchar(20) NOT NULL,
  `approvedBy_id` bigint DEFAULT NULL,
  PRIMARY KEY (`requestId`),
  KEY `core_documentrequest_documentType_id_1f4c1c66_fk_core_docu` (`documentType_id`),
  KEY `core_documentrequest_semester_id_4fe7c9a0_fk_core_seme` (`semester_id`),
  KEY `core_documentrequest_approvedBy_id_3587c067_fk_core_admi` (`approvedBy_id`),
  CONSTRAINT `core_documentrequest_approvedBy_id_3587c067_fk_core_admi` FOREIGN KEY (`approvedBy_id`) REFERENCES `core_admin` (`user_id`),
  CONSTRAINT `core_documentrequest_documentType_id_1f4c1c66_fk_core_docu` FOREIGN KEY (`documentType_id`) REFERENCES `core_documenttype` (`documentTypeId`),
  CONSTRAINT `core_documentrequest_semester_id_4fe7c9a0_fk_core_seme` FOREIGN KEY (`semester_id`) REFERENCES `core_semester` (`semesterId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_documentrequest`
--

LOCK TABLES `core_documentrequest` WRITE;
/*!40000 ALTER TABLE `core_documentrequest` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_documentrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_documentrequest_student`
--

DROP TABLE IF EXISTS `core_documentrequest_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_documentrequest_student` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `documentrequest_id` varchar(20) NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_documentrequest_stu_documentrequest_id_stude_88ae6393_uniq` (`documentrequest_id`,`student_id`),
  KEY `core_documentrequest_student_id_e3bf47c3_fk_core_stud` (`student_id`),
  CONSTRAINT `core_documentrequest_documentrequest_id_0b785bae_fk_core_docu` FOREIGN KEY (`documentrequest_id`) REFERENCES `core_documentrequest` (`requestId`),
  CONSTRAINT `core_documentrequest_student_id_e3bf47c3_fk_core_stud` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_documentrequest_student`
--

LOCK TABLES `core_documentrequest_student` WRITE;
/*!40000 ALTER TABLE `core_documentrequest_student` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_documentrequest_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_documenttype`
--

DROP TABLE IF EXISTS `core_documenttype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_documenttype` (
  `documentTypeId` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL,
  `description` longtext,
  `maxRequestsPerSemester` int NOT NULL,
  `processingDays` int NOT NULL,
  `status` varchar(10) NOT NULL,
  PRIMARY KEY (`documentTypeId`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_documenttype`
--

LOCK TABLES `core_documenttype` WRITE;
/*!40000 ALTER TABLE `core_documenttype` DISABLE KEYS */;
INSERT INTO `core_documenttype` VALUES ('DT001','Transcript','TRANSCRIPT','Transcript document',3,7,'active'),('DT002','Certificate','CERT','Certificate document',3,7,'active'),('DT003','Enrollment Letter','ENROLL','Enrollment Letter document',3,7,'active');
/*!40000 ALTER TABLE `core_documenttype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_grade`
--

DROP TABLE IF EXISTS `core_grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_grade` (
  `gradeId` varchar(20) NOT NULL,
  `assginmentscore` decimal(3,1) DEFAULT NULL,
  `midterm_score` decimal(3,1) DEFAULT NULL,
  `final_score` decimal(3,1) DEFAULT NULL,
  `average_score` decimal(3,1) DEFAULT NULL,
  `letterGrade` varchar(10) NOT NULL,
  `gradePoint` decimal(3,1) NOT NULL,
  `isPassed` tinyint(1) NOT NULL,
  `createdAt` datetime(6) NOT NULL,
  `updatedAt` datetime(6) NOT NULL,
  `courseClass_id` varchar(20) NOT NULL,
  `semester_id` varchar(20) NOT NULL,
  `subject_id` varchar(20) NOT NULL,
  `student_id` bigint NOT NULL,
  `teacher_id` bigint DEFAULT NULL,
  PRIMARY KEY (`gradeId`),
  KEY `core_grade_courseClass_id_f5fd5335_fk_core_cour` (`courseClass_id`),
  KEY `core_grade_semester_id_0ac49b3b_fk_core_semester_semesterId` (`semester_id`),
  KEY `core_grade_subject_id_f6214db2_fk_core_subject_subjectId` (`subject_id`),
  KEY `core_grade_student_id_7a78bbfb_fk_core_student_user_id` (`student_id`),
  KEY `core_grade_teacher_id_b72745b7_fk_core_teacher_user_id` (`teacher_id`),
  CONSTRAINT `core_grade_courseClass_id_f5fd5335_fk_core_cour` FOREIGN KEY (`courseClass_id`) REFERENCES `core_courseclass` (`courseClassId`),
  CONSTRAINT `core_grade_semester_id_0ac49b3b_fk_core_semester_semesterId` FOREIGN KEY (`semester_id`) REFERENCES `core_semester` (`semesterId`),
  CONSTRAINT `core_grade_student_id_7a78bbfb_fk_core_student_user_id` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`user_id`),
  CONSTRAINT `core_grade_subject_id_f6214db2_fk_core_subject_subjectId` FOREIGN KEY (`subject_id`) REFERENCES `core_subject` (`subjectId`),
  CONSTRAINT `core_grade_teacher_id_b72745b7_fk_core_teacher_user_id` FOREIGN KEY (`teacher_id`) REFERENCES `core_teacher` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_grade`
--

LOCK TABLES `core_grade` WRITE;
/*!40000 ALTER TABLE `core_grade` DISABLE KEYS */;
INSERT INTO `core_grade` VALUES ('GR000000',7.5,6.9,8.8,6.9,'F',0.0,0,'2025-10-21 11:52:30.134720','2025-10-21 11:52:30.134758','CC001','SEM001','SUB001',4,2),('GR000001',7.2,8.7,9.7,8.4,'D',1.0,1,'2025-10-21 11:52:30.147376','2025-10-21 11:52:30.147409','CC002','SEM001','SUB002',4,2),('GR001000',10.0,7.2,8.5,7.8,'C',2.0,1,'2025-10-21 11:52:30.159909','2025-10-21 11:52:30.159949','CC001','SEM001','SUB001',5,2),('GR001001',9.9,8.8,9.2,6.8,'D',1.0,1,'2025-10-21 11:52:30.222429','2025-10-21 11:52:30.222468','CC002','SEM001','SUB002',5,2),('GR002000',8.4,8.4,8.3,8.2,'B',3.0,1,'2025-10-21 11:52:30.233441','2025-10-21 11:52:30.233474','CC001','SEM001','SUB001',6,2),('GR002001',9.7,7.6,7.6,9.0,'F',0.0,0,'2025-10-21 11:52:30.244209','2025-10-21 11:52:30.244242','CC002','SEM001','SUB002',6,2),('GR003000',9.2,7.2,7.8,7.7,'C',2.0,1,'2025-10-21 11:52:30.255205','2025-10-21 11:52:30.255243','CC001','SEM001','SUB001',10,2),('GR003001',8.8,8.1,8.1,9.0,'C',2.0,1,'2025-10-21 11:52:30.266091','2025-10-21 11:52:30.266144','CC002','SEM001','SUB002',10,2),('GR004000',7.7,7.3,6.6,7.6,'A',4.0,1,'2025-10-21 11:52:30.278685','2025-10-21 11:52:30.278713','CC001','SEM001','SUB001',11,2),('GR004001',9.9,7.0,7.8,8.3,'C',2.0,1,'2025-10-21 11:52:30.289328','2025-10-21 11:52:30.289357','CC002','SEM001','SUB002',11,2),('GR005000',9.4,8.7,7.5,7.4,'C',2.0,1,'2025-10-21 11:52:30.300131','2025-10-21 11:52:30.300162','CC001','SEM001','SUB001',12,2),('GR005001',8.5,6.7,8.3,8.4,'F',0.0,0,'2025-10-21 11:52:30.311071','2025-10-21 11:52:30.311099','CC002','SEM001','SUB002',12,2),('GR006000',8.8,6.6,7.1,7.1,'D',1.0,1,'2025-10-21 11:52:30.321769','2025-10-21 11:52:30.321798','CC001','SEM001','SUB001',13,2),('GR006001',9.7,6.9,9.2,8.9,'A',4.0,1,'2025-10-21 11:52:30.334219','2025-10-21 11:52:30.334258','CC002','SEM001','SUB002',13,2),('GR007000',7.6,7.2,7.6,9.1,'A',4.0,1,'2025-10-21 11:52:30.345706','2025-10-21 11:52:30.345741','CC001','SEM001','SUB001',14,2),('GR007001',9.8,8.4,9.3,7.2,'A',4.0,1,'2025-10-21 11:52:30.356545','2025-10-21 11:52:30.356576','CC002','SEM001','SUB002',14,2),('GR008000',7.8,7.8,7.6,7.8,'D',1.0,1,'2025-10-21 11:52:30.367127','2025-10-21 11:52:30.367155','CC001','SEM001','SUB001',15,2),('GR008001',8.8,8.7,8.8,9.0,'A',4.0,1,'2025-10-21 11:52:30.378157','2025-10-21 11:52:30.378190','CC002','SEM001','SUB002',15,2),('GR009000',7.9,7.3,9.3,8.7,'F',0.0,0,'2025-10-21 11:52:30.388463','2025-10-21 11:52:30.388492','CC001','SEM001','SUB001',16,2),('GR009001',8.1,6.4,7.9,9.0,'C',2.0,1,'2025-10-21 11:52:30.399049','2025-10-21 11:52:30.399079','CC002','SEM001','SUB002',16,2);
/*!40000 ALTER TABLE `core_grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_major`
--

DROP TABLE IF EXISTS `core_major`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_major` (
  `majorId` varchar(20) NOT NULL,
  `majorCode` varchar(20) NOT NULL,
  `majorName` varchar(100) NOT NULL,
  `durationYears` int NOT NULL,
  `totalCredits` int NOT NULL,
  `status` tinyint(1) NOT NULL,
  `department_id` varchar(20) NOT NULL,
  PRIMARY KEY (`majorId`),
  UNIQUE KEY `majorCode` (`majorCode`),
  KEY `core_major_department_id_72892f65_fk_core_depa` (`department_id`),
  CONSTRAINT `core_major_department_id_72892f65_fk_core_depa` FOREIGN KEY (`department_id`) REFERENCES `core_department` (`departmentId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_major`
--

LOCK TABLES `core_major` WRITE;
/*!40000 ALTER TABLE `core_major` DISABLE KEYS */;
INSERT INTO `core_major` VALUES ('MAJ001','SE','Software Engineeringg',4,140,1,'DEPT002'),('MAJ0011','See','Software Engineeringqg',4,140,1,'DEPT001'),('MAJ002','CS','Computer Science',4,140,1,'DEPT001'),('MAJ003','BA','Business Administration',4,140,1,'DEPT002'),('MAJ004','CE','Civil Engineering',4,140,1,'DEPT003');
/*!40000 ALTER TABLE `core_major` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_notification`
--

DROP TABLE IF EXISTS `core_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_notification` (
  `notificationId` varchar(20) NOT NULL,
  `title` varchar(100) NOT NULL,
  `content` longtext NOT NULL,
  `targetAudience` varchar(10) NOT NULL,
  `targetId` longtext NOT NULL,
  `notificationType` varchar(14) NOT NULL,
  `priority` int NOT NULL,
  `scheduledAt` datetime(6) DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  `createdBy_id` bigint DEFAULT NULL,
  PRIMARY KEY (`notificationId`),
  KEY `core_notification_createdBy_id_c158ef98_fk_core_user_id` (`createdBy_id`),
  CONSTRAINT `core_notification_createdBy_id_c158ef98_fk_core_user_id` FOREIGN KEY (`createdBy_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_notification`
--

LOCK TABLES `core_notification` WRITE;
/*!40000 ALTER TABLE `core_notification` DISABLE KEYS */;
INSERT INTO `core_notification` VALUES ('NOT001','Welcome New Students','Welcome to new academic year!','all','[]','general',1,NULL,'active',7),('NOT002','Exam Schedule','Final exam schedule is now available.','all','[]','general',1,NULL,'active',7),('NOT003','Registration Reminder','Course registration deadline is approaching.','all','[]','general',1,NULL,'active',7),('NOTIF001','Welcome to New Semester','New semester starts on September 1st','all','[]','general',1,NULL,'active',7);
/*!40000 ALTER TABLE `core_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_notificationrecipient`
--

DROP TABLE IF EXISTS `core_notificationrecipient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_notificationrecipient` (
  `recipientId` varchar(100) NOT NULL,
  `deliveryStatus` varchar(10) NOT NULL,
  `readAt` datetime(6) DEFAULT NULL,
  `deliveredAt` datetime(6) NOT NULL,
  `notification_id` varchar(20) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`recipientId`),
  KEY `core_notificationrec_notification_id_48f0f193_fk_core_noti` (`notification_id`),
  KEY `core_notificationrecipient_user_id_858a1705_fk_core_user_id` (`user_id`),
  CONSTRAINT `core_notificationrec_notification_id_48f0f193_fk_core_noti` FOREIGN KEY (`notification_id`) REFERENCES `core_notification` (`notificationId`),
  CONSTRAINT `core_notificationrecipient_user_id_858a1705_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_notificationrecipient`
--

LOCK TABLES `core_notificationrecipient` WRITE;
/*!40000 ALTER TABLE `core_notificationrecipient` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_notificationrecipient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_passwordresettoken`
--

DROP TABLE IF EXISTS `core_passwordresettoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_passwordresettoken` (
  `token` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `is_used` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`token`),
  KEY `core_passwordresettoken_user_id_6e2470b2_fk_core_user_id` (`user_id`),
  CONSTRAINT `core_passwordresettoken_user_id_6e2470b2_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_passwordresettoken`
--

LOCK TABLES `core_passwordresettoken` WRITE;
/*!40000 ALTER TABLE `core_passwordresettoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_passwordresettoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_semester`
--

DROP TABLE IF EXISTS `core_semester`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_semester` (
  `semesterId` varchar(20) NOT NULL,
  `semesterCode` varchar(20) NOT NULL,
  `semesterName` varchar(100) NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `registrationStart` datetime(6) NOT NULL,
  `registrationEnd` datetime(6) NOT NULL,
  `status` varchar(10) NOT NULL,
  `academicYear_id` varchar(20) NOT NULL,
  PRIMARY KEY (`semesterId`),
  UNIQUE KEY `semesterCode` (`semesterCode`),
  KEY `core_semester_academicYear_id_4c520951_fk_core_acad` (`academicYear_id`),
  CONSTRAINT `core_semester_academicYear_id_4c520951_fk_core_acad` FOREIGN KEY (`academicYear_id`) REFERENCES `core_academicyear` (`yearId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_semester`
--

LOCK TABLES `core_semester` WRITE;
/*!40000 ALTER TABLE `core_semester` DISABLE KEYS */;
INSERT INTO `core_semester` VALUES ('SEM001','2024-1','Semester 1 - 2024','2024-09-01','2024-12-31','2024-08-15 08:00:00.000000','2024-08-30 17:00:00.000000','active','AY2024');
/*!40000 ALTER TABLE `core_semester` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_student`
--

DROP TABLE IF EXISTS `core_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_student` (
  `user_id` bigint NOT NULL,
  `studentId` varchar(20) NOT NULL,
  `studentCode` varchar(20) NOT NULL,
  `dateOfBirth` date DEFAULT NULL,
  `gender` varchar(10) NOT NULL,
  `enrollmentYear` int NOT NULL,
  `gpa` decimal(3,1) DEFAULT NULL,
  `totalCredits` int NOT NULL,
  `studentClass_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `studentId` (`studentId`),
  UNIQUE KEY `studentCode` (`studentCode`),
  KEY `core_student_studentClass_id_c7967f20_fk_core_stud` (`studentClass_id`),
  CONSTRAINT `core_student_studentClass_id_c7967f20_fk_core_stud` FOREIGN KEY (`studentClass_id`) REFERENCES `core_studentclass` (`classId`),
  CONSTRAINT `core_student_user_id_666ccffd_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_student`
--

LOCK TABLES `core_student` WRITE;
/*!40000 ALTER TABLE `core_student` DISABLE KEYS */;
INSERT INTO `core_student` VALUES (4,'S001','SE001','2000-01-01','male',2024,1.0,3,'CL003'),(5,'S002','SE002','2000-01-01','male',2024,1.5,6,'CL003'),(6,'S003','SE003','2000-01-01','male',2024,3.0,3,'CL001'),(10,'S004','SE004','2000-01-01','male',2024,2.0,6,'CL003'),(11,'S005','SE005','2000-01-01','male',2024,0.0,0,'CL003'),(12,'S006','SE006','2000-01-01','male',2024,0.0,0,'CL002'),(13,'S007','SE007','2000-01-01','male',2024,0.0,0,'CL002'),(14,'S008','SE008','2000-01-01','male',2024,0.0,0,'CL001'),(15,'S009','SE009','2000-01-01','male',2024,0.0,0,'CL002'),(16,'S010','SE010','2000-01-01','male',2024,0.0,0,'CL001'),(17,'S011','SE011','2000-01-01','male',2024,0.0,0,'CL001'),(18,'S012','SE012','2000-01-01','male',2024,0.0,0,'CL003'),(19,'S013','SE013','2000-01-01','male',2024,0.0,0,'CL002'),(20,'S014','SE014','2000-01-01','male',2024,0.0,0,'CL002'),(21,'S015','SE015','2000-01-01','male',2024,0.0,0,'CL003'),(22,'S016','SE016','2000-01-01','male',2024,0.0,0,'CL003'),(23,'S017','SE017','2000-01-01','male',2024,0.0,0,'CL002'),(24,'S018','SE018','2000-01-01','male',2024,0.0,0,'CL002'),(25,'S019','SE019','2000-01-01','male',2024,0.0,0,'CL001'),(26,'S020','SE020','2000-01-01','male',2024,0.0,0,'CL003');
/*!40000 ALTER TABLE `core_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_studentclass`
--

DROP TABLE IF EXISTS `core_studentclass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_studentclass` (
  `classId` varchar(20) NOT NULL,
  `classCode` varchar(20) NOT NULL,
  `className` varchar(100) NOT NULL,
  `academicYear` varchar(20) NOT NULL,
  `maxStudents` int NOT NULL,
  `currentStudents` int NOT NULL,
  `status` tinyint(1) NOT NULL,
  `major_id` varchar(20) NOT NULL,
  `advisorTeacher_id` bigint DEFAULT NULL,
  PRIMARY KEY (`classId`),
  UNIQUE KEY `classCode` (`classCode`),
  KEY `core_studentclass_major_id_f1aa1877_fk_core_major_majorId` (`major_id`),
  KEY `core_studentclass_advisorTeacher_id_3d6e8c6f_fk_core_teac` (`advisorTeacher_id`),
  CONSTRAINT `core_studentclass_advisorTeacher_id_3d6e8c6f_fk_core_teac` FOREIGN KEY (`advisorTeacher_id`) REFERENCES `core_teacher` (`user_id`),
  CONSTRAINT `core_studentclass_major_id_f1aa1877_fk_core_major_majorId` FOREIGN KEY (`major_id`) REFERENCES `core_major` (`majorId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_studentclass`
--

LOCK TABLES `core_studentclass` WRITE;
/*!40000 ALTER TABLE `core_studentclass` DISABLE KEYS */;
INSERT INTO `core_studentclass` VALUES ('CL001','SE2024A','Software Engineering 2024A','2024-2025',30,0,1,'MAJ001',2),('CL002','SE2024B','Software Engineering 2024B','2024-2025',30,0,1,'MAJ001',2),('CL003','CS2024A','Computer Science 2024A','2024-2025',30,0,1,'MAJ002',2),('CL004','BA2024A','Business Administration 2024A','2024-2025',30,0,1,'MAJ003',2);
/*!40000 ALTER TABLE `core_studentclass` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_subject`
--

DROP TABLE IF EXISTS `core_subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_subject` (
  `subjectId` varchar(20) NOT NULL,
  `subjectCode` varchar(20) NOT NULL,
  `subjectName` varchar(100) NOT NULL,
  `credits` int NOT NULL,
  `theoryHours` int NOT NULL,
  `practiceHours` int NOT NULL,
  `status` varchar(10) NOT NULL,
  `department_id` varchar(20) NOT NULL,
  PRIMARY KEY (`subjectId`),
  UNIQUE KEY `subjectCode` (`subjectCode`),
  KEY `core_subject_department_id_9e6ee46c_fk_core_depa` (`department_id`),
  CONSTRAINT `core_subject_department_id_9e6ee46c_fk_core_depa` FOREIGN KEY (`department_id`) REFERENCES `core_department` (`departmentId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_subject`
--

LOCK TABLES `core_subject` WRITE;
/*!40000 ALTER TABLE `core_subject` DISABLE KEYS */;
INSERT INTO `core_subject` VALUES ('SUB001','CS101','Introduction to Programming',3,30,15,'active','DEPT001'),('SUB002','CS102','Data Structures',3,30,15,'active','DEPT001'),('SUB003','CS103','Database Systems',4,30,15,'active','DEPT001'),('SUB004','CS104','Web Development',3,30,15,'active','DEPT001'),('SUB005','BUS101','Business Management',3,30,15,'active','DEPT002'),('SUB006','ENG101','Engineering Mathematics',4,30,15,'active','DEPT003');
/*!40000 ALTER TABLE `core_subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_subject_prerequisites`
--

DROP TABLE IF EXISTS `core_subject_prerequisites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_subject_prerequisites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `from_subject_id` varchar(20) NOT NULL,
  `to_subject_id` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_subject_prerequisit_from_subject_id_to_subje_38e7d186_uniq` (`from_subject_id`,`to_subject_id`),
  KEY `core_subject_prerequ_to_subject_id_a91cc3aa_fk_core_subj` (`to_subject_id`),
  CONSTRAINT `core_subject_prerequ_from_subject_id_2a79e35e_fk_core_subj` FOREIGN KEY (`from_subject_id`) REFERENCES `core_subject` (`subjectId`),
  CONSTRAINT `core_subject_prerequ_to_subject_id_a91cc3aa_fk_core_subj` FOREIGN KEY (`to_subject_id`) REFERENCES `core_subject` (`subjectId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_subject_prerequisites`
--

LOCK TABLES `core_subject_prerequisites` WRITE;
/*!40000 ALTER TABLE `core_subject_prerequisites` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_subject_prerequisites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_subject_teachers`
--

DROP TABLE IF EXISTS `core_subject_teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_subject_teachers` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subject_id` varchar(20) NOT NULL,
  `teacher_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_subject_teachers_subject_id_teacher_id_1970684e_uniq` (`subject_id`,`teacher_id`),
  KEY `core_subject_teacher_teacher_id_784cd24b_fk_core_teac` (`teacher_id`),
  CONSTRAINT `core_subject_teacher_subject_id_aa459afc_fk_core_subj` FOREIGN KEY (`subject_id`) REFERENCES `core_subject` (`subjectId`),
  CONSTRAINT `core_subject_teacher_teacher_id_784cd24b_fk_core_teac` FOREIGN KEY (`teacher_id`) REFERENCES `core_teacher` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_subject_teachers`
--

LOCK TABLES `core_subject_teachers` WRITE;
/*!40000 ALTER TABLE `core_subject_teachers` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_subject_teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_teacher`
--

DROP TABLE IF EXISTS `core_teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_teacher` (
  `user_id` bigint NOT NULL,
  `teacherId` varchar(20) NOT NULL,
  `teacherCode` varchar(20) NOT NULL,
  `position` varchar(50) NOT NULL,
  `hireDate` date NOT NULL,
  `department_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `teacherId` (`teacherId`),
  UNIQUE KEY `teacherCode` (`teacherCode`),
  KEY `core_teacher_department_id_027feac8_fk_core_depa` (`department_id`),
  CONSTRAINT `core_teacher_department_id_027feac8_fk_core_depa` FOREIGN KEY (`department_id`) REFERENCES `core_department` (`departmentId`),
  CONSTRAINT `core_teacher_user_id_0d56ab99_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_teacher`
--

LOCK TABLES `core_teacher` WRITE;
/*!40000 ALTER TABLE `core_teacher` DISABLE KEYS */;
INSERT INTO `core_teacher` VALUES (2,'T001','IT001','Lecturer','2020-01-01','DEPT001'),(3,'T002','IT002','Lecturer','2020-01-01','DEPT001'),(8,'T003','BUS001','Lecturer','2020-01-01','DEPT002'),(9,'T004','ENG001','Lecturer','2020-01-01','DEPT003');
/*!40000 ALTER TABLE `core_teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_tuitionfee`
--

DROP TABLE IF EXISTS `core_tuitionfee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_tuitionfee` (
  `tuitionFee` varchar(20) NOT NULL,
  `totalCredit` int NOT NULL,
  `feePerCredit` decimal(10,3) NOT NULL,
  `totalAmount` decimal(10,3) NOT NULL,
  `paidAmount` decimal(10,3) NOT NULL,
  `paymentStatus` varchar(12) NOT NULL,
  `dueDate` date NOT NULL,
  `paymentDate` datetime(6) DEFAULT NULL,
  `notes` longtext,
  `semester_id` varchar(20) NOT NULL,
  `student_id` bigint NOT NULL,
  `updatedBy_id` bigint DEFAULT NULL,
  PRIMARY KEY (`tuitionFee`),
  KEY `core_tuitionfee_semester_id_9d26f963_fk_core_semester_semesterId` (`semester_id`),
  KEY `core_tuitionfee_student_id_3e783acb_fk_core_student_user_id` (`student_id`),
  KEY `core_tuitionfee_updatedBy_id_b2577141_fk_core_admin_user_id` (`updatedBy_id`),
  CONSTRAINT `core_tuitionfee_semester_id_9d26f963_fk_core_semester_semesterId` FOREIGN KEY (`semester_id`) REFERENCES `core_semester` (`semesterId`),
  CONSTRAINT `core_tuitionfee_student_id_3e783acb_fk_core_student_user_id` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`user_id`),
  CONSTRAINT `core_tuitionfee_updatedBy_id_b2577141_fk_core_admin_user_id` FOREIGN KEY (`updatedBy_id`) REFERENCES `core_admin` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_tuitionfee`
--

LOCK TABLES `core_tuitionfee` WRITE;
/*!40000 ALTER TABLE `core_tuitionfee` DISABLE KEYS */;
INSERT INTO `core_tuitionfee` VALUES ('TF000',12,500000.000,6000000.000,3000000.000,'partial_paid','2024-10-15',NULL,NULL,'SEM001',4,NULL),('TF001',12,500000.000,6000000.000,3000000.000,'partial_paid','2024-10-15',NULL,NULL,'SEM001',5,NULL),('TF002',12,500000.000,6000000.000,3000000.000,'partial_paid','2024-10-15',NULL,NULL,'SEM001',6,NULL),('TF003',12,500000.000,6000000.000,3000000.000,'partial_paid','2024-10-15',NULL,NULL,'SEM001',10,NULL),('TF004',12,500000.000,6000000.000,3000000.000,'partial_paid','2024-10-15',NULL,NULL,'SEM001',11,NULL);
/*!40000 ALTER TABLE `core_tuitionfee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user`
--

DROP TABLE IF EXISTS `core_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `user_type` varchar(10) NOT NULL,
  `status` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user`
--

LOCK TABLES `core_user` WRITE;
/*!40000 ALTER TABLE `core_user` DISABLE KEYS */;
INSERT INTO `core_user` VALUES (1,'pbkdf2_sha256$870000$7U8tqnimCTR0dIbmZY38At$X5GhFOnK/68BTe4sj4gGhtITkOV8XMW+P21T+nwkgNY=',NULL,0,'admin','','','admin@test.com',0,1,'2025-10-21 11:02:03.838525','System Admin',NULL,'admin','active','2025-10-21 11:02:03.839547','2025-10-21 11:02:03.839565'),(2,'pbkdf2_sha256$870000$nJyPhhJGlR4d0a0EBwh9Nt$+nlop5f0lMllJWPAxQIZRJXswgTQLZu+dmfd8CQL5Hs=','2025-10-22 04:01:14.232252',0,'teacher1','','','teacher1@test.com',0,1,'2025-10-21 11:02:04.700137','Nguyen Van A','121212','teacher','active','2025-10-21 11:02:04.700434','2025-10-23 05:20:37.190073'),(3,'pbkdf2_sha256$870000$ivDk7kTay9EvbYGLT7EiS6$0ZAQbZma0gHPsCzKhq7DIyyjx5XxCcil3Eh+huPRtIg=',NULL,0,'teacher2','','','teacher2@test.com',0,1,'2025-10-21 11:02:05.618725','Tran Thi B',NULL,'teacher','active','2025-10-21 11:02:05.618975','2025-10-21 11:02:05.618987'),(4,'pbkdf2_sha256$870000$cIDG5f0G1oXiio1msBINYk$Tl8uMAI0xGE8d7F5SdwZvg/h6n6s3CvYPD7DClchd7s=','2025-10-22 03:54:19.175900',0,'student1','','','student1@test.com',0,1,'2025-10-21 11:02:06.535799','Le Van C','0329768959','student','active','2025-10-21 11:02:06.536071','2025-10-23 05:42:11.194157'),(5,'pbkdf2_sha256$870000$9UUFDHOdX5yZHGqmcuHOr2$82dFEJ/sKFbVeQAyZyi14Zfue5eXxgZXEMu0pqhe64U=',NULL,0,'student2','','','student2@test.com',0,1,'2025-10-21 11:02:07.451844','Pham Thi D',NULL,'student','active','2025-10-21 11:02:07.452199','2025-10-21 11:02:07.452211'),(6,'pbkdf2_sha256$870000$0ITzaQcvyCBNoQfn60QYnt$+cELl7Yjk1PLgN06HL06yXAZnhBRGlMiS5blkB7CM1c=',NULL,0,'student3','','','student3@test.com',0,1,'2025-10-21 11:02:08.371028','Hoang Van E',NULL,'student','active','2025-10-21 11:02:08.371412','2025-10-21 11:02:08.371428'),(7,'pbkdf2_sha256$870000$F15IODIq94Tm9dBaIJKDhw$RuoG/R6hI41Xhxi6bkXXHB8JKFkwPLIGS1iZ6kxyF3U=','2025-10-23 14:38:47.884746',1,'master','','','master@admin.com',1,1,'2025-10-21 11:13:41.462381','Master Administrator',NULL,'admin','active','2025-10-21 11:13:41.463360','2025-10-21 11:13:41.463376'),(8,'pbkdf2_sha256$870000$7Sb2ruT16ouT3MwFhbgsFx$RsVIyIwqzanSjhmvd+4kqM1ko1PhldAQCYDfn88EUUQ=',NULL,0,'teacher3','','','teacher3@test.com',0,1,'2025-10-21 11:52:10.498464','Prof. Mike Johnson','0329768959','teacher','active','2025-10-21 11:52:10.498908','2025-10-23 04:55:59.488043'),(9,'pbkdf2_sha256$870000$cYAmDbnfNtuHj5L5FfZdGR$a3Plq+DxFeMP42Q+HM2fmXXffq9rxNuFSXJCDyOKWdo=',NULL,0,'teacher4','','','teacher4@test.com',0,1,'2025-10-21 11:52:11.420292','Dr. Sarah Wilson',NULL,'teacher','active','2025-10-21 11:52:11.420543','2025-10-21 11:52:11.420555'),(10,'pbkdf2_sha256$870000$dYarKcr6s4ZpqqoEzZcmLA$7WbYNsJ/ExyHa5p11gP6t+7zCwFkpO7dS/5X69vRRQQ=',NULL,0,'student4','','','student4@test.com',0,1,'2025-10-21 11:52:15.074611','Student 4',NULL,'student','active','2025-10-21 11:52:15.074922','2025-10-21 11:52:15.074937'),(11,'pbkdf2_sha256$870000$OFXhqNYlftUIEqZfD4dOMJ$Mr6gpdDwm0qc5t9mocGG3LDx7n+0/xYz42H3OZZ7W+A=',NULL,0,'student5','','','student5@test.com',0,1,'2025-10-21 11:52:16.016827','Student 5',NULL,'student','active','2025-10-21 11:52:16.017173','2025-10-21 11:52:16.017186'),(12,'pbkdf2_sha256$870000$iFHgArNwEnIwDukqI3svBm$TQZ3wf5Fcra5F7qOXeTK+KwQ0mWztckkucDP/CA3oMs=',NULL,0,'student6','','','student6@test.com',0,1,'2025-10-21 11:52:16.921619','Student 6',NULL,'student','active','2025-10-21 11:52:16.921944','2025-10-21 11:52:16.921959'),(13,'pbkdf2_sha256$870000$qldCLBP2DbMo4uAaVb6k1l$qELS0HjI0RYQML+fcMm94V2LhEUPokyWuwWLkbcYuOg=',NULL,0,'student7','','','student7@test.com',0,1,'2025-10-21 11:52:17.813795','Student 7',NULL,'student','active','2025-10-21 11:52:17.814076','2025-10-21 11:52:17.814090'),(14,'pbkdf2_sha256$870000$58bPXaAuBpDi380APkdC5J$1KiFR8Nd9bFrGmzKC7MJHEchcOgBp4sTkG0CRTuZCXw=',NULL,0,'student8','','','student8@test.com',0,1,'2025-10-21 11:52:18.726607','Student 8',NULL,'student','active','2025-10-21 11:52:18.726852','2025-10-21 11:52:18.726864'),(15,'pbkdf2_sha256$870000$UNZqAZSvbzfpwFucQBcS2L$oV9mjGMQJnhDohTPb0m8yhDkH7a+juG9XqvgcE/zH2Y=',NULL,0,'student9','','','student9@test.com',0,1,'2025-10-21 11:52:19.614243','Student 9',NULL,'student','active','2025-10-21 11:52:19.614507','2025-10-21 11:52:19.614521'),(16,'pbkdf2_sha256$870000$smmM9LKNq0T0SEX53xmfgy$kyCpp9N3gvtd49756f3ikVV2KgYsl7crOxidHTbpngk=',NULL,0,'student10','','','student10@test.com',0,1,'2025-10-21 11:52:20.498563','Student 10',NULL,'student','active','2025-10-21 11:52:20.498972','2025-10-21 11:52:20.498988'),(17,'pbkdf2_sha256$870000$k1xz5YpzwsCUs0edOlZqX2$TqS2j4+CfPSHaKIbz+OfSckIRi+IfOB34SbhXnjkDN4=',NULL,0,'student11','','','student11@test.com',0,1,'2025-10-21 11:52:21.395625','Student 11',NULL,'student','active','2025-10-21 11:52:21.395892','2025-10-21 11:52:21.395904'),(18,'pbkdf2_sha256$870000$Bdsqol5RVg27GnTKUyzznK$ANeeMLYzKY2N0tsYhJo3cnUV1+/X90N814P9V55o3AI=',NULL,0,'student12','','','student12@test.com',0,1,'2025-10-21 11:52:22.277997','Student 12',NULL,'student','active','2025-10-21 11:52:22.278265','2025-10-21 11:52:22.278276'),(19,'pbkdf2_sha256$870000$rce3QzZttgALHxBsZ4nPHy$CnaYCb6RzxVITs9QmSu/0r4loZg9Oe0zYwdxH7ZAGOU=',NULL,0,'student13','','','student13@test.com',0,1,'2025-10-21 11:52:23.167293','Student 13',NULL,'student','active','2025-10-21 11:52:23.167629','2025-10-21 11:52:23.167644'),(20,'pbkdf2_sha256$870000$yLrifetmmyvvzBuf1c6vmR$7rC+cg1xWCTD25twy25KAv9NtRTfbfM7WaUzXOH5WjY=',NULL,0,'student14','','','student14@test.com',0,1,'2025-10-21 11:52:24.067677','Student 14',NULL,'student','active','2025-10-21 11:52:24.068047','2025-10-21 11:52:24.068060'),(21,'pbkdf2_sha256$870000$s0H8sMMzZ2tjfEGAidDZb6$V7Wp3Cg335ZY0XArz7VbLvwqLgrLerD+KftgeZuCipw=',NULL,0,'student15','','','student15@test.com',0,1,'2025-10-21 11:52:24.970142','Student 15',NULL,'student','active','2025-10-21 11:52:24.970391','2025-10-21 11:52:24.970402'),(22,'pbkdf2_sha256$870000$RqMZ5mp6Lj4YneKYrhiyDc$5CtcWRc/3fCiA+ZUqtj/T9b8ySgZjEd3gR/44ElBXVs=',NULL,0,'student16','','','student16@test.com',0,1,'2025-10-21 11:52:25.885432','Student 16',NULL,'student','active','2025-10-21 11:52:25.885707','2025-10-21 11:52:25.885718'),(23,'pbkdf2_sha256$870000$p78HEEq56yvmLyVxdAUmU5$9t98xlRvwwhEVjQs2ftjq8yVLJaO0WTF74kAkuQP0ac=','2025-10-22 03:59:36.495088',0,'student17','','','student17@test.com',0,1,'2025-10-21 11:52:26.813898','Student 17',NULL,'student','active','2025-10-21 11:52:26.814162','2025-10-21 11:52:26.814173'),(24,'pbkdf2_sha256$870000$sWmaGDRsGUuM78b7TGrBNP$OeShDOh52fORLRc0jDxDftLA/MozCYjXsLihvJ7EadM=',NULL,0,'student18','','','student18@test.com',0,1,'2025-10-21 11:52:27.722906','Student 18',NULL,'student','active','2025-10-21 11:52:27.723193','2025-10-21 11:52:27.723205'),(25,'pbkdf2_sha256$870000$jVNXFwkMjDZ1M8wZKTeWka$o2Xl9qNXvqRlI4Gp9KFCmyGvrPhHSa8p+Lvrc8IB8QE=',NULL,0,'student19','','','student19@test.com',0,1,'2025-10-21 11:52:28.650454','Student 19',NULL,'student','active','2025-10-21 11:52:28.650720','2025-10-21 11:52:28.650733'),(26,'pbkdf2_sha256$870000$EcwGlvq2i4RrGBlVuo2rAo$R3tKPoIViZT8X/TnCvKFJFS3oCKehOAi1DqT5xCy7hs=',NULL,0,'student20','','','student20@test.com',0,1,'2025-10-21 11:52:29.530098','Student 20',NULL,'student','active','2025-10-21 11:52:29.530449','2025-10-21 11:52:29.530461');
/*!40000 ALTER TABLE `core_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user_groups`
--

DROP TABLE IF EXISTS `core_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_groups_user_id_group_id_c82fcad1_uniq` (`user_id`,`group_id`),
  KEY `core_user_groups_group_id_fe8c697f_fk_auth_group_id` (`group_id`),
  CONSTRAINT `core_user_groups_group_id_fe8c697f_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `core_user_groups_user_id_70b4d9b8_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user_groups`
--

LOCK TABLES `core_user_groups` WRITE;
/*!40000 ALTER TABLE `core_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user_user_permissions`
--

DROP TABLE IF EXISTS `core_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_user_permissions_user_id_permission_id_73ea0daa_uniq` (`user_id`,`permission_id`),
  KEY `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` (`permission_id`),
  CONSTRAINT `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `core_user_user_permissions_user_id_085123d3_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user_user_permissions`
--

LOCK TABLES `core_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `core_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_core_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (20,'admin','logentry'),(22,'auth','group'),(21,'auth','permission'),(23,'contenttypes','contenttype'),(2,'core','academicyear'),(8,'core','admin'),(13,'core','courseclass'),(19,'core','courseregistration'),(3,'core','department'),(18,'core','documentrequest'),(4,'core','documenttype'),(17,'core','grade'),(5,'core','major'),(6,'core','notification'),(12,'core','notificationrecipient'),(11,'core','passwordresettoken'),(7,'core','semester'),(9,'core','student'),(16,'core','studentclass'),(10,'core','subject'),(15,'core','teacher'),(14,'core','tuitionfee'),(1,'core','user'),(24,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-10-21 11:01:04.833082'),(2,'contenttypes','0002_remove_content_type_name','2025-10-21 11:01:05.103797'),(3,'auth','0001_initial','2025-10-21 11:01:06.067573'),(4,'auth','0002_alter_permission_name_max_length','2025-10-21 11:01:06.246249'),(5,'auth','0003_alter_user_email_max_length','2025-10-21 11:01:06.263194'),(6,'auth','0004_alter_user_username_opts','2025-10-21 11:01:06.278952'),(7,'auth','0005_alter_user_last_login_null','2025-10-21 11:01:06.295672'),(8,'auth','0006_require_contenttypes_0002','2025-10-21 11:01:06.306523'),(9,'auth','0007_alter_validators_add_error_messages','2025-10-21 11:01:06.321260'),(10,'auth','0008_alter_user_username_max_length','2025-10-21 11:01:06.336769'),(11,'auth','0009_alter_user_last_name_max_length','2025-10-21 11:01:06.353862'),(12,'auth','0010_alter_group_name_max_length','2025-10-21 11:01:06.391725'),(13,'auth','0011_update_proxy_permissions','2025-10-21 11:01:06.412168'),(14,'auth','0012_alter_user_first_name_max_length','2025-10-21 11:01:06.426852'),(15,'core','0001_initial','2025-10-21 11:01:16.276626'),(16,'admin','0001_initial','2025-10-21 11:01:16.688533'),(17,'admin','0002_logentry_remove_auto_add','2025-10-21 11:01:16.715745'),(18,'admin','0003_logentry_add_action_flag_choices','2025-10-21 11:01:16.749915'),(19,'sessions','0001_initial','2025-10-21 11:01:16.859801');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('8zf9m9yd7xnd3nw1f56hkvtb4acoogds','.eJxVjjsOwjAQRO_iGlkm_qek5wyW17smBuSgOJFAiLtDUApo570ZzZOFuMxDWBpNoSDrmWW73wxiulBdAZ5jPY08jXWeCvBV4Rtt_DgiXQ-b-zcwxDZ82hlU1ymBMWkvyYIDUBJ1NiCUNZnISOu8ROHAa8jOQ4q496SdjxrT91Wj1spYA91vZXqwXhohXm9sU0Bb:1vBwSl:CozIND5xsEUxD_fzFs9KoC38Onqb9PC7pNxhoYBP-wc','2025-10-23 15:38:47.893545'),('908683tcx9zq92xiie1k60zdwkcbsmuh','.eJxVjjsOwjAQRO_iGlkm_qek5wyW17smBuSgOJFAiLtDUApo570ZzZOFuMxDWBpNoSDrmWW73wxiulBdAZ5jPY08jXWeCvBV4Rtt_DgiXQ-b-zcwxDZ82hlU1ymBMWkvyYIDUBJ1NiCUNZnISOu8ROHAa8jOQ4q496SdjxrT91Wj1spYA91vZXqwXhohXm9sU0Bb:1vBmmM:_ShHrF9uvDJeec3Dv9Q2aqoPcP4yrCbuPHAJeeYo9Ag','2025-10-23 05:18:22.906387'),('bvda1jhdgzi9canfwrk1athxl2crwp52','.eJxVjjsOwjAQRO_iGlkm_qek5wyW17smBuSgOJFAiLtDUApo570ZzZOFuMxDWBpNoSDrmWW73wxiulBdAZ5jPY08jXWeCvBV4Rtt_DgiXQ-b-zcwxDZ82hlU1ymBMWkvyYIDUBJ1NiCUNZnISOu8ROHAa8jOQ4q496SdjxrT91Wj1spYA91vZXqwXhohXm9sU0Bb:1vBp2J:JEm8XakVtdLZlyGi0GVpxJkUb6YcxVALd1P77ipMz3Q','2025-10-23 07:42:59.281262'),('dalcjq1qst0c9et0tosvx753wdajqvbi','.eJxVjjsOwjAQRO_iGlkm_qek5wyW17smBuSgOJFAiLtDUApo570ZzZOFuMxDWBpNoSDrmWW73wxiulBdAZ5jPY08jXWeCvBV4Rtt_DgiXQ-b-zcwxDZ82hlU1ymBMWkvyYIDUBJ1NiCUNZnISOu8ROHAa8jOQ4q496SdjxrT91Wj1spYA91vZXqwXhohXm9sU0Bb:1vBmp9:6sQ6A_viDnIt0-aqLRR20KoQbmrtL_xAL4ORGEskTf8','2025-10-23 05:21:15.679484'),('froxgbaxpqbmb8nxmzxbhlwgfslq1ul5','.eJxVjDsOwjAQBe_iGlkm_lPS5wzWrneNA8iR4qRC3B0ipYD2zcx7iQTbWtPWeUkTiYvw4vS7IeQHtx3QHdptlnlu6zKh3BV50C7Hmfh5Pdy_gwq9fuuCZhiMIsg2avYYEI0mWxwq411hdtqHqEkFjBZLiJiBzpFtiGApe_H-APfkOIU:1vBQA6:o2vc0kY3nib-HYwG1YXsZePq0gt9Vcp-QRc0J_V6oqM','2025-10-22 05:09:22.774996'),('lz6lsi5cw6rh9e0uytgdlz95sudzoz4p','.eJxVjjsOwjAQRO_iGlkm_qek5wyW17smBuSgOJFAiLtDUApo570ZzZOFuMxDWBpNoSDrmWW73wxiulBdAZ5jPY08jXWeCvBV4Rtt_DgiXQ-b-zcwxDZ82hlU1ymBMWkvyYIDUBJ1NiCUNZnISOu8ROHAa8jOQ4q496SdjxrT91Wj1spYA91vZXqwXhohXm9sU0Bb:1vBBAZ:MsWdMIKqHr3U_tLEAiY9UYgQ0bNNlWMBxh1V-SPVIHU','2025-10-21 13:08:51.067116'),('m0vdtfqm6b2tetm9jf2r4yd07kil6uu6','.eJxVjjsOwjAQRO_iGlkm_qek5wyW17smBuSgOJFAiLtDUApo570ZzZOFuMxDWBpNoSDrmWW73wxiulBdAZ5jPY08jXWeCvBV4Rtt_DgiXQ-b-zcwxDZ82hlU1ymBMWkvyYIDUBJ1NiCUNZnISOu8ROHAa8jOQ4q496SdjxrT91Wj1spYA91vZXqwXhohXm9sU0Bb:1vBp2E:b5mrIG9yB61GJXbPOhhi5FC7p0Hhe99mlkQKT2yxr7g','2025-10-23 07:42:54.125370'),('nkgk8ojrr4k34fg4rlar5n6a0mdvbtzy','.eJxVjjsOwjAQRO_iGlkm_qek5wyW17smBuSgOJFAiLtDUApo570ZzZOFuMxDWBpNoSDrmWW73wxiulBdAZ5jPY08jXWeCvBV4Rtt_DgiXQ-b-zcwxDZ82hlU1ymBMWkvyYIDUBJ1NiCUNZnISOu8ROHAa8jOQ4q496SdjxrT91Wj1spYA91vZXqwXhohXm9sU0Bb:1vBojL:H5Wt95Z9M_jO0ZMlGK69iJ6RnxFZ6_M5E6MYbNV5rPk','2025-10-23 07:23:23.608117'),('npkhbtuzwxsz95xqeyx82jpa3hxd9em1','.eJxVjjsOwjAQRO_iGlkm_qek5wyW17smBuSgOJFAiLtDUApo570ZzZOFuMxDWBpNoSDrmWW73wxiulBdAZ5jPY08jXWeCvBV4Rtt_DgiXQ-b-zcwxDZ82hlU1ymBMWkvyYIDUBJ1NiCUNZnISOu8ROHAa8jOQ4q496SdjxrT91Wj1spYA91vZXqwXhohXm9sU0Bb:1vBmoE:d0hvn7gn8fP-q-3TX2M0MgdDjBL5-890hfGr1Tnd1LE','2025-10-23 05:20:18.148848'),('t7i7rhsx1zkgx3wk5q22lvetp2lu7fi3','.eJxVjDsOwjAQBe_iGlkm_lPS5wzWrneNA8iR4qRC3B0ipYD2zcx7iQTbWtPWeUkTiYvw4vS7IeQHtx3QHdptlnlu6zKh3BV50C7Hmfh5Pdy_gwq9fuuCZhiMIsg2avYYEI0mWxwq411hdtqHqEkFjBZLiJiBzpFtiGApe_H-APfkOIU:1vBAJM:_5qQP75qqTE_NlxJrul6H_lU-brZ9zQb6E3OEft9ZB8','2025-10-21 12:13:52.016057'),('uq000bkg8h0avad1zv1y8k98a18tqxy8','.eJxVjjsOwjAQRO_iGlkm_qek5wyW17smBuSgOJFAiLtDUApo570ZzZOFuMxDWBpNoSDrmWW73wxiulBdAZ5jPY08jXWeCvBV4Rtt_DgiXQ-b-zcwxDZ82hlU1ymBMWkvyYIDUBJ1NiCUNZnISOu8ROHAa8jOQ4q496SdjxrT91Wj1spYA91vZXqwXhohXm9sU0Bb:1vBnmX:dzJ_UqhiU4kRJAZnxmev-uJtrfaq9uBI0Ry1Kk0tgIU','2025-10-23 06:22:37.249106'),('wdkkz78bo9h0rlef5mgqb6wd7nrj3fax','.eJxVjEEOwiAQRe_C2hAGKp126d4zkAGmFjXQlDbRGO-uTbrQ7X_vv5dwtC6jWyvPLkXRCy0Ov5uncOO8gXilfCkylLzMyctNkTut8lwi30-7-xcYqY7fN3tqwUD0QUcTzWCUbYM1jaZ24A48A-oGVex0FwgQ7LFR3iAiByaEsEUr15pKdvyY0vwUvbFKvT9MWD-g:1vBQ5e:jl4JJLzFiLKyjjG0WyMyEgeXIUWQNhRnXnEblKsBobw','2025-10-22 05:04:46.680530');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-25 20:57:54
