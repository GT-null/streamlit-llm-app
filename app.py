import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

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
            st.success(f"✅ {selected_expert}に質問しました")
            st.write(f"**質問内容:** {input_message}")
            
            # TODO: ここに実際のLLM API呼び出しを実装
            st.info("💡 実際のLLM連携機能は実装予定です")
