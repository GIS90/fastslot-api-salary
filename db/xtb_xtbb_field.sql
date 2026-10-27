/*
 Navicat Premium Data Transfer

 Source Server         : MY-110.40.141.32[mingliang.gao]
 Source Server Type    : MySQL
 Source Server Version : 100328
 Source Host           : 110.40.141.32:3306
 Source Schema         : salary

 Target Server Type    : MySQL
 Target Server Version : 100328
 File Encoding         : 65001

 Date: 17/10/2026 15:55:35
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for xtb_xtbb_field
-- ----------------------------
DROP TABLE IF EXISTS `xtb_xtbb_field`;
CREATE TABLE `xtb_xtbb_field` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键，自增ID',
  `field` varchar(35) NOT NULL COMMENT '数据库字段名称',
  `name_zh` varchar(35) NOT NULL COMMENT '字段英文名称',
  `name_ch` varchar(35) NOT NULL COMMENT '字段中文名称',
  `md5` varchar(64) NOT NULL COMMENT '数据唯一标识：MD5-ID',
  `xtbb` varchar(35) NOT NULL COMMENT '系统报表名称，关联xtb_xtbb表',
  `remark` varchar(100) DEFAULT NULL COMMENT '字段说明',
  `width` decimal(10,4) NOT NULL COMMENT '宽度',
  `align` varchar(15) DEFAULT NULL COMMENT '对齐方式：left center right',
  `fixed` varchar(35) NOT NULL COMMENT '锁定：left right',
  `list` tinyint(1) DEFAULT 1 COMMENT '列表：1支持；0不支持',
  `list_type` varchar(35) NOT NULL COMMENT 'List字段类型',
  `export` tinyint(1) DEFAULT 1 COMMENT '导出：1支持；0不支持',
  `export_type` varchar(35) NOT NULL COMMENT 'Export字段类型',
  `null` tinyint(1) DEFAULT 1 COMMENT '空值：1允许；0不允许（主要涉及系统数据展示、数据导出）',
  `id_auto` tinyint(1) DEFAULT 1 COMMENT 'ID自增：1自增；0非自增，只对ID字段生效',
  `extend` tinyint(1) DEFAULT 0 COMMENT '扩展字段：1扩展字段；0非扩展字段，拓展字段只对表头字段有效',
  `filter` text DEFAULT NULL COMMENT '字段筛选字段内容，主要是select、radio、checkbox',
  `create_rtx` varchar(35) DEFAULT NULL COMMENT '创建用户RTX-ID',
  `create_time` datetime DEFAULT current_timestamp() COMMENT '创建时间',
  `update_rtx` varchar(35) DEFAULT NULL COMMENT '更新用户RTX-ID',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `delete_rtx` varchar(35) DEFAULT NULL COMMENT '删除用户RTX-ID',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `status` tinyint(1) DEFAULT 0 COMMENT '数据状态：1删除；0正常（默认）',
  `order_id` int(11) DEFAULT NULL COMMENT '排序ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `md5` (`md5`),
  UNIQUE KEY `xtb_xtbb_field_md5_index` (`md5`) USING HASH COMMENT 'md5索引'
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COMMENT='系统表-系统报表字段';

-- ----------------------------
-- Records of xtb_xtbb_field
-- ----------------------------
BEGIN;
INSERT INTO `xtb_xtbb_field` (`id`, `field`, `name_zh`, `name_ch`, `md5`, `xtbb`, `remark`, `width`, `fixed`, `list`, `list_type`, `export`, `export_type`, `null`, `id_auto`, `extend`, `filter`, `create_rtx`, `create_time`, `update_rtx`, `update_time`, `delete_rtx`, `delete_time`, `status`, `order_id`) VALUES (1, 'id', 'id', '序号', '3aabf39f2d943fa886d86dcbbee4d910', 'SystemMainUser', '主键，自增ID', 100.0000, '', 1, 'integer', 1, 'int', 0, 1, 0, '', 'admin', '2026-10-11 00:20:16', NULL, NULL, NULL, NULL, 0, 1);
INSERT INTO `xtb_xtbb_field` (`id`, `field`, `name_zh`, `name_ch`, `md5`, `xtbb`, `remark`, `width`, `fixed`, `list`, `list_type`, `export`, `export_type`, `null`, `id_auto`, `extend`, `filter`, `create_rtx`, `create_time`, `update_rtx`, `update_time`, `delete_rtx`, `delete_time`, `status`, `order_id`) VALUES (2, 'rtx_id', 'rtxId', '账号', 'b1c2d3e4f5a60718293a4b5c6d7e8f90', 'SystemMainUser', 'RTX-ID唯一标识，英文+数字组成', 200.0000, '', 1, 'string', 1, 'string', 0, 0, 0, '{\"type\":\"input\",\"placeholder\":\"请输入账号\"}', 'admin', '2026-10-11 00:20:16', NULL, NULL, NULL, NULL, 0, 2);
INSERT INTO `xtb_xtbb_field` (`id`, `field`, `name_zh`, `name_ch`, `md5`, `xtbb`, `remark`, `width`, `fixed`, `list`, `list_type`, `export`, `export_type`, `null`, `id_auto`, `extend`, `filter`, `create_rtx`, `create_time`, `update_rtx`, `update_time`, `delete_rtx`, `delete_time`, `status`, `order_id`) VALUES (3, 'avatar', 'avatar', '头像', '293a4b5c6d7e8f901223344556677889', 'SystemMainUser', '头像地址', 130.0000, '', 1, 'string', 1, 'string', 1, 0, 0, '', 'admin', '2026-10-11 00:20:16', NULL, NULL, NULL, NULL, 0, 3);
INSERT INTO `xtb_xtbb_field` (`id`, `field`, `name_zh`, `name_ch`, `md5`, `xtbb`, `remark`, `width`, `fixed`, `list`, `list_type`, `export`, `export_type`, `null`, `id_auto`, `extend`, `filter`, `create_rtx`, `create_time`, `update_rtx`, `update_time`, `delete_rtx`, `delete_time`, `status`, `order_id`) VALUES (4, 'name', 'name', '昵称', 'd3e4f5a60718293a4b5c6d7e8f901223', 'SystemMainUser', '昵称', 200.0000, '', 1, 'string', 1, 'string', 1, 0, 0, '{\"type\":\"input\",\"placeholder\":\"请输入昵称\"}', 'admin', '2026-10-11 00:20:16', NULL, NULL, NULL, NULL, 0, 4);
INSERT INTO `xtb_xtbb_field` (`id`, `field`, `name_zh`, `name_ch`, `md5`, `xtbb`, `remark`, `width`, `fixed`, `list`, `list_type`, `export`, `export_type`, `null`, `id_auto`, `extend`, `filter`, `create_rtx`, `create_time`, `update_rtx`, `update_time`, `delete_rtx`, `delete_time`, `status`, `order_id`) VALUES (5, 'sex', 'sex', '性别', 'a60718293a4b5c6d7e8f901223344556', 'SystemMainUser', '性别', 130.0000, '', 1, 'string', 1, 'string', 1, 0, 0, '{\"type\":\"select\",\"placeholder\":\"请选择性别\",\"options\":[{\"label\":\"男\",\"value\":\"男\"},{\"label\":\"女\",\"value\":\"女\"},{\"label\":\"保密\",\"value\":\"保密\"}]}', 'admin', '2026-10-11 00:20:16', NULL, NULL, NULL, NULL, 0, 5);
INSERT INTO `xtb_xtbb_field` (`id`, `field`, `name_zh`, `name_ch`, `md5`, `xtbb`, `remark`, `width`, `fixed`, `list`, `list_type`, `export`, `export_type`, `null`, `id_auto`, `extend`, `filter`, `create_rtx`, `create_time`, `update_rtx`, `update_time`, `delete_rtx`, `delete_time`, `status`, `order_id`) VALUES (6, 'phone', 'phone', '电话', '18293a4b5c6d7e8f9012233445566778', 'SystemMainUser', '电话', 150.0000, '', 1, 'string', 1, 'string', 1, 0, 0, '{\"type\":\"input\",\"placeholder\":\"请输入电话\"}', 'admin', '2026-10-11 00:20:16', NULL, NULL, NULL, NULL, 0, 6);
INSERT INTO `xtb_xtbb_field` (`id`, `field`, `name_zh`, `name_ch`, `md5`, `xtbb`, `remark`, `width`, `fixed`, `list`, `list_type`, `export`, `export_type`, `null`, `id_auto`, `extend`, `filter`, `create_rtx`, `create_time`, `update_rtx`, `update_time`, `delete_rtx`, `delete_time`, `status`, `order_id`) VALUES (7, 'email', 'email', '邮箱', '0718293a4b5c6d7e8f90122334455667', 'SystemMainUser', '邮箱', 200.0000, '', 1, 'string', 1, 'string', 1, 0, 0, '{\"type\":\"input\",\"placeholder\":\"请输入邮箱\"}', 'admin', '2026-10-11 00:20:16', NULL, NULL, NULL, NULL, 0, 7);
INSERT INTO `xtb_xtbb_field` (`id`, `field`, `name_zh`, `name_ch`, `md5`, `xtbb`, `remark`, `width`, `fixed`, `list`, `list_type`, `export`, `export_type`, `null`, `id_auto`, `extend`, `filter`, `create_rtx`, `create_time`, `update_rtx`, `update_time`, `delete_rtx`, `delete_time`, `status`, `order_id`) VALUES (8, 'introduction', 'introduction', '描述', '3a4b5c6d7e8f90122334455667788990', 'SystemMainUser', '描述', 300.0000, '', 0, 'string', 1, 'string', 1, 0, 0, '{\"type\":\"input\",\"placeholder\":\"请输入描述\"}', 'admin', '2026-10-11 00:20:16', NULL, NULL, NULL, NULL, 0, 8);
INSERT INTO `xtb_xtbb_field` (`id`, `field`, `name_zh`, `name_ch`, `md5`, `xtbb`, `remark`, `width`, `fixed`, `list`, `list_type`, `export`, `export_type`, `null`, `id_auto`, `extend`, `filter`, `create_rtx`, `create_time`, `update_rtx`, `update_time`, `delete_rtx`, `delete_time`, `status`, `order_id`) VALUES (9, 'department', 'department', '部门', '5c6d7e8f901223344556677889900a1b', 'SystemMainUser', '部门MD5-ID值，关联department表', 200.0000, '', 1, 'string', 1, 'string', 1, 0, 0, '{\"type\":\"input\",\"placeholder\":\"请输入部门名称\"}', 'admin', '2026-10-11 00:20:16', NULL, NULL, NULL, NULL, 0, 9);
INSERT INTO `xtb_xtbb_field` (`id`, `field`, `name_zh`, `name_ch`, `md5`, `xtbb`, `remark`, `width`, `fixed`, `list`, `list_type`, `export`, `export_type`, `null`, `id_auto`, `extend`, `filter`, `create_rtx`, `create_time`, `update_rtx`, `update_time`, `delete_rtx`, `delete_time`, `status`, `order_id`) VALUES (10, 'create_rtx', 'createRtx', '创建人', '6d7e8f901223344556677889900a1b2c', 'SystemMainUser', '创建用户RTX-ID', 200.0000, '', 1, 'string', 1, 'string', 0, 0, 0, '{\"type\":\"input\",\"placeholder\":\"请输入创建人\"}', 'admin', '2026-10-11 00:20:16', 'admin', '2026-10-17 15:48:42', NULL, NULL, 0, 10);
INSERT INTO `xtb_xtbb_field` (`id`, `field`, `name_zh`, `name_ch`, `md5`, `xtbb`, `remark`, `width`, `fixed`, `list`, `list_type`, `export`, `export_type`, `null`, `id_auto`, `extend`, `filter`, `create_rtx`, `create_time`, `update_rtx`, `update_time`, `delete_rtx`, `delete_time`, `status`, `order_id`) VALUES (11, 'create_time', 'createTime', '创建时间', '7e8f901223344556677889900a1b2c3d', 'SystemMainUser', '创建时间', 180.0000, '', 1, 'datetime', 1, 'datetime', 0, 0, 0, '{\"type\":\"daterange\",\"placeholder\":\"请选择创建时间\"}', 'admin', '2026-10-11 00:20:16', 'admin', '2026-10-17 15:48:37', NULL, NULL, 0, 11);
INSERT INTO `xtb_xtbb_field` (`id`, `field`, `name_zh`, `name_ch`, `md5`, `xtbb`, `remark`, `width`, `fixed`, `list`, `list_type`, `export`, `export_type`, `null`, `id_auto`, `extend`, `filter`, `create_rtx`, `create_time`, `update_rtx`, `update_time`, `delete_rtx`, `delete_time`, `status`, `order_id`) VALUES (12, 'options', 'options', '操作', '93da65a9fd0004d9477aeac024e08e15', 'SystemMainUser', '操作按钮', 160.0000, 'right', 1, 'string', 0, 'string', 0, 0, 0, '', 'admin', '2026-10-11 00:20:16', 'admin', '2026-10-17 15:48:34', NULL, NULL, 0, 12);
INSERT INTO `xtb_xtbb_field` (`id`, `field`, `name_zh`, `name_ch`, `md5`, `xtbb`, `remark`, `width`, `fixed`, `list`, `list_type`, `export`, `export_type`, `null`, `id_auto`, `extend`, `filter`, `create_rtx`, `create_time`, `update_rtx`, `update_time`, `delete_rtx`, `delete_time`, `status`, `order_id`) VALUES (13, 'status', 'status', '状态管理', '223344556677889900a1b2c3d4e5f678', 'SystemMainUser', '数据状态：1注销；0启用（默认）', 180.0000, 'right', 1, 'boolean', 1, 'user_status_text', 1, 0, 1, '{\"type\":\"select\",\"placeholder\":\"请选择状态\",\"options\":[{\"label\":\"启用\",\"value\":false}, {\"label\": \"注销\",\"value\":true}]}', 'admin', '2026-10-11 00:20:16', 'admin', '2026-10-17 15:48:31', NULL, NULL, 0, 13);
INSERT INTO `xtb_xtbb_field` (`id`, `field`, `name_zh`, `name_ch`, `md5`, `xtbb`, `remark`, `width`, `fixed`, `list`, `list_type`, `export`, `export_type`, `null`, `id_auto`, `extend`, `filter`, `create_rtx`, `create_time`, `update_rtx`, `update_time`, `delete_rtx`, `delete_time`, `status`, `order_id`) VALUES (14, 'id', 'ID', '序号', '1aadf55f7539c28ce54f88ba9931d845', 'SystemMainRole', '', 0.0000, '', 1, '', 1, '', 1, 1, 0, '', 'admin', '2026-10-12 22:05:44', NULL, NULL, NULL, NULL, 0, 1);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
