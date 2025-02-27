## 实验选课系统
import sys
import Font
import dearpygui.dearpygui as dpg
import pandas as pd
import dearpygui.demo as demo

from mysql import *



def ad_stu_enter(sender, app_data, user_data):
    ad_s_id = dpg.get_value(user_data['学号'])
    ad_s_pass = dpg.get_value(user_data['密码'])
    ad_s_name = dpg.get_value(user_data['姓名'])
    ad_s_class = dpg.get_value(user_data['班级'])
    ad_s_sex = dpg.get_value(user_data['性别'])
    ad_s_faculty = dpg.get_value(user_data['学院'])
    ad_s_birth = dpg.get_value(user_data['生日'])
    ad_stu_info = [ad_s_id,ad_s_pass,ad_s_name,ad_s_class,
                   ad_s_sex,ad_s_faculty,ad_s_birth]
    ad_stu_list = []
    for i in ad_stu_info:
        if i == '':
            with dpg.window(modal=True,label="警告", tag="model_id_enter",
                            show=True,pos=(400,200),no_close=True,no_collapse=True):
                dpg.add_button(label="输入有空！！", callback=lambda : dpg.delete_item("model_id_enter"))
            break
        else:
            ad_stu_list.append(i)
            if len(ad_stu_list) == 7:
                add_sql1 = ("insert into s_user value('%s','%s','%s','%s','%s','%s','%s')"
                            %(ad_s_id,ad_s_pass,
                            ad_s_name,ad_s_class,
                            ad_s_sex,ad_s_faculty,ad_s_birth))
                add_sql2 = ("insert into login value('%s','%s')"%(ad_s_id, ad_s_pass))
                cursor.execute(add_sql1)
                cursor.execute(add_sql2)
                mange('ad_stu', app_data, user_data)
            else:
                continue

def ad_stu_delete(sender, app_data, user_data):
    ad_s_id = dpg.get_value(user_data['学号'])
    check_delete_sql = ("select * from s_user where id = '%s' "%(ad_s_id))
    cursor.execute(check_delete_sql)
    check_delete_sql2 = ("select * from login where user_id = '%s' " % (ad_s_id))
    cursor.execute(check_delete_sql2)
    colum_list = cursor.fetchall()
    if len(colum_list) == 0:
        with dpg.window(modal=True, label="警告", tag="model_id_delete_check_none",
                        show=True, pos=(400, 200), no_close=True,
                        no_collapse=True):
            dpg.add_button(label="请输入有效数据！！", callback=lambda: dpg.delete_item("model_id_delete_check_none"))

    else:
        delete_sql = ("delete from s_user where id = '%s' " % (ad_s_id))
        cursor.execute(delete_sql)
        delete_sql2 = ("delete from login where user_id = '%s' " % (ad_s_id))
        cursor.execute(delete_sql2)
        mange('ad_stu',app_data,user_data)

def ad_stu_check(sender, app_data, user_data):
    colum_name = ['学号','密码','姓名','班级','性别','学院','生日']
    ad_s_id = dpg.get_value(user_data['学号'])
    check_sql = ("select * from s_user where id = '%s' "%(ad_s_id))
    cursor.execute(check_sql)
    colum_list = cursor.fetchall()
    if len(colum_list) == 0:
        with dpg.window(modal=True, label="警告", tag="model_id_check_none", show=True, pos=(400, 200), no_close=True,
                        no_collapse=True):
            dpg.add_button(label="请输入有效数据！！", callback=lambda: dpg.delete_item("model_id_check_none"))
    else:
        cursor.execute(check_sql)
        colum_list = cursor.fetchall()[0]
        with dpg.window(modal=True, label="查找", tag="check_win",pos=(200, 200),width=900,height=130,
                        no_close=True,no_collapse=True):
            with dpg.table(header_row=True,
                               parent='check_win',
                               row_background=True,
                               borders_innerH=True,
                               borders_innerV=True, borders_outerV=True, borders_outerH=True, tag='ad_stu_table_check'):
                for i in colum_name:
                        dpg.add_table_column(label=i)

                with dpg.table_row():
                    for j in colum_list:
                        dpg.add_text(f"{j}")
            dpg.add_button(label="ok!", callback=lambda: dpg.delete_item("check_win"))

