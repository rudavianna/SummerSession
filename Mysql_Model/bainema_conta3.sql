-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: bainema
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `conta3`
--

DROP TABLE IF EXISTS `conta3`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conta3` (
  `ID_venda` smallint DEFAULT NULL,
  `Dinheiro` decimal(5,2) DEFAULT NULL,
  `Cartao` decimal(5,2) DEFAULT NULL,
  `Pix` decimal(5,2) DEFAULT NULL,
  `Situacao` enum('Pago','Pendente','') DEFAULT '',
  `ID_produto` smallint NOT NULL,
  `Qtd` smallint unsigned NOT NULL,
  `PrecoVendido` decimal(5,2) unsigned NOT NULL,
  UNIQUE KEY `ID_produto` (`ID_produto`),
  KEY `fk_ID_venda_3` (`ID_venda`),
  CONSTRAINT `fk_ID_produto_3` FOREIGN KEY (`ID_produto`) REFERENCES `produtos` (`ID_produto`),
  CONSTRAINT `fk_ID_venda_3` FOREIGN KEY (`ID_venda`) REFERENCES `venda` (`ID_venda`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conta3`
--

LOCK TABLES `conta3` WRITE;
/*!40000 ALTER TABLE `conta3` DISABLE KEYS */;
INSERT INTO `conta3` VALUES (3,10.00,0.00,0.00,'Pago',6,1,10.00);
/*!40000 ALTER TABLE `conta3` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-08  7:41:51
