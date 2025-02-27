from typing import Union, Any

import pymysql

class mysql:
    def __init__(self):
        pass

    def set_mysql(self):
        conn = pymysql.connect(
            host='127.0.0.1',  # 连接主机, 默认127.0.0.1
            user='root',  # 用户名
            passwd='123123',  # 密码
            port=3306,  # 端口，默认为3306
            db='test',  # 数据库名称
            charset='utf8'  # 字符编码
            ,autocommit=True
        )
        cursor = conn.cursor()
        return cursor, conn

    def close_mysql(self, cursor, conn):
        cursor.close()
        conn.close()

if __name__ == "__main__":
    x = mysql()
    cursor, conn = x.set_mysql()
    sql = "select user_password from login where user_id = 'root'"
    cursor.execute(sql)  # 返回值是查询到的数据数量
    # 通过 fetchall方法获得数据
    data = cursor.fetchone()
    print(data[0])


    x.close_mysql(cursor, conn)
