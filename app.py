import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

# LangChainとOpenAIのインポート
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

def get_expert_response_with_langchain(input_text: str, selected_expert: str) -> str:
    """
    LangChainを使用してLLMから専門家の回答を取得する関数
    
    Args:
        input_text (str): ユーザーの質問内容
        selected_expert (str): 選択された専門家（"医療事務員" or "看護師"）
    
    Returns:
        str: LLMからの回答
    """
    try:
        # ChatOpenAIインスタンスを作成
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.5,
            max_tokens=500,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # 専門家に応じてシステムプロンプトを設定
        if selected_expert == "医療事務員":
            system_content = """
            あなたは経験豊富な医療事務員です。
            受付手順、事務手続き、医療費、保険関連の質問に対して、
            正確で親切な回答を提供してください。
            """
        else:  # 看護師
            system_content = """
            あなたは経験豊富な看護師です。
            診察、検査、治療、患者ケアに関する質問に対して、
            専門的で親切な回答を提供してください。
            ただし、診断や具体的な医療判断は医師の専門領域であることを伝えてください。
            """
        
        # ChatPromptTemplateを使用してプロンプトを構築
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_content),
            ("human", "{user_input}")
        ])
        
        # チェーンを作成して実行
        chain = prompt | llm
        response = chain.invoke({"user_input": input_text})
        
        return response.content
        
    except Exception as e:
        return f"申し訳ございません。回答の取得中にエラーが発生しました: {str(e)}"

st.title("課題LMMアプリ: このアプリは専門家のアドバイスを提供します。")
st.write("##### 専門家1: 医療事務員")
st.write("##### 専門家2: 看護師")
st.write("入力フォームにテキストを入力し、「実行」ボタンを押すことで専門家に質問することができます。")

selected_expert = st.radio(
    "質問したい専門家を選択してください。",
    ["医療事務員", "看護師"]
)

st.divider()

# 専門家に応じてプレースホルダーを変更
if selected_expert == "医療事務員":
    placeholder = "受付手順や事務手続き、医療費などについての質問に対応します。"
else:
    placeholder = "診察や検査、治療などについての質問に対応します。"

input_message = st.text_area(
    label="質問内容を入力してください。",
    placeholder=placeholder,
    height=100
)

if st.button("実行"):
    if not input_message.strip():
        st.error("質問内容を入力してから「実行」ボタンを押してください。")
    else:
        with st.spinner(f"{selected_expert}が回答を準備中..."):
            # LangChainを使用してLLM応答を取得
            response = get_expert_response_with_langchain(input_message, selected_expert)
            
            st.success(f"✅ {selected_expert}からの回答")
            st.write(f"**質問内容:** {input_message}")
            st.write("**回答:**")
            st.write(response)
