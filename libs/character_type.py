import re

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
    # End def

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


if __name__ == '__main__':
    main()
