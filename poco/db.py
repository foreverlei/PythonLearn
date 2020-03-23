# -*- coding: UTF-8 -*-

import pymysql

class DB:
    def __init__(self):
        self.db = pymysql.connect(
            host='192.168.206.128',
            port=3306,
            user='pyresource',
            password='yJKBeKmsfYpmxbkj',
            database='pyresource',
            charset='utf8',
            )
        self.cursor = self.db.cursor()
        print(self.cursor.execute("SELECT VERSION()"))


    def insertOnceToTitleList(self,pid,title="",url="",type1="",date=""):
        # SQL 插入语句
        sql = "INSERT INTO py_page_title_list(pid, title, url, type, date)  VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(pid,title,url,type1,date)
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()
    
    def getIfExit(self,pid):
        # SQL 查询语句
        sql = "SELECT * FROM py_page_title_list  WHERE pid = '%s'" % (pid)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchone()
            if results and len(results) > 0:
                return True
                
        except:
            print ("Error: unable to fetch data")
        return False

    #################

    def insertOnceToPageList(self,pid,title,urlself,urldownload,html,date):
        # SQL 插入语句
        sql = """INSERT INTO py_pahe_one_list(pid, title, urlself,urldownload, html, date)  
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')""".format(pid,title,urlself,urldownload,html,date)
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()


if __name__ == "__main__":
    db = DB()
    # db.insertOnceToTitleList("aaapid",'aaatitle','aaaurl','aaatype','aaadate')
    print( db.getIfExit('aaapida'))


