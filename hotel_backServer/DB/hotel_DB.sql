-- --------------------------------------------------------
-- 主机:                           localhost
-- 服务器版本:                        8.3.0 - MySQL Community Server - GPL
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  12.6.0.6816
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 导出 hotel_db 的数据库结构
CREATE DATABASE IF NOT EXISTS `hotel_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `hotel_db`;

-- 导出  存储过程 hotel_db.add_order 结构
DELIMITER //
CREATE PROCEDURE `add_order`(
	IN `订单编号` VARCHAR(50),
	IN `用户id` VARCHAR(50),
	IN `房型编号` VARCHAR(50),
	IN `身份证号码` VARCHAR(50),
	IN `入住日期` DATE,
	IN `退房日期` DATE
)
BEGIN
SET @room_num_order = 0;
SET @roon_num = 0;
SET @per_day_price = 0;
SELECT COUNT(*) INTO @room_num_order FROM 订单表 book  WHERE 
((book.预计入住日期 >= 入住日期 AND book.预计入住日期 <= 退房日期) 
OR (book.`预计离开日期`<= 退房日期 AND book.`预计离开日期`>= 入住日期)
OR (book.`预计入住日期`<=入住日期 AND book.`预计离开日期` >= 退房日期)
)AND book.`房型号` = 房型编号;
SELECT 房型数量 INTO @room_num FROM 房型表 WHERE 房型表.`房型号`= 房型编号;
SELECT 房型价格 INTO @per_day_price FROM 房型表 WHERE 房型表.`房型号`= 房型编号;
if @room_num_order<@room_num then
INSERT INTO 订单表 VALUE (订单编号,用户id,房型编号,身份证号码,入住日期,退房日期,(退房日期-入住日期)*@per_day_price,'未支付'); 
END if;
END//
DELIMITER ;

-- 导出  表 hotel_db.入住登记表 结构
CREATE TABLE IF NOT EXISTS `入住登记表` (
  `订单编号` char(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `服务人员编号` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `房间号` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `证件号码` char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `姓名` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `入住日期` datetime NOT NULL,
  `押金` float NOT NULL COMMENT '一人100',
  `预计离开日期` datetime NOT NULL,
  PRIMARY KEY (`订单编号`) USING BTREE,
  KEY `FK_入住登记表_房间表` (`房间号`) USING BTREE,
  KEY `FK_入住登记表_服务人员表` (`服务人员编号`) USING BTREE,
  CONSTRAINT `FK_入住登记表_房间表` FOREIGN KEY (`房间号`) REFERENCES `房间表` (`房间号`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_入住登记表_服务人员表` FOREIGN KEY (`服务人员编号`) REFERENCES `服务人员表` (`服务人员编号`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_入住登记表_订单表` FOREIGN KEY (`订单编号`) REFERENCES `订单表` (`订单编号`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  hotel_db.入住登记表 的数据：~3 rows (大约)
INSERT INTO `入住登记表` (`订单编号`, `服务人员编号`, `房间号`, `证件号码`, `姓名`, `入住日期`, `押金`, `预计离开日期`) VALUES
	('1234', '1', '204', '213', '32', '2024-06-01 09:27:14', 32, '2024-06-02 00:00:00'),
	('2Ydwuygd+dg', 'staff123', '203', 'wetyu54334546787720', 'pyy', '2024-05-29 20:43:19', 200, '2024-05-31 20:43:31'),
	('5lAziS4-HJvw', 'staff123', '502', '431032137978139289', '周棵', '2024-05-28 00:00:00', 200, '2024-06-06 00:00:00');

-- 导出  表 hotel_db.房型表 结构
CREATE TABLE IF NOT EXISTS `房型表` (
  `房型号` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `房型类别` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '标准单人、标准双人、标准三人、高级单人、高级双人、高级三人、豪华单人、豪华双人、豪华三人',
  `房型价格` float NOT NULL COMMENT '每天的房型价格',
  `房型数量` int NOT NULL COMMENT '9种房型的各自的总数量',
  `面积` float DEFAULT NULL,
  `床` char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `每日打扫` enum('有','没有') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `牙刷` enum('有','没有') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `牙膏` enum('有','没有') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `沐浴露` enum('有','没有') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `洗发水` enum('有','没有') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `免费wifi` enum('有','没有') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `电视` enum('有','没有') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `毛巾` enum('有','没有') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `私人卫浴` enum('有','没有') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `吹风机` enum('有','没有') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `房型介绍` char(50) DEFAULT NULL,
  PRIMARY KEY (`房型号`) USING BTREE,
  KEY `房型类别` (`房型类别`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  hotel_db.房型表 的数据：~9 rows (大约)
INSERT INTO `房型表` (`房型号`, `房型类别`, `房型价格`, `房型数量`, `面积`, `床`, `每日打扫`, `牙刷`, `牙膏`, `沐浴露`, `洗发水`, `免费wifi`, `电视`, `毛巾`, `私人卫浴`, `吹风机`, `房型介绍`) VALUES
	('1', '单人房', 150, 15, 15, '一张1.8米单人床', '有', '有', '有', '有', '有', '有', '有', '有', '有', '有', '商务大床房'),
	('2', '双人房', 236, 10, 25, '一张1.8米双人床', '有', '有', '有', '有', '有', '有', '有', '有', '有', '有', '普通双人床'),
	('3', '双床房', 288, 10, 30, '两张1.8米单人床', '有', '有', '有', '有', '有', '有', '有', '有', '有', '有', '商务双床房'),
	('4', '套房', 500, 10, 50, '两张1.8米双人床', '有', '有', '有', '有', '有', '有', '有', '有', '有', '有', '一个套房里有两个房间，和一个洗手间'),
	('5', '大床房', 300, 10, 30, '一张1.8米单人床', '有', '有', '有', '有', '有', '有', '有', '有', '有', '有', '豪华大床房'),
	('6', '豪华双人房', 450, 10, 50, '一张1.8米双人床', '有', '有', '有', '有', '有', '有', '有', '有', '有', '有', '豪华双人床'),
	('7', '豪华双床房', 516, 10, 60, '两张1.8米单人床', '有', '有', '有', '有', '有', '有', '有', '有', '有', '有', '豪华双床房'),
	('8', '套房', 800, 5, 100, '三张1.8米单人床', '有', '有', '有', '有', '有', '有', '有', '有', '有', '有', '豪华套房'),
	('9', '总统套房', 1888, 3, 200, '两张2.0米双人床', '有', '有', '有', '有', '有', '有', '有', '有', '有', '有', '这是总统套房');

-- 导出  表 hotel_db.房间表 结构
CREATE TABLE IF NOT EXISTS `房间表` (
  `房间号` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `房型号` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `使用状态` enum('空','满') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '空' COMMENT '是或否',
  PRIMARY KEY (`房间号`) USING BTREE,
  KEY `FK_房间表_房型表` (`房型号`) USING BTREE,
  CONSTRAINT `FK_房间表_房型表` FOREIGN KEY (`房型号`) REFERENCES `房型表` (`房型号`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  hotel_db.房间表 的数据：~84 rows (大约)
INSERT INTO `房间表` (`房间号`, `房型号`, `使用状态`) VALUES
	('1000', '9', '空'),
	('1001', '9', '空'),
	('1002', '9', '空'),
	('200', '1', '空'),
	('201', '1', '空'),
	('202', '1', '空'),
	('203', '1', '满'),
	('204', '1', '空'),
	('205', '1', '空'),
	('206', '1', '空'),
	('207', '1', '空'),
	('208', '1', '空'),
	('209', '1', '空'),
	('210', '1', '空'),
	('211', '1', '空'),
	('212', '1', '空'),
	('213', '1', '空'),
	('214', '1', '空'),
	('215', '1', '空'),
	('300', '2', '空'),
	('301', '2', '空'),
	('302', '2', '空'),
	('303', '2', '空'),
	('304', '2', '空'),
	('305', '2', '空'),
	('306', '2', '空'),
	('307', '2', '空'),
	('308', '2', '空'),
	('309', '2', '空'),
	('400', '3', '空'),
	('401', '3', '空'),
	('402', '3', '空'),
	('403', '3', '空'),
	('404', '3', '空'),
	('405', '3', '空'),
	('406', '3', '空'),
	('407', '3', '空'),
	('408', '3', '空'),
	('409', '3', '空'),
	('500', '4', '空'),
	('501', '4', '空'),
	('502', '4', '空'),
	('503', '4', '满'),
	('504', '4', '满'),
	('505', '4', '空'),
	('506', '4', '满'),
	('507', '4', '空'),
	('508', '4', '空'),
	('509', '4', '空'),
	('600', '5', '空'),
	('601', '5', '空'),
	('602', '5', '空'),
	('603', '5', '空'),
	('604', '5', '空'),
	('605', '5', '空'),
	('606', '5', '空'),
	('607', '5', '空'),
	('608', '5', '空'),
	('609', '5', '空'),
	('700', '6', '空'),
	('701', '6', '空'),
	('702', '6', '空'),
	('703', '6', '空'),
	('704', '6', '空'),
	('705', '6', '空'),
	('706', '6', '空'),
	('707', '6', '空'),
	('708', '6', '空'),
	('709', '6', '空'),
	('800', '7', '空'),
	('801', '7', '空'),
	('802', '7', '空'),
	('803', '7', '空'),
	('804', '7', '空'),
	('805', '7', '空'),
	('806', '7', '空'),
	('807', '7', '空'),
	('808', '7', '空'),
	('809', '7', '空'),
	('900', '8', '空'),
	('901', '8', '空'),
	('902', '8', '空'),
	('903', '8', '空'),
	('904', '8', '空');

-- 导出  表 hotel_db.接站预约表 结构
CREATE TABLE IF NOT EXISTS `接站预约表` (
  `接站订单编号` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `接送形式编码` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `订单编号` char(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `接站日期` datetime NOT NULL,
  `接站地址` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `完成状态` enum('已完成','未完成') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '未完成',
  PRIMARY KEY (`接站订单编号`) USING BTREE,
  KEY `FK_接送预约表_接送服务表` (`接送形式编码`) USING BTREE,
  KEY `接站日期` (`接站日期`) USING BTREE,
  KEY `FK_接站预约表_订单表` (`订单编号`) USING BTREE,
  CONSTRAINT `FK_接站预约表_订单表` FOREIGN KEY (`订单编号`) REFERENCES `订单表` (`订单编号`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_接送预约表_接送服务表` FOREIGN KEY (`接送形式编码`) REFERENCES `接送类型表` (`接送形式编码`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  hotel_db.接站预约表 的数据：~1 rows (大约)
INSERT INTO `接站预约表` (`接站订单编号`, `接送形式编码`, `订单编号`, `接站日期`, `接站地址`, `完成状态`) VALUES
	('wduydablih213', '2', 'AmCKa4wVGRh4', '2024-05-27 20:39:12', '北京大兴国际机场', '未完成');

-- 导出  表 hotel_db.接送类型表 结构
CREATE TABLE IF NOT EXISTS `接送类型表` (
  `接送形式编码` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `接送形式` char(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '标准、高级、豪华',
  `接送费用` float NOT NULL COMMENT '每次的费用',
  `接送介绍` char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`接送形式编码`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  hotel_db.接送类型表 的数据：~3 rows (大约)
INSERT INTO `接送类型表` (`接送形式编码`, `接送形式`, `接送费用`, `接送介绍`) VALUES
	('1', '普通接送', 5, '我们提供经济实惠的普通接送服务，确保您安全、准时地抵达目的地。无论您是来自哪里，都能享受到舒适的乘车体验。'),
	('2', '公务接送', 30, '我们的公务接送服务为商务旅行者提供高效、便捷的交通解决方案。我们的专业司机团队会确保您按时到达会议地点或商务活动。'),
	('3', '豪华接送', 200, '豪华接送服务为您提供一流的乘车体验，配备舒适的座椅、高级车辆以及专业司机。无论是商务会议还是休闲旅行，我们都能满足您的高品质需求。');

-- 导出  表 hotel_db.服务人员表 结构
CREATE TABLE IF NOT EXISTS `服务人员表` (
  `服务人员编号` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `服务人员姓名` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `服务人员性别` enum('男','女') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '男、女',
  `服务人员登录密码` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `服务人员联系电话` char(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`服务人员编号`) USING BTREE,
  UNIQUE KEY `服务人员联系电话` (`服务人员联系电话`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  hotel_db.服务人员表 的数据：~2 rows (大约)
INSERT INTO `服务人员表` (`服务人员编号`, `服务人员姓名`, `服务人员性别`, `服务人员登录密码`, `服务人员联系电话`) VALUES
	('1', '1', '男', '1', '1'),
	('staff123', 'qwe', '男', 'staffpwd', 'staff123');

-- 导出  表 hotel_db.点餐表 结构
CREATE TABLE IF NOT EXISTS `点餐表` (
  `点餐单号` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `房间号` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `套餐编号` char(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `订单编号` char(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `送餐时间` datetime NOT NULL,
  `就餐人数` int DEFAULT NULL,
  `点餐费用` float NOT NULL,
  `套餐口味` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `备注` tinytext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `完成状态` enum('已完成','未完成') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '未完成',
  PRIMARY KEY (`点餐单号`) USING BTREE,
  KEY `FK_点餐表_入住登记表` (`房间号`) USING BTREE,
  KEY `FK_点餐表_餐单表` (`套餐编号`) USING BTREE,
  KEY `FK_点餐表_订单表` (`订单编号`) USING BTREE,
  CONSTRAINT `FK_点餐表_入住登记表` FOREIGN KEY (`房间号`) REFERENCES `入住登记表` (`房间号`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_点餐表_订单表` FOREIGN KEY (`订单编号`) REFERENCES `订单表` (`订单编号`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_点餐表_餐单表` FOREIGN KEY (`套餐编号`) REFERENCES `餐单表` (`套餐编号`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  hotel_db.点餐表 的数据：~0 rows (大约)

-- 导出  表 hotel_db.用户表 结构
CREATE TABLE IF NOT EXISTS `用户表` (
  `用户ID` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `用户名` char(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `姓名` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `证件号码` char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `年龄` tinyint DEFAULT NULL COMMENT '不超过150',
  `证件类型` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '身份证、港澳台通行证、外国人永久居留身份证、护照',
  `性别` enum('男','女') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '男、女',
  `联系电话` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `邮箱` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `登录密码` char(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`用户ID`) USING BTREE,
  UNIQUE KEY `联系电话` (`联系电话`),
  KEY `证件号码` (`证件号码`) USING BTREE,
  KEY `姓名` (`姓名`) USING BTREE,
  KEY `用户名` (`用户名`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  hotel_db.用户表 的数据：~6 rows (大约)
INSERT INTO `用户表` (`用户ID`, `用户名`, `姓名`, `证件号码`, `年龄`, `证件类型`, `性别`, `联系电话`, `邮箱`, `登录密码`) VALUES
	('DSP1XuS0', 'Barry_zhou', '张三', '431032137978139289', 18, '身份证', '男', '15307834681', '1985759001@qq.com', '123456'),
	('mfaZ_z7U', '123456789', '王五', '12135432423', 18, '身份证', '男', '213243543', '43453@41.com', '123456789'),
	('O0IX5Ezi', '1234567890', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '1234567890'),
	('SLTlkQzk', 'pyy050208', 'pyy', '430426123728894794', 18, '身份证', '女', '13267687363', 'pyy@edu.cau.com', '2022308160235'),
	('w1he3-BY', '12345678', '李四', '430426200407170012', 18, '身份证', '男', '15307834682', '1985759001@qq.com', '12345678'),
	('YdpKtIi_', '这是一个新的账户', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '12345678');

-- 导出  表 hotel_db.订单表 结构
CREATE TABLE IF NOT EXISTS `订单表` (
  `订单编号` char(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `用户ID` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `房型号` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `证件号码` char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `预计入住日期` date NOT NULL,
  `预计离开日期` date NOT NULL,
  `预计住宿费用` float NOT NULL COMMENT '房型价格×天数',
  `定金支付状态` enum('已支付','未支付') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '未支付',
  PRIMARY KEY (`订单编号`) USING BTREE,
  KEY `FK_订单表_用户表` (`用户ID`) USING BTREE,
  KEY `FK_订单表_房型表` (`房型号`) USING BTREE,
  CONSTRAINT `FK_订单表_房型表` FOREIGN KEY (`房型号`) REFERENCES `房型表` (`房型号`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_订单表_用户表` FOREIGN KEY (`用户ID`) REFERENCES `用户表` (`用户ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  hotel_db.订单表 的数据：~6 rows (大约)
INSERT INTO `订单表` (`订单编号`, `用户ID`, `房型号`, `证件号码`, `预计入住日期`, `预计离开日期`, `预计住宿费用`, `定金支付状态`) VALUES
	('1234', 'w1he3-BY', '2', '430426200407170012', '2024-06-01', '2024-06-02', 1416, '未支付'),
	('2Ydwuygd+dg', 'SLTlkQzk', '8', '213214435434354666', '2024-05-29', '2024-05-31', 200, '未支付'),
	('5lAziS4-HJvw', 'DSP1XuS0', '4', '431032137978139289', '2024-05-20', '2024-05-25', 500, '已支付'),
	('AmCKa4wVGRh4', 'DSP1XuS0', '4', '431032137978139289', '2024-06-03', '2024-06-04', 500, '已支付'),
	('dasd@43dsfhyt0', 'SLTlkQzk', '2', '34567sdfyytu3242433', '2024-06-03', '2024-06-07', 300, '未支付'),
	('W1GDNCPsqZ84', 'DSP1XuS0', '9', '431032137978139289', '2024-06-05', '2024-06-07', 3776, '已支付');

-- 导出  表 hotel_db.账单表 结构
CREATE TABLE IF NOT EXISTS `账单表` (
  `订单编号` char(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `用户ID` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `服务人员编号` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `实际住宿费用` float NOT NULL,
  `预计住宿费用` float NOT NULL,
  `点餐费用` float NOT NULL,
  `损坏费用` float NOT NULL,
  `接站费用` float NOT NULL,
  `送站费用` float NOT NULL,
  `押金` float NOT NULL,
  `总费用` float NOT NULL,
  `退房日期` datetime NOT NULL,
  ` 支付状态` enum('未支付','已支付') NOT NULL DEFAULT '未支付',
  PRIMARY KEY (`订单编号`) USING BTREE,
  KEY `FK_账单表_用户表` (`用户ID`) USING BTREE,
  KEY `FK_账单表_服务人员表` (`服务人员编号`) USING BTREE,
  CONSTRAINT `FK_账单表_服务人员表` FOREIGN KEY (`服务人员编号`) REFERENCES `服务人员表` (`服务人员联系电话`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_账单表_用户表` FOREIGN KEY (`用户ID`) REFERENCES `用户表` (`用户ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_账单表_订单表` FOREIGN KEY (`订单编号`) REFERENCES `订单表` (`订单编号`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  hotel_db.账单表 的数据：~1 rows (大约)
INSERT INTO `账单表` (`订单编号`, `用户ID`, `服务人员编号`, `实际住宿费用`, `预计住宿费用`, `点餐费用`, `损坏费用`, `接站费用`, `送站费用`, `押金`, `总费用`, `退房日期`, ` 支付状态`) VALUES
	('5lAziS4-HJvw', 'DSP1XuS0', 'staff123', 0, 500, 200, 0, 0, 0, 200, -800, '2024-06-03 00:00:00', '未支付');

-- 导出  表 hotel_db.退房登记表 结构
CREATE TABLE IF NOT EXISTS `退房登记表` (
  `退房日期` datetime NOT NULL,
  `损坏费用` float NOT NULL,
  `损坏情况描述` char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '没有、一般、严重',
  `订单编号` char(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `服务人员联系电话` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `实际住宿费用` float NOT NULL,
  PRIMARY KEY (`订单编号`) USING BTREE,
  KEY `FK_退房登记表_服务人员表` (`服务人员联系电话`) USING BTREE,
  CONSTRAINT `FK_退房登记表_服务人员表` FOREIGN KEY (`服务人员联系电话`) REFERENCES `服务人员表` (`服务人员联系电话`),
  CONSTRAINT `FK_退房登记表_订单表` FOREIGN KEY (`订单编号`) REFERENCES `订单表` (`订单编号`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  hotel_db.退房登记表 的数据：~1 rows (大约)
INSERT INTO `退房登记表` (`退房日期`, `损坏费用`, `损坏情况描述`, `订单编号`, `服务人员联系电话`, `实际住宿费用`) VALUES
	('2024-06-03 00:00:00', 0, '无', '5lAziS4-HJvw', 'staff123', 0);

-- 导出  表 hotel_db.送站预约表 结构
CREATE TABLE IF NOT EXISTS `送站预约表` (
  `送站订单编号` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `接送形式编码` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `订单编号` char(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `送站日期` datetime NOT NULL,
  `送站地址` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `完成状态` enum('已完成','未完成') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '未完成',
  PRIMARY KEY (`送站订单编号`) USING BTREE,
  KEY `FK_送人预约表_接送服务表` (`接送形式编码`) USING BTREE,
  KEY `送站日期` (`送站日期`) USING BTREE,
  KEY `FK_送站预约表_订单表` (`订单编号`) USING BTREE,
  CONSTRAINT `FK_送人预约表_接送服务表` FOREIGN KEY (`接送形式编码`) REFERENCES `接送类型表` (`接送形式编码`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_送站预约表_订单表` FOREIGN KEY (`订单编号`) REFERENCES `订单表` (`订单编号`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  hotel_db.送站预约表 的数据：~1 rows (大约)
INSERT INTO `送站预约表` (`送站订单编号`, `接送形式编码`, `订单编号`, `送站日期`, `送站地址`, `完成状态`) VALUES
	('5abDUMXpHIiX', '3', 'AmCKa4wVGRh4', '2024-05-31 14:31:20', '大兴国际机场', '未完成');

-- 导出  表 hotel_db.餐单表 结构
CREATE TABLE IF NOT EXISTS `餐单表` (
  `套餐编号` char(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `套餐类别` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '早餐、中餐、晚餐',
  `套餐名字` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `套餐价格` float NOT NULL,
  `套餐口味` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '无辣、微辣、中辣、特辣',
  `套餐介绍` char(50) DEFAULT NULL,
  PRIMARY KEY (`套餐编号`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 正在导出表  hotel_db.餐单表 的数据：~11 rows (大约)
INSERT INTO `餐单表` (`套餐编号`, `套餐类别`, `套餐名字`, `套餐价格`, `套餐口味`, `套餐介绍`) VALUES
	('1', '早餐', '极简主义', 15, '咸口', '（一人份）香酥大油条+原味豆浆'),
	('10', '晚餐', '贵州风味', 150, '酸', '（两人份）+酸汤鱼+时令蔬菜+米饭'),
	('11', '晚餐', '山西风味', 25, '不辣', '（一人份）+山西刀削面'),
	('2', '早餐', '肉食主义', 20, '咸口', '（一人份）小笼包+原味豆浆'),
	('3', '早餐', '煎饼大侠', 25, '咸口', '（一人份）天津煎饼果子（内含火腿、鸡蛋、薄脆等）+原味豆浆'),
	('4', '午餐', '湖南风味', 35, '辣', '（一人份）辣椒炒肉+时令蔬菜+金钱蛋+米饭'),
	('5', '午餐', '四川风味', 45, '综合', '（一人份）翘脚牛肉+狼牙土豆+醪糟汤圆+米饭'),
	('6', '午餐', '东北风味', 198, '不辣', '（四人份）铁锅炖大鹅+米饭'),
	('7', '午餐', '广东风味', 40, '清淡', '（一人份）+虾仁煲仔饭+时令蔬菜'),
	('8', '晚餐', '江西风味', 25, '辣', '（一人份）+南昌拌粉'),
	('9', '晚餐', '新疆风味', 25, '辣', '（一人份）+新疆炒米粉');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
