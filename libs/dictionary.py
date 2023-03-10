# coding: utf-8
import os
import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.dirname(sys.argv[0]))
import json
import time
import random
import threading
from libs.word_info import WordInfo


class DictClass():

    def __init__(self):
        self.thread = None
        self.stop_event = None
        self.wi = WordInfo()
        base_dir = os.path.dirname(sys.argv[0])
        self.dict_dir = os.path.join(base_dir, 'dictionary')
        os.makedirs(self.dict_dir, exist_ok=True)
        self.dict_kotobank_path = os.path.join(self.dict_dir, 'dict_kotobank.json')
        if not os.path.exists(self.dict_kotobank_path):
            tmp_json = {"あ": []}
            with open(self.dict_kotobank_path, 'w') as f:
                json.dump(tmp_json, f, ensure_ascii=False)
        # End if
        with open(self.dict_kotobank_path, 'r') as f:
            self.dict_koto_json_load = json.load(f)
        # End with
        self.vocabulary = []
        for dict_values in self.dict_koto_json_load.values():
            self.vocabulary.extend(dict_values)
        # End for
    # End def

    def get_words(self, initial=''):
        if (initial in self.dict_koto_json_load):
            words = self.dict_koto_json_load[initial]
        else:
            words = []
        # End if
        return words

    def get_vocabulaty_len(self):
        return len(self.vocabulary)

    def start_increase_vocabulary(self, start_serch_word=''):
        if self.thread is None:
            self.stop_event = threading.Event()
            self.thread = threading.Thread(target=self._inc_loop, args=(start_serch_word, ))
            self.thread.start()
            print('start learn')
        # End if
    # End def

    def stop_increase_vocabulary(self):
        if self.thread is not None:
            self.stop_event.set()
            self.thread.join()
            print('stop learn')
            self.thread = None
            self.stop_event = None
        # End if
        with open(self.dict_kotobank_path, 'w') as f:
            json.dump(self.dict_koto_json_load, f, ensure_ascii=False)
        # End with
        self.vocabulary = []
        for dict_values in self.dict_koto_json_load.values():
            self.vocabulary.extend(dict_values)
    # End def

    def _inc_loop(self, first_word=''):
        if first_word == '':
            first_word = 'しりとり'
        # End if
        if (first_word in self.vocabulary):
            serch_words = self.vocabulary
        else:
            serch_words = [first_word]
        # End if
        while not self.stop_event.wait(0.5):
            debug_txt = ''
            and_words_dict = set(serch_words) & set(self.vocabulary)
            diff_serch_words = list(set(serch_words) ^ and_words_dict)
            if len(diff_serch_words) < 10:
                if len(serch_words) <= 1:
                    choise = 0
                else:
                    choise = random.randrange(0, len(serch_words) - 1, 1)
                # 検索する語彙を関連単語で増やす
                debug_txt += 'serch : ' + serch_words[choise]
                words = self.wi.get_relation_words(serch_words[choise], False)
                serch_words.extend(words)
                serch_words = list(set(serch_words))
            else:
                # 語彙として登録する。
                choise = random.randrange(0, len(diff_serch_words) - 1, 1)
                select_word = diff_serch_words[choise]
                winfo = self.wi.get_word_info(select_word, debug=False)
                self._add_word('kotobank', winfo[1], select_word)
                debug_txt += 'add   : ' + select_word
                for dict_values in self.dict_koto_json_load.values():
                    self.vocabulary.extend(dict_values)
                    self.vocabulary = list(set(self.vocabulary))
            # End if
            debug_txt += ', serch word len: ' + str(len(serch_words)) + ', vocabulary len:' + str(len(self.vocabulary))
            # print(debug_txt)
        # End while
    # End def

    def add_words(self, source_type, words):
        """_summary_

        Args:
            source_type (str): 'kotobank' , '...'
            words (list): [[initial, word],[initial, word],...]
        """
        for words_info in words:
            self._add_word(source_type, words_info[0], words_info[1])
        # End for
        with open(self.dict_kotobank_path, 'w') as f:
            json.dump(self.dict_koto_json_load, f, ensure_ascii=False)
        # End with
        self.vocabulary = []
        for dict_values in self.dict_koto_json_load.values():
            self.vocabulary.extend(dict_values)
        print(f' voc: {len(self.vocabulary)}')
    # End def

    def _add_word(self, source_type, initial, word):
        if source_type == 'kotobank':
            if initial in self.dict_koto_json_load:
                words_list = self.dict_koto_json_load[initial]
                if not (word in words_list):
                    words_list.append(word)
                    self.dict_koto_json_load[initial] = words_list
                # End if
            else:
                self.dict_koto_json_load[initial] = [word]
            # End if
        # End if
    # End def
# End class


def main():
    dict_class = DictClass()
    word_list = [['あ', '合言葉'], ['あ', '合言葉'], ['あ', 'あほ'], ['い', '犬']]
    dict_class.add_words('kotobank', word_list)
    dict_class.start_increase_vocabulary()
    time.sleep(100)
    dict_class.stop_increase_vocabulary()
    print(dict_class.vocabulary)
    print(len(dict_class.vocabulary))


if __name__ == '__main__':
    main()
