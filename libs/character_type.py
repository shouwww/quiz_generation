import re
import os
import sys
import json


class CharTypeClass:
    def __init__(self):
        self.is_small_alpha = re.compile('[a-zａ-ｚ]+')
        self.is_big_alpha = re.compile('[A-ZＡ-Ｚ]+')
        self.is_numeric = re.compile('[0-9０-９]+')
        self.is_hira = re.compile('[\u3041-\u309F]+')
        self.is_small_hira = re.compile('[ぁぃぅぇぉっゃゅょゎ]+')
        self.is_kana = re.compile('[\u30A1-\u30FF]+')
        self.is_small_kana = re.compile('[ァィゥェォッャュョヮ]+')
        self.is_kanji = re.compile('[\u3401-\u4DBF\u4E01-\u9FFF]+')
        self.voc_char = {}
    # End def

    def _set_voc(self):
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
        for dict_values in self.dict_koto_json_load.values():
            for word in dict_values:
                char = self.change_char_type_str(word)
                if char in self.voc_char:
                    word_list = self.voc_char[char]
                    if not (word in word_list):
                        word_list.append(word)
                        self.voc_char[char] = word_list
                    # End if
                else:
                    self.voc_char[char] = [word]
                # End if
            # End for
        # End for
        char_type_json_path = os.path.join(self.dict_dir, 'dict_char_type.json')
        with open(char_type_json_path, 'w') as f:
            json.dump(self.voc_char, f, ensure_ascii=False)

    def get_word_list(self, char_type=''):
        ret_list = []
        if char_type in self.voc_char:
            ret_list = self.voc_char[char_type]
        # End if
        return ret_list

    def get_char_type_list(self):
        return self.voc_char.keys()

    def change_char_type_str(self, input_text):
        ret_string = ''
        for moji in input_text:
            if self.is_small_alpha.fullmatch(moji) is not None:
                ret_string = ret_string + 'a'
            elif self.is_big_alpha.fullmatch(moji) is not None:
                ret_string = ret_string + 'A'
            elif self.is_numeric.fullmatch(moji) is not None:
                ret_string = ret_string + '1'
            elif self.is_hira.fullmatch(moji) is not None:
                if self.is_small_hira.fullmatch(moji) is not None:
                    ret_string = ret_string + 'ぁ'
                else:
                    ret_string = ret_string + 'あ'
            elif self.is_kana.fullmatch(moji) is not None:
                if self.is_small_kana.fullmatch(moji) is not None:
                    ret_string = ret_string + 'ァ'
                else:
                    ret_string = ret_string + 'ア'
            elif self.is_kanji.fullmatch(moji) is not None:
                ret_string = ret_string + '漢'
            else:
                ret_string = ret_string + moji
            # End if
        # End for
        return ret_string
    # End def

    def __del__(self):
        pass


def main():
    mojiretsu = 'ヤバイTシャツ屋さん'
    ctc = CharTypeClass()
    mojishu_str = ctc.change_char_type_str(mojiretsu)
    print(mojiretsu + ' = ' + mojishu_str)
    ctc._set_voc()
    print(ctc.get_word_list('漢漢漢'))
    print(ctc.get_char_type_list())


if __name__ == '__main__':
    main()
