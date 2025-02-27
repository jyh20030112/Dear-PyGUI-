import mysql

x = mysql.mysql()
cursor, conn = x.set_mysql()

sql = "select c_id, c_course, t_id, t_name from cour_ele_info where s_id = 's123'"
cursor.execute(sql)
data1 = cursor.fetchall()
print(data1)
x.close_mysql(cursor, conn)

