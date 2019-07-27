-- MySQL dump 10.13  Distrib 5.6.45, for Linux (x86_64)
--
-- Host: localhost    Database: Player
-- ------------------------------------------------------
-- Server version	5.6.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `Player`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `Player` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `Player`;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` varchar(200) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_delete` tinyint(1) NOT NULL DEFAULT '0',
  `uid` int(11) NOT NULL,
  `vid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `uid` (`uid`),
  KEY `vid` (`vid`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`vid`) REFERENCES `video` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,'ggh','2019-07-23 18:29:58',0,6,13),(2,'content','2019-07-26 16:35:45',0,6,14),(3,'content','2019-07-26 16:36:22',0,7,14),(4,'content','2019-07-26 16:36:31',0,7,14),(5,'content','2019-07-26 16:36:33',0,7,14),(6,'content','2019-07-26 16:36:36',0,7,14),(7,'content','2019-07-26 16:36:38',0,7,14),(8,'content','2019-07-26 16:37:44',0,7,13),(9,'content','2019-07-26 16:37:50',0,7,13),(10,'content','2019-07-26 16:37:52',0,7,13),(11,'content','2019-07-26 16:37:54',0,7,13),(12,'content','2019-07-26 16:37:57',0,7,13);
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(20) DEFAULT NULL,
  `name` varchar(30) NOT NULL,
  `password` varchar(32) NOT NULL,
  `mobile` varchar(11) DEFAULT NULL,
  `email_addr` varchar(30) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `wx_openid` varchar(50) DEFAULT NULL,
  `qq_openid` varchar(50) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `mobile` (`mobile`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,NULL,'6263jjkkk','5566888888','13555767654',NULL,'2019-07-19 17:53:19',NULL,NULL,0),(2,NULL,'626e4w3kkk','5566888888','13578767654',NULL,'2019-07-19 17:57:20',NULL,NULL,0),(3,NULL,'rfasc','retweh','13473523572',NULL,'2019-07-20 01:00:25',NULL,NULL,0),(4,NULL,'dsve','3425325','13232737472',NULL,'2019-07-20 01:04:46',NULL,NULL,0),(5,NULL,'awefsrvs','djfjsgjksd','14334453653',NULL,'2019-07-20 01:08:10',NULL,NULL,0),(6,NULL,'sdfa','12124412','14634634723',NULL,'2019-07-22 21:20:02',NULL,NULL,0),(7,NULL,'media','intel123','13666666666',NULL,'2019-07-26 16:35:14',NULL,NULL,0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video`
--

DROP TABLE IF EXISTS `video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(20) NOT NULL,
  `content` varchar(255) DEFAULT NULL,
  `addr` varchar(100) NOT NULL,
  `img` varchar(100) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_delete` tinyint(1) NOT NULL DEFAULT '0',
  `uid` int(11) NOT NULL,
  `duration` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  KEY `uid` (`uid`),
  CONSTRAINT `video_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video`
--

LOCK TABLES `video` WRITE;
/*!40000 ALTER TABLE `video` DISABLE KEYS */;
INSERT INTO `video` VALUES (13,'bbb_sunflower',NULL,'/bbb_sunflower_1080p_30fps_normal.mp4','/thumbnail/bbb_sunflower_1080p_30fps_normal.mp4.png','2019-07-23 18:14:46',0,2,634),(14,'Nature.mp4',NULL,'/bbb_sunflower_1080p_30fps_normal.mp4','/thumbnail/bbb_sunflower_1080p_30fps_normal.mp4.png','2019-07-26 16:31:13',0,6,60),(15,'Nature_test.mp4',NULL,'/bbb_sunflower_1080p_30fps_normal.mp4','/thumbnail/bbb_sunflower_1080p_30fps_normal.mp4.png','2019-07-26 16:33:33',0,6,60),(17,'Nature_test2.mp4',NULL,'/bbb_sunflower_1080p_30fps_normal.mp4','/thumbnail/bbb_sunflower_1080p_30fps_normal.mp4.png','2019-07-26 23:54:36',0,7,60);
/*!40000 ALTER TABLE `video` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-07-26 23:56:42
