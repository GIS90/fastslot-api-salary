# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    Redis客户端库类（升级版）
    使用连接池管理Redis连接，支持 RESP2 协议兼容老版本 Redis
    兼容 Redis 4.x/5.x/6.x/7.x

base_info:
    __author__ = PyGo
    __time__ = 2026/09/09
    __version__ = v.2.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = redis_lib.py

usage:
    # 初始化
    redis_client = RedisClientLib(
        host='localhost',
        port=6379,
        db=0,
        password=None,
        max_connections=50,
        decode_responses=True
    )

    # 基本操作
    redis_client.set_key('key', 'value', ex=60)
    value = redis_client.get_key('key')
    redis_client.delete_key('key')

    # 使用上下文管理器
    with redis_client.get_connection() as conn:
        conn.set('foo', 'bar')
        data = conn.get('foo')

design:
    1. 使用连接池管理连接，提高性能
    2. protocol=2 强制使用 RESP2 协议，兼容 Redis 4.x/5.x
    3. 自动重连机制
    4. 全面的异常捕获和日志记录

reference urls:
    https://redis-py.readthedocs.io/
    https://github.com/redis/redis-py

python version:
    python3.8+

Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""

import redis
from typing import Optional, Any, Union, List, Dict, Tuple
from contextlib import contextmanager
from datetime import timedelta, datetime
from deploy.utils.logger import logger as LOG


