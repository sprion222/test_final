from py2neo import Graph
from question_classifier import *
from question_parser import *

#基于neo4j图数据库的问题查找器
class Answersearch:
    def __init__(self):
        #使用租用服务器的公网ip进行访问部署到服务器上的neo4j图数据库
        self.g=Graph("http://8.130.77.231:7474/browser/",auth=("neo4j","Cdslqyqxhz31203"),name="neo4j")


    #sqls=[{'question_type': 'plant_level', 'sql': ["MATCH (n:Plant) where n.name='三七'  MATCH (n)-[:level]->(m:Level) RETURN n.name,m.name"]},
    #      {'question_type': 'plant_ph',    'sql': ["MATCH (n:Plant) where n.name='三七'  MATCH (n)-[:need_ph]->(m:Ph) RETURN n.name,m.name"]}]
    def search_main(self,sqls):
        final_answer = []
        #一个问题一个问题进行处理
        for sql in sqls:
            question_type=sql['question_type'] #问题类型
            queries=sql['sql']
            answers=[]
            
            for query in queries:
                res=self.g.run(query).data()
                answers+=res
            #返回为字典的形式 [{'n.name': '三七', 'm.name': '较难'}]
            # print(answers)
            res_answer=self.answer_reply(question_type,answers)

            #多个问题,将回复进行拼接
            if res_answer:
                final_answer.append(res_answer)

        return final_answer
    
    #模板形式回复生成
    def answer_reply(self,question_type,answer):
        final_answer=[]
        if not answer:
            return ''
        #判断是否使用了别名
        
        diff_name_answer=''
        search_answer=''
        # print(answer)
        if 't.name' not in answer[0]:
            #没有使用别名
            pass
        else:
            #使用了别名
            diff_name=answer[0]['t.name']
            plant_name=[]
            #对同组进行筛查切割
            for data in answer:
                plant=data['n.name']
                if plant not in plant_name:
                    plant_name.append(plant)
            
            if len(plant_name)==1:
                diff_name_answer='您使用了一个植物的别名，{0}的学名有{1}。'.format(diff_name,plant_name[0])+"\n"
            else:
                diff_name_answer='您使用了一个植物的别名，{0}的学名有{1}。'.format(diff_name,'、'.join(plant_name))+"\n"

        #可能使用别名查询的时候会出现多个植物
        #询问作物的别称
        if question_type=='plant_diff_name':
            search_plant=[]
            search_diff_name_data=[]
            search_diff_name=''
            #对同组进行切割
            for data in answer:
                plant=data['n.name']
                if plant not in search_plant:

                    if search_diff_name !='':
                        search_diff_name_data.append(search_diff_name)
                    
                    search_diff_name=''
                    search_plant.append(plant)
                
                search_diff_name=search_diff_name + ' ' + data['m.name']

            search_diff_name_data.append(search_diff_name)

            i=0
            #各个作物进行分别处理
            for  plant in search_plant:
                search_answer+= ('{0}的别名有：{1}。'.format(plant, search_diff_name_data[i]))
                i+=1
            
            
        
        #询问物种的颜色
        elif question_type=='plant_color':
            for data in answer:
                search_plant=data['n.name']
                search_res=data['m.name']
                search_answer+=('{0}的颜色是：{1}。'.format(search_plant, search_res))

        #询问物种的类型
        elif question_type=='plant_category':
            for data in answer:
                search_plant=data['n.name']
                search_res=data['m.name']
                search_answer+=('{0}的物种类型是：{1}。'.format(search_plant, search_res))

        #询问物种的味道
        elif question_type=='plant_taste':
            for data in answer:
                search_plant=data['n.name']
                search_res=data['m.name']
                search_answer+=('{0}的味道总体上是{1}的。'.format(search_plant, search_res))

        #询问物种的外形
        elif question_type=='plant_shape':
            for data in answer:
                search_plant=data['n.name']
                search_res1=data['m.name']
                search_res2=data['n.feature']
                search_answer+=('常态{0}的外形是{1}的，{2}。'.format(search_plant, search_res1, search_res2))

        #询问物种的光照需求
        elif question_type=='plant_light':
            for data in answer:
                search_plant=data['n.name']
                search_res=data['m.name']
                search_answer+=('培育{0}需要的光照强度是：{1}。'.format(search_plant, search_res))
        
        #询问物种的开花时间
        elif question_type=='plant_session':
            for data in answer:
                search_plant=data['n.name']
                search_res1=data['m.name']
                search_res2=data['n.flowering_form']
                search_answer+=('{0}开花的时间是{1}，{2}。'.format(search_plant, search_res1, search_res2))
        
        #询问物种的培育难度
        elif question_type=='plant_level':
            for data in answer:
                search_plant=data['n.name']
                search_res=data['m.name']
                search_answer+=('培育{0}的难度是：{1}。'.format(search_plant, search_res))
        
        #询问物种的培育温度
        elif question_type=='plant_temperature':
            for data in answer:
                search_plant=data['n.name']
                search_res=data['m.name']
                search_answer+=('培育{0}需要的温度：{1}。'.format(search_plant, search_res))
        
        #询问物种的酸碱范围
        elif question_type=='plant_ph':
            for data in answer:
                search_plant=data['n.name']
                search_res=data['m.name']
                search_answer+=('培育{0}的环境最适宜的ph值(酸碱范围)为：{1}。'.format(search_plant, search_res))
        
        #介绍作物
        elif question_type=='plant_desc':
            for data in answer:
                search_plant=data['n.name']
                search_res=data['n.desc']
                search_answer+=('{0}，基础信息：{1}。'.format(search_plant, search_res))
        
        #询问作物种植方法
        elif question_type=='plant_cultivation_method':
            for data in answer:
                search_plant=data['n.name']
                search_res=data['n.cultivation_method']
                search_answer+=('{0}，种植方法：{1}。'.format(search_plant, search_res))
        
        #询问作物繁殖方式
        elif question_type=='plant_reproduction':
            for data in answer:
                search_plant=data['n.name']
                search_res=data['n.reproduction']
                search_answer+=('{0}，繁殖方式：{1}。'.format(search_plant, search_res))
        
        return diff_name_answer + search_answer + '\n'
        
        
 
            
