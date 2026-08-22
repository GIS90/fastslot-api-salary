> ## 1、项目架构

基于Python语言研发，使用FastAPI、Pydantic、异步数据库搭建的后端APIs脚手架，备具Restful API、JWT验证、Utils、Delib（第三方工具包封装）等功能，技术栈列表：

|    技术栈     |   版本   | 描述                              |
|:----------:|:------:|:--------------------------------|
| Python |  3.12  | 开发语言，官网：https://www.python.org/ |
| FastAPI | 0.123.7  | 脚手架开发语言使用的Web框架，一款API异步框架，推荐    |
|    Uvicorn    | 0.38.0 | web服务与应用app之间的管理                |
|   Pydantic    | 2.12.4  | 数据验证库                           |
|    Mysql    | 10.3.28-MariaDB | 数据库                             |
|    Supervisor    | 4.2.2  | 项目进程的启动、停止、重启等管理                |
  
***git clone***之后修改配置即可运行，在此基础上可进行二次开发，用于后台独立运行。   
项目可以运行于Linux、Windows、Macos等系统上，建议使用Centos7.5，支持性较好。


> ## 2、运维

### 环境搭建
- Centos7.5系统服务器一台
- Python3、Mysql、Supervisor等基础配套的环境安装
- 安装好数据库之后，执行README.md文件中的数据库初始化模块，里面配置数据库名称、用户名、密码等（根据需求改成项目需要的）
- 安装requirements.txt需要的包，命令pip install -r requirements.txt 或者 uv sync，建议用**conda/uv**管理Python版本环境
- 更新.env配置与对应的web配置文件：etc/prod.yaml（线上）、etc/dev.yaml（测试），根据不同需求进行配置更改
- 启动项目（cd 项目目录）：
  - Uvicorn方式：uvicorn deploy:app --reload --host 127.0.0.1 --port 8000
  - Python方式：python startup.py，端口在startup.py手工配置
- 选做：安装supervisor && 项目加入supervisor进行管理，项目包含了supervisord配置文件&&项目supervisorctl配置文件

### 配置说明
项目配置主要有2套，位于项目的根目录etc下，用于项目db、log等项目开发用的所有配置，具体的明细可以查看toml配置文件，有注释
- dev：测试环境
- prod：线上环境   

**强调一点**：测试环境http，线上环境https。.toml格式的配置文件是有deploy/config.py进行解析的，如果在config.toml配置文件中添加配置信息，需要在此文件进行解析添加。  
另外，supervisor_XXXX.conf是项目进程管理的配置信息，部署到线上。

## 数据库
详情见db.sql。


> ## 3、架构

### 项目目录
- deploy：项目源码
  - app：脚手架FSWebAppClass类的配置，包含exception、middleware
  - curd：数据库模型
  - delib：第三方工具包封装类
  - schema：包含数据格式定义：
    - po[API Route请求参数对象]：Parameter Object，base class：_po_base_model.py
    - dao[Modal数据访问对象]：Data Access Object，base class：_dao_base_model.py
    - dto[Modal数据传输API Route对象]：Data Transfer Object
  - service：用于写View与Modal之间的逻辑层
  - static：静态文件，集成了swagger-ui相关的文件，不然在查看接口说明的时间有时候加载失败
  - utils：常用的工具类
  - view：API路由定义
  - __init__.py：FSWebAppClass类初始化
  - config.py：解析配置文件的脚步
- etc：配置
- log：日志
- .env：具体使用哪个配置文件
- requirements.txt：项目依赖包
- startup.py：手动启动文件

### delib封装包
- dtalk_lib.py   
  DingTalk Api class, it use to push message  
  采用单例模式的DingApi类，主要用请求dingTalk openApi来操作DingDing进行发消息等操作  
  目前，只支持机器人推送消息操作  
  类添加了is_avail对access token进行判断是否可用，如果不可用中止程序
