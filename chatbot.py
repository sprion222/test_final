from question_classifier import *
from question_parser import *
from answer_search import *
from merge_file import *

#问答主体
class Chatbotgraph:
    def __init__(self):
        merge_file=merge_all()
        merge_file.merge_main()
        self.classifier=Questionclassifier() #问题分类器
        self.parser=Questionparser() #问题解析器
        self.searcher=Answersearch() #答案查找器

    def chat_main(self,sent):
        #接收用户输入并对输入的问题进行分类
        #res_classify = {'args': {'三七': ['Plant'], '春季': ['Session'], '中光': ['Light']}, 'question_types': ['plant_level', 'plant_ph']}
        res_classify = self.classifier.classify(sent)
        #没有找到问题的分类
        if not res_classify:
            answer=["抱歉，我没有理解您的问题，请输入更准确的描述"]
            return answer
        
        #对分类的问题进行解析ant_level', 'sql': ["MATCH (n:Plant) where n.name='三七'  MATCH (n)-[:level]->(m:Level) RETURN n.name,m.name"]},
        #            {'question_type': 'plant_ph',    'sql': ["MATCH (n:Plant) where n.name='三七'  MATCH (n)-[:need_ph]->(m:Ph) RETURN n.name,m.name"]}]
        res_parser=self.parser.parser_main(res_classify)
        #对解析的内容利用答案查找器查找答案,并对答案进行润色返回
        
        res_search=self.searcher.search_main(res_parser)
        
        #对问题查找失败的处理
        if not res_search:
            answer=["对不起，我理解了您的问题，但我的知识库中没有相关的答案，请确定输入关键词的准确性或查找其它内容"]
            return answer
        else:
            return res_search 

if __name__=='__main__':
    merge_file=merge_all()
    merge_file.merge_main()
    # print("ok")
    chatbot=Chatbotgraph()
    while True:
        question=input('问题: ')
        answer=chatbot.chat_main(question)
        print('回答: ',answer)
        
