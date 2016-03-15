-- MySQL dump 10.13  Distrib 5.5.47, for debian-linux-gnu (x86_64)
--
-- Host: srvmysql.imerir.com    Database: SmartForest
-- ------------------------------------------------------
-- Server version	5.1.73

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
-- Table structure for table `acces_balise`
--

DROP TABLE IF EXISTS `acces_balise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acces_balise` (
  `idAcces` int(11) NOT NULL AUTO_INCREMENT,
  `idUser` int(11) DEFAULT NULL,
  `idBalise` int(11) DEFAULT NULL,
  PRIMARY KEY (`idAcces`),
  KEY `idUser` (`idUser`),
  KEY `idBalise` (`idBalise`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acces_balise`
--

LOCK TABLES `acces_balise` WRITE;
/*!40000 ALTER TABLE `acces_balise` DISABLE KEYS */;
INSERT INTO `acces_balise` VALUES (1,14,1);
/*!40000 ALTER TABLE `acces_balise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acces_puce`
--

DROP TABLE IF EXISTS `acces_puce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acces_puce` (
  `idAcces` int(11) NOT NULL AUTO_INCREMENT,
  `idUser` int(11) DEFAULT NULL,
  `idPuce` int(11) DEFAULT NULL,
  PRIMARY KEY (`idAcces`),
  KEY `idUser` (`idUser`),
  KEY `idPuce` (`idPuce`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acces_puce`
--

LOCK TABLES `acces_puce` WRITE;
/*!40000 ALTER TABLE `acces_puce` DISABLE KEYS */;
/*!40000 ALTER TABLE `acces_puce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `acces_station`
--

DROP TABLE IF EXISTS `acces_station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acces_station` (
  `idAcces` int(11) NOT NULL AUTO_INCREMENT,
  `idUser` int(11) DEFAULT NULL,
  `idStation` int(11) DEFAULT NULL,
  PRIMARY KEY (`idAcces`),
  KEY `idUser` (`idUser`),
  KEY `idStation` (`idStation`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acces_station`
--

LOCK TABLES `acces_station` WRITE;
/*!40000 ALTER TABLE `acces_station` DISABLE KEYS */;
/*!40000 ALTER TABLE `acces_station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donnees_gps`
--

DROP TABLE IF EXISTS `donnees_gps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donnees_gps` (
  `idReleve` int(11) NOT NULL AUTO_INCREMENT,
  `idPuce` int(11) DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `dateReleve` int(11) DEFAULT NULL,
  PRIMARY KEY (`idReleve`),
  KEY `idPuce` (`idPuce`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donnees_gps`
--

LOCK TABLES `donnees_gps` WRITE;
/*!40000 ALTER TABLE `donnees_gps` DISABLE KEYS */;
/*!40000 ALTER TABLE `donnees_gps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donnees_lora`
--

DROP TABLE IF EXISTS `donnees_lora`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donnees_lora` (
  `idReleve` int(11) NOT NULL AUTO_INCREMENT,
  `idBalise` int(11) DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `ozone` float DEFAULT NULL,
  `humidite` float DEFAULT NULL,
  `dateReleve` int(11) DEFAULT NULL,
  `hygrometrie` float DEFAULT NULL,
  PRIMARY KEY (`idReleve`),
  KEY `idBalise` (`idBalise`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donnees_lora`
--

LOCK TABLES `donnees_lora` WRITE;
/*!40000 ALTER TABLE `donnees_lora` DISABLE KEYS */;
INSERT INTO `donnees_lora` VALUES (2,1,14,12,12,1454284800,12),(3,1,14.2,12,12,1454371200,12);
/*!40000 ALTER TABLE `donnees_lora` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donnees_meteo`
--

DROP TABLE IF EXISTS `donnees_meteo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donnees_meteo` (
  `idReleve` int(11) NOT NULL AUTO_INCREMENT,
  `idStation` int(11) DEFAULT NULL,
  `ensoileillement` float DEFAULT NULL,
  `vitesseVent` float DEFAULT NULL,
  `orientationVent` float DEFAULT NULL,
  `dateReleve` int(11) DEFAULT NULL,
  `precipitation` float DEFAULT NULL,
  PRIMARY KEY (`idReleve`),
  KEY `idStation` (`idStation`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donnees_meteo`
--

LOCK TABLES `donnees_meteo` WRITE;
/*!40000 ALTER TABLE `donnees_meteo` DISABLE KEYS */;
/*!40000 ALTER TABLE `donnees_meteo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `info_balise`
--

DROP TABLE IF EXISTS `info_balise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `info_balise` (
  `idBalise` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `dateDeploiement` int(11) DEFAULT NULL,
  PRIMARY KEY (`idBalise`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `info_balise`
--

LOCK TABLES `info_balise` WRITE;
/*!40000 ALTER TABLE `info_balise` DISABLE KEYS */;
INSERT INTO `info_balise` VALUES (1,'toto',0,0,NULL);
/*!40000 ALTER TABLE `info_balise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `info_connexion`
--

DROP TABLE IF EXISTS `info_connexion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `info_connexion` (
  `idConnection` int(11) NOT NULL AUTO_INCREMENT,
  `idUser` int(11) DEFAULT NULL,
  `login` varchar(30) DEFAULT NULL,
  `motDePasse` varchar(70) DEFAULT NULL,
  `cleAdmin` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`idConnection`),
  KEY `idUser` (`idUser`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `info_connexion`
--

LOCK TABLES `info_connexion` WRITE;
/*!40000 ALTER TABLE `info_connexion` DISABLE KEYS */;
INSERT INTO `info_connexion` VALUES (14,25,'toto','f71dbe52628a3f83a77ab494817525c6',0),(3,14,'abe','f71dbe52628a3f83a77ab494817525c6',1),(4,14,'abe1','f71dbe52628a3f83a77ab494817525c6',0),(5,14,'abe2','f71dbe52628a3f83a77ab494817525c6',0);
/*!40000 ALTER TABLE `info_connexion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `info_puce`
--

DROP TABLE IF EXISTS `info_puce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `info_puce` (
  `idPuce` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) DEFAULT NULL,
  `dateDeploiement` int(11) DEFAULT NULL,
  PRIMARY KEY (`idPuce`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `info_puce`
--

LOCK TABLES `info_puce` WRITE;
/*!40000 ALTER TABLE `info_puce` DISABLE KEYS */;
/*!40000 ALTER TABLE `info_puce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `info_station`
--

DROP TABLE IF EXISTS `info_station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `info_station` (
  `idStation` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `dateDeploiement` int(11) DEFAULT NULL,
  PRIMARY KEY (`idStation`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `info_station`
--

LOCK TABLES `info_station` WRITE;
/*!40000 ALTER TABLE `info_station` DISABLE KEYS */;
/*!40000 ALTER TABLE `info_station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `info_utilisateur`
--

DROP TABLE IF EXISTS `info_utilisateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `info_utilisateur` (
  `idUser` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(30) DEFAULT NULL,
  `prenom` varchar(30) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idUser`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `info_utilisateur`
--

LOCK TABLES `info_utilisateur` WRITE;
/*!40000 ALTER TABLE `info_utilisateur` DISABLE KEYS */;
INSERT INTO `info_utilisateur` VALUES (1,'Toto','Toto','Chef de projet'),(2,'tata','tata','Chef de projet'),(20,'toto','toto','Chef de projet'),(19,'toto','toto','Chef de projet'),(18,'toto','toto','Chef de projet'),(17,'toto','toto','Chef de projet'),(16,'Bes','Arnaud','Chef de projet'),(15,'Bes','Arnaud','Chef de projet'),(14,'Bes','Arnaud','Chef de projet'),(21,'toto','toto','Chef de projet'),(22,'toto','toto','Chef de projet'),(23,'toto','toto','Chef de projet'),(24,'toto','toto','Chef de projet'),(25,'toto','toto','Chef de projet');
/*!40000 ALTER TABLE `info_utilisateur` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-03-08  8:52:56