class RedisClientLib:
    """
    Redis 客户端库类（升级版）

    Args:
        host (str): Redis服务器主机地址
        port (int): Redis服务器端口号，默认 6379
        db (int): 要连接的数据库编号，默认 0
        password (Optional[str]): Redis服务器密码，无密码则传入 None
        max_connections (int): 连接池最大连接数，默认 50
        decode_responses (bool): 是否自动解码响应数据，默认 True
        socket_timeout (Optional[int]): Socket 超时时间（秒），默认 None
        socket_connect_timeout (Optional[int]): 连接超时时间（秒），默认 None
        retry_on_error (Optional[List]): 需要重试的错误类型，默认 [ConnectionError, TimeoutError]
        protocol (int): Redis 协议版本，默认 2（RESP2），兼容老版本
        health_check_interval (int): 健康检查间隔（秒），默认 30

    Returns:
        None
    """
    # 连接默认配置
    _DEFAULT_MAX_CONNECTIONS: int = 50
    _DEFAULT_SOCKET_TIMEOUT: int = 5
    _DEFAULT_SOCKET_CONNECT_TIMEOUT: int = 3
    _DEFAULT_RETRY_TIMES: int = 3
    _DEFAULT_PROTOCOL: int = 2
    _DEFAULT_HEALTH_CHECK_INTERVAL: int = 30

    def __init__(
            self,
            host: str,
            port: int = 6379,
            db: int = 0,
            password: Optional[str] = None,
            max_connections: int = _DEFAULT_MAX_CONNECTIONS,
            decode_responses: bool = True,
            socket_timeout: int = _DEFAULT_SOCKET_TIMEOUT,
            socket_connect_timeout: int = _DEFAULT_SOCKET_CONNECT_TIMEOUT,
            retry_on_error: Optional[List] = None,
            protocol: int = _DEFAULT_PROTOCOL,  # 强制使用 RESP2 协议，兼容老版本 Redis
            health_check_interval: int = _DEFAULT_HEALTH_CHECK_INTERVAL
    ) -> None:
        self.HOST: str = host
        self.PORT: int = port
        self.DB: int = db
        self.PASSWORD: Optional[str] = password
        self.MAX_CONNECTIONS: int = max_connections
        self.DECODE_RESPONSES: bool = decode_responses
        self.SOCKET_TIMEOUT: Optional[int] = socket_timeout
        self.SOCKET_CONNECT_TIMEOUT: Optional[int] = socket_connect_timeout
        self.PROTOCOL: int = protocol
        self.HEALTH_CHECK_INTERVAL: int = health_check_interval
        # 默认重试错误类型
        if retry_on_error is None:
            self.RETRY_ON_ERROR = [
                redis.ConnectionError,
                redis.TimeoutError,
                redis.BusyLoadingError,
            ]
        else:
            self.RETRY_ON_ERROR = retry_on_error
        self._pool: Optional[redis.ConnectionPool] = None
        self._client: Optional[redis.Redis] = None
        self._is_closed: bool = False

    def __str__(self) -> str:
        return f"RedisClientLib Class: [host: {self.HOST}] [port: {self.PORT}] [db: {self.DB}] "

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def pool(self) -> redis.ConnectionPool:
        """获取或创建连接池"""
        if self._pool is None:
            try:
                self._pool = redis.ConnectionPool(
                    host=self.HOST,
                    port=self.PORT,
                    db=self.DB,
                    password=self.PASSWORD,
                    max_connections=self.MAX_CONNECTIONS,
                    decode_responses=self.DECODE_RESPONSES,
                    socket_timeout=self.SOCKET_TIMEOUT,
                    socket_connect_timeout=self.SOCKET_CONNECT_TIMEOUT,
                    retry_on_error=self.RETRY_ON_ERROR,
                    protocol=self.PROTOCOL,  # 关键：强制使用 RESP2
                    health_check_interval=self.HEALTH_CHECK_INTERVAL,
                )
                LOG.info(f"[RedisClientLib] 连接池创建成功: {self}")
            except redis.RedisError as e:
                LOG.error(f"[RedisClientLib] 创建连接池失败: {e}")
                raise

        return self._pool

    @property
    def client(self) -> redis.Redis:
        """获取 Redis 客户端实例（使用连接池）"""
        if self._client is None or self._is_closed:
            try:
                self._client = redis.Redis(connection_pool=self.pool)
                # 测试连接
                self._client.ping()
                LOG.info(f"[RedisClientLib] Redis 客户端初始化成功: {self}")
            except redis.RedisError as e:
                LOG.error(f"[RedisClientLib] 创建 Redis 客户端失败: {e}")
                raise

        return self._client

    def close(self) -> None:
        """关闭连接池和客户端"""
        self._is_closed = True
        if self._client:
            try:
                self._client.close()
            except Exception as e:
                LOG.warning(f"[RedisClientLib] 关闭客户端时出错: {e}")
            finally:
                self._client = None

        if self._pool:
            try:
                self._pool.disconnect()
            except Exception as e:
                LOG.warning(f"[RedisClientLib] 断开连接池时出错: {e}")
            finally:
                self._pool = None

        LOG.info(f"[RedisClientLib] Redis 连接已关闭")

    @contextmanager
    def get_connection(self) -> redis.Redis:
        """
        获取 Redis 连接的上下文管理器
        使用示例:
            with redis_client.get_connection() as conn:
                conn.set('key', 'value')
        """
        conn = None
        try:
            conn = self.client
            yield conn
        except redis.RedisError as e:
            LOG.error(f"[RedisClientLib] Redis 操作异常: {e}")
            raise
        except Exception as e:
            LOG.error(f"[RedisClientLib] 未知异常: {e}")
            raise
        finally:
            # 连接池管理，不需要主动关闭连接
            pass

    def ping(self) -> bool:
        """检查 Redis 连接是否正常"""
        try:
            with self.get_connection() as conn:
                return conn.ping()
        except redis.RedisError as e:
            LOG.error(f"[RedisClientLib] ping 失败: {e}")
            return False

    # ==================== 基础操作 ====================

    def set_key(
            self,
            key: str,
            value: Any,
            ex: Optional[Union[int, timedelta]] = None,
            px: Optional[Union[int, timedelta]] = None,
            nx: bool = False,
            xx: bool = False,
    ) -> Optional[bool]:
        """
        设置键值对

        Args:
            key: 键名
            value: 值
            ex: 过期时间（秒）
            px: 过期时间（毫秒）
            nx: 仅当键不存在时设置
            xx: 仅当键存在时设置
        """
        with self.get_connection() as conn:
            return conn.set(key, value, ex=ex, px=px, nx=nx, xx=xx)

    def get_key(self, key: str) -> Optional[Any]:
        """获取键对应的值，键不存在返回 None"""
        with self.get_connection() as conn:
            return conn.get(key)

    def delete_key(self, *keys: str) -> int:
        """删除一个或多个键，返回成功删除的数量"""
        if not keys:
            return 0
        with self.get_connection() as conn:
            return conn.delete(*keys)

    def exists_key(self, *keys: str) -> int:
        """检查键是否存在，返回存在的键数量"""
        if not keys:
            return 0
        with self.get_connection() as conn:
            return conn.exists(*keys)

    def expire_key(self, key: str, time: Union[int, timedelta]) -> bool:
        """设置键的过期时间，成功返回 True"""
        with self.get_connection() as conn:
            return conn.expire(key, time)

    def expireat_key(self, key: str, when: Union[int, datetime]) -> bool:
        """设置键的过期时间（指定时间戳），成功返回 True"""
        with self.get_connection() as conn:
            return conn.expireat(key, when)

    def ttl_key(self, key: str) -> int:
        """获取键的剩余生存时间（秒），-1 表示永久，-2 表示不存在"""
        with self.get_connection() as conn:
            return conn.ttl(key)

    def pttl_key(self, key: str) -> int:
        """获取键的剩余生存时间（毫秒）"""
        with self.get_connection() as conn:
            return conn.pttl(key)

    def incr_key(self, key: str, amount: int = 1) -> int:
        """自增键的值，返回自增后的值"""
        with self.get_connection() as conn:
            return conn.incr(key, amount)

    def decr_key(self, key: str, amount: int = 1) -> int:
        """自减键的值，返回自减后的值"""
        with self.get_connection() as conn:
            return conn.decr(key, amount)

    # ==================== 哈希操作 ====================

    def hset(self, name: str, key: str, value: Any) -> int:
        """设置哈希表中的字段值"""
        with self.get_connection() as conn:
            return conn.hset(name, key, value)

    def hset_dict(self, name: str, mapping: Dict[str, Any]) -> int:
        """批量设置哈希表字段"""
        with self.get_connection() as conn:
            return conn.hset(name, mapping=mapping)

    def hget(self, name: str, key: str) -> Optional[Any]:
        """获取哈希表中指定字段的值"""
        with self.get_connection() as conn:
            return conn.hget(name, key)

    def hgetall(self, name: str) -> Dict[str, Any]:
        """获取哈希表所有字段和值"""
        with self.get_connection() as conn:
            return conn.hgetall(name)

    def hdel(self, name: str, *keys: str) -> int:
        """删除哈希表中的一个或多个字段"""
        with self.get_connection() as conn:
            return conn.hdel(name, *keys)

    def hexists(self, name: str, key: str) -> bool:
        """检查哈希表中是否存在指定字段"""
        with self.get_connection() as conn:
            return conn.hexists(name, key)

    def hkeys(self, name: str) -> List[str]:
        """获取哈希表的所有字段名"""
        with self.get_connection() as conn:
            return conn.hkeys(name)

    def hvals(self, name: str) -> List[Any]:
        """获取哈希表的所有值"""
        with self.get_connection() as conn:
            return conn.hvals(name)

    def hlen(self, name: str) -> int:
        """获取哈希表的字段数量"""
        with self.get_connection() as conn:
            return conn.hlen(name)

    # ==================== 列表操作 ====================

    def lpush(self, name: str, *values: Any) -> int:
        """在列表头部插入一个或多个值"""
        with self.get_connection() as conn:
            return conn.lpush(name, *values)

    def rpush(self, name: str, *values: Any) -> int:
        """在列表尾部插入一个或多个值"""
        with self.get_connection() as conn:
            return conn.rpush(name, *values)

    def lpop(self, name: str, count: int = 1) -> Any:
        """从列表头部移除并返回元素"""
        with self.get_connection() as conn:
            return conn.lpop(name, count)

    def rpop(self, name: str, count: int = 1) -> Any:
        """从列表尾部移除并返回元素"""
        with self.get_connection() as conn:
            return conn.rpop(name, count)

    def lrange(self, name: str, start: int, end: int) -> List[Any]:
        """获取列表指定范围的元素"""
        with self.get_connection() as conn:
            return conn.lrange(name, start, end)

    def llen(self, name: str) -> int:
        """获取列表长度"""
        with self.get_connection() as conn:
            return conn.llen(name)

    # ==================== 集合操作 ====================

    def sadd(self, name: str, *values: Any) -> int:
        """向集合添加一个或多个元素"""
        with self.get_connection() as conn:
            return conn.sadd(name, *values)

    def srem(self, name: str, *values: Any) -> int:
        """从集合移除一个或多个元素"""
        with self.get_connection() as conn:
            return conn.srem(name, *values)

    def smembers(self, name: str) -> set:
        """获取集合的所有元素"""
        with self.get_connection() as conn:
            return conn.smembers(name)

    def sismember(self, name: str, value: Any) -> bool:
        """检查元素是否属于集合"""
        with self.get_connection() as conn:
            return conn.sismember(name, value)

    def scard(self, name: str) -> int:
        """获取集合的元素数量"""
        with self.get_connection() as conn:
            return conn.scard(name)

    # ==================== 有序集合操作 ====================

    def zadd(self, name: str, mapping: Dict[Any, float]) -> int:
        """向有序集合添加一个或多个元素"""
        with self.get_connection() as conn:
            return conn.zadd(name, mapping)

    def zrange(
            self, name: str, start: int, end: int, withscores: bool = False
    ) -> Union[List[Any], List[Tuple[Any, float]]]:
        """按索引范围获取有序集合元素"""
        with self.get_connection() as conn:
            return conn.zrange(name, start, end, withscores=withscores)

    def zrevrange(
            self, name: str, start: int, end: int, withscores: bool = False
    ) -> Union[List[Any], List[Tuple[Any, float]]]:
        """按索引范围获取有序集合元素（降序）"""
        with self.get_connection() as conn:
            return conn.zrevrange(name, start, end, withscores=withscores)

    def zrem(self, name: str, *values: Any) -> int:
        """从有序集合移除一个或多个元素"""
        with self.get_connection() as conn:
            return conn.zrem(name, *values)

    def zcard(self, name: str) -> int:
        """获取有序集合的元素数量"""
        with self.get_connection() as conn:
            return conn.zcard(name)

    # ==================== 批量操作 ====================

    def mget(self, *keys: str) -> List[Optional[Any]]:
        """批量获取多个键的值"""
        if not keys:
            return []
        with self.get_connection() as conn:
            return conn.mget(*keys)

    def mset(self, mapping: Dict[str, Any]) -> bool:
        """批量设置多个键值对"""
        with self.get_connection() as conn:
            return conn.mset(mapping)

    # ==================== 管道操作 ====================

    @contextmanager
    def pipeline(self, transaction: bool = True):
        """
        获取 Redis 管道的上下文管理器
        Redis 管道用于批量执行命令，减少网络往返延迟

        使用示例:
            with redis_client.pipeline() as pipe:
                pipe.set('key1', 'value1')
                pipe.set('key2', 'value2')
                results = pipe.execute()
        """
        with self.get_connection() as conn:
            pipe = conn.pipeline(transaction=transaction)
            try:
                yield pipe
            except Exception as e:
                pipe.reset()
                LOG.error(f"[RedisClientLib] 管道操作异常: {e}")
                raise
            finally:
                pass

    # ==================== 锁操作 ====================

    def lock(
            self,
            name: str,
            timeout: Optional[int] = None,
            blocking_timeout: Optional[int] = None,
            lock_class: Optional[redis.lock.Lock] = None,
    ) -> redis.lock.Lock:
        """
        获取 Redis 分布式锁

        Args:
            name: 锁名称
            timeout: 锁超时时间（秒）
            blocking_timeout: 等待获取锁的超时时间（秒）
            lock_class: 锁类

        使用示例:
            with redis_client.lock('my_lock', timeout=10):
                # 临界区代码
                pass
        """
        with self.get_connection() as conn:
            if lock_class:
                return lock_class(conn, name, timeout=timeout, blocking_timeout=blocking_timeout)
            return conn.lock(name, timeout=timeout, blocking_timeout=blocking_timeout)

    # ==================== 工具方法 ====================

    def keys(self, pattern: str = '*') -> List[str]:
        """获取匹配模式的所有键（生产环境慎用，可能导致性能问题）"""
        with self.get_connection() as conn:
            return conn.keys(pattern)

    def randomkey(self) -> Optional[str]:
        """随机返回一个键"""
        with self.get_connection() as conn:
            return conn.randomkey()

    def dbsize(self) -> int:
        """获取当前数据库的键数量"""
        with self.get_connection() as conn:
            return conn.dbsize()

    def flushdb(self) -> bool:
        """清空当前数据库（危险操作）"""
        LOG.warning(f"[RedisClientLib] 执行 flushdb 操作，清空数据库: {self.DB}")
        with self.get_connection() as conn:
            return conn.flushdb()

    def flushall(self) -> bool:
        """清空所有数据库（危险操作）"""
        LOG.warning("[RedisClientLib] 执行 flushall 操作，清空所有数据库")
        with self.get_connection() as conn:
            return conn.flushall()


# ==================== 方法调用（可选） ====================
def create_redis_client(
        host: str,
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        max_connections: int = 50,
        decode_responses: bool = True,
        protocol: int = 2,
) -> RedisClientLib:
    """
    创建 Redis 客户端的便捷函数

    使用示例:
        redis_client = create_redis_client(
            host='localhost',
            port=6379,
            db=0,
            password='your_password'
        )
        redis_client.set_key('key', 'value', ex=60)
    """
    return RedisClientLib(
        host=host,
        port=port,
        db=db,
        password=password,
        max_connections=max_connections,
        decode_responses=decode_responses,
        protocol=protocol,
    )