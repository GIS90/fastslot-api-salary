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
    `department` varchar(55) COMMENT '部门MD5-ID值，关联department表',
    `create_rtx` varchar(35) COMMENT '创建用户RTX-ID',
    `create_time` datetime default CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_rtx` varchar(35) COMMENT '更新用户RTX-ID',
    `update_time` datetime COMMENT '更新时间',
    `delete_rtx` varchar(35) COMMENT '删除用户RTX-ID',
    `delete_time` datetime COMMENT '删除时间',
    `status` bool default False COMMENT '状态：1注销/删除；0启用/正常（默认）',

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
    `status` bool default False COMMENT '状态：1注销/删除；0启用/正常（默认）',

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
    `authority` varchar(255) NULL COMMENT '角色权限ID集合，用英文；分割',
    `introduction` text NULL COMMENT '描述',
    `create_rtx` varchar(35) COMMENT '创建用户RTX-ID',
    `create_time` datetime default CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_rtx` varchar(35) COMMENT '更新用户RTX-ID',
    `update_time` datetime COMMENT '更新时间',
    `delete_rtx` varchar(35) COMMENT '删除用户RTX-ID',
    `delete_time` datetime COMMENT '删除时间',
    `status` bool default False COMMENT '状态：1注销/删除；0启用/正常（默认）',

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
    `link` varchar(100) COMMENT '菜单类型=LINK的时候，外链接地址',
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
    `status` bool default False COMMENT '状态：1注销/删除；0启用/正常（默认）',

    PRIMARY KEY (`id`),
    UNIQUE INDEX `xtb_menu_md5_index`(`md5`) USING HASH COMMENT '菜单md5唯一索引',
    UNIQUE INDEX `xtb_menu_name_index`(`name`) USING HASH COMMENT '菜单name唯一索引'
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
(5, '工资', 'Salary', '/salary', 1, 1, 'b083a446a3588547410dbd6c571c2a09', '/salary', FALSE, '', 'Briefcase', TRUE, FALSE, FALSE, 'MENU', TRUE, 100, 'admin', FALSE, FALSE, ''),
--   > 通知管理[二级菜单]
(15, '消息通知', 'ToolNotify', '/salary/notify', 5, 2, '365fc754afb9cf062b6563eae3894f55', '/salary/notify', FALSE, '', 'BellFilled', TRUE, FALSE, FALSE, 'MENU', TRUE, 110, 'admin', FALSE, FALSE, ''),
--   >> [三级级菜单]
(16, '钉钉绩效', 'ToolNotifyDtalk', '/salary/notify/dtalk', 15, 3, '735d60bec2c85e6b9b82b40e0bbbcc3f', '/salary/notify/dtalk/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 111, 'admin', FALSE, TRUE, ''),
(17, '企微通知', 'ToolNotifyQywx', '/salary/notify/qywx', 15, 3, '288da65f09e781e8406aa6e20ad73843', '/salary/notify/qywx/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 112, 'admin', FALSE, TRUE, ''),
(18, '邮件通知', 'ToolNotifyMessage', '/salary/notify/message', 15, 3, '55c26864748b7cd5e79c3cf71ff54c48', '/salary/notify/message/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 113, 'admin', FALSE, TRUE, ''),
(18, '短信通知', 'ToolNotifyMessage', '/salary/notify/message', 15, 3, '55c26864748b7cd5e79c3cf71ff54c48', '/salary/notify/message/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 113, 'admin', FALSE, TRUE, ''),

-- 工具模块[一级菜单]
(5, '工具', 'Tool', '/tool', 1, 1, 'd421fd439cd14456726791338b3b397e', '/tool', FALSE, '', 'Briefcase', TRUE, FALSE, FALSE, 'MENU', TRUE, 100, 'admin', FALSE, FALSE, ''),
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
--   > 表格工具[二级菜单]
(6, '文档工具', 'ToolOffice', '/tool/office', 5, 2, '5e2046640dc73d9da730f00d30ad8da4', '/tool/office', FALSE, '', 'List', TRUE, FALSE, FALSE, 'MENU', TRUE, 101, 'admin', FALSE, FALSE, ''),
--   >> [三级级菜单]
(7, 'PDF转WORD', 'ToolOfficePdfToWord', '/tool/office/pdf2word', 6, 3, 'a882a196eb0c6fef268ee1d8dc354a27', '/tool/office/pdf2Word/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 102, 'admin', FALSE, TRUE, ''),
(8, '表格合并', 'ToolOfficeExcelMerge', '/tool/office/merge', 6, 3, 'b8d978cf3d1e0914aa1cc175cea6c6c2', '/tool/office/excelMerge/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 103, 'admin', FALSE, TRUE, ''),
(9, '表格拆分', 'ToolOfficeExcelSplit', '/tool/office/split', 6, 3, '51ffc9b1886f777bfbd8d649f819cb13', '/tool/office/excelSplit/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 104, 'admin', FALSE, TRUE, ''),
(10, '表格历史', 'ToolOfficeExcelHistory', '/tool/office/history', 6, 3, '19b45123670ad06b20e905569f8c5a24', '/tool/office/excelHistory/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 105, 'admin', FALSE, TRUE, ''),
-- * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
--   > 知识平台[二级菜单]
(11, '知识平台', 'ToolSearch', '/tool/search', 5, 2, '52c4f504e2a4c20dba94c8b6a51bdfca', '/tool/search', FALSE, '', 'Shop', TRUE, FALSE, FALSE, 'MENU', TRUE, 106, 'admin', FALSE, FALSE, ''),
--   >> [三级级菜单]
(12, 'SQL仓库', 'ToolSearchSqlbase', '/tool/search/sqlbase', 11, 3, '282668ccf52cee4ff58e3dcb093fe1cb', '/tool/search/sqlbase/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 107, 'admin', FALSE, TRUE, ''),
(13, '问题检索', 'ToolSearchProbase', '/tool/search/probase', 11, 3, '07059a7d498655c21282f08f807d0251', '/tool/search/probase/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 108, 'admin', FALSE, TRUE, ''),
(14, '知识分享', 'ToolSearchShare', '/tool/search/share', 11, 3, '1fb353280f4bf05af34c7b971d5c9a2b', '/tool/search/share/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 109, 'admin', FALSE, TRUE, ''),
-- ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^

-- & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & &
--   > 其他工具[二级菜单]
(19, '其他工具', 'ToolOther', '/tool/other', 5, 2, '86be6c29afcab6c8908e11b3ff238491', '/tool/other', FALSE, '', 'Opportunity', TRUE, FALSE, FALSE, 'MENU', TRUE, 900, 'admin', FALSE, FALSE, ''),
--   >> [三级级菜单]
(20, '羊毛工具', 'ToolOtherSheep', '/tool/other/sheep', 19, 3, '60a3e4bbef35c9144e36542ceccea545', '/tool/other/sheep/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 901, 'admin', FALSE, TRUE, ''),
(21, '暴力短信', 'ToolOtherViolent', '/tool/other/violent', 19, 3, '1c514c36f3a1da02b4a5c51afcd37a5e', '/tool/other/violent/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 902, 'admin', FALSE, TRUE, ''),
(22, '拓扑关系', 'ToolOtherTopology', '/tool/other/topology', 19, 3, '3f9d2be2825ca7c300b2e04c318d465d', '/tool/other/topology/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 903, 'admin', FALSE, TRUE, ''),


-- 财务模块[一级菜单]
(23, '财务', 'Finance', '/finance', 1, 1, 'c482980d384a9d0e7bc39e1140270870', '/finance', FALSE, '', 'Coin', TRUE, FALSE, FALSE, 'MENU', TRUE, 1000, 'admin', FALSE, FALSE, ''),
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
--   > 驾驶舱[二级菜单]
(24, '驾驶舱', 'FinanceDesktop', '/finance/desktop', 23, 2, '1671a094d6ebc2fdf2bf3d5960344957', '/finance/desktop/index', FALSE, '', 'PieChart', TRUE, FALSE, FALSE, 'MENU', TRUE, 1001, 'admin', FALSE, FALSE, 'NEW'),
--   > 记账本[二级菜单]
(25, '记账本', 'FinanceCashBook', '/finance/cashbook', 23, 2, 'a1933b994fc52f72f6b2aa1c784a123a', '/finance/cashbook/index', FALSE, '', 'Notebook', TRUE, FALSE, FALSE, 'MENU', TRUE, 1002, 'admin', FALSE, FALSE, 'NEW'),
--   > 表格工具[二级菜单]
(26, '日常费用', 'FinanceDaily', '/finance/daily', 23, 2, '796e760873f7a3d8af311e7da970fa09', '/finance/daily', FALSE, '', 'Calendar', TRUE, FALSE, FALSE, 'MENU', TRUE, 1003, 'admin', FALSE, FALSE, 'NEW'),
--   >> [三级级菜单]
(27, '收入来源', 'FinanceDailyIncome', '/finance/daily/income', 26, 3, '8892e032777d8ec0f2d276b10ff57f81', '/finance/daily/income/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 1004, 'admin', FALSE, TRUE, ''),
(28, '支出记录', 'FinanceDailyPay', '/finance/daily/pay', 26, 3, 'f4400db1e7d6e32527118a27e9d58cb6', '/finance/daily/pay/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 1005, 'admin', FALSE, TRUE, ''),
(29, '日常统计', 'FinanceDailyState', '/finance/daily/state', 26, 3, '1301092e5e41973a7e16580d38d8eec3', '/finance/daily/state/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 1006, 'admin', FALSE, TRUE, ''),


-- 日报模块[一级菜单]
(30, '日报', 'Diary', '/diary', 1, 1, 'edcf7eb3a7d5eab2be6688cb3e59fcee', '/diary', FALSE, '', 'Flag', TRUE, FALSE, FALSE, 'MENU', TRUE, 1100, 'admin', FALSE, FALSE, ''),
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
--   > 驾驶舱[二级菜单]
(31, '工作日报', 'DiaryWork', '/diary/work', 30, 2, '75bf5f6f679a0c19de96d02f73d81265', '/diary/work/index', FALSE, '', 'Sunny', TRUE, FALSE, FALSE, 'MENU', TRUE, 1101, 'admin', FALSE, FALSE, 'NEW'),
--   > 记账本[二级菜单]
(32, '随笔', 'DiaryJotter', '/diary/jotter', 30, 2, '212deeba5e5b83cb9535a59a9b997dd4', '/diary/jotter/index', FALSE, '', 'MoonNight', TRUE, FALSE, FALSE, 'MENU', TRUE, 1102, 'admin', FALSE, FALSE, 'NEW'),


-- 系统模块[一级菜单]
(33, '系统', 'System', '/system', 1, 1, 'a45da96d0bf6575970f2d27af22be28a', '/system', FALSE, '', 'HelpFilled', TRUE, FALSE, FALSE, 'MENU', TRUE, 2001, 'admin', FALSE, FALSE, ''),
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
--   > 系统维护[二级菜单]
(34, '系统维护', 'SystemOps', '/system/ops', 33, 2, '4059b0251f66a18cb56f544728796875', '/system/ops', FALSE, '', 'Operation', TRUE, FALSE, FALSE, 'MENU', TRUE, 2002, 'admin', FALSE, FALSE, ''),
--   >> [三级级菜单]
(35, '部门架构', 'SystemOpsDepart', '/system/ops/depart', 34, 3, '1d17cb9923b99f823da9f5a16dc460e5', '/system/ops/depart/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2003, 'admin', FALSE, TRUE, ''),
(36, '数据字典', 'SystemOpsDict', '/system/ops/dict', 34, 3, '91516e7a50ce0a67a8eb1f9229c293d1', '/system/ops/dict/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2004, 'admin', FALSE, TRUE, ''),
(37, '后台API', 'SystemOpsApi', '/system/ops/api', 34, 3, '4ae6c8f4429f7bacb050c9c980cf51d3', '/system/ops/api/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2005, 'admin', FALSE, TRUE, ''),
(38, '头像管理', 'SystemOpsAvatar', '/system/ops/avatar', 34, 3, 'eafdc02f3b847285bf1815f55f1f4e46', '/system/ops/avatar/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2006, 'admin', FALSE, TRUE, ''),
(39, '系统日志', 'SystemOpsLog', '/system/ops/log', 34, 3, 'fa83d9352d3c8fab04893bbf60be7e06', '/system/ops/log/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2007, 'admin', FALSE, TRUE, ''),
(40, '任务中心', 'SystemOpsTask', '/system/ops/task', 34, 3, '0d5939c51f761fe1d7fe3c9409577a6f', '/system/ops/task/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2008, 'admin', FALSE, TRUE, ''),
-- * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
--   > 系统维护[二级菜单]
(41, '权限管理', 'SystemMain', '/system/main', 33, 2, '34e34c43ec6b943c10a3cc1a1a16fb11', '/system/main', FALSE, '', 'Lock', TRUE, FALSE, FALSE, 'MENU', TRUE, 2008, 'admin', FALSE, FALSE, ''),
--   >> [三级级菜单]
(42, '用户管理', 'SystemMainUser', '/system/main/user', 41, 3, '8f9bfe9d1345237cb3b2b205864da075', '/system/main/user/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2009, 'admin', FALSE, TRUE, ''),
(43, '角色管理', 'SystemMainRole', '/system/main/role', 41, 3, 'bbbabdbe1b262f75d99d62880b953be1', '/system/main/role/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2010, 'admin', FALSE, TRUE, ''),
(44, '菜单管理', 'SystemMainMenu', '/system/main/menu', 41, 3, 'b61541208db7fa7dba42c85224405911', '/system/main/menu/index', FALSE, '', '', TRUE, FALSE, FALSE, 'MENU', TRUE, 2011, 'admin', FALSE, TRUE, ''),


-- 个人中心[一级菜单]
(45, '设置', 'Setter', '/setter', 1, 1, '130bdeec588552954b9e3bea0ef364b2', '/setter', FALSE, '', 'Setting', TRUE, FALSE, FALSE, 'MENU', TRUE, 10000, 'admin', FALSE, FALSE, ''),
--   > [二级菜单]
(46, '个人中心', 'SetterProfile', '/setter/profile', 45, 2, 'cce99c598cfdb9773ab041d54c3d973a', '/setter/profile/index', FALSE, '', 'User', TRUE, FALSE, FALSE, 'MENU', TRUE, 10001, 'admin', FALSE, TRUE, ''),
(47, '系统向导', 'SetterGuide', '/setter/guide', 45, 2, '6602bbeb2956c035fb4cb5e844a4861b', '/setter/guide/index', FALSE, '', 'Guide', TRUE, FALSE, FALSE, 'MENU', TRUE, 10002, 'admin', FALSE, TRUE, '');
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =