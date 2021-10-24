/*
 Navicat Premium Data Transfer

 Source Server         : toby
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 16/10/2021 11:38:55
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for student_2
-- ----------------------------
DROP TABLE IF EXISTS "student_2";
CREATE TABLE "student_2" (
  "No" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "number" integer NOT NULL,
  "name" TEXT NOT NULL,
  "TEXT"
);

-- ----------------------------
-- Records of student_2
-- ----------------------------
INSERT INTO "student_2" VALUES (1, 1962120002, '陈凯', NULL);
INSERT INTO "student_2" VALUES (2, 1962120007, '陈禹良', NULL);
INSERT INTO "student_2" VALUES (3, 1962120027, '宋青', NULL);
INSERT INTO "student_2" VALUES (4, 1962120032, '牛力斌', NULL);
INSERT INTO "student_2" VALUES (5, 1962120033, '张雲峰', NULL);
INSERT INTO "student_2" VALUES (6, 1962120036, '王路平', NULL);
INSERT INTO "student_2" VALUES (7, 1962120039, '王学鹏', NULL);
INSERT INTO "student_2" VALUES (8, 1962120058, '陈冰瑶', NULL);
INSERT INTO "student_2" VALUES (9, 1962120060, '李雨苁', NULL);
INSERT INTO "student_2" VALUES (10, 1962120061, '林钰怡', NULL);
INSERT INTO "student_2" VALUES (11, 1962120062, '倪思思', NULL);
INSERT INTO "student_2" VALUES (12, 1962120071, '吴万隆', NULL);
INSERT INTO "student_2" VALUES (13, 1962120072, '杨恒涛', NULL);
INSERT INTO "student_2" VALUES (14, 1962120086, '刘奇', NULL);
INSERT INTO "student_2" VALUES (15, 1962120087, '彭青', NULL);
INSERT INTO "student_2" VALUES (16, 1962120095, '管伟杰', NULL);
INSERT INTO "student_2" VALUES (17, 1962120100, '张星兵', NULL);
INSERT INTO "student_2" VALUES (18, 1962120103, '陈凯', NULL);
INSERT INTO "student_2" VALUES (19, 1962120106, '毛宇杰', NULL);
INSERT INTO "student_2" VALUES (20, 1962120111, '陈思滔', NULL);
INSERT INTO "student_2" VALUES (21, 1962120112, '何安妮', NULL);
INSERT INTO "student_2" VALUES (22, 1962120114, '王姝婧', NULL);
INSERT INTO "student_2" VALUES (23, 1962120117, '袁堃彬', NULL);
INSERT INTO "student_2" VALUES (24, 1962120127, '贺泽龙', NULL);
INSERT INTO "student_2" VALUES (25, 1962150038, '赵奕骏', NULL);
INSERT INTO "student_2" VALUES (26, 1963140038, '胡艺婷', NULL);
INSERT INTO "student_2" VALUES (27, 1963170027, '陶嘉轩', NULL);
INSERT INTO "student_2" VALUES (28, 1963910008, '杨振', NULL);
INSERT INTO "student_2" VALUES (29, 1965110108, '柳洲洋', NULL);
INSERT INTO "student_2" VALUES (30, 1965130033, '卢思宇', NULL);

-- ----------------------------
-- Auto increment value for student_2
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 30 WHERE name = 'student_2';

PRAGMA foreign_keys = true;