- excel_lib.py   
  Excel表读取、写入工具  
  使用了xlrd、xlwt、openpyxl，Excel表格处理包进行开发的lib工具包
- file_lib.py   
  文件处理包(the file dealing lib)  
  静态工具包，适用于任何项目以及脚本
- http_lib.py    
  HTTP请求工具，基于requests
- image_lib.py    
  图片处理
- qywx_lib.py    
  企业微信消息通知  
  腾讯企业微信官网提供一整套WebHook API接口，内容相当丰富，可以实现内部、第三方等各种各样的功能
- redis_lib.py    
  Redis客户端库类
  用于创建和管理Redis数据库连接的客户端库
- store_lib.py    
  对象存储  
  使用了七牛（qiniu.com）面对对象存储，注册免费使用10G空间

### 工具类方法
- base_class.py 基类
- command.py 命令行
- converter.py 转换器
- decorator.py 装饰器
- depend.py Depend依赖
- enumeration.py 枚举
- exception.py 异常类
- logger.py 日志
- printer.py 打印器
- status.py **API response JSON**
- status_value.py **API response JSON message**
- utils.py 工具方法，任何Python（version：3）项目都适合使用
- token.py Token

### crontab配置
采用Linux系统的crontab命令进行定时任务，脚手架默认自带：
- 日志清理：crontab/auto_clear_logs.sh
配置log_dir日志目录、keep_day保留天数

- 数据库备份：crontab/mysql_backup.task.sh
需要配置db_user、db_passwd、db_backup_dir、db_names数据库相关变量

  
> ## 4、开发特定点

### 项目启动startup、shutdown提示
文件：deploy/app/tip.py

- 配置__STARTUP_ASCII、__SHUTDOWN_ASCII变量进行项目启动、关闭提示。
- tip_color_startup、tip_color_shutdown配置tip颜色

### Excel合并与拆分
文件：deploy/delib/excel_lib.py

在开发Excel功能上，使用了openpyxl、xlwt && xlrd，但是都一些小问题，如下：
- openpyxl: 不支持.xls（老版本excel）
- xlwt、xlrd: 表格行数限制65535
只好，根据操作Excel数据文件的格式进行判断，去执行指定的方法，如果操作的数据文件包含一个.xls文件，就用xlwt、xlrd去处理，否则就用openpyxl。

### 枚举值缓存接口
文件：deploy/service/system/config/enum_value.py -> enum_by_name_money
对于系统功能使用到的枚举值，采用Redis进行缓存，获取机制采用：Redis->数据库


> ## 5、API接口标准
### 返回值标准格式
```
{
    "code": 200,
    "message": "Success",
    "data": {}
}   
```