def ad_stu_alter_fun(sender,app_data, user_data):
    ad_alter_id = user_data['修改学号']
    ad_s_id = dpg.get_value(user_data['学号'])
    ad_s_pass = dpg.get_value(user_data['密码'])
    ad_s_name = dpg.get_value(user_data['姓名'])
    ad_s_class = dpg.get_value(user_data['班级'])
    ad_s_sex = dpg.get_value(user_data['性别'])
    ad_s_faculty = dpg.get_value(user_data['学院'])
    ad_s_birth = dpg.get_value(user_data['生日'])
    ad_stu_info_dict={
        'id':ad_s_id, 'password':ad_s_pass, 'name':ad_s_name,
        'class':ad_s_class, 'sex':ad_s_sex, 'faculty':ad_s_faculty,
        'birth':ad_s_birth
    }
    number = 0
    for i,j in ad_stu_info_dict.items():
        if j == "":
            number+=1
            if number == 7:
                with dpg.window(modal=True, label="警告", tag="model_id_alter_check",
                                show=True, pos=(400, 200), no_close=True,no_collapse=True):
                    dpg.add_button(label="请输入有效数据！！",
                                   callback=lambda: dpg.delete_item("model_id_alter_check"))
        else:
            sql_alter = ("update s_user set %s = '%s' where id = '%s'"%(i,j,ad_alter_id))
            cursor.execute(sql_alter)
            if i == 'id':
                sql_alter2 = ("update login set user_id = '%s' where user_id = '%s'" % (j, ad_alter_id))
                print(sql_alter2)
                cursor.execute(sql_alter2)
            elif i == 'password':
                sql_alter2 = ("update login set user_password = '%s' where user_password = '%s'" % (j, ad_alter_id))
                print(sql_alter2)
                cursor.execute(sql_alter2)
    if number != 7:
        with dpg.window(modal=True, label="警告", tag="model_alter_check_success", show=True, pos=(400, 200), no_close=True,
                        no_collapse=True):
            dpg.add_button(label="修改成功", callback=refsh)

def refsh(sender, app_data, user_data):
    dpg.delete_item("model_alter_check_success")
    mange('ad_stu', app_data, user_data)

def ad_stu_alter(sender, app_data, user_data):
    ad_alter_id = dpg.get_value(user_data['学号'])
    alter_sql = ("select * from s_user where id = '%s' " % (ad_alter_id))
    cursor.execute(alter_sql)
    colum_list = cursor.fetchall()
    if len(colum_list) == 0:
        with dpg.window(modal=True, label="警告", tag="model_id_delete_check_none",
                        show=True, pos=(400, 200), no_close=True,
                        no_collapse=True):
            dpg.add_button(label="请输入有效数据！！", callback=lambda: dpg.delete_item("model_id_delete_check_none"))
    else:
        with dpg.window(modal=False, label="修改", tag="ad_stu_alter_win",show=True, pos=(400, 200), no_close=True,
                        no_collapse=True):
            dpg.add_text(default_value="学号：", pos=(20, 50))
            ad_stu_id = dpg.add_input_text(pos=(80, 50), width=150, height=150)
            dpg.add_text(default_value="密码：", pos=(20, 100))
            ad_stu_pass = dpg.add_input_text(pos=(80, 100), width=150, height=150)
            dpg.add_text(default_value="姓名：", pos=(20, 150))
            ad_stu_name = dpg.add_input_text(pos=(80, 150), width=150, height=150)
            dpg.add_text(default_value="班级：", pos=(20, 200))
            ad_stu_class = dpg.add_input_text(pos=(80, 200), width=150, height=150)
            dpg.add_text(default_value="性别：", pos=(270, 50))
            ad_stu_sex = dpg.add_input_text(hint='男/女', pos=(330, 50), width=150, height=150)
            dpg.add_text(default_value="学院：", pos=(270, 100))
            ad_stu_faculty = dpg.add_input_text(pos=(330, 100), width=150, height=150)
            dpg.add_text(default_value="生日：", pos=(270, 150))
            ad_stu_birth = dpg.add_input_text(hint='2003-1-12', pos=(330, 150), width=150, height=150)

            info_dict = {'修改学号': ad_alter_id ,'学号': ad_stu_id, '密码': ad_stu_pass,
                         '姓名': ad_stu_name, '班级': ad_stu_class,
                         '性别': ad_stu_sex, '学院': ad_stu_faculty, '生日': ad_stu_birth}
            dpg.add_button(label='修改',pos=(260, 200), width=90, height=35,
                           callback=ad_stu_alter_fun,tag='ad_s_alter_but',user_data=info_dict)
            dpg.add_button(label='取消',pos=(380,200),width=90, height=35,tag='ad_s_cancel_but',
                           callback=lambda: dpg.delete_item("ad_stu_alter_win"))


