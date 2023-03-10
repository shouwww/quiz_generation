# coding: utf-8
import streamlit as st
from libs.character_type import CharTypeClass

st.set_page_config(layout="wide")
st.title('文字種クイズ')

# 履歴を格納するリスト
if 'chat_history' not in st.session_state:
    st.session_state.str_history = []
# End if
if 'ctc' not in st.session_state:
    st.session_state.ctc = CharTypeClass()
    st.session_state.ctc._set_voc()
# End if

# チャット入力フォームを表示する部分
st.subheader("文字種を選んでください。")
char_type = st.selectbox('文字種を選択する', st.session_state.ctc.get_char_type_list())
st.subheader("文字種に該当する単語を入力してください。")
user_input = st.text_input("入力")
if st.button("送信"):
    # 返信メッセージを取得
    bot_response = st.session_state.ctc.change_char_type_str(user_input)
    # 履歴に追加
    # st.session_state.str_history.append({"user": user_input, "bot": bot_response})
    st.session_state.str_history.insert(0, {"org": user_input, "ctc": bot_response})
if st.button('該当単語を表示する'):
    st.write(st.session_state.ctc.get_word_list(char_type=char_type))

# チャット履歴を表示する部分
st.subheader("履歴")
if len(st.session_state.str_history) == 0:
    st.write("まだありません")
else:
    for chat in st.session_state.str_history:
        st.write(f"元の言葉：{chat['org']} ,  文字種：{chat['ctc']}")
