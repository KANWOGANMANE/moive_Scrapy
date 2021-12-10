import pymysql
import re
import pandas as pd

def con_douban():
    try:
        # 创建连接
        con = pymysql.connect(host="localhost", user="root", password="", database="douban",port=3306)
        # 创建游标对象
        cur = con.cursor()
        # 编写创建表的sql
        sql = """
            create table douban_movie(
            title nchar(100) primary key,             
            directors nchar(100) not null,
            scraptwriter nchar(100) not null,
            type nchar(50) not null,
            country nchar(100) not null ,
            language nchar(100) not null,
            date nchar(50) not null,
            flength nchar(100) not null,
            rate nchar(10)
            )
            """
        # 执行创建表的sql
        cur.execute(sql)
        print("Create table successfully")
    except Exception as e:
        print("Mysql Error %d: %s"%(e.args[0],e.args[1]))
    finally:
        cur.close()
        con.close()

def insert_data(data):
    try:
        data_tup = tuple(data.values())
        con = pymysql.connect(host="localhost", user="root", password="", database="douban")
        cur = con.cursor()
        sql = "INSERT INTO douban_movie(title,directors,scraptwriter,type,country,language,date,flength,rate) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        print(data_tup)
        cur.execute(sql, data_tup)
        con.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()


def expore_data():
    try:
        con = pymysql.connect(host="localhost", user="root", password="", database="douban")
        cur = con.cursor()
        sql = '''
        select *
        from douban_movie
        '''
        cur.execute(sql)
        douban_all_data = cur.fetchall()
        name = ['title','directors','scraptwriter','type','country','language','date','flength','rate']
        df = pd.DataFrame(data=douban_all_data,columns=name)
        df.to_csv('douban_movie.csv',encoding='utf_8_sig')
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()