def ad_tea_enter(sender, app_data, user_data):
    pass

def ad_tea_delete(sender, app_data, user_data):
    pass

def ad_tea_check(sender, app_data, user_data):
    pass

def mange(sender, app_data, user_data):
    dpg.delete_item('ad_table_win')
    dpg.delete_item('ad_components')
    if sender == 'ad_stu':
        colum_name = ['学号','密码','姓名','班级','性别','学院','生日']
        sql = "select * from s_user"
        cursor.execute(sql)
        colum_list = cursor.fetchall()
        dpg.add_child_window(parent='Administrator', pos=(10, 100), tag='ad_table_win', height=200)
        with dpg.table(header_row=True,
                       parent='ad_table_win',
                       row_background=True,
                       borders_innerH=True,
                       borders_innerV=True, borders_outerV=True, borders_outerH=True, tag='ad_table'):
            for i in colum_name:
                dpg.add_table_column(label=i)

            for i in colum_list:
                with dpg.table_row():
                    for j in i:
                        dpg.add_text(f"{j}")

        with dpg.group(parent='Administrator', tag='ad_components'):
            dpg.add_text(default_value="学号：", pos=(50, 350))
            ad_stu_id = dpg.add_input_text(pos=(110, 350), width=150, height=150)
            dpg.add_text(default_value="密码：", pos=(50, 400))
            ad_stu_pass = dpg.add_input_text(pos=(110, 400), width=150, height=150)
            dpg.add_text(default_value="姓名：", pos=(50, 450))
            ad_stu_name = dpg.add_input_text(pos=(110, 450), width=150, height=150)
            dpg.add_text(default_value="班级：", pos=(50, 500))
            ad_stu_class = dpg.add_input_text(pos=(110, 500), width=150, height=150)
            dpg.add_text(default_value="性别：", pos=(300, 350))
            ad_stu_sex = dpg.add_input_text(hint='男/女', pos=(360, 350), width=150, height=150)
            dpg.add_text(default_value="学院：", pos=(300, 400))
            ad_stu_faculty = dpg.add_input_text(pos=(360, 400), width=150, height=150)
            dpg.add_text(default_value="生日：", pos=(300, 450))
            ad_stu_birth = dpg.add_input_text(hint='2003-1-12', pos=(360, 450), width=150, height=150)

            info_dict={'学号':ad_stu_id,'密码':ad_stu_pass,
                    '姓名':ad_stu_name,'班级':ad_stu_class,
                    '性别':ad_stu_sex,'学院':ad_stu_faculty,'生日':ad_stu_birth}

            dpg.add_button(label='录入', pos=(550, 380), width=150, height=35,callback=ad_stu_enter,
                           user_data=info_dict,tag='ad_s_enter')
            dpg.add_button(label='删除(请输入学号)', pos=(750, 380), width=170, height=35,callback=ad_stu_delete,
                           user_data=info_dict,tag='ad_s_delete')
            dpg.add_button(label="查询(请输入学号)",pos=(650, 440), width=170, height=35,callback=ad_stu_check,
                           user_data=info_dict,tag='ad_s_check')
            dpg.add_button(label="修改(请输入学号)",pos=(650,490),width=170, height=35,callback=ad_stu_alter,
                           user_data=info_dict,tag='ad_s_alter')

    elif sender == 'ad_tea':
        colum_name = ['教师编号', '密码', '姓名', '性别', '所任课程', '职称', '学院']
        sql = "select * from t_user"
        cursor.execute(sql)
        colum_list = cursor.fetchall()
        dpg.add_child_window(parent='Administrator', pos=(10, 100), tag='ad_table_win', height=200)
        with dpg.table(header_row=True,
                       parent='ad_table_win',
                       row_background=True,
                       borders_innerH=True,
                       borders_innerV=True, borders_outerV=True, borders_outerH=True, tag='ad_table'):
            for i in colum_name:
                dpg.add_table_column(label=i)

            for i in colum_list:
                with dpg.table_row():
                    for j in i:
                        dpg.add_text(f"{j}")
        with dpg.group(parent='Administrator', tag='ad_components'):
            dpg.add_text(default_value="教师编号：", pos=(20, 350))
            ad_tea_id = dpg.add_input_text(pos=(110, 350), width=150, height=150)
            dpg.add_text(default_value="密码：", pos=(50, 400))
            ad_tea_pass = dpg.add_input_text(pos=(110, 400), width=150, height=150)
            dpg.add_text(default_value="姓名：", pos=(50, 450))
            ad_tea_name = dpg.add_input_text(pos=(110, 450), width=150, height=150)
            dpg.add_text(default_value="性别：", pos=(50, 500))
            ad_tea_sex = dpg.add_input_text(hint='男/女',pos=(110, 500), width=150, height=150)
            dpg.add_text(default_value="所任课程：", pos=(270, 350))
            ad_tea_course = dpg.add_input_text(pos=(360, 350), width=150, height=150)
            dpg.add_text(default_value="职称：", pos=(300, 400))
            ad_tea_title = dpg.add_input_text(pos=(360, 400), width=150, height=150)
            dpg.add_text(default_value="学院：", pos=(300, 450))
            ad_tea_faculty = dpg.add_input_text(pos=(360, 450), width=150, height=150)
            info_dict={'教师编号':ad_tea_id,'密码':ad_tea_pass,
                    '姓名':ad_tea_name,'性别':ad_tea_sex,
                    '所任课程':ad_tea_course,'职称':ad_tea_title,'学院':ad_tea_faculty}
            dpg.add_button(label='录入', pos=(550, 380), width=150, height=35, callback=ad_tea_enter,
                           user_data=info_dict, tag='ad_s_enter')
            dpg.add_button(label='删除(请输入教师编号)', pos=(750, 380), width=200, height=35, callback=ad_tea_delete,
                           user_data=info_dict, tag='ad_s_delete')
            dpg.add_button(label="查询(请输入教师编号)", pos=(650, 450), width=200, height=35, callback=ad_tea_check,
                           user_data=info_dict, tag='ad_s_check')
            dpg.add_button(label="修改(请输入教师编号)", pos=(650, 490), width=170, height=35, callback=ad_stu_alter,
                           user_data=info_dict, tag='ad_s_alter')

    elif sender == 'ad_cour':
        colum_name = ['课程编号', '课程', '课时', '教师编号', '教师', '实验', '实验室']
        sql = "select * from cour_info"
        cursor.execute(sql)
        colum_list = cursor.fetchall()
        dpg.add_child_window(parent='Administrator', pos=(10, 100), tag='ad_table_win', height=200)
        with dpg.table(header_row=True,
                       parent='ad_table_win',
                       row_background=True,
                       borders_innerH=True,
                       borders_innerV=True, borders_outerV=True, borders_outerH=True, tag='ad_table'):
            for i in colum_name:
                dpg.add_table_column(label=i)

            for i in colum_list:
                with dpg.table_row():
                    for j in i:
                        dpg.add_text(f"{j}")
        with dpg.group(parent='Administrator', tag='ad_components'):
            dpg.add_text(default_value="课程编号：", pos=(20, 350))
            ad_cour_id = dpg.add_input_text(pos=(110, 350), width=150, height=150)
            dpg.add_text(default_value="课程：", pos=(50, 400))
            ad_cour_name = dpg.add_input_text(pos=(110, 400), width=150, height=150)
            dpg.add_text(default_value="课时：", pos=(50, 450))
            ad_cour_time = dpg.add_input_text(pos=(110, 450), width=150, height=150)
            dpg.add_text(default_value="教师编号：", pos=(50, 500))
            ad_tea_sex = dpg.add_input_text(pos=(110, 500), width=150, height=150)
            dpg.add_text(default_value="教师：", pos=(270, 350))
            ad_cour_tea_name = dpg.add_input_text(pos=(360, 350), width=150, height=150)
            dpg.add_text(default_value="实验：", pos=(300, 400))
            ad_cour_task = dpg.add_input_text(pos=(360, 400), width=150, height=150)
            dpg.add_text(default_value="实验室：", pos=(300, 450))
            ad_cour_lab = dpg.add_input_text(pos=(360, 450), width=150, height=150)
            info_dict = {'课程编号': ad_cour_id, '课程': ad_cour_name,
                         '课时': ad_cour_time, '教师编号': ad_tea_sex,
                         '教师': ad_cour_tea_name, '实验': ad_cour_task, '实验室':ad_cour_lab}
            dpg.add_button(label='录入', pos=(550, 380), width=150, height=35, callback=ad_tea_enter,
                           user_data=info_dict, tag='ad_s_enter')
            dpg.add_button(label='删除(请输入课程编号)', pos=(750, 380), width=200, height=35, callback=ad_tea_delete,
                           user_data=info_dict, tag='ad_s_delete')
            dpg.add_button(label="查询(请输入课程编号)", pos=(650, 450), width=200, height=35, callback=ad_tea_check,
                           user_data=info_dict, tag='ad_s_check')
            dpg.add_button(label="修改(请输入课程编号)", pos=(650, 490), width=170, height=35, callback=ad_stu_alter,
                           user_data=info_dict, tag='ad_s_alter')

