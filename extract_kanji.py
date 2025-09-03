# -*- coding: utf-8 -*-
import re
import os
from janome.tokenizer import Tokenizer
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import cm

def get_kanji_with_reading(text):
    """
    テキストから漢字とその読み方を抽出する関数
    """
    t = Tokenizer()
    kanji_readings = {}
    for token in t.tokenize(text):
        surface = token.surface
        reading = token.reading

        if re.search(r'[\u4e00-\u9faf]', surface) and reading:
            hiragana_reading = "".join([chr(ord(c) - ord('ァ') + ord('ぁ')) if 'ァ' <= c <= 'ヶ' else c for c in reading])
            kanji_readings[surface] = hiragana_reading

    return kanji_readings

def create_kanji_pdf(kanji_readings):
    """
    抽出した漢字と読み方をPDFファイルとして出力する関数。
    ファイル名を自動で生成し、そのファイル名を返す。
    """
    number = 0
    output_filename = f"kanji_list_{number:02d}.pdf"

    while os.path.exists(output_filename):
        number += 1
        output_filename = f"kanji_list_{number:02d}.pdf"

    try:
        pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
    except KeyError:
        print("HeiseiMin-W3フォントが見つかりません。ReportLabを適切に設定しているか確認してください。")
        return None

    c = canvas.Canvas(output_filename, pagesize=A4)
    c.setFont('HeiseiMin-W3', 12)

    c.drawString(2.5*cm, 27*cm, f"漢字と読み方リスト - {number:02d}")

    y_position = 26*cm

    for kanji, reading in kanji_readings.items():
        if y_position < 2*cm:
            c.showPage()
            c.setFont('HeiseiMin-W3', 12)
            y_position = 28*cm

        text = f"{kanji} / {reading}"
        c.drawString(2.5*cm, y_position, text)
        y_position -= 0.8*cm

    c.save()
    print(f"PDFファイル '{output_filename}' が正常に生成されました。")
    return output_filename # PDFファイル名を返すように修正