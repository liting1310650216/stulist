# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

from dbconn import db_cursor

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/main.html")


class CourseListHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/cou_list.html", courses = dal_list_courses())
                                          #从下面知，将每个数据添加到cou_list上

def dal_list_courses():#将每一个学生数据赋值给date
    data = []
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT cou_sn, cou_no, name, sex, bir, num, notes FROM course ORDER BY cou_sn DESC
        """
        cur.execute(s)      
        for r in cur.fetchall():
            cou = dict(cou_sn=r[0], cou_no=r[1], name=r[2],sex=r[3],bir=[4],num=r[5] )
            data.append(cou)
    print(data)
    return data

