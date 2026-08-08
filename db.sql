-- 创建数据库 用户 授权
CREATE DATABASE `salary` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'salary'@'%' IDENTIFIED BY '28aa838315633f0e44049ce88de36803';
GRANT ALL ON `salary`.* TO 'salary'@'%';
FLUSH PRIVILEGES;
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- 系统表-用户表
DROP TABLES IF EXISTS `xtb_user`;
CREATE TABLE `xtb_user` (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '主键，自增ID',
    `rtx_id` varchar(35) not null unique COMMENT 'RTX-ID唯一标识，英文+数字组成',
    `md5` varchar(64) not null unique COMMENT '数据唯一标识：MD5-ID',
    `name` varchar(30) not null COMMENT '名称',
    `password` varchar(120) not null COMMENT '密码[md5加密]',
    `salt` varchar(32) COMMENT '密码盐值，随机MD5-ID[32位]',
    `sex` varchar(2) COMMENT '性别',
    `email` varchar(80) COMMENT '邮箱',
    `phone` varchar(15) COMMENT '电话',
    `avatar` varchar(120) COMMENT '头像地址',
    `introduction` text COMMENT '描述',
    `role` varchar(255) COMMENT '角色RTX-ID值（大写），关联role表，多角色用;分割',
    `department` varchar(64) COMMENT '部门MD5-ID值，关联department表',
    `create_rtx` varchar(35) COMMENT '创建用户RTX-ID',
    `create_time` datetime default CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_rtx` varchar(35) COMMENT '更新用户RTX-ID',
    `update_time` datetime COMMENT '更新时间',
    `delete_rtx` varchar(35) COMMENT '删除用户RTX-ID',
    `delete_time` datetime COMMENT '删除时间',
    `status` bool default False COMMENT '数据状态：1注销；0启用（默认）',

    PRIMARY KEY (`id`)
) COMMENT='系统表-用户表';

-- create index
CREATE UNIQUE INDEX xtb_user_rtx_id_index ON xtb_user (`rtx_id`);

-- insert default admin
insert into
xtb_user(rtx_id, md5, name, `password`, email , phone, avatar, introduction, role, create_rtx, status)
VALUES
('admin', '21232f297a57a5a743894a0e4a801fc3', 'ADMIN系统管理员', 'e10adc3949ba59abbe56e057f20f883e', 'gaoming971366@163.com', '13051355646',
'http://pygo2.top/images/article_github.jpg', 'SUPER_ADMIN系统管理员', 'ADMIN', 'admin', FALSE);
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- 系统表-请求表
-- create && index
DROP TABLES IF EXISTS `xtb_request`;
CREATE TABLE `xtb_request`  (
    `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键，自增ID',
    `md5` varchar(64) NOT NULL unique COMMENT '数据唯一标识：MD5-ID',
    `rtx_id` varchar(35) COMMENT '请求访问用户RTX-ID',
    `ip` varchar(15) COMMENT '用户请求IP',
    `method` varchar(10) COMMENT '请求方法',
    `params` varchar(100) COMMENT '请求参数',
    `path` varchar(55) COMMENT '请求路径',
    `full_path` varchar(155) COMMENT '请求路径+参数',
    `host_url` varchar(100) COMMENT '请求HOST',
    `url` varchar(255) COMMENT '请求全路径',
    `cost` decimal(10, 4) COMMENT '运行时间',
    `create_time` datetime default CURRENT_TIMESTAMP COMMENT '创建时间',
    `create_date` date not null COMMENT '创建日期',
    `delete_rtx` varchar(35) COMMENT '删除用户RTX-ID',
    `delete_time` datetime COMMENT '删除时间',
    `status` bool default False COMMENT '数据状态：1删除；0正常（默认）',

    PRIMARY KEY (`id`),
    UNIQUE INDEX `index_id`(`id`) USING HASH COMMENT 'id索引'
) COMMENT='系统表-请求表';

-- delete
delete from xtb_request;
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- 系统表-角色权限表
-- create table && index
DROP TABLES IF EXISTS `xtb_role`;
CREATE TABLE `xtb_role`  (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '主键，自增ID',
    `engname` varchar(35) UNIQUE NOT NULL COMMENT '角色唯一标识，英文+数字组成',
    `chnname` varchar(35) NOT NULL COMMENT '角色中文名称',
    `md5` varchar(64) not null unique COMMENT '数据唯一标识：MD5-ID',
    `authority` varchar(255) COMMENT '角色权限ID集合，用英文,分割',
    `introduction` text COMMENT '描述',
    `create_rtx` varchar(35) COMMENT '创建用户RTX-ID',
    `create_time` datetime default CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_rtx` varchar(35) COMMENT '更新用户RTX-ID',
    `update_time` datetime COMMENT '更新时间',
    `delete_rtx` varchar(35) COMMENT '删除用户RTX-ID',
    `delete_time` datetime COMMENT '删除时间',
    `status` bool default False COMMENT '数据状态：1删除；0正常（默认）',

    PRIMARY KEY (`id`),
    UNIQUE INDEX `xtb_role_md5_index`(`md5`) USING HASH COMMENT 'md5唯一索引',
    UNIQUE INDEX `xtb_role_engname_index`(`engname`) USING HASH COMMENT 'engname唯一索引'
) COMMENT='系统表-角色权限表';

-- insert default role
insert into
xtb_role(engname, chnname, md5,  authority, introduction, create_rtx, status)
VALUES
('ADMIN', 'Super管理员', '21232f297a57a5a743894a0e4a801fc3', '', '系统所有功能权限', 'admin', FALSE);
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- 系统表-菜单
-- create table && index
DROP TABLES IF EXISTS `xtb_menu`;
CREATE TABLE `xtb_menu`  (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '主键，自增ID',
    `name` varchar(55) NOT NULL COMMENT '路由英文名称，大驼峰命名方式[注：需要与父节点连接映射]，例如SystemMenu',
    `path` varchar(255) NOT NULL COMMENT '路由path，全小写字母[注：需要与父节点连接映射]',
    `title` varchar(35) NOT NULL COMMENT '菜单标题',
    `pid` int NOT NULL COMMENT '父ID',
    `level` int default 1 NOT NULL COMMENT '菜单级别，默认1级菜单，根节点为0',
    `md5` varchar(64) NOT NULL unique COMMENT '数据唯一标识：MD5-ID',
    `type` varchar(35) default 'MENU' NOT NULL COMMENT '菜单类型：MENU=菜单，LINK=外链，BUTTON=按钮',
    `component` varchar(255) NOT NULL COMMENT '路由组件，与Vue router mappings映射[注：需要与父节点连接映射]',
    `hidden` bool default False COMMENT '是否在SideBar显示，默认为false',
    `redirect` varchar(255) COMMENT '菜单重定向，主要用于URL一级菜单跳转',
    `icon` varchar(35) COMMENT '菜单图标',
    `cache` bool default true COMMENT '页面是否进行cache，默认true缓存',
    `affix` bool default false COMMENT '是否在tags-view固定，默认false',
    `full` bool default false COMMENT '是否全屏，默认false',
    `breadcrumb` bool default true COMMENT '是否Breadcrumb中显示，默认true',
    `shortcut` bool default True COMMENT 'Dashboard快捷入口是否显示，默认true',
    `tag` varchar(10) COMMENT '菜单TAG，用于二级菜单',
    `order_id` int default 1 COMMENT '排序ID',
    `create_rtx` varchar(35) COMMENT '创建用户RTX-ID',
    `create_time` datetime default CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_rtx` varchar(35) COMMENT '更新用户RTX-ID',
    `update_time` datetime COMMENT '更新时间',
    `delete_rtx` varchar(35) COMMENT '删除用户RTX-ID',
    `delete_time` datetime COMMENT '删除时间',
    `status` bool default False COMMENT '数据状态：1删除；0正常（默认）',

    PRIMARY KEY (`id`),
    UNIQUE INDEX `xtb_menu_md5_index`(`md5`) USING HASH COMMENT 'md5唯一索引',
    UNIQUE INDEX `xtb_menu_name_index`(`name`) USING HASH COMMENT 'name唯一索引'
) COMMENT='系统表-菜单';

