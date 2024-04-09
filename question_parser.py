#问题解析器
import sqlite3
from question_classifier import *

class Questionparser:
    def __init__(self):
        pass
    
    def parser_main(self,res_classify):
        args=res_classify['args']
        #实体字典
        entity_dict={}
        for arg,types in args.items():
            for type in types:
                if type not in entity_dict:
                    #新增:用列表存储arg,防止有多个实体的问题: {'Plant': ['三七'], 'Session': ['春季'], 'Light': ['中光']}
                    entity_dict[type]=[arg]
                else:
                    entity_dict[type].append(arg)
        
        question_types=res_classify['question_types']
        
        #新增: 对于多个问题,保存问题的序列
        sqls=[]
        #一次处理一个问题
        for question_type in question_types:
            sql_get={}

            sql_get['question_type']=question_type
            

            sql=self.get_sql(question_type,entity_dict)

            if sql:
                sql_get['sql']=sql
                sqls.append(sql_get)
        
        #可以是多个问题,所以可以有多个sql查询语句
        return sqls
            
    

    def get_sql(self,question_type,entity_dict):
        sql=[]
        #flag=1表示使用了别名,要多一步处理
        flag=0
        #未使用别名
        if not entity_dict.get('Different_name'):
            #询问物种的别名
            if question_type=='plant_diff_name':
                sql=self.sql_transfer(question_type,entity_dict.get('Plant'),flag)
            
            #可能使用了别名对使用了别名的进行单独处理
            #询问物种的颜色
            elif question_type=='plant_color':
                sql=self.sql_transfer(question_type,entity_dict.get('Plant'),flag)

            #询问物种的类型
            elif question_type=='plant_category':
                sql = self.sql_transfer(question_type, entity_dict.get('Plant'),flag)
            
            #询问物种的味道
            elif question_type=='plant_taste':
                sql = self.sql_transfer(question_type, entity_dict.get('Plant'),flag)

            #询问物种的外形
            elif question_type=='plant_shape':
                sql = self.sql_transfer(question_type, entity_dict.get('Plant'),flag)

            #询问物种的光照需求
            elif question_type=='plant_light':
                sql = self.sql_transfer(question_type, entity_dict.get('Plant'),flag)
            
            #询问物种的开花时间
            elif question_type=='plant_session':
                sql = self.sql_transfer(question_type, entity_dict.get('Plant'),flag)
            
            #询问物种的培育难度
            elif question_type=='plant_level':
                sql = self.sql_transfer(question_type, entity_dict.get('Plant'),flag)
            
            #询问物种的培育温度
            elif question_type=='plant_temperature':
                sql = self.sql_transfer(question_type, entity_dict.get('Plant'),flag)
            
            #询问物种的酸碱范围
            elif question_type=='plant_ph':
                sql = self.sql_transfer(question_type, entity_dict.get('Plant'),flag)
            
            #介绍作物
            elif question_type=='plant_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('Plant'),flag)
            
            #询问作物种植方法
            elif question_type=='plant_cultivation_method':
                sql=self.sql_transfer(question_type, entity_dict.get('Plant'),flag)
            
            #询问作物繁殖方式
            elif question_type=='plant_reproduction':
                sql=self.sql_transfer(question_type, entity_dict.get('Plant'),flag)

        #使用了别名
        else:
            flag=1
            #询问物种的别名
            if question_type=='plant_diff_name':
                sql=self.sql_transfer(question_type,entity_dict.get('Different_name'),flag)

            #询问物种的颜色
            elif question_type=='plant_color':
                sql=self.sql_transfer(question_type,entity_dict.get('Different_name'),flag)

            #询问物种的类型
            elif question_type=='plant_category':
                sql = self.sql_transfer(question_type, entity_dict.get('Different_name'),flag)
            
            #询问物种的味道
            elif question_type=='plant_taste':
                sql = self.sql_transfer(question_type, entity_dict.get('Different_name'),flag)

            #询问物种的外形
            elif question_type=='plant_shape':
                sql = self.sql_transfer(question_type, entity_dict.get('Different_name'),flag)

            #询问物种的光照需求
            elif question_type=='plant_light':
                sql = self.sql_transfer(question_type, entity_dict.get('Different_name'),flag)
            
            #询问物种的开花时间
            elif question_type=='plant_session':
                sql = self.sql_transfer(question_type, entity_dict.get('Different_name'),flag)
            
            #询问物种的培育难度
            elif question_type=='plant_level':
                sql = self.sql_transfer(question_type, entity_dict.get('Different_name'),flag)
            
            #询问物种的培育温度
            elif question_type=='plant_temperature':
                sql = self.sql_transfer(question_type, entity_dict.get('Different_name'),flag)
            
            #询问物种的酸碱范围
            elif question_type=='plant_ph':
                sql = self.sql_transfer(question_type, entity_dict.get('Different_name'),flag)
            
            #介绍作物
            elif question_type=='plant_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('Different_name'),flag)
            
            #询问作物种植方法
            elif question_type=='plant_cultivation_method':
                sql=self.sql_transfer(question_type, entity_dict.get('Different_name'),flag)
            
            #询问作物繁殖方式
            elif question_type=='plant_reproduction':
                sql=self.sql_transfer(question_type, entity_dict.get('Different_name'),flag)

        return sql

    #对问题分别进行处理
    def sql_transfer(self,question_type,entities,flag):
        if not entities:
            return []
        
        #设定查询语句
        sql=[]
        #entities = ['三七']
        #未使用别名
        if flag==0:
            #询问作物的别称
            if question_type=='plant_diff_name':
                sql=["MATCH (n:Plant) where n.name='{0}'  MATCH (n)-[:other_name]->(m:Different_name) RETURN n.name,m.name".format(i) for i in entities] #多个实体一个问题用for处理
            
            #询问物种的颜色
            elif question_type=='plant_color':
                sql=["MATCH (n:Plant) where n.name='{0}'  MATCH (n)-[:color]->(m:Color) RETURN n.name,m.name".format(i) for i in entities]

            #询问物种的类型
            elif question_type=='plant_category':
                sql=["MATCH (n:Plant) where n.name='{0}'  MATCH (n)-[:category]->(m:Category) RETURN n.name,m.name".format(i) for i in entities]

            #询问物种的味道
            elif question_type=='plant_taste':
                sql=["MATCH (n:Plant) where n.name='{0}'  MATCH (n)-[:taste]->(m:Taste) RETURN n.name,m.name".format(i) for i in entities]

            #询问物种的外形
            elif question_type=='plant_shape':
                sql=["MATCH (n:Plant) where n.name='{0}'  MATCH (n)-[:shape]->(m:Shape) RETURN n.name,n.feature,m.name".format(i) for i in entities]

            #询问物种的光照需求
            elif question_type=='plant_light':
                sql=["MATCH (n:Plant) where n.name='{0}'  MATCH (n)-[:light_requirement]->(m:Light) RETURN n.name,m.name".format(i) for i in entities]
            
            #询问物种的开花时间
            elif question_type=='plant_session':
                sql=["MATCH (n:Plant) where n.name='{0}'  MATCH (n)-[:flower_session]->(m:Session) RETURN n.name,n.flowering_form,m.name".format(i) for i in entities]
            
            #询问物种的培育难度
            elif question_type=='plant_level':
                sql=["MATCH (n:Plant) where n.name='{0}'  MATCH (n)-[:level]->(m:Level) RETURN n.name,m.name".format(i) for i in entities]
            
            #询问物种的培育温度
            elif question_type=='plant_temperature':
                sql=["MATCH (n:Plant) where n.name='{0}'  MATCH (n)-[:need_temperature]->(m:Temperature) RETURN n.name,m.name".format(i) for i in entities]
            
            #询问物种的酸碱范围
            elif question_type=='plant_ph':
                sql=["MATCH (n:Plant) where n.name='{0}'  MATCH (n)-[:need_ph]->(m:Ph) RETURN n.name,m.name".format(i) for i in entities]
            
            #介绍作物
            elif question_type=='plant_desc':
                sql=["MATCH (n:Plant) where n.name='{0}' return n.name,n.desc".format(i) for i in entities]
            
            #询问作物种植方法
            elif question_type=='plant_cultivation_method':
                sql=["MATCH (n:Plant) where n.name='{0}' return n.name,n.cultivation_method".format(i) for i in entities]
            
            #询问作物繁殖方式
            elif question_type=='plant_reproduction':
                sql=["MATCH (n:Plant) where n.name='{0}' return n.name,n.reproduction".format(i) for i in entities]
        
        #使用了别名
        else:
            #先找出别名对应的实体(Plant)(默认是一个别名就偷懒没写)
            #会存在一个别名对应多个作物的情况
            sql_find_plant=["MATCH (t:Different_name) where t.name='{0}'  MATCH (t)<-[:other_name]-(n:Plant)".format(i) for i in entities]


            #询问作物的别称
            if question_type=='plant_diff_name':
                sql_1=["MATCH (n)-[:other_name]->(m:Different_name)  RETURN t.name,n.name,m.name"] #多个实体一个问题用for处理
            
            #询问物种的颜色
            elif question_type=='plant_color':
                sql_1=["MATCH (n)-[:color]->(m:Color)   RETURN t.name,n.name,m.name"]

            #询问物种的类型
            elif question_type=='plant_category':
                sql_1=["MATCH (n)-[:category]->(m:Category)  RETURN t.name,n.name,m.name"]
            #询问物种的味道
            elif question_type=='plant_taste':
                sql_1=["MATCH (n)-[:taste]->(m:Taste)  RETURN t.name,n.name,m.name"]

            #询问物种的外形
            elif question_type=='plant_shape':
                sql_1=["MATCH (n)-[:shape]->(m:Shape) RETURN t.name,n.name,n.feature,m.name"]

            #询问物种的光照需求
            elif question_type=='plant_light':
                sql_1=["MATCH (n)-[:light_requirement]->(m:Light) RETURN t.name,n.name,m.name"]
            
            #询问物种的开花时间
            elif question_type=='plant_session':
                sql_1=["MATCH (n)-[:flower_session]->(m:Session) RETURN t.name,n.name,n.flowering_form,m.name"]
            
            #询问物种的培育难度
            elif question_type=='plant_level':
                sql_1=["MATCH (n)-[:level]->(m:Level) RETURN t.name,n.name,m.name"]
            
            #询问物种的培育温度
            elif question_type=='plant_temperature':
                sql_1=["MATCH (n)-[:need_temperature]->(m:Temperature) RETURN t.name,n.name,m.name"]
            
            #询问物种的酸碱范围
            elif question_type=='plant_ph':
                sql_1=["MATCH (n)-[:need_ph]->(m:Ph) RETURN t.name,n.name,m.name"]
            
            #介绍作物
            elif question_type=='plant_desc':
                sql_1=["return t.name,n.name,n.desc"]
            
            #询问作物种植方法
            elif question_type=='plant_cultivation_method':
                sql_1=["return t.name,n.name,n.cultivation_method"]
            
            #询问作物繁殖方式
            elif question_type=='plant_reproduction':
                sql_1=["return t.name,n.name,n.reproduction"]
            
            
            #对查询语句进行拼接
            sql= [sql_find_plant[0] +' '+ sql_1[0]]
            # print(sql_find_plant)
            # print(sql_1)
            # print(sql)
        
        return sql
        
if __name__=='__main__':
    b=Questionparser()
    a=Questionclassifier()
    while(1):
        question=input("问题: ")
        res_classify=a.classify(question)
        # res_classify={'args': {'三七': ['Plant'], '春季': ['Session'], '中光': ['Light']}, 'question_types': ['plant_level', 'plant_ph']}
        # res_classify={'args': {'鸡矢果': ['Different_name']}, 'question_types': ['plant_color']}
        # res_classify={'args': {'鸡矢果': ['Different_name']}, 'question_types': ['plant_diff_name']}
        # res_classify={'args': {'鸡矢果': ['Different_name']}, 'question_types': ['plant_ph']}
        sql=b.parser_main(res_classify)
        print(sql)

            

        