if __name__=='__main__':
    b=Questionparser()
    a=Questionclassifier()
    c=Answersearch()
    # sqls=[{'question_type': 'plant_level', 'sql': ["MATCH (n:Plant) where n.name='三七'  MATCH (n)-[:level]->(m:Level) RETURN n.name,m.name"]}, {'question_type': 'plant_ph', 'sql': ["MATCH (n:Plant) where n.name='三七'  MATCH (n)-[:need_ph]->(m:Ph) RETURN n.name,m.name"]}]
    # sqls=[{'question_type': 'plant_color', 'sql': ["MATCH (t:Different_name) where t.name='鸡矢果'  MATCH (t)<-[:other_name]-(n:Plant) MATCH (n)-[:color]->(m:Color)   RETURN t.name,n.name,m.name"]}]
    # sqls=[{'question_type': 'plant_diff_name', 'sql': ["MATCH (t:Different_name) where t.name='鸡矢果'  MATCH (t)<-[:other_name]-(n:Plant) MATCH (n)-[:other_name]->(m:Different_name)  RETURN t.name,n.name,m.name"]}]
    # sqls=[{'question_type': 'plant_ph', 'sql': ["MATCH (t:Different_name) where t.name='鸡矢果'  MATCH (t)<-[:other_name]-(n:Plant) MATCH (n)-[:need_ph]->(m:Ph) RETURN t.name,n.name,m.name"]}]
    while(1):
        question=input("问题: ")
        res_classify=a.classify(question)
        # res_classify={'args': {'三七': ['Plant'], '春季': ['Session'], '中光': ['Light']}, 'question_types': ['plant_level', 'plant_ph']}
        # res_classify={'args': {'鸡矢果': ['Different_name']}, 'question_types': ['plant_color']}
        # res_classify={'args': {'鸡矢果': ['Different_name']}, 'question_types': ['plant_diff_name']}
        # res_classify={'args': {'鸡矢果': ['Different_name']}, 'question_types': ['plant_ph']}
        sql=b.parser_main(res_classify)
        res=c.search_main(sql)      
        print(res)