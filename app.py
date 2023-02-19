# coding: utf-8
import streamlit as st
from libs.shiritoriman import ShiritoriMan

def main():
    st.set_page_config(layout="wide")
    st.title("hello")


def test():
    bot = ShiritoriMan()
    bot.start_learn_word()
    try:
        while True:
            x = input(' input word')
            if x == 'q' or x == '':
                break
            ret_word = bot.res_shiritori(x)
            print(ret_word)
            print(f'vocablary : {bot.get_words_len()}')
    except Exception as e:
        print(e)
    finally:
        bot.stop_learn_word()
        bot.clear_shiritori()


if __name__ == '__main__':
    # test()
    main()
