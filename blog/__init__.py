#!/usr/bin/python3
from sqlalchemy.engine import create_engine
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.core import handler
import re
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table
from sqlalchemy import Integer, String
from sqlalchemy.sql import select
from sqlalchemy.sql import and_
from sqlalchemy.sql import or_
class MyAppBaseController(CementBaseController):

    class Meta:
        label = 'base'

class AbstractBaseController(CementBaseController):

    class Meta:
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
            ( ['-f', '--foo'], dict(help='notorious foo option')),
            ]

    def _setup(self, base_app):
        super(AbstractBaseController, self)._setup(base_app)
        self.engine = create_engine('sqlite:///tutorial.db',echo=False)
        metadata = MetaData(bind=self.engine)
        self.category_table = Table('category', metadata,
                    Column('name', String(40)),
                    Column('cat_id', Integer, primary_key=True),
                    )
        self.post_table = Table('post', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('post_title', String(40)),
                    Column('post_content',String(40))
                    )
        self.post_category_table = Table('post_category', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('cat_id', Integer, primary_key=True),
                    )
        
        # create tables in database
        metadata.create_all()

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
     
        print("post_content : %s" % self.app.pargs.extra_arguments[0])
        print("post_title: %s" % self.app.pargs.extra_arguments[1])  
        ins = self.post_table.insert()
        result = self.engine.execute(ins, post_title=self.app.pargs.extra_arguments[0],post_content=self.app.pargs.extra_arguments[1])
        s = select([self.post_table])
        print("Post Added")
        if self.app.pargs.usercat:
           conn = self.engine.connect()
           cat_id= select([self.category_table],self.category_table.c.cat_id==self.app.pargs.usercat)
           # Cat is not present in DB
           if cat_id==None:
              ins = self.category_table.insert()
              result = self.engine.execute(ins, name=self.app.pargs.usercat)
              ins = self.post_category_table.insert()
              
              result = self.engine.execute(ins, id=self.app.pargs.extra_arguments[1],cat_id=self.app.pargs.extra_arguments[0])   
           print("Catogry assigned to post")

    @expose()
    def search(self):
        print("String : %s" % self.app.pargs.extra_arguments[0])
        data = select([self.post_table],or_(self.post_table.c.post_title==self.app.pargs.extra_arguments[0], self.post_table.c.post_content==self.app.pargs.extra_arguments[0]))
        result = data.execute()
        for row in result:
          print(row)
    

    @expose()
    def list(self):
        s = select([self.post_table])
        result = s.execute()
        for row in result:
          print(row)
    
        

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
       
       print("name : %s" % self.app.pargs.extra_arguments[0])
       ins = self.category_table.insert()
       result = self.engine.execute(ins, name=self.app.pargs.extra_arguments[0])
       
       

    @expose()
    def list(self):
        s = select([self.category_table])
        result = s.execute()
        for row in result:
          print(row)
    

    @expose()
    def assign(self):
       
        data= select([self.category_table],self.category_table.c.cat_id==self.app.pargs.extra_arguments[0])
        print("Catogry is  assigned to post")            
       
        if data==None:
           print("Catogary not exist")
           data= select([self.post_table],self.post_table.c.id==self.app.pargs.extra_arguments[1])
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
