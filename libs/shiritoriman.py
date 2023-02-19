# coding: utf-8
import os
import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.dirname(sys.argv[0]))
import time
import random
from libs.dictionary import DictClass
from libs.word_info import WordInfo

class ShiritoriMan():
    def __init__(self):
        self.dict_class = DictClass()
        self.wi = WordInfo()
        self.used_words = []
        self.remember_words = []
        self.shiritori_cnt = 0

    def res_shiritori(self, input_txt):
        self.used_words.append(input_txt)
        word_info = self.wi.get_word_info(input_txt, True)
        self.remember_words.append([word_info[1], input_txt])
        if word_info[0] == '':
            return_word = '私はその言葉がわかりません。'
        elif word_info[2] == 'ん':
            return_word = '「ん」で終わる言葉です。あなたの負けです。'
        else:
            ret_word_list = self.dict_class.get_words(word_info[2])
            if len(ret_word_list) != 0:
                while True:
                    and_words_dict = set(self.used_words) & set(ret_word_list)
                    diff_serch_words = list(set(ret_word_list) ^ and_words_dict)
                    if len(diff_serch_words) == 0:
                        print(diff_serch_words)
                        print(ret_word_list)
                        return_word = '負けました。1'
                        break
                    choise = random.randrange(0, len(diff_serch_words) - 1, 1)
                    return_word = ret_word_list[choise]
                    ret_wi = self.wi.get_word_info(return_word, True)
                    if ret_wi[2] != 'ん':
                        self.used_words.append(return_word)
                        break
                    # End if
                # End while
            else:
                return_word = '負けました。2'
            # End if
        # End if
        self.shiritori_cnt += 1
        return return_word
    # End def

    def start_learn_word(self):
        self.dict_class.start_increase_vocabulary()
    # End def

    def stop_learn_word(self):
        self.dict_class.stop_increase_vocabulary()
    # End def

    def get_words_len(self):
        return self.dict_class.get_vocabulaty_len()

    def clear_shiritori(self):
        print('しりとりを終了します。')
        print(f'{self.shiritori_cnt}回続きました。')
        self.dict_class.add_words('kotobank', self.remember_words)
        self.remember_words = []
        self.used_words = []
    # End def

    def __del__(self):
        self.dict_class.stop_increase_vocabulary()
    # End def


def main():
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



if __name__ == '__main__':
    main()