### 状态码
|  分类	   | 状态码	  | 说明        |
|:------:|:-----:|:----------|
|  成功	   | 100	  | 成功        |
|        | 101	  | 成功，请求数据为空 |
|  登录	   | 200	| 用户未登录|
|        | 201	| 用户不存在
|        | 202	| 用户未注册
|        | 203	| 用户已注销
|        | 204	| 输入的账户/密码有误
|        | 205	| 用户输入的旧密码有误
|        | 206	| 输入的两次新密码不一致
|        | 207	| 无效用户
|        | 208	| 用户未分配系统菜单权限，请联系管理员
|        | 209	| 缺少用户名/密码
| Token	 | 250	| 没有发现用户TOKEN
|        | 251	| 用户TOKEN验证失败
|        | 252	| 用户TOKEN与RTX-ID不匹配
|        | 253	| 用户TOKEN已过期
|        | 254	| 生成用户TOKEN失败
|  请求方式  | 300	| 请求方式错误
|  请求参数  | 400	| 缺少请求参数
|        | 4001	| 缺少RTX-ID请求参数
|        | 4002	| 缺少MD5请求参数
|        | 401	| 请求参数不合法
|        | 402	| 请求参数类型不合法
|        | 403	| 请求参数不允许为空
|        | 404	| 请求参数值错误（如电话号11位、邮箱@符号、枚举值问题等）
|        | 405	| 请求参数长度超出限制
|        | 406	| 请求参数RTX-ID与Token不匹配
|  请求文件  | 450	| 缺少上传文件
|        | 451	| 文件不存在
|        | 452	| 文件内容不存在
|        | 453	| 文件超过最大65535行数
|        | 454	| 文件格式不支持
|        | 455	| 文件内容不符合要求
|        | 456	| 文件本地存储失败
|        | 457	| 文件云存储失败
|        | 458	| 文件数据已存在
|        | 459	| 文件导出数据为空
|        | 460	| 文件全部上传失败
|        | 461	| 文件部分上传失败
|        | 462	| 文件存储数据库记录失败
|        | 463	| 文件超出操作的SHEET索引
|        | 464	| 文件存储目录不存在
|        | 465	| 文件压缩有误
|        | 466	| 文件模板不匹配
|  数据提示  | 500	| 管理员用户数据，不允许操作
|        | 501	| 数据不存在
|        | 502	| 数据已存在，不允许新增
|        | 503	| 数据已删除，不允许操作
|        | 504	| 非数据权限人员，无权限操作
|        | 505	| 数据不完整，缺少信息
|        | 506	| 数据锁定字段不允许更新
|        | 507	| 部分数据新增成功
|        | 508	| 部分数据删除成功
|        | 509	| 部分数据更新成功
|        | 510	| 数据含有子数据，不允许删除
|        | 511	| 数据已锁定，请先解锁再进行操作
|  数据库	  | 600	| 数据库异常
|        | 601	| 数据库新增失败
|        | 602	| 数据库删除失败
|        | 603	| 数据库更新失败
|        | 604	| 数据库查询失败
|        | 605	| 数据库提交失败
|   其他   | 900	| 服务端API请求发生异常，请稍后尝试
|        | 901	| HTTP异常
|        | 902	| 第三方API接口异常
|        | 903	| 第三方TOKEN初始化失败
|        | 999	| 未知名异常
| 自定义异常	 |10000	|自定义异常原因|
|        |10001	 |禁止访问|


> ## 6、其他

### supervisor
管理项目进程的启动、停止、重启等操作
安装：pip install supervisor
把指定环境的supervisor_XXXX.conf cp到/etc/supervisord.d/include/*下。  
项目root根目录下有supervisord.conf文件，用来配置supervisord，放在/etc/supervisord.d目录下。

### uvicorn
负责web项目进程、服务，安装：pip install uvicorn，具体用法请uvicorn --help查看。

### qiniu对象存储
官网开发手册Python API：https://developer.qiniu.com/kodo/1242/python
1.七牛API上传文件发送ProtocolError-Connection-aborted错误
解决：
1.1 找到Pyhton的第三方包qiniu config.py配置文件
https://github.com/qiniu/python-sdk/blob/master/qiniu/config.py
1.2 修改参数
```
_config = {
    'default_zone': zone.Zone(),
    'default_rs_host': RS_HOST,
    'default_rsf_host': RSF_HOST,
    'default_api_host': API_HOST,
    'default_uc_host': UC_HOST,
    'connection_timeout': 120,  # 链接超时为时间为30s
    'connection_retries': 3,  # 链接重试次数为3次
    'connection_pool': 10,  # 链接池个数为10
    'default_upload_threshold': 2 * _BLOCK_SIZE  # put_file上传方式的临界默认值
}
```
把connection_timeout连接时间由默认的30秒修改为120秒。
原因是服务器带宽不够导致上传超时。


> ## 7、联系方式

* ***Github:*** https://github.com/GIS90
* ***Email:*** gaoming971366@163.com
* ***Blog:*** http://pygo.space
* ***OPENTOOL-Z:*** http://2l.pygo.space
* ***WeChat:*** PyGo90


Enjoy the good life every day！！！