-- insert default menu
delete from xtb_menu;

insert into
    xtb_menu(id, `title`, `name`, `path`, `pid`, `level`, `md5`, `component`, `hidden`, `redirect`, `icon`, `cache`, `affix`, `full`, `type`, `breadcrumb`, `order_id`, `create_rtx`, `status`, `shortcut`, `tag`)
VALUES
-- root[根节点]
(1, '根节点', 'Root', '/', 0, 0, 'fa03eb688ad8aa1db593d33dabd89bad', '', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 0, 'admin', FALSE, FALSE, ''),


-- 首页[一级菜单]
(2, '首页', 'Home', '/', 1, 1, '8cf04a9734132302f96da8e113e80ce5', '/home', FALSE, '', 'Platform', TRUE, FALSE, FALSE, 'MENU', TRUE, 1, 'admin', FALSE, FALSE, ''),
--   > 控制台[二级菜单]
(3, '控制台', 'HomeDashboard', '/dashboard', 2, 2, '7e359079d011694cfb41d864ea66a5da', '/home/index', FALSE, '', 'Grid', TRUE, TRUE, FALSE, 'MENU', TRUE, 2, 'admin', FALSE, FALSE, ''),
(4, '数据面板', 'HomeDataPan', '/datapan', 2, 2, 'd97c7ab6c1fb8827f81a21c2b8dff8c4', '/home/dataPan', FALSE, '', 'Histogram', TRUE, TRUE, FALSE, 'MENU', TRUE, 3, 'admin', FALSE, FALSE, ''),


-- 工资模块[一级菜单]
(5, '工资', 'Salary', '/salary', 1, 1, 'b083a446a3588547410dbd6c571c2a09', '/salary', FALSE, '', 'Promotion', TRUE, FALSE, FALSE, 'MENU', TRUE, 1000, 'admin', FALSE, FALSE, ''),
--   > 通知管理[二级菜单]
(6, '消息通知', 'SalaryNotify', '/salary/notify', 5, 2, '365fc754afb9cf062b6563eae3894f55', '/salary/notify', FALSE, '', 'BellFilled', TRUE, FALSE, FALSE, 'MENU', TRUE, 1100, 'admin', FALSE, FALSE, ''),
--   >> [三级级菜单]
(7, '钉钉绩效', 'SalaryNotifyDtalk', '/salary/notify/dtalk', 6, 3, '735d60bec2c85e6b9b82b40e0bbbcc3f', '/salary/notify/dtalk/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 1101, 'admin', FALSE, TRUE, ''),
(8, '企微通知', 'SalaryNotifyQywx', '/salary/notify/qywx', 6, 3, '288da65f09e781e8406aa6e20ad73843', '/salary/notify/qywx/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 1102, 'admin', FALSE, TRUE, ''),
(9, '邮件通知', 'SalaryNotifyEmail', '/salary/notify/email', 6, 3, '55c26864748b7cd5e79c3cf71ff54c48', '/salary/notify/email/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 1103, 'admin', FALSE, TRUE, ''),
(10, '短信通知', 'SalaryNotifyMessage', '/salary/notify/message', 6, 3, '86a3276bf7aebc620b86e3595998d753', '/salary/notify/message/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 1104, 'admin', FALSE, TRUE, ''),


-- 工具模块[一级菜单]
(11, '工具', 'Tool', '/tool', 1, 1, 'd421fd439cd14456726791338b3b397e', '/tool', FALSE, '', 'Briefcase', TRUE, FALSE, FALSE, 'MENU', TRUE, 2000, 'admin', FALSE, FALSE, ''),
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
--   > 表格工具[二级菜单]
(12, '文档工具', 'ToolOffice', '/tool/office', 11, 2, '5e2046640dc73d9da730f00d30ad8da4', '/tool/office', FALSE, '', 'List', TRUE, FALSE, FALSE, 'MENU', TRUE, 2100, 'admin', FALSE, FALSE, ''),
--   >> [三级级菜单]
(13, 'PDF转WORD', 'ToolOfficePdfToWord', '/tool/office/pdf2word', 12, 3, 'a882a196eb0c6fef268ee1d8dc354a27', '/tool/office/pdf2Word/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2101, 'admin', FALSE, TRUE, ''),
(14, '表格合并', 'ToolOfficeExcelMerge', '/tool/office/merge', 12, 3, 'b8d978cf3d1e0914aa1cc175cea6c6c2', '/tool/office/excelMerge/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2102, 'admin', FALSE, TRUE, ''),
(15, '表格拆分', 'ToolOfficeExcelSplit', '/tool/office/split', 12, 3, '51ffc9b1886f777bfbd8d649f819cb13', '/tool/office/excelSplit/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2103, 'admin', FALSE, TRUE, ''),
(16, '表格历史', 'ToolOfficeExcelHistory', '/tool/office/history', 12, 3, '19b45123670ad06b20e905569f8c5a24', '/tool/office/excelHistory/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2104, 'admin', FALSE, TRUE, ''),
-- * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
--   > 知识平台[二级菜单]
(17, '知识平台', 'ToolSearch', '/tool/search', 11, 2, '52c4f504e2a4c20dba94c8b6a51bdfca', '/tool/search', FALSE, '', 'Shop', TRUE, FALSE, FALSE, 'MENU', TRUE, 2200, 'admin', FALSE, FALSE, ''),
--   >> [三级级菜单]
(18, 'SQL仓库', 'ToolSearchSqlbase', '/tool/search/sqlbase', 17, 3, '282668ccf52cee4ff58e3dcb093fe1cb', '/tool/search/sqlbase/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2201, 'admin', FALSE, TRUE, ''),
(19, '问题检索', 'ToolSearchProbase', '/tool/search/probase', 17, 3, '07059a7d498655c21282f08f807d0251', '/tool/search/probase/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2202, 'admin', FALSE, TRUE, ''),
(20, '知识分享', 'ToolSearchShare', '/tool/search/share', 17, 3, '1fb353280f4bf05af34c7b971d5c9a2b', '/tool/search/share/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2203, 'admin', FALSE, TRUE, ''),
-- & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & &
--   > 其他工具[二级菜单]
(21, '其他工具', 'ToolOther', '/tool/other', 11, 2, '86be6c29afcab6c8908e11b3ff238491', '/tool/other', FALSE, '', 'Opportunity', TRUE, FALSE, FALSE, 'MENU', TRUE, 2900, 'admin', FALSE, FALSE, ''),
--   >> [三级级菜单]
(22, '羊毛工具', 'ToolOtherSheep', '/tool/other/sheep', 21, 3, '60a3e4bbef35c9144e36542ceccea545', '/tool/other/sheep/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2901, 'admin', FALSE, TRUE, ''),
(23, '暴力短信', 'ToolOtherViolent', '/tool/other/violent', 21, 3, '1c514c36f3a1da02b4a5c51afcd37a5e', '/tool/other/violent/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2902, 'admin', FALSE, TRUE, ''),
(24, '拓扑关系', 'ToolOtherTopology', '/tool/other/topology', 21, 3, '3f9d2be2825ca7c300b2e04c318d465d', '/tool/other/topology/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2903, 'admin', FALSE, TRUE, ''),


-- 财务模块[一级菜单]
(25, '财务', 'Finance', '/finance', 1, 1, 'c482980d384a9d0e7bc39e1140270870', '/finance', FALSE, '', 'Coin', TRUE, FALSE, FALSE, 'MENU', TRUE, 3000, 'admin', FALSE, FALSE, ''),
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
--   > 驾驶舱[二级菜单]
(26, '驾驶舱', 'FinanceDesktop', '/finance/desktop', 25, 2, '1671a094d6ebc2fdf2bf3d5960344957', '/finance/desktop/index', FALSE, '', 'PieChart', TRUE, FALSE, FALSE, 'MENU', TRUE, 3100, 'admin', FALSE, FALSE, 'NEW'),
--   > 记账本[二级菜单]
(27, '记账本', 'FinanceCashBook', '/finance/cashbook', 25, 2, 'a1933b994fc52f72f6b2aa1c784a123a', '/finance/cashbook/index', FALSE, '', 'Notebook', TRUE, FALSE, FALSE, 'MENU', TRUE, 3200, 'admin', FALSE, FALSE, 'NEW'),
--   > 表格工具[二级菜单]
(28, '日常费用', 'FinanceDaily', '/finance/daily', 25, 2, '796e760873f7a3d8af311e7da970fa09', '/finance/daily', FALSE, '', 'Calendar', TRUE, FALSE, FALSE, 'MENU', TRUE, 3300, 'admin', FALSE, FALSE, 'NEW'),
--   >> [三级级菜单]
(29, '收入来源', 'FinanceDailyIncome', '/finance/daily/income', 28, 3, '8892e032777d8ec0f2d276b10ff57f81', '/finance/daily/income/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 3301, 'admin', FALSE, TRUE, ''),
(30, '支出记录', 'FinanceDailyPay', '/finance/daily/pay', 28, 3, 'f4400db1e7d6e32527118a27e9d58cb6', '/finance/daily/pay/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 3302, 'admin', FALSE, TRUE, ''),
(31, '日常统计', 'FinanceDailyState', '/finance/daily/state', 28, 3, '1301092e5e41973a7e16580d38d8eec3', '/finance/daily/state/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 3303, 'admin', FALSE, TRUE, ''),


-- 日报模块[一级菜单]
(32, '日报', 'Diary', '/diary', 1, 1, 'edcf7eb3a7d5eab2be6688cb3e59fcee', '/diary', FALSE, '', 'Flag', TRUE, FALSE, FALSE, 'MENU', TRUE, 4000, 'admin', FALSE, FALSE, ''),
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
--   > 驾驶舱[二级菜单]
(33, '工作日报', 'DiaryWork', '/diary/work', 32, 2, '75bf5f6f679a0c19de96d02f73d81265', '/diary/work/index', FALSE, '', 'Sunny', TRUE, FALSE, FALSE, 'MENU', TRUE, 4001, 'admin', FALSE, FALSE, 'NEW'),
--   > 记账本[二级菜单]
(34, '随笔', 'DiaryJotter', '/diary/jotter', 32, 2, '212deeba5e5b83cb9535a59a9b997dd4', '/diary/jotter/index', FALSE, '', 'MoonNight', TRUE, FALSE, FALSE, 'MENU', TRUE, 4002, 'admin', FALSE, FALSE, 'NEW'),


-- 系统模块[一级菜单]
(35, '系统', 'System', '/system', 1, 1, 'a45da96d0bf6575970f2d27af22be28a', '/system', FALSE, '', 'HelpFilled', TRUE, FALSE, FALSE, 'MENU', TRUE, 10000, 'admin', FALSE, FALSE, ''),
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
--   > 系统维护[二级菜单]
(36, '系统维护', 'SystemOps', '/system/ops', 35, 2, '4059b0251f66a18cb56f544728796875', '/system/ops', FALSE, '', 'Operation', TRUE, FALSE, FALSE, 'MENU', TRUE, 10100, 'admin', FALSE, FALSE, ''),
--   >> [三级级菜单]
(37, '部门架构', 'SystemOpsDepart', '/system/ops/depart', 36, 3, '1d17cb9923b99f823da9f5a16dc460e5', '/system/ops/depart/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 10101, 'admin', FALSE, TRUE, ''),
(38, '头像管理', 'SystemOpsAvatar', '/system/ops/avatar', 36, 3, 'eafdc02f3b847285bf1815f55f1f4e46', '/system/ops/avatar/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 10102, 'admin', FALSE, TRUE, ''),
(39, '系统日志', 'SystemOpsLog', '/system/ops/log', 36, 3, 'fa83d9352d3c8fab04893bbf60be7e06', '/system/ops/log/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 10103, 'admin', FALSE, TRUE, ''),
(40, '任务中心', 'SystemOpsTask', '/system/ops/task', 36, 3, '0d5939c51f761fe1d7fe3c9409577a6f', '/system/ops/task/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 10104, 'admin', FALSE, TRUE, ''),
-- * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
--   > 系统维护[二级菜单]
(41, '系统配置', 'SystemConfig', '/system/config', 35, 2, 'a59948b9e45358eaaaa1b13d9cedc248', '/system/config', FALSE, '', 'SetUp', TRUE, FALSE, FALSE, 'MENU', TRUE, 10200, 'admin', FALSE, FALSE, ''),
(42, '参数配置', 'SystemConfigXtcs', '/system/config/xtcs', 41, 3, '01a048451007391f41a139858d9a9ac9', '/system/config/xtcs/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 10201, 'admin', FALSE, TRUE, ''),
(43, '数据字典', 'SystemConfigDict', '/system/config/dict', 41, 3, 'ae4f23009c2738728e4ecd415cbd6167', '/system/config/dict/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 10202, 'admin', FALSE, TRUE, ''),
(44, '报表配置', 'SystemConfigReport', '/system/config/report', 41, 3, '8607a3d3d8db823f68a24f335bf147d9', '/system/config/report/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 10203, 'admin', FALSE, TRUE, ''),
(45, '后台API', 'SystemConfigApi', '/system/config/api', 41, 3, '4ae6c8f4429f7bacb050c9c980cf51d3', '/system/config/api/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 10204, 'admin', FALSE, TRUE, ''),
-- * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
--   > 系统维护[二级菜单]
(46, '权限管理', 'SystemMain', '/system/main', 35, 2, '34e34c43ec6b943c10a3cc1a1a16fb11', '/system/main', FALSE, '', 'Lock', TRUE, FALSE, FALSE, 'MENU', TRUE, 10300, 'admin', FALSE, FALSE, ''),
--   >> [三级级菜单]
(47, '用户管理', 'SystemMainUser', '/system/main/user', 46, 3, '8f9bfe9d1345237cb3b2b205864da075', '/system/main/user/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 10301, 'admin', FALSE, TRUE, ''),
(48, '角色管理', 'SystemMainRole', '/system/main/role', 46, 3, 'bbbabdbe1b262f75d99d62880b953be1', '/system/main/role/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 10302, 'admin', FALSE, TRUE, ''),
(49, '菜单管理', 'SystemMainMenu', '/system/main/menu', 46, 3, 'b61541208db7fa7dba42c85224405911', '/system/main/menu/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 10303, 'admin', FALSE, TRUE, ''),


-- 个人中心[一级菜单]
(50, '设置', 'Setter', '/setter', 1, 1, '130bdeec588552954b9e3bea0ef364b2', '/setter', FALSE, '', 'Setting', TRUE, FALSE, FALSE, 'MENU', TRUE, 11000, 'admin', FALSE, FALSE, ''),
--   > [二级菜单]
(51, '个人中心', 'SetterProfile', '/setter/profile', 50, 2, 'cce99c598cfdb9773ab041d54c3d973a', '/setter/profile/index', FALSE, '', 'User', TRUE, FALSE, FALSE, 'MENU', TRUE, 11001, 'admin', FALSE, TRUE, ''),
(52, '系统向导', 'SetterGuide', '/setter/guide', 50, 2, '6602bbeb2956c035fb4cb5e844a4861b', '/setter/guide/index', FALSE, '', 'Guide', TRUE, FALSE, FALSE, 'MENU', TRUE, 11002, 'admin', FALSE, TRUE, '');
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- 系统表-系统参数
-- create table && index
DROP TABLES IF EXISTS `xtb_xtcs`;
CREATE TABLE `xtb_xtcs`  (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '主键，自增ID',
    `key` varchar(35) NOT NULL COMMENT '参数KEY（大写）',
    `md5` varchar(64) NOT NULL UNIQUE COMMENT '数据唯一标识：MD5-ID',
    `remark` varchar(35) COMMENT '参数说明',
    `value` varchar(255) COMMENT '参数值',
    `create_rtx` varchar(35) COMMENT '创建用户RTX-ID',
    `create_time` datetime default CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_rtx` varchar(35) COMMENT '更新用户RTX-ID',
    `update_time` datetime COMMENT '更新时间',
    `delete_rtx` varchar(35) COMMENT '删除用户RTX-ID',
    `delete_time` datetime COMMENT '删除时间',
    `lock` bool default False COMMENT '锁定状态：1锁定；0非锁定',
    `status` bool default False COMMENT '数据状态：1删除；0正常（默认）',
    `order_id` int COMMENT '排序ID',

    PRIMARY KEY (`id`),
    UNIQUE INDEX `xtb_xtcs_md5_index`(`md5`) USING HASH COMMENT 'md5唯一索引'
) COMMENT='系统表-系统参数';

delete from xtb_xtcs;

insert into xtb_xtcs(`key`, `md5`, `remark`, `value`, `create_rtx`, `lock`, `status`, `order_id`) VALUES
('ADMIN-DATA-AUTHORITY', '6cfc35fda5cebaa3d39afa1a438a0e27', '管理员数据权限用户列表', 'a1,b2,c3', 'admin', False, False, 1),
('REDIS-CACHE-EXPIRE', '4b8edc2094cb917ecb179453e9e472d7', 'Redis数据缓存时间，单位为秒，默认为4小时', '14400', 'admin', False, False, 2),
('USER-DEFAULT-PASSWORD', '2560983a81db89c5f8ac7bc59ceec23e', '用户默认密码', 'abcd1234@', 'admin', False, False, 3),
('USER-DEFAULT-AVATAR', 'ef2cee999bde28a0f2b2485127d8a389', '用户默认头像', 'http://2lstore.pygo.space/avatars/default.png', 'admin', False, False, 4),
('USER-IMPORT-URL', '8c303643ae592c91ed5a7c45cd030fc1', '用户上传默认模板URL地址', 'http://2lstore.pygo.space/templates/%E7%B3%BB%E7%BB%9F%E7%94%A8%E6%88%B7%E6%89%B9%E9%87%8F%E5%AF%BC%E5%85%A5%E6%A8%A1%E6%9D%BFV1.0.xlsx', 'admin', False, False, 5),
('UPLOAD-FILE-MAX', '19a7fd901645cd10a0de9b495d1f6088', '文件上传最大文件数量', '15', 'admin', False, False, 6),
('SYSTEM-TITLE', '1700a58b93fe99d9edf8eec318737f1e', '系统登录页信息展示：系统标题', '智行工具平台', 'admin', False, False, 7),
('SYSTEM-VERSION', '7bf8a92528d9e53f020bb24d80bfb967', '系统登录页信息展示：系统版本', '1.1.2', 'admin', False, False, 8),
('SYSTEM-FEATURE', 'c827459d2ee5da92adfd826355588039', '系统登录页信息展示：系统特色', '定制化 / 高性能 / 精优雅', 'admin', False, False, 9),
('SYSTEM-SUMMARY', 'b48ef16d13363753454a38b1ccf255a4', '系统登录页信息展示：系统简述', '践行践远，智慧前行，总有一款工具让工作变得更加轻松，助你提质增效。', 'admin', False, False, 10),
('HOME-TIP-MORNING', '16d037c51df631d8c4260f04bdbee199', '系统登录温馨提示：凌晨6点～中午12点', '希望您有一个元气满满的早晨，充满动力地开始新的一天，加油哦！', 'admin', False, False, 11),
('HOME-TIP-NOON', 'a6856a3069a3fcb0201dd43a8cc382f0', '系统登录温馨提示：中午12点～下午14点', '忙碌了一上午，确实应该适当休息一下，记得按时吃午饭，补充能量才能更好地完成下午的工作！', 'admin', False, False, 12),
('HOME-TIP-AFTERNOON', 'a262837654996d535aa3f3790a6eba4f', '系统登录温馨提示：下午14点～下午18点', '下午是继续推进各项任务的好时间，保持专注和效率，希望您能够保持良好的状态，顺利完成每一天的目标！', 'admin', False, False, 13),
('HOME-TIP-NIGHT', '2cb3bb4adb5d010267204a7effd2c8da', '系统登录温馨提示：下午18点～凌晨6点', '一天的努力即将结束，回顾今天的成就，为明天做好准备。别忘了放松一下自己，享受美好的夜晚时光，睡觉要有好梦。', 'admin', False, False, 14);
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- CSB_ENUM_EKY 枚举Key表
-- create table && index
DROP TABLES IF EXISTS `csb_enum_key`;
CREATE TABLE `csb_enum_key`  (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '主键，自增ID',
    `key` varchar(35) NOT NULL COMMENT '枚举KEY值RTX-ID',
    `md5` varchar(64) NOT NULL UNIQUE COMMENT '数据唯一标识：MD5-ID',
    `value` varchar(35) COMMENT '枚举说明',
    `create_rtx` varchar(35) COMMENT '创建用户RTX-ID',
    `create_time` datetime default CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_rtx` varchar(35) COMMENT '更新用户RTX-ID',
    `update_time` datetime COMMENT '更新时间',
    `delete_rtx` varchar(35) COMMENT '删除用户RTX-ID',
    `delete_time` datetime COMMENT '删除时间',
    `lock` bool default False COMMENT '锁定状态：1锁定；0非锁定',
    `status` bool default False COMMENT '数据状态：1删除；0正常（默认）',
    `order_id` int COMMENT '排序ID',

    PRIMARY KEY (`id`),
    UNIQUE INDEX `index_id`(`id`) USING HASH COMMENT 'id索引'
) COMMENT='参数表-枚举Key表';

delete from csb_enum_key;

insert into csb_enum_key(`key`, `md5`, `value`, `lock`, `status`, `create_rtx`, `order_id`) VALUES
('bool-type', '5886ecb16dfd303f97ef685f943f4735', '布尔', False, False, 'admin', 1),
('sex-type', 'ce765ac3af6fc7823db049d70b3aa33d', '性别', False, False, 'admin', 2),
('download-select', 'ccf0ffc2e43a2bc62cb89b69834ad0ce', '表格下载方式', False, False, 'admin', 3),
('download-format', '894b127df244af241341d04ae290fdcf', '表格下载格式', False, False, 'admin', 4),
('menu-type', 'e32c70446571ce05a25702889c56cbac', '菜单类型', False, False, 'admin', 5),
('menu-level', 'cde5d071f0b5bbb56033121304b6604a', '菜单级别', False, False, 'admin', 6),
('api-type', 'ddf8dac28ba9f6a1d86d2b79b6e9cbe9', '请求类型', False, False, 'admin', 7),
('task-status', 'a4115b287aab1804586eb9390841ab6b', '任务状态', False, False, 'admin', 8);

-- CSB_ENUM_VALUE枚举 Value表
-- create table && index
DROP TABLES IF EXISTS `csb_enum_value`;
CREATE TABLE `csb_enum_value`  (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '主键，自增ID',
    `name` varchar(35) NOT NULL COMMENT '枚举子集对应的key（csb_enum_key）',
    `md5` varchar(64) NOT NULL UNIQUE COMMENT '数据唯一标识：MD5-ID',
    `key` varchar(35) NOT NULL COMMENT '枚举VALUE值RTX-ID',
    `value` varchar(35) COMMENT '枚举子集对应的value',
    `remark` text COMMENT '枚举子集对应的value说明',
    `create_rtx` varchar(35) COMMENT '创建用户RTX-ID',
    `create_time` datetime default CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_rtx` varchar(35) COMMENT '更新用户RTX-ID',
    `update_time` datetime COMMENT '更新时间',
    `delete_rtx` varchar(35) COMMENT '删除用户RTX-ID',
    `delete_time` datetime COMMENT '删除时间',
    `lock` bool default False COMMENT '锁定状态：1锁定；0非锁定',
    `status` bool default False COMMENT '数据状态：1删除；0正常（默认）',
    `order_id` int COMMENT '排序ID',

    PRIMARY KEY (`id`),
    UNIQUE INDEX `index_id`(`id`) USING HASH COMMENT 'id索引'
) COMMENT='参数表-枚举Value表';

delete from csb_enum_value;

insert into csb_enum_value(`name`, `md5`, `key`, `value`, `remark`, `lock`, `status`, `create_rtx`, `order_id`) VALUES
('bool-type', '9a5f13cb385c7fa20c2242a657896aca', 'Y', '是', '布尔枚举值：YES', False, False, 'admin', 1),
('bool-type', '771e7a50ad44f434ef93958fb9a1a8aa', 'N', '否', '布尔枚举值：NO', False, False, 'admin', 2),
('sex-type', '228708a5966408d2dbd19f1976270223', 'NO', '保密', '性别枚举值：NO', False, False, 'admin', 1),
('sex-type', '63889cfb9d3cbe05d1bd2be5cc9953fd', 'M', '男', '性别枚举值：Male', False, False, 'admin', 2),
('sex-type', '1f856b81d54a3c3f966336f54f59576a', 'F', '女', '性别枚举值：Female', False, False, 'admin', 3),
('download-select', 'bc1c7c26bfeac3a75a5a07a9926b8d08', 'ALL', '全部数据', '表格下载方式 > 全部数据', False, False, 'admin', 1),
('download-select', 'ced53e5b8a5f4835eaf895b966d02fd9', 'SELECT', '选择数据', '表格下载方式 > 已选择数据', False, False, 'admin', 2),
('download-format', '48a12305af5c8e87edefaeaf8b139bda', '.xls', '.xls', '表格下载文件保存格式 > .xls', False, False, 'admin', 1),
('download-format', '7078549a73f443430b655112015b3f91', '.xlsx', '.xlsx', '表格下载文件保存格式 > .xlsx', False, False, 'admin', 2),
('menu-type', 'de11acf0945e056b6111df2344b61e56', 'MENU', '菜单', '菜单类型 > 菜单', False, False, 'admin', 1),
('menu-type', '3d26943e03fc06d7942bb94e2768cdd1', 'LINK', '链接', '菜单类型 > 链接', False, False, 'admin', 2),
('menu-type', '989708ebdc1349a0ecb161bce861e6ba', 'BUTTON', '按钮', '菜单类型 > 按钮', True, False, 'admin', 3),
('menu-level', 'd000c56ed7f06f4ab0e49749ff9e7219', '0', '根目录', '菜单级别 > 根目录', False, False, 'admin', 1),
('menu-level', 'fae5bfbcfdebe7d1a522fd2d10c91284', '1', '一级菜单', '菜单级别 > 一级菜单', False, False, 'admin', 2),
('menu-level', '7da62425a607c5fc8d0e5f4d07875a1f', '2', '二级菜单', '菜单级别 > 二级菜单', False, False, 'admin', 3),
('menu-level', '2d86b6dc56da98dc0eb1f35ebf3bbda1', '3', '三级菜单', '菜单级别 > 三级菜单', False, False, 'admin', 4),
('menu-level', 'dd521a6f75a7145e327abf945c588acf', '4', '四级菜单', '菜单级别 > 四级菜单', True, False, 'admin', 5),
('menu-level', 'be1be8e2be606888227b2a18393b6cd9', '5', '五级菜单', '菜单级别 > 五级菜单', True, False, 'admin', 6),
('menu-level', '3910b181c2b6541537424984a885180a', '6', '六级菜单', '菜单级别 > 六级菜单', True, False, 'admin', 7),
('menu-level', '6a585ff1b9247fc7ac701d51bc735dc8', '7', '七级菜单', '菜单级别 > 七级菜单', True, False, 'admin', 8),
('menu-level', 'f54c2a67f5981f11ea34d7326b5eae87', '8', '八级菜单', '菜单级别 > 八级菜单', True, False, 'admin', 9),
('menu-level', '72a2e1da9e70462d8f31cc139147a9d9', '9', '九级菜单', '菜单级别 > 九级菜单', True, False, 'admin', 10),
('menu-level', '896e19f6470e5bfc60ba1d2a6ac8e4f1', '10', '十级菜单', '菜单级别 > 十级菜单', True, False, 'admin', 11),
('api-type', '6e0902c24a7c2ba5eff38c893288454f', 'success', 'POST', 'API接口操作类型 > 新增', False, False, 'admin', 1),
('api-type', '055360b96a9712758ba22cea8cb4cda0', 'danger', 'DELETE', 'API接口操作类型 > 删除', False, False, 'admin', 2),
('api-type', '42c142615a0f68e436d8f6021d566ec2', 'info', 'PUT', 'API接口操作类型 > 修改', False, False, 'admin', 3),
('api-type', 'cba31eaae518a4695c40d22f87812072', 'primary', 'GET', 'API接口操作类型 > 查询', False, False, 'admin', 4),
('api-type', 'de77797d9f646e2055e7d6e08b6421d3', 'error', 'OTHER', 'API接口操作类型 > 其他', False, False, 'admin', 5),
('task-status', 'f6c92121b95675feb64d8bf785859f2f', 'SUCCESS', '成功', '任务状态 > 成功', False, False, 'admin', 1),
('task-status', '9b3bd908456381af4ef69f98f9810846', 'FAILURE', '失败', '任务状态 > 失败', False, False, 'admin', 2),
('task-status', '85a78a1c4bfc5ad70a542c0e32c43026', 'WORKING', '执行中', '任务状态 > 执行中', False, True, 'admin', 3);






('excel-type', 'ecf0b1978b354bfcf243ef316c252101', '1', '合并', '表格处理方式 > 合并', 1, 'admin', 1),
('excel-type', '67128fcae7732df36a12e6e760aa39c7', '2', '拆分', '表格处理方式 > 拆分', 1, 'admin', 2),
('excel-split-store', '37ca191a1f70223c75c002fe80066a79', '1', '多表一Sheet', '表格拆分 > 存储方式 > 多表一Sheet', 1, 'admin', 1),
('excel-split-store', '1cf44e3c01b8c185e829a912375c3d88', '2', '一表多Sheet', '表格拆分 > 存储方式 > 一表多Sheet', 1, 'admin', 2),
('excel-num', 'ed6bfec14176d9717f16049ceaef1997', '1', '行', '表格拆分 > 拆分方式 > 行', 1, 'admin', 1),
('excel-num', '41a761bd675bda3f95fabb16987675e9', '2', '列', '表格拆分 > 拆分方式 > 列', 1, 'admin', 2),

('file-type', '9086ab2a079b27a89e959a7588063e13', '1', 'WORD', '文件类型 > WORD文档', 1, 'admin', 1),
('file-type', 'f65e091a48c00c5439e6bf536b35c03a', '2', 'EXCEL', '文件类型 > EXCEL表格', 1, 'admin', 2),
('file-type', 'd9e8eab4ac9e4dba2d7798b64a335e36', '3', 'PPT', '文件类型 > PPT演示文稿', 1, 'admin', 3),
('file-type', 'b3e251df695d0d1381f356c9a2de6f81', '4', '文本', '文件类型 > 文本文件', 1, 'admin', 4),
('file-type', 'e88041819de93ea5fe50d02816b6d443', '5', 'PDF', '文件类型 > PDF文件', 1, 'admin', 5),
('file-type', '8ba23dbd99ce1fd1721848806f396a2d', '99', '其他', '文件类型 > 其他类型文件', 1, 'admin', 6),
('qywx-type', '882c0c19dbc420c129e696532e75f027', 'text', '文本消息', '企业微信消息类型 > 文本消息', 1, 'admin', 1),
('qywx-type', '3fc72ebfbc1cccb57c0be9755cd05a6a', 'image', '图片消息', '企业微信消息类型 > 图片消息', 1, 'admin', 2),
('qywx-type', 'f93a4f42766340e21d84d117f0e8ee2b', 'voice', '语音消息', '企业微信消息类型 > 语音消息', 1, 'admin', 3),
('qywx-type', '88f8a7b7e659c25e1168830587273a95', 'video', '视频消息', '企业微信消息类型 > 视频消息', 1, 'admin', 4),
('qywx-type', '6bb6b85b36e06aeb31ecfe7ab1f4d894', 'file', '文件消息', '企业微信消息类型 > 文件消息', 1, 'admin', 5),
('qywx-type', 'b4fd5e4d7e033fe6c022d9d9237efd17', 'textcard', '文本卡片消息', '企业微信消息类型 > 文本卡片消息', 0, 'admin', 6),
('qywx-type', '259225b177117c2f44b39de0ae3d3457', 'news', '图文消息', '企业微信消息类型 > 图文消息', 0, 'admin', 7),
('qywx-type', 'febc81425c4542429956d7cf3477bb46', 'markdown', 'markdown消息', '企业微信消息类型 > markdown消息', 1, 'admin', 9),
('qywx-type', '88e59bdf04e4843ca649e33f7872bcbb', 'miniprogram_notice', '小程序通知消息', '企业微信消息类型 > 小程序通知消息', 0, 'admin', 10),
('qywx-type', 'd046e3333d903c8962e927571660452f', 'template_card@text_notice', '模板卡片消息 > 文本通知型', '企业微信消息类型 > 模板卡片消息 > 文本通知型', 0, 'admin', 11),

('qywx-type', '4da311801e0c3b85161223855540be41', 'mpnews', '多图文消息', '企业微信消息类型 > 多图文消息', 0, 'admin', 8),
('qywx-type', '684fb803a898eeb2497c6b5e6921e0b6', 'template_card@news_notice', '模板卡片消息 > 图文展示型', '企业微信消息类型 > 模板卡片消息 > 图文展示型', 0, 'admin', 12),
('qywx-type', '1848b73595df91d0c29cdf5127897040', 'template_card@button_interaction', '模板卡片消息 > 按钮交互型', '企业微信消息类型 > 模板卡片消息 > 按钮交互型', 0, 'admin', 13),
('qywx-type', '16bef9b5ef7a95422d8b355714e92367', 'template_card@vote_interaction', '模板卡片消息 > 投票选择型', '企业微信消息类型 > 模板卡片消息 > 投票选择型', 0, 'admin', 14),
('qywx-type', 'a805e896e02b83115987743cff27d507', 'template_card@multiple_interaction', '模板卡片消息 > 多项选择型', '企业微信消息类型 > 模板卡片消息 > 多项选择型', 0, 'admin', 15),
('db-type', '01a9bf972fa7c09be40d08d668419da1', 'DB2', 'DB2', '数据库类型 > 关系型数据库 > DB2', 1, 'admin', 1),
('db-type', 'c555fd735b52b0f37cba6616f5f584d2', 'Oracle', 'Oracle', '数据库类型 > 关系型数据库 > Oracle', 1, 'admin', 2),
('db-type', '2f7bde83268fab2083719214e29f620c', 'MySQL', 'MySQL', '数据库类型 > 关系型数据库 > MySQL', 1, 'admin', 3),
('db-type', '086fa1c6e5790ed66183907e975f8ac1', 'SqlServer', 'SqlServer', '数据库类型 > 关系型数据库 > SqlServer', 1, 'admin', 4),
('db-type', 'c995768c30121e6171909886effc2bd2', 'SQLite', 'SQLite', '数据库类型 > 关系型数据库 > SQLite', 1, 'admin', 5),
('db-type', 'ae6725e88e8fab0f5d26dc87f785f0a8', 'PostgreSQL', 'PostgreSQL', '数据库类型 > 关系型数据库 > PostgreSQL', 1, 'admin', 6),
('db-type', '4e0d61664feab705c27a1a07eb304ac5', 'Redis', 'Redis', '数据库类型 > 非关系型数据库 > Redis', 1, 'admin', 7),
('db-type', '358841380e96a757c6293278a1e76528', 'Memcache', 'Memcache', '数据库类型 > 非关系型数据库 > Memcache', 1, 'admin', 8),
('db-type', 'ae5816aea7485d94c4bf782e8f9fa2c7', 'MongoDb', 'MongoDb', '数据库类型 > 非关系型数据库 > MongoDb', 1, 'admin', 9),
('db-type', 'c9c0821ca988ca2fd7c8c10d9198058f', 'HBase', 'HBase', '数据库类型 > 非关系型数据库 > HBase', 1, 'admin', 10),
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- xtb_user_task 系统表-用户任务表
-- create table && index
DROP TABLES IF EXISTS `xtb_user_task`;
CREATE TABLE `xtb_user_task`  (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '主键，自增ID',
    `rtx_id` varchar(35) COMMENT '创建用户',
    `api` varchar(55) NOT NULL COMMENT 'API接口名称',
    `name` varchar(55) NOT NULL COMMENT '文件名称',
    `data` varchar(35) NOT NULL COMMENT '数据下载类型',
    `md5` varchar(64) NOT NULL COMMENT '唯一标识：MD5-ID',
    `task` varchar(35) NOT NULL COMMENT '任务状态：success failure working',
    `cost` decimal(10, 4) COMMENT '任务数据运行时间',
    `create_time` datetime default CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` datetime COMMENT '更新时间',
    `delete_rtx` varchar(35) COMMENT '删除用户RTX-ID',
    `delete_time` datetime COMMENT '删除时间',
    `status` bool default False COMMENT '数据状态：1删除；0正常（默认）',

    PRIMARY KEY (`id`),
    UNIQUE INDEX `xtb_user_task_md5_index`(`md5`) USING HASH COMMENT 'md5唯一索引'
) COMMENT='系统表-用户任务表';
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- 系统表-用户部门表
-- create xtb_department
DROP TABLES IF EXISTS `xtb_department`;
CREATE TABLE `xtb_department`  (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '主键，自增ID',
    `name` varchar(30) NOT NULL COMMENT '部门名称',
    `md5` varchar(64) NOT NULL COMMENT '唯一标识：MD5-ID',
    `description` text COMMENT '部门描述',
    `pid` int NOT NULL DEFAULT 1 COMMENT '上级部门ID',
    `leaf` boolean DEFAULT False COMMENT '是否为叶子节点，如果为True不允许有子节点，默认为False',
    `lock` boolean DEFAULT False COMMENT '是否锁定，如果为True为锁定，默认为False',
    `level` int NOT NULL DEFAULT 1 COMMENT '部门层级，默认为1级',
    `dept_path` varchar(254) NULL COMMENT '部门名称全路径，用>进行分割',
    `manage_rtx` varchar(254) COMMENT '部门主管rtx-id，多用户，用英文,分割',
    `create_rtx` varchar(35) COMMENT '创建用户',
    `create_time` datetime default CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_rtx` varchar(35) COMMENT '最新更新用户',
    `update_time` datetime COMMENT '最新更新时间',
    `delete_rtx` varchar(35) COMMENT '删除用户',
    `delete_time` datetime COMMENT '删除时间',
    `status` bool default False COMMENT '数据状态：1删除；0正常（默认）',
    `order_id` int COMMENT '排序ID',

  PRIMARY KEY (`id`)
) COMMENT='系统表-用户部门表';

-- default value
-- 根节点
insert into
xtb_department(`id`, `name`, `md5`, `description`, `pid`, `leaf`, `lock`, `level`, `dept_path`, `manage_rtx`, `create_rtx`, `status`, `order_id`)
VALUES
(1, '根节点', '63a9f0ea7bb98050796b649e85481845', '部门根节点', 0, True , False, 1, '根节点', 'admin', 'admin', False, 1),
(2, '基础研发部', 'f99199aa3e689f8d339b909734aabdcb', '基础研发部', 1, True , False, 2, '根节点>基础研发部', 'admin', 'admin', False, 2),
(3, '推广销售部', 'b9639531758dcdb8d0e7494d6ed9b5ac', '推广销售部', 1, True , False, 2, '根节点>推广销售部', 'admin', 'admin', False, 3),
(4, '人力资源部', '38d7f0998b7acaf8db182219c7fb202c', '人力资源部', 1, True , True, 2, '根节点>人力资源部', 'admin', 'admin', False, 4);
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- PDF文件记录表
-- create table
DROP TABLES IF EXISTS `tool_office_pdf`;

CREATE TABLE `tool_office_pdf` (
    `id` int NOT NULL AUTO_INCREMENT COMMENT '主键，自增ID',
    `rtx_id` varchar(35) COMMENT '创建用户',
    `name` varchar(100) NOT NULL COMMENT '文件名称',
    `store_name` varchar(100) COMMENT '文件存储名称',
    `transfer_name` varchar(100) COMMENT '文件转换store存储名称',
    `md5` varchar(64) NOT NULL COMMENT '唯一标识：MD5-ID',
    `transfer` bool DEFAULT False COMMENT '转换状态',
    `transfer_time` datetime COMMENT '转换时间',
    `local_url` varchar(130) COMMENT '文件本地资源路径（绝对路径）',
    `store_url` varchar(130) COMMENT '原始文件store对象存储资源路径（绝对路径）',
    `transfer_url` varchar(130) COMMENT '转换文件store对象存储资源路径（绝对路径）',
    `mode` bool DEFAULT True COMMENT '转换模式：True页码，False指定页码',
    `start` int COMMENT '转换开始页',
    `end` int COMMENT '转换结束页',
    `pages` varchar(120) COMMENT '指定的转换页码，用英文,分割',
    `create_time` datetime default CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_rtx` varchar(35) COMMENT '最新更新用户',
    `update_time` datetime COMMENT '最新更新时间',
    `delete_rtx` varchar(35) COMMENT '删除用户',
    `delete_time` datetime COMMENT '删除时间',
    `status` bool default False COMMENT '数据状态：1注销；0启用（默认）',

    PRIMARY KEY (`id`)
) COMMENT='PDF文件记录表';

CREATE UNIQUE INDEX tool_office_pdf_index ON tool_office_pdf (`md5`);
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


