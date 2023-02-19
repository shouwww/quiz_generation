# coding: utf-8
import streamlit as st
from libs.character_type import CharTypeClass

st.title('文字種クイズ')

# 履歴を格納するリスト
if 'chat_history' not in st.session_state:
    st.session_state.str_history = []
# End if
if 'ctc' not in st.session_state:
    st.session_state.ctc = CharTypeClass()
# End if

# チャット入力フォームを表示する部分
st.subheader("単語や言葉を入力してください。")
user_input = st.text_input("ユーザー入力")
if st.button("送信"):
    # 返信メッセージを取得
    bot_response = st.session_state.ctc.change_char_type_str(user_input)
    # 履歴に追加
    # st.session_state.str_history.append({"user": user_input, "bot": bot_response})
    st.session_state.str_history.insert(0, {"org": user_input, "ctc": bot_response})

# チャット履歴を表示する部分
st.subheader("履歴")
if len(st.session_state.str_history) == 0:
    st.write("まだありません")
else:
    for chat in st.session_state.str_history:
        st.write(f"元の言葉：{chat['org']} ,  文字種：{chat['ctc']}")
