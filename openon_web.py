import streamlit as st
from chatbot import *


#设置网页的标题
st.set_page_config(
    page_title="农业咨询",
    layout="wide",
    
)
#设置标题
st.title("智能农业问答系统展示")

#设置左侧框
with st.sidebar:
    
    st.markdown("本问答系统基于自主构建的农业中文知识图谱,可以回复用户关于农业种植基础知识的问题,如种植方法、农作物适宜Ph值等")
    #编写示例
    with st.expander("查看问题示例"):
        st.markdown("1.芥菜的种植方法")
        st.markdown("2.芥菜的别名有哪些")
        st.markdown("3.芥的开花时间")
        st.markdown("4.芥菜的开花时间和适宜光照条件是什么")
        st.markdown("5.今晚吃什么(无法识别)")
        st.markdown("6.日本薯蓣的别名是什么(无法在数据库中找到答案)")


#将用户问答的历史信息进行存储
if "history" not in st.session_state:
    st.balloons()
    st.session_state.history=[]

#显示历史信息
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#传递问题,得到问答机器人的回复
def communicate(question):
    chatbot=Chatbotgraph()
    response=chatbot.chat_main(question)
    return response


#页面接收用户问题,将问答机器人的回复返回给用户
if openon_input:=st.chat_input(""):
    #在页面显示用户的输入
    with st.chat_message("User"):
        st.markdown(openon_input)
    
    #得到模型生成的回复
    response=communicate(openon_input)


    #将用户输入加入历史
    st.session_state.history.append({"role": "user", "content": openon_input})

    for response_one in response:
        #在页面上显示模型生成的回复
        with st.chat_message("assistant"):
            st.markdown(response_one)
    #将模型的输入加入到历史信息中
        st.session_state.history.append({"role": "assistant", "content": response_one})


