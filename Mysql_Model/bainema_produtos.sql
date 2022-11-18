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
-- Table structure for table `produtos`
--

DROP TABLE IF EXISTS `produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produtos` (
  `ID_produto` smallint NOT NULL AUTO_INCREMENT,
  `Nome` varchar(25) NOT NULL,
  `Qtd` smallint unsigned NOT NULL DEFAULT '0',
  `Tipo` enum('Comida','Bebida') NOT NULL,
  `Preco` decimal(6,2) unsigned NOT NULL,
  `Situacao` enum('Ativo','Inativo') DEFAULT 'Ativo',
  PRIMARY KEY (`ID_produto`),
  UNIQUE KEY `Nome` (`Nome`),
  KEY `idx_tipo` (`Tipo`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos`
--

LOCK TABLES `produtos` WRITE;
/*!40000 ALTER TABLE `produtos` DISABLE KEYS */;
INSERT INTO `produtos` VALUES (1,'Heineken',100,'Bebida',12.00,'Ativo'),(2,'Coca-Cola',1055,'Bebida',10.00,'Ativo'),(3,'Moqueca de Camarao',18,'Comida',120.00,'Inativo'),(4,'Moqueca de Peixe',50,'Comida',120.50,'Inativo'),(5,'Moqueca de Polvo',50,'Comida',120.00,'Inativo'),(6,'Brigadeiro',50,'Comida',10.00,'Inativo'),(7,'PF Peixe Frito',50,'Comida',60.00,'Inativo'),(8,'PF Aratu',50,'Comida',60.00,'Inativo'),(9,'Amstel',50,'Bebida',10.00,'Ativo'),(10,'Agua de Coco',45,'Bebida',6.00,'Ativo'),(11,'Caipi Limao',50,'Bebida',20.00,'Ativo'),(12,'Roska Limao',50,'Bebida',25.00,'Ativo'),(13,'Roska Maracuja',50,'Bebida',25.00,'Ativo'),(14,'Caipi Maracuja',50,'Bebida',20.00,'Ativo'),(15,'Lambreta',50,'Bebida',10.00,'Ativo'),(16,'Suco de Manga',50,'Bebida',10.00,'Ativo'),(17,'Suco de Mangaba',50,'Bebida',10.00,'Ativo'),(18,'Suco de Graviola',50,'Bebida',10.00,'Ativo'),(19,'Suco de Acerola',50,'Bebida',10.00,'Ativo'),(20,'Dose Cachaca',50,'Bebida',10.00,'Ativo'),(21,'Cuba Libre',50,'Bebida',10.00,'Ativo'),(31,'Roska Cacau ',25,'Bebida',7.00,'Ativo');
/*!40000 ALTER TABLE `produtos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-08  7:41:49
