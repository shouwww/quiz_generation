# coding: utf-8
import os
import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.dirname(sys.argv[0]))
import re
import requests
import binascii
import libs.kana_check as kana_check
import jaconv
from bs4 import BeautifulSoup

class WordInfo():
    def __init__(self):
        pass
    # End def

    def get_word_info(self, word, debug=False):
        """_summary_

        Args:
            word (str): 単語

        Returns:
            list[yomi(str), initial(str), tail(str)]: yomi 単語の読み, initial 単語の最初の文字, tail 単語の最後の文字
        """
        find_url = self._make_url(word, debug)
        yomi = self._get_yomi(find_url, debug)
        if len(yomi) > 0:
            initial = yomi[0]
            tail = yomi[-1]
            if kana_check.is_hiragana(initial) is False:
                if kana_check.is_katakana(initial) is True:
                    initial = jaconv.kata2hira(initial)
                else:
                    yomi = ''
                    initial = ''
                    tail = ''
                # End if
            # End if
            if (kana_check.is_katakana(tail) is True) and tail != '':
                tail = jaconv.kata2hira(tail)
            # End if
        else:
            initial = ''
            tail = ''
        return [yomi, initial, tail, find_url]

    def get_relation_words(self, word, debug=False):
        find_url = self._make_url(word, debug)
        html = requests.get(find_url).text
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', attrs={'href': re.compile(r'.*/word/%.*$')})
        ret_list = []
        for link in links:
            ret_list.append(link.text)
        # End for
        if debug:
            print(word)
            print(ret_list)
        return ret_list

    def _get_yomi(self, url, debug=False):
        """_summary_

        Args:
            url (str): 単語のコトバンクのURL

        Returns:
            yomi (str): 単語の読みを返す
        """
        yomi = ''
        html_txt = requests.get(url).text
        soup = BeautifulSoup(html_txt, 'html.parser')
        page_tag = soup.find('title')
        title_str = page_tag.string     # <title>, </title>を除く
        if title_str == 'コトバンク - お探しのページは見つかりません':
            yomi = ''
        else:
            yomi = title_str.replace('とは？ 意味や使い方 - コトバンク', '')
            if ('(' in yomi) and (')' in yomi):
                first_index = yomi.index('(') + 1
                yomi = yomi[first_index:-1]
            # End if
        if debug:
            print(f'title : {title_str}')
        return yomi
    # End def

    def _make_url(self, word, debug=False):
        base_url = 'https://kotobank.jp/word/'
        # byteに変換
        word_byte = word.encode('utf-8')
        # byte列から16進数文字列に変換　https://qiita.com/masakielastic/items/21ba9f68ef6c4fd7692d
        word_str_hex = str(binascii.hexlify(word_byte), 'utf-8')
        # 大文字に変換
        word_str_hex = word_str_hex.upper()
        splits = []
        # 2文字ずつにわけて%でくっつける
        for i in range(len(word_str_hex) // 2):
            splits.append(word_str_hex[i * 2: (i + 1) * 2])
        # End for
        word_url = '%'.join(splits)
        # 最初の% と ベースURLでくっつける
        ret_url = base_url + '%' + word_url
        if debug:
            print(f'url : {ret_url}')
        return ret_url

# End class

def main():
    wi = WordInfo()
    serch_word = 'しりとり'
    words = wi.get_relation_words(serch_word, True)
    winfo = wi.get_word_info(serch_word, True)
    print(words)
    print(winfo)
# End def


if __name__ == '__main__':
    main()