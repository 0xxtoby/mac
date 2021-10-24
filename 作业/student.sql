/*
 Navicat Premium Data Transfer

 Source Server         : toby
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 15/10/2021 21:41:29
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS "student";
CREATE TABLE "student" (
  "No" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  " number" integer NOT NULL,
  "name" TEXT NOT NULL,
  "TEXT"
);

-- ----------------------------
-- Auto increment value for student
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 2 WHERE name = 'student';

PRAGMA foreign_keys = true;
