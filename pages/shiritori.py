# coding: utf-8
import streamlit as st
from libs.shiritoriman import ShiritoriMan


# チャット履歴を格納するリスト
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
# End if
if 'shiritoriman' not in st.session_state:
    st.session_state.bot = ShiritoriMan()
# End if
# ユーザー入力を受け付け、返信メッセージを返す関数


# Streamlitアプリの設定
st.set_page_config(page_title="しりとりアプリ", page_icon=":speech_balloon:", layout="wide")

st.title('しりとりアプリ')
st.subheader("bot 情報")
if st.button('start learn word'):
    st.session_state.bot.start_learn_word()
if st.button('stop learn word'):
    st.session_state.bot.stop_learn_word()
st.text('bot vocabulary :' + str(st.session_state.bot.get_words_len()))
if st.button('reload'):
    pass


# チャット入力フォームを表示する部分
st.subheader("メッセージを入力してください")
user_input = st.text_input("ユーザー入力")
if st.button('Clear '):
    st.session_state.bot.clear_shiritori()
    st.session_state.chat_history = []
if st.button("送信"):
    # 返信メッセージを取得
    bot_response = st.session_state.bot.res_shiritori(user_input)
    # 履歴に追加
    # st.session_state.chat_history.append({"user": user_input, "bot": bot_response})
    st.session_state.chat_history.insert(0, {"user": user_input, "bot": bot_response})

# チャット履歴を表示する部分
st.subheader("チャット履歴")
if len(st.session_state.chat_history) == 0:
    st.write("まだメッセージはありません")
else:
    for chat in st.session_state.chat_history:
        st.write(f"ボット：{chat['bot']}")
        st.write(f"ユーザー：{chat['user']}")
