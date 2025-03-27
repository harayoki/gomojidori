# ５文字取り

`python .\src\gomojidori.py --ui`

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

![image](https://github.com/user-attachments/assets/6d846675-dadf-48f7-a364-473eae305b40)

