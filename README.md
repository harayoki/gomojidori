# ５文字取り

入力スタッフロールテキストを5文字取りルールで並べてSVG出力するツール。
コマンドラインインターフェースとGUIインターフェースを持つ。

## 動作環境

Windows 11 / Python 3.11 で開発。その他環境での動作は未検証。

## 簡単な使い方

`python .\gomojidori.py --ui`
を実行し、表示されたURLをクリックしてブラウザで実行。

## 入力テキストの簡単な説明

* 1行に1人 人名前を記述
* 空白行は有効
* 苗字と名前の間に半角スペースを入れるとレイアウト時に考慮される
* 半角スペース自体を記述したい場合は半角の "_" を使う（ "_"自体を表示したい場合は全角を使う ）
* 先頭および行末のスペースは無視される

## GUIの各設定項目について

基本的にコマンドライン動作に準ずる。後述のコマンドラインヘルプを参照。

![image](https://github.com/user-attachments/assets/6d846675-dadf-48f7-a364-473eae305b40)

## コマンドヘルプ

```
usage: gomojidori.py [-h] [-f FONT] [-s FONT_SIZE] [-sp FONT_SPACE]
                     [-ms MIN_SCALE] [-c FONT_COLOR] [-l LINE_HEIGHT]
                     [--space-line-height SPACE_LINE_HEIGHT] [-w WIDTH]
                     [-i INPUT] [-o OUTPUT] [--debug] [--ui]

５文字取りルールで入力スタッフロールテキストをSVGに変換する

options:
  -h, --help            show this help message and exit
  -f FONT, --font FONT  フォントファイル（ttf）のパス
  -s FONT_SIZE, --font-size FONT_SIZE
                        フォントサイズ
  -sp FONT_SPACE, --font-space FONT_SPACE
                        フォントスペース
  -ms MIN_SCALE, --min-scale MIN_SCALE
                        最小縮小スケール
  -c FONT_COLOR, --font-color FONT_COLOR
                        フォントカラー
  -l LINE_HEIGHT, --line-height LINE_HEIGHT
                        行の高さ
  --space-line-height SPACE_LINE_HEIGHT
                        スペースのみの行の高さ
  -w WIDTH, --width WIDTH
                        SVGの横幅
  -i INPUT, --input INPUT
                        入力テキストファイル
  -o OUTPUT, --output OUTPUT
                        出力SVGファイル名
  --debug               デバッグ表示（中央線・ガイド）
  --ui                  GradioによるUIを表示する
```