def stu_select_course(sender, app_data, user_data):
    student_id = user_data[0][0]
    student_course_id = dpg.get_value(user_data[0][1])
    sql1 = "select c_num, c_name, t_id, t_name from cour_info where c_num = '%s' "%(student_course_id)
    cursor.execute(sql1)
    data1 = cursor.fetchall()[0]
    sql2 = "select id, name from s_user where id = '%s' "%(student_id)
    cursor.execute(sql2)
    data2 = cursor.fetchall()[0]
    data = data1+data2
    sql3 = "insert into cour_ele_info values ('%s','%s','%s','%s','%s','%s')  "%(data)
    print(sql3)
    cursor.execute(sql3)


def stu_mange(sender,app_data,user_data):
    dpg.delete_item('stu_table')
    dpg.delete_item('stu_table_win')
    dpg.delete_item('stu_table_group')
    if sender == 'stu_persons_info':
        sql = "select * from s_user where id = '%s' " % (user_data)
        cursor.execute(sql)
        colum_list = cursor.fetchall()[0]
        colum_name = ['学号', '密码', '姓名', '班级', '性别', '学院', '生日']
        text_pos_x = 320
        text_pos_y = 120
        text_pos_x1 = 370
        text_pos_y1 = 120
        with dpg.group(parent='Student', tag='stu_table'):
            for  i in colum_name:
                dpg.add_text(default_value=i+':', pos=(text_pos_x, text_pos_y))
                text_pos_y += 50
            for ii in colum_list:
                dpg.add_text(default_value=ii, pos=(text_pos_x1, text_pos_y1))
                text_pos_y1 += 50


    elif sender == 'stu_course':
        colum_name = ['课程编号', '课程', '课时', '教师编号', '教师', '实验', '实验室']
        sql = "select * from cour_info"
        cursor.execute(sql)
        colum_list = cursor.fetchall()
        dpg.add_child_window(parent='Student', pos=(10, 100), tag='stu_table_win', height=200)
        with dpg.table(header_row=True,
                       parent='stu_table_win',
                       row_background=True,
                       borders_innerH=True,
                       borders_innerV=True, borders_outerV=True, borders_outerH=True, tag='stu_table'):
            for i in colum_name:
                dpg.add_table_column(label=i)

            for i in colum_list:
                with dpg.table_row():
                    for j in i:
                        dpg.add_text(f"{j}")

        with dpg.group(parent='Student', tag='stu_table_group'):
            stu_cour_id = dpg.add_input_text(hint= '请输入课程编号',pos=(110, 350), width=150, height=150)
            student_info = [user_data, stu_cour_id]
            dpg.add_button(label='选课', pos=(550, 380), width=150, height=35,
                           callback=stu_select_course,tag='ad_s_enter',user_data=[student_info])

    elif sender == "stu_cour_success":
        colum_name = ['课程编号', '课程',  '教师编号', '教师']
        sql = "select c_id, c_course, t_id, t_name from cour_ele_info where s_id = '%s' "%(user_data)
        print(sql)
        cursor.execute(sql)
        colum_list = cursor.fetchall()
        print(colum_list)
        dpg.add_child_window(parent='Student', pos=(10, 100), tag='stu_table_win', height=200)
        with dpg.table(header_row=True,
                       parent='stu_table_win',
                       row_background=True,
                       borders_innerH=True,
                       borders_innerV=True, borders_outerV=True, borders_outerH=True, tag='stu_table'):
            for i in colum_name:
                dpg.add_table_column(label=i)

            for i in colum_list:
                with dpg.table_row():
                    for j in i:
                        dpg.add_text(f"{j}")


