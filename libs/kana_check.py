# coding: utf-8
import os
import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.dirname(sys.argv[0]))
import re


def is_hiragana(value):
    """_summary_
    平仮名判定

    Args:
        value (str): 判定したい文字列

    Returns:
        bool: すべて平仮名ならTrue, それ以外はFalse
    """
    return re.match(r'^[\u3040-\u309F]+$', value) is not None


def is_katakana(value):
    """_summary_
    カタカナ判定
    Args:
        value (str): 判定したい文字列

    Returns:
        bool: すべてカタカナならTrue それ以外はFalse
    """
    return re.match(r'^[\u30A0-\u30FF]+$', value) is not None
