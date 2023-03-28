
import sqlite3
import threading

from constants import DATABASE


def get_connection():
    """获取SQLite的连接"""
    # check_same_thread=False: 表示允许 sqlite 被多个线程同时访问
    return sqlite3.connect(DATABASE, check_same_thread=False)


class Computer:
    def __init__(self):
        # 获取数据库连接对象和游标对象
        self.conn = get_connection()
        self.c = self.conn.cursor()
        self.table_name = None
        self.tmp = []

    def create(self, table_name):
        """
        建表
        :param table_name: 表名
        """
        try:
            self.c.execute("drop table if exists {};".format(table_name))
            sql = "CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT,prod_name TEXT," \
                  "config TEXT,shop TEXT,price TEXT);".format(table_name)
            self.c.execute(sql)
            # print("数据表创建成功...")
            self.conn.commit()  # 事务提交
        except Exception as e:
            print("建表失败，发生错误：{}".format(e))
        finally:
            self.table_name = table_name

    def insert(self, data_lst):
        """
        一次向表中插入多行数据
        :param data_lst: 由多行数据组成的列表
        """
        lock = threading.Lock()  # 加锁
        try:
            lock.acquire(True)
            sql = "INSERT INTO {} (prod_name,config,shop,price) VALUES (?,?,?,?)".format(self.table_name)
            self.c.executemany(sql, data_lst)
            self.conn.commit()
        except Exception as e:
            # self.conn.rollback()
            self.tmp.append(data_lst)
        finally:
            lock.release()
        # print("第{}条数据插入成功...".format(i+1))

    def select(self, table_name):
        """"""
        try:
            sql = "SELECT * FROM {};".format(table_name)
            return self.c.execute(sql).fetchall()
        except Exception as e:
            print("查询数据失败...发生错误：".format(e))

    def close(self):
        """关闭数据库连接和游标"""
        self.conn.close()
        self.c.close()


computer = Computer()


# if __name__ == '__main__':
#     print(DATABASE)
#     computer = Computer()
#     info = "￥3599.00,惠普HP 星15青春版 15英寸大屏网课轻薄笔记本电脑(8核锐龙R7处理器 16G 512G 高速WIFI6 7×24h在线服务 银),2万+条评价,惠普京东自营官方旗舰店"
#     # data = split_info(info, ",")
#     # print(data)
#     result = computer.select("laptop")
#     print(result)
