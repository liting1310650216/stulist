#! /usr/bin/env python3
# -*- coding:UTF-8 -*-

from dbconn import db_cursor

def create_db():
    sqlstr = """
    DROP TABLE IF EXISTS course;

    CREATE TABLE IF NOT EXISTS course  (
        cou_sn   INTEGER,     --学生序号
        cou_no   TEXT,        --学生班级
        name     TEXT,        --学生姓名
        sex      TEXT,        --学生性别
        bir      TEXT,        --出生日期
        num      TEXT,        --学号
        notes    TEXT,
        PRIMARY KEY(cou_sn)
    );
    -- CREATE UNIQUE INDEX idx_course_no ON course(cou_no)创建唯一索引;

    CREATE SEQUENCE seq_cou_sn 
        START 10000 INCREMENT 1 OWNED BY course.cou_sn;

    """
    with db_cursor() as cur :
        cur.execute(sqlstr) # 执行SQL语句
    
def init_data():
    sqlstr = """
    DELETE FROM course;

    INSERT INTO course (cou_sn, cou_no, name,sex,bir ,num)  VALUES 
        (100, '信息二班',  '丁荣昌','男','1993.12.08','1310650205'), 
        (101, '信息一班',  '黄雅琪','女','1653.05.06','1310650215'),
        (102, '信息四班',  '裤衩','男','1996.05.25','1310650406');

    """
    with db_cursor() as cur :
        cur.execute(sqlstr)    

if __name__ == '__main__':
    create_db()
    init_data()
    print('数据库已初始化完毕！')

