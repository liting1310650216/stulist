# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

from dbconn import db_cursor

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/main.html")

class CourseDingHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/cou_listq.html",courses = dal_ding_courses())
#等待修正
        
class CourseListHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pages/cou_list.html", courses = dal_list_courses())

class CourseEditHandler(tornado.web.RequestHandler):
    def get(self, cou_sn):

        cou = None
        if cou_sn != 'new' :
            cou = dal_get_course(cou_sn)
        
        if cou is None:
            cou = dict(cou_sn='new', cou_no='', name='', sex='',bir='',num='',notes='')

        self.render("pages/cou_edit.html", course = cou)

    def post(self, cou_sn):
        cou_no = self.get_argument('cou_no')
        name = self.get_argument('name', '')
        sex = self.get_argument('sex', '')
        bir = self.get_argument('bir', '')
        num = self.get_argument('num', '')
        notes = self.get_argument('notes', '')

        if cou_sn == 'new' :
            dal_create_course(cou_no, name,sex,bir,num, notes)
        else:
            dal_update_course(cou_sn, cou_no, name,sex,bir,num, notes)

        self.redirect('/coulist')

class CourseDelHandler(tornado.web.RequestHandler):
    def get(self, cou_sn):
        dal_del_course(cou_sn)
        self.redirect('/coulist')

# -------------------------------------------------------------------------

def dal_list_courses():
    data = []
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT cou_sn, cou_no, name,sex,bir,num, notes FROM course ORDER BY cou_sn DESC
        """
        cur.execute(s)      
        for r in cur.fetchall():
            cou = dict(cou_sn=r[0], cou_no=r[1], name=r[2],sex=r[3],bir=r[4], num=r[5],notes=r[6])
            data.append(cou)
    return data
#以下
def dal_ding_courses():
    data = []
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
#        s1="""SELECT cou_no FROM course ORDER BY cou_sn DESC"""
#        cur.execute(s1)
#        s = """
#        SELECT cou_sn, cou_no, name,sex,bir,num, notes FROM course ORDER BY cou_sn DESC
#        """
        ss="""SELECT cou_sn, cou_no, name,sex,bir,num, notes FROM course ORDER BY cou_no """
        cur.execute(ss)      
        for r in cur.fetchall():
            cou = dict(cou_sn=r[0], cou_no=r[1], name=r[2],sex=r[3],bir=r[4], num=r[5],notes=r[6])
            data.append(cou)
     #   cur.execute(s)
     #   for r in cur.fetchall():
     #       if (r[1]=="信息一班" or r[1]=="信息1班"):
     #           cou = dict(cou_sn=r[0], cou_no=r[1], name=r[2],sex=r[3],bir=r[4],num=r[5],notes=r[6])
        #        data.append(cou)
     #   cur.execute(s)        
     #   for r in cur.fetchall():
     #       if (r[1]=="信息二班" or r[1]=="信息2班"):
     #           cou = dict(cou_sn=r[0], cou_no=r[1], name=r[2],sex=r[3],bir=r[4], num=r[5],notes=r[6])
     #           data.append(cou)
     #   cur.execute(s)        
     #   for r in cur.fetchall():
     #       if (r[1]=="信息三班"or r[1]=="信息3班"):
     #           cou = dict(cou_sn=r[0], cou_no=r[1], name=r[2],sex=r[3],bir=r[4],num=r[5],notes=r[6])
     #           data.append(cou)
     #   cur.execute(s)        
     #   for r in cur.fetchall():
     #       if (r[1]=="信息四班"or r[1]=="信息4班"):
     #           cou = dict(cou_sn=r[0], cou_no=r[1], name=r[2],sex=r[3],bir=r[4],num=r[5],notes=r[6])
     #           data.append(cou)                
#    #    t=cur.rowcount()
#    #    for i in range(0,t):
#            r[i]=cur.fetchone()
#            data.append(r[i])        
#        if (cou_sn=="信息一班"or"信息1班"):
 #           cou = dict(cou_sn=r[0], cou_no=r[1], name=r[2],sex=r[3],bir=r[4], notes=r[5])
  #          data.append(cou)
    return data
#以上
def dal_get_course(cou_sn):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        SELECT cou_sn, cou_no, name, sex, bir, num,notes FROM course WHERE cou_sn=%s
        """
        cur.execute(s, (cou_sn, ))
        r = cur.fetchone()
        if r :
            return dict(cou_sn=r[0], cou_no=r[1], name=r[2],sex=r[3],bir=r[4], num=r[5],notes=r[6])


def dal_create_course(cou_no, name, sex,bir,num,notes):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        cur.execute("SELECT nextval('seq_cou_sn')")
        cou_sn = cur.fetchone()
        assert cou_sn is not None

        print('新学生内部序号%d: ' % cou_sn)

        s = """
        INSERT INTO course (cou_sn, cou_no, name,sex,bir, num, notes) 
        VALUES (%(cou_sn)s, %(cou_no)s, %(name)s, %(sex)s,%(bir)s,%(num)s, %(notes)s)
        """
        cur.execute(s, dict(cou_sn=cou_sn, cou_no=cou_no, name=name, sex=sex, bir=bir,num=num, notes=notes))


def dal_update_course(cou_sn, cou_no, name, sex, bir,num, notes):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        UPDATE course SET
          cou_no=%(cou_no)s, 
          name=%(name)s,
          sex=%(sex)s,
          bir=%(bir)s,
          num=%(num)s,
          notes=%(notes)s 
        WHERE cou_sn=%(cou_sn)s
        """
        cur.execute(s, dict(cou_sn=cou_sn, cou_no=cou_no, name=name, sex=sex, bir=bir ,num=num, notes=notes))


def dal_del_course(cou_sn):
    with db_cursor() as cur : # 取得操作数据的游标，记为cur
        s = """
        DELETE FROM course WHERE cou_sn=%(cou_sn)s
        """
        cur.execute(s, dict(cou_sn=cou_sn))
        print('删除%d条记录' % cur.rowcount)


