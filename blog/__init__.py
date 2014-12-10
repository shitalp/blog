#!/usr/bin/python3
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.core import handler
import pymysql
import re

class AbstractBaseController(CementBaseController):

    class Meta:
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
            ( ['-f', '--foo'], dict(help='notorious foo option')),
            ]

    def _setup(self, base_app):
        super(AbstractBaseController, self)._setup(base_app)
        try:
        # add a common object that will be used in any sub-class
           with open("/etc/blog/blog.cfg")as file:
            text=file.read()
            mapping=re.findall(r'DB_USER.*',text)
            user=mapping[0].split('\'')[2]
            mapping=re.findall(r'DB_HOST.*',text)
            host=mapping[0].split('\'')[2]
            mapping=re.findall(r'DB_PASSWORD.*',text)
            password=mapping[0].split('\'')[2]
            mapping=re.findall(r'DB_NAME.*',text)
            db=mapping[0].split('\'')[2]
            self.db=pymysql.connect(host,user,password,db)
            cursor=self.db.cursor()
            cursor.execute("create table if not exists post(id int,post_title varchar(500),post_content varchar(500),primary key(id))")
            cursor.execute("create table if not exists category(name varchar(500),cat_id int,primary key(cat_id))")
            cursor.execute("create table if not exists post_category(id int,cat_id int)")
        except:
          print("cant connect to datbase ..check your conncetion")
        
          self.cursor = dict()


class MyAppBaseController(CementBaseController):

    class Meta:
        label = 'base'
class Controller1(AbstractBaseController):
    class Meta:
        label = 'post'
        stacked_type = 'nested'
        stacked_on = 'base'
        description = 'this is the second controller namespace'
        arguments = [
            (['-C', '--category'],
             dict(help='the notorious foo option', action='store', dest='usercat')),
            (['extra_arguments'],
             dict(action='store', nargs='*')),
        ]

    @expose()
    def add(self):
     try:
        print("post_content : %s" % self.app.pargs.extra_arguments[0])
        print("post_title: %s" % self.app.pargs.extra_arguments[1])    
        cursor=self.db.cursor()
        cursor.execute("select max(id)+1 from post")
        id=cursor.fetchone()
        cursor.execute('''insert into post(id,post_content,post_title)values(%s,%s,%s)''',(id,self.app.pargs.extra_arguments[0],self.app.pargs.extra_arguments[1]))
        cursor=self.db.cursor()
        cursor.execute("select id,post_title,post_content from post")
        print("Post Added")
        if self.app.pargs.usercat:
            cursor=self.db.cursor()
            cursor.execute("select cat_id from category where name=%s",self.app.pargs.usercat)
            cat_id=cursor.fetchone()
            # Cat is not present in DB
            if cat_id==None:
                cursor.execute("select max(cat_id)+1 from category")
                cat_id=cursor.fetchone()
                cursor=self.db.cursor()
                cursor.execute('''insert into category(name,cat_id)values(%s,%s)''',(self.app.pargs.usercat,cat_id))
                cursor.execute("insert into post_category(id,cat_id)values(%s,%s)",(id,cat_id));

            print("Catogry assigned to post")
     except:
            cursor.execute('''insert into post(id,post_content,post_title)values(%s,%s,%s)''',(1,self.app.pargs.extra_arguments[0],self.app.pargs.extra_arguments[1]))
            self.db.commit()
            self.db.close()

    @expose()
    def search(self):
        print("String : %s" % self.app.pargs.extra_arguments[0])
        cursor=self.db.cursor()
        cursor.execute("select id,post_title,post_content from post where post_title=%s OR post_content=%s ",(self.app.pargs.extra_arguments[0],self.app.pargs.extra_arguments[0]))
        print(cursor.fetchall())
        self.db.close()

    @expose()
    def list(self):
        cursor=self.db.cursor()
        cursor.execute("select id,post_title,post_content from post")
        print(cursor.fetchall())
        self.db.close()

class Controller2(AbstractBaseController):
    class Meta:
        label = 'category'
        stacked_type = 'nested'
        stacked_on = 'base'

        description = 'this is the second controller namespace'
        arguments = [
            (['-f', '--foo'],
             dict(help='the notorious foo option', action='store')),
            (['extra_arguments'],
             dict(action='store', nargs='*')),
        ]


    @expose()
    def add(self):

     try:      

        cursor=self.db.cursor()
        cursor.execute("select max(cat_id)+1 from category")
        cat_id=cursor.fetchone()
        print("name: %s" % self.app.pargs.extra_arguments[0])
        cursor=self.db.cursor()
        cursor.execute('''insert into category(name,cat_id)values(%s,%s)''',(self.app.pargs.extra_arguments[0],cat_id))
    
     except:
        cursor.execute('''insert into category(name,cat_id)values(%s,%s)''',(self.app.pargs.extra_arguments[0],1))
        
     self.db.commit();
     self.db.close()



    @expose()
    def list(self):
        cursor=self.db.cursor()
        cursor.execute("select name,cat_id from category")
        print(cursor.fetchall())
        self.db.close()

    def assign(self):
        cursor=self.db.cursor()
        cursor.execute("select cat_id from category where cat_id=%s",self.app.pargs.extra_arguments[0])
        data=cursor.fetchone()
        if data==None:
            print("Catogary not exist")
        else:
            cursor.execute("select id from post where id=%s",self.app.pargs.extra_arguments[1])
            data=cursor.fetchone()
            if data==None:
                print("Post not exist")
            else:
                # You need to create third table
                cursor.execute("select id,cat_id from post_catagory where id=%s and cat_id=%s",(self.app.pargs.extra_arguments[1],self.app.pargs.extra_arguments[0]))
                data=cursor.fetchone()
                if data==None:
                    cursor.execute("insert into post_catagory(id,cat_id)values(%s,%s)",(self.app.pargs.extra_arguments[1],self.app.pargs.extra_arguments[0]));
                    print("Catogry assigned to post")
                else:
                    print("Catogry is allready assigned to post")



def main():
    app = CementApp('blog')

    # register controllers handlers
    handler.register(MyAppBaseController)
    handler.register(Controller1)
    handler.register(Controller2)

    app.setup()
    app.run()

    app.close()

if __name__ == '__main__':
    main()
