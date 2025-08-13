/*
 Navicat MySQL Data Transfer

 Source Server         : 本机SQL
 Source Server Type    : MySQL
 Source Server Version : 50719
 Source Host           : localhost:3306
 Source Schema         : bsdb

 Target Server Type    : MySQL
 Target Server Version : 50719
 File Encoding         : 65001

 Date: 13/08/2025 01:22:05
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for application
-- ----------------------------
DROP TABLE IF EXISTS `application`;
CREATE TABLE `application`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '申请人姓名',
  `type` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '请假类型',
  `start_time` datetime NULL DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime NULL DEFAULT NULL COMMENT '结束时间',
  `reason` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '请假说明',
  `apply_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '申请时间',
  `status` int(255) NOT NULL DEFAULT 0 COMMENT '状态',
  `audit_remark` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '审批意见',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '请假表\r\n' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of application
-- ----------------------------
INSERT INTO `application` VALUES (9, '钱伟烨', '事假', '2025-08-01 00:00:00', '2025-08-02 00:00:00', 'aa', '2025-08-04 00:25:34', 2, '拒绝');
INSERT INTO `application` VALUES (15, '钱伟烨', '事假', '2025-07-31 00:00:00', '2025-08-29 00:00:00', 'bb', '2025-08-04 00:53:34', 1, '通过');
INSERT INTO `application` VALUES (20, '钱伟烨', '事假', '2025-07-30 00:00:00', '2025-08-29 00:00:00', 'dd', '2025-08-05 02:12:35', 1, '批准');
INSERT INTO `application` VALUES (21, '李五', '病假', '2025-08-01 00:00:00', '2025-08-20 00:00:00', '生病了', '2025-08-05 23:20:23', 1, '准了');
INSERT INTO `application` VALUES (22, '李五', '校外实习', '2025-08-01 00:00:00', '2025-10-24 00:00:00', '实习', '2025-08-05 23:23:46', 1, '好好实习');
INSERT INTO `application` VALUES (23, '钱伟烨', '丧假', '2025-08-01 00:00:00', '2025-08-28 00:00:00', 'aa', '2025-08-11 00:01:09', 0, NULL);
INSERT INTO `application` VALUES (24, '钱七', '病假', '2025-08-01 00:00:00', '2025-08-02 00:00:00', '生病了', '2025-08-11 00:43:14', 0, NULL);

-- ----------------------------
-- Table structure for college
-- ----------------------------
DROP TABLE IF EXISTS `college`;
CREATE TABLE `college`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `college_id` int(11) NOT NULL,
  `college_name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '学院表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of college
-- ----------------------------
INSERT INTO `college` VALUES (1, 101, '计算机学院');
INSERT INTO `college` VALUES (2, 102, '工程学院');
INSERT INTO `college` VALUES (3, 103, '商学院');
INSERT INTO `college` VALUES (4, 104, '艺术学院');
INSERT INTO `college` VALUES (5, 105, '医学院');
INSERT INTO `college` VALUES (7, 109, '信息工程学院');

-- ----------------------------
-- Table structure for counsellor
-- ----------------------------
DROP TABLE IF EXISTS `counsellor`;
CREATE TABLE `counsellor`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `username` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '123456',
  `email` varchar(120) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `sex` tinyint(1) NULL DEFAULT NULL,
  `phone` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `role_id` int(11) NOT NULL DEFAULT 2,
  `register_time` datetime NULL DEFAULT NULL,
  `last_login_time` datetime NULL DEFAULT NULL,
  `ip` varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `description` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `speciality_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '教师表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of counsellor
-- ----------------------------
INSERT INTO `counsellor` VALUES (1, '张教授', 'prof_zhang', '123456', 'prof_zhang@univ.edu', 1, '13800139001', 2, '2021-03-15 09:30:00', '2023-11-05 08:45:22', '192.168.2.101', '计算机科学主任', 1001);
INSERT INTO `counsellor` VALUES (2, '李导师', 'tutor_li', '123456', 'tutor_li@univ.edu', 2, '13800139002', 2, '2020-09-10 10:15:00', '2023-11-05 10:20:15', '192.168.2.102', '软件工程导师', 1002);
INSERT INTO `counsellor` VALUES (3, '王讲师', 'lect_wang', '123456', 'lect_wang@univ.edu', 1, '13800139003', 2, '2019-12-01 11:00:00', '2023-11-05 11:30:45', '192.168.2.103', '网络工程讲师', 1001);
INSERT INTO `counsellor` VALUES (4, '赵教师', 'teach_zhao', '123456', 'teach_zhao@univ.edu', 2, '13800139004', 2, '2022-05-20 13:45:00', '2023-11-05 13:15:30', '192.168.2.104', '人工智能教师', 1001);
INSERT INTO `counsellor` VALUES (5, '陈副教授', 'a_prof_chen', '123456', 'a_prof_chen@univ.edu', 1, '13800139005', 2, '2020-02-18 14:30:00', '2023-11-05 14:40:18', '192.168.2.105', '数据科学副教授', 1001);
INSERT INTO `counsellor` VALUES (6, '刘导师', 'tutor_liu', '123456', 'tutor_liu@univ.edu', 2, '13800139006', 2, '2018-07-05 15:20:00', '2023-11-05 15:25:22', '192.168.2.106', '系统架构导师', 1001);
INSERT INTO `counsellor` VALUES (7, '杨讲师', 'lect_yang', '123456', 'lect_yang@univ.edu', 1, '13800139007', 2, '2019-04-10 16:10:00', '2023-11-05 16:35:40', '192.168.2.107', '算法设计讲师', 1001);
INSERT INTO `counsellor` VALUES (8, '徐教师', 'teach_xu', '123456', 'teach_xu@univ.edu', 2, '13800139008', 2, '2021-11-25 08:45:00', '2023-11-06 09:10:25', '192.168.2.108', '软件测试教师', 1001);
INSERT INTO `counsellor` VALUES (9, '周教授', 'prof_zhou', '123456', 'prof_zhou@univ.edu', 1, '13800139009', 2, '2020-06-15 10:30:00', '2023-11-06 10:45:15', '192.168.2.109', '计算机视觉教授', 1001);
INSERT INTO `counsellor` VALUES (10, '吴导师', 'tutor_wu', '123456', 'tutor_wu@univ.edu', 2, '13800139010', 2, '2019-09-05 11:15:00', '2023-11-06 11:50:30', '192.168.2.110', '前端开发导师', 1001);
INSERT INTO `counsellor` VALUES (11, '郑讲师', 'lect_zheng', '123456', 'lect_zheng@univ.edu', 1, '13800139011', 2, '2021-02-20 13:00:00', '2023-11-06 13:20:45', '192.168.2.111', '后端开发讲师', 1001);
INSERT INTO `counsellor` VALUES (12, '孙教师', 'teach_sun', '123456', 'teach_sun@univ.edu', 2, '13800139012', 2, '2018-11-10 14:45:00', '2023-11-06 14:30:10', '192.168.2.112', '网络安全教师', 1001);
INSERT INTO `counsellor` VALUES (13, '钱副教授', 'a_prof_qian', '123456', 'a_prof_qian@univ.edu', 1, '13800139013', 2, '2019-05-30 15:30:00', '2023-11-06 15:40:20', '192.168.2.113', '嵌入式系统副教授', 1001);
INSERT INTO `counsellor` VALUES (14, '冯导师', 'tutor_feng', '123456', 'tutor_feng@univ.edu', 2, '13800139014', 2, '2020-08-20 16:20:00', '2023-11-06 16:55:35', '192.168.2.114', '数据库管理导师', 1001);
INSERT INTO `counsellor` VALUES (15, '朱讲师', 'lect_zhu', '123456', 'lect_zhu@univ.edu', 1, '13800139015', 2, '2022-01-05 08:30:00', '2023-11-06 17:10:50', '127.0.0.1', '云计算讲师', 1001);
INSERT INTO `counsellor` VALUES (17, '戴益飞', 'dyf', '222', 'dyf@qq.com', 1, '12355778899', 2, NULL, NULL, '127.0.0.1', '小程序开发讲师', 1001);

-- ----------------------------
-- Table structure for log
-- ----------------------------
DROP TABLE IF EXISTS `log`;
CREATE TABLE `log`  (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '操作内容',
  `time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '操作时间',
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '操作人',
  `ip` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'IP地址',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 128 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '操作日志表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of log
-- ----------------------------
INSERT INTO `log` VALUES (120, '登录系统', '2025-08-12 01:39:59', 'dyf', '127.0.0.1');
INSERT INTO `log` VALUES (121, '登录系统', '2025-08-12 01:41:21', 'qwy', '127.0.0.1');
INSERT INTO `log` VALUES (122, '登录系统', '2025-08-12 01:44:27', 'dyf', '127.0.0.1');
INSERT INTO `log` VALUES (123, '登录系统', '2025-08-12 23:54:47', 'qwy', '127.0.0.1');
INSERT INTO `log` VALUES (124, '登录系统', '2025-08-13 00:06:21', 'qwy', '127.0.0.1');
INSERT INTO `log` VALUES (125, '登录系统', '2025-08-13 00:12:30', 'qwy', '127.0.0.1');
INSERT INTO `log` VALUES (126, '登录系统', '2025-08-13 00:12:56', 'qwy', '127.0.0.1');
INSERT INTO `log` VALUES (127, '登录系统', '2025-08-13 00:13:08', 'qwy', '127.0.0.1');

-- ----------------------------
-- Table structure for menu
-- ----------------------------
DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu`  (
  `id` int(11) NOT NULL,
  `menuCode` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '菜单编码',
  `menuName` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '菜单名字',
  `menuLevel` varchar(2) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '菜单级别',
  `menuParentCode` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '菜单的父code',
  `menuClick` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '点击触发的函数',
  `menuRight` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '权限 1表示管理员，2表示教师，3表示学生，可以用逗号组合使用',
  `menuComponent` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `menuIcon` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '菜单表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of menu
-- ----------------------------
INSERT INTO `menu` VALUES (1, '001', '监控大屏', '1', NULL, 'Monitor', '1', 'MonitorManage/Monitor.vue', 'el-icon-s-platform');
INSERT INTO `menu` VALUES (2, '002', '学院专业管理', '1', NULL, 'CollegeMajor', '1', '', 'el-icon-school');
INSERT INTO `menu` VALUES (3, '003', '用户管理', '1', NULL, 'User', '1', '', 'el-icon-user');
INSERT INTO `menu` VALUES (4, '004', '教师管理', '2', '003', 'Counsellor', '1', 'UserManage/Counsellor.vue', '');
INSERT INTO `menu` VALUES (5, '005', '学生管理', '2', '003', 'Student', '1', 'UserManage/Student.vue', NULL);
INSERT INTO `menu` VALUES (6, '006', '学院管理', '2', '002', 'College', '1', 'SchoolManage/College.vue', NULL);
INSERT INTO `menu` VALUES (7, '007', '专业管理', '2', '002', 'Speciality', '1', 'SchoolManage/Speciality.vue', NULL);
INSERT INTO `menu` VALUES (8, '008', '请假管理', '1', NULL, 'Leave', '1,2,3', '', 'el-icon-s-management');
INSERT INTO `menu` VALUES (9, '009', '请假申请', '2', '008', 'Application', '3', 'LeaveManage/Application.vue', NULL);
INSERT INTO `menu` VALUES (10, '010', '我的请假', '2', '008', 'MyLeave', '3', 'LeaveManage/MyLeave.vue', NULL);
INSERT INTO `menu` VALUES (11, '011', '请假审批', '2', '008', 'Approval', '1,2', 'LeaveManage/Approval.vue', NULL);
INSERT INTO `menu` VALUES (12, '012', '个人信息', '1', NULL, 'Information', '1,2,3', 'InformationManage/Information.vue', 'el-icon-s-custom');
INSERT INTO `menu` VALUES (13, '013', '操作日志', '1', NULL, 'Log', '1', 'LogManage/Log.vue', 'el-icon-s-order');
INSERT INTO `menu` VALUES (14, '014', '公告管理', '1', NULL, 'Notice', '1', 'NoticeManage/Notice.vue', 'el-icon-s-promotion');

-- ----------------------------
-- Table structure for notice
-- ----------------------------
DROP TABLE IF EXISTS `notice`;
CREATE TABLE `notice`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '公告名称',
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '公告内容',
  `time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '公告时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notice
-- ----------------------------
INSERT INTO `notice` VALUES (1, '震惊!!,大数据2321班主任竟然做出这等事??!', '陈云涛请假班主任不理!', '2025-08-09 01:46:34');
INSERT INTO `notice` VALUES (2, '信工学院学长竟半夜翻墙?', '原来是信工的猫学长', '2025-08-09 01:46:20');
INSERT INTO `notice` VALUES (7, '处分公告!', '大数据2321陈云涛天天请假,赐死!', '2025-08-09 01:45:11');
INSERT INTO `notice` VALUES (8, '嘉奖公告', '大数据2321钱伟烨王者荣耀巅峰赛上1800了!!!', '2025-08-09 01:45:48');
INSERT INTO `notice` VALUES (9, '放假公告', '大数据2321班级全体放假两年', '2025-08-09 01:47:00');

-- ----------------------------
-- Table structure for speciality
-- ----------------------------
DROP TABLE IF EXISTS `speciality`;
CREATE TABLE `speciality`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `speciality_id` int(11) NOT NULL COMMENT '专业ID',
  `speciality_name` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '专业名称',
  `college_id` int(11) NOT NULL COMMENT '所属学院ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '专业表\r\n' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of speciality
-- ----------------------------
INSERT INTO `speciality` VALUES (1, 1001, '软件工程', 101);
INSERT INTO `speciality` VALUES (2, 2001, '机械工程', 102);
INSERT INTO `speciality` VALUES (3, 3001, '金融学', 103);
INSERT INTO `speciality` VALUES (4, 4001, '设计学', 104);
INSERT INTO `speciality` VALUES (5, 5001, '临床医学', 105);
INSERT INTO `speciality` VALUES (9, 1002, '网络安全', 101);

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `username` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '123456',
  `sex` tinyint(1) NULL DEFAULT NULL,
  `email` varchar(120) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `student_id` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `phone` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `last_login_time` datetime NULL DEFAULT NULL,
  `ip` varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `role_id` int(11) NOT NULL DEFAULT 3,
  `college_id` int(11) NOT NULL,
  `speciality_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '学生表\r\n' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES (2, '李五', 'lisi', '123456', 1, 'lisi@qq.com', '20231002', '13800138002', '2023-11-01 10:20:15', '192.168.1.102', 3, 101, 1001);
INSERT INTO `student` VALUES (3, '王芳', 'wangfang', '123456', 2, 'wangfang@univ.edu', '20231003', '13800138003', '2023-11-01 11:30:45', '192.168.1.103', 3, 102, 2001);
INSERT INTO `student` VALUES (4, '刘洋', 'liuyang', '123456', 1, 'liuyang@univ.edu', '20231004', '13800138004', '2023-11-01 13:45:20', '192.168.1.104', 3, 102, 2001);
INSERT INTO `student` VALUES (5, '陈晨', 'chenchen', '123456', 2, 'chenchen@univ.edu', '20231005', '13800138005', '2023-11-01 14:30:18', '192.168.1.105', 3, 103, 3001);
INSERT INTO `student` VALUES (6, '周六', 'zhouliu', '123456', 1, 'zhouliu@qq.com', '20231006', '13800138006', '2023-11-01 15:20:30', '192.168.1.106', 3, 103, 3001);
INSERT INTO `student` VALUES (7, '钱七', 'qianqi', '123456', 1, 'qianqi@univ.edu', '20231007', '13800138007', '2023-11-02 08:45:22', '192.168.1.107', 3, 104, 4001);
INSERT INTO `student` VALUES (8, '孙八', 'sunba', '123456', 1, 'sunba@univ.edu', '20231008', '13800138008', '2023-11-02 10:15:40', '192.168.1.108', 3, 104, 4001);
INSERT INTO `student` VALUES (9, '周九', 'zhoujiu', '123456', 1, 'zhoujiu@univ.edu', '20231009', '13800138009', '2023-11-02 11:30:10', '192.168.1.109', 3, 105, 5001);
INSERT INTO `student` VALUES (10, '吴十', 'wushi', '123456', 1, 'wushi@univ.edu', '20231010', '13800138010', '2023-11-02 14:20:35', '192.168.1.110', 3, 105, 5001);
INSERT INTO `student` VALUES (11, '郑洁', 'zhengjie', '123456', 2, 'zhengjie@univ.edu', '20231011', '13800138011', '2023-11-03 09:40:25', '192.168.1.111', 3, 101, 1001);
INSERT INTO `student` VALUES (12, '王丽', 'wangli', '123456', 2, 'wangli@univ.edu', '20231012', '13800138012', '2023-11-03 10:50:15', '192.168.1.112', 3, 102, 2001);
INSERT INTO `student` VALUES (13, '李婷', 'liting', '123456', 2, 'liting@univ.edu', '20231013', '13800138013', '2023-11-03 13:15:30', '192.168.1.113', 3, 103, 3001);
INSERT INTO `student` VALUES (14, '张华', 'zhanghua', '123456', 1, 'zhanghua@univ.edu', '20231014', '13800138014', '2023-11-03 15:30:45', '192.168.1.114', 3, 104, 4001);
INSERT INTO `student` VALUES (15, '刘伟', 'liuwei', '123456', 1, 'liuwei@univ.edu', '20231015', '13800138015', '2023-11-03 16:40:20', '192.168.1.115', 3, 105, 5001);
INSERT INTO `student` VALUES (25, '钱伟烨', 'qwy', '111', 1, '233@qq.com', '20231023', '12355668888', '2025-08-26 19:31:22', '127.0.0.1', 3, 101, 1001);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `email` varchar(120) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `role_id` int(11) NULL DEFAULT NULL,
  `last_login_time` datetime NULL DEFAULT NULL,
  `ip` varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `description` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'qwy', '123', '2902427356@qq.com', 1, NULL, '127.0.0.1', NULL);
INSERT INTO `user` VALUES (2, 'wnn', '234', '1314@wy.com', 1, NULL, '127.0.0.1', NULL);

SET FOREIGN_KEY_CHECKS = 1;