def back(sender, app_data):
    dpg.delete_item()


def my_test(sender, app_data):
    log_in = dpg.get_value(login)
    pass_word = dpg.get_value(password)
    sql = "select * from login"
    cursor.execute(sql)
    data = cursor.fetchall()
    account_num = []
    for i in data:
        account_num.append(i[0])
    for identity in account_num:
        if log_in == 'root':
            if log_in == identity:
                sql = ("select user_password from login where user_id = '%s' " %(log_in))
                cursor.execute(sql)
                pass_num = cursor.fetchone()[0]
                if pass_word == pass_num:
                    dpg.add_child_window(label="Administrator", tag='Administrator', parent="main_window")
                    dpg.add_button(label="学生信息管理", tag='ad_stu', pos=(100, 50), callback=mange,
                                   parent="Administrator")
                    dpg.add_button(label="教师信息管理", tag='ad_tea', pos=(400, 50), callback=mange,
                                   parent="Administrator")
                    dpg.add_button(label="实验课程信息管理", tag='ad_cour', pos=(700, 50), callback=mange,
                                   parent="Administrator")
                else:
                    with dpg.window(modal=True, label="警告", tag="model_id3", show=True, pos=(400, 200),
                                    no_close=True,no_collapse=True):
                        dpg.add_button(label="密码错误！！", callback=lambda: dpg.delete_item("model_id3"))
                    break



        elif log_in[0] == 's':
            if log_in == identity:
                sql = ("select user_password from login where user_id = '%s' " % (log_in))
                cursor.execute(sql)
                pass_num = cursor.fetchone()[0]
                if pass_word == pass_num:
                    dpg.add_child_window(label="Student", tag='Student', parent="main_window")
                    dpg.add_button(label="个人信息", tag='stu_persons_info', pos=(100, 50), callback=stu_mange,
                                   parent="Student", user_data=log_in)
                    dpg.add_button(label="选课", tag='stu_course', pos=(400, 50), callback=stu_mange,
                                   parent="Student",user_data=log_in)
                    dpg.add_button(label="已选课信息", tag='stu_cour_success', pos=(700, 50), callback=stu_mange,
                                   parent="Student",user_data=log_in)
                else:
                    with dpg.window(modal=True, label="警告", tag="model_id3", show=True, pos=(400, 200),
                                    no_close=True, no_collapse=True):
                        dpg.add_button(label="密码错误！！", callback=lambda: dpg.delete_item("model_id3"))
                    break

        elif log_in[0] == 't':
            if log_in == identity:
                with dpg.window(label="Teacher", tag="Teacher",modal=True,):
                    print("老师进来了")
                break

        else:
            print("good")
            with dpg.window(modal=True,label="警告", tag="model_id1",show=True,pos=(400,200),
                            no_close=True,no_collapse=True):
                dpg.add_button(label="账号或密码错误！！", callback=lambda : dpg.delete_item("model_id1"))
            break


def win_exit(sender, app_data):
    dpg.destroy_context()


if __name__ == "__main__":
    # 创建上下文
    dpg.create_context()
    mysql = mysql()
    cursor, conn = mysql.set_mysql()
    font1 = Font.set_chinese_font("Deng.ttf", 20)
    # 创建上下文
    with dpg.window(label="demo", tag="main_window", show=True):
        dpg.add_text(default_value="实验选课系统", pos=(448, 120),tag='test')
        dpg.add_text(default_value="账号：", pos=(300, 200))
        login = dpg.add_input_text(pos=(360, 200), width=300, height=150)
        dpg.add_text(default_value="密码：", pos=(300, 250))
        password = dpg.add_input_text(pos=(360, 250), width=300, height=150, password=True)
        dpg.add_button(label="登录", pos=(400, 350), callback=my_test)
        dpg.add_button(label="退出", pos=(530, 350), callback=win_exit)

    dpg.create_viewport(title="Experimental course selection system", width=1000, height=600)
    dpg.set_primary_window("main_window", True)
    dpg.setup_dearpygui()
    dpg.bind_font(font1)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
