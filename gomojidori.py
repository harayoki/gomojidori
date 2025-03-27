import argparse
import svgwrite
from PIL import ImageFont, ImageDraw, Image
from pathlib import Path
from fontTools.ttLib import TTFont
import os
import tempfile
import re
import gradio as gr

__all__ = ["run_ui", "get_arg_parser", "DEFAULT_INPUT"]

FONT_DIR = Path(__file__).parent / "fonts"

DEFAULT_INPUT = (
    "田中 一郎\n鈴木次郎\n乾 三平\n\n四条 保\n吾郎丸\n清六\nnana\n\n"
    "八ノ戸 力\n万 久太郎\nⅩ\n一二三十一\n\n"
    "１２イエモン\n１３日の金曜日\n"
    "１４日の土曜午後\n１５日の日曜日深夜\n\n"
    "東京都渋谷区渋谷町渋谷\n"
    "Mac\nLinux\nWindows\n\n"
    "Famicom_Guy\n"
    "Michael_Lawson\n"
    "Seven_Seven_Seven\n"
    "May_the_force_be_with_you\n"
    "ブースケ・サマンサオバタ\n"
    "寿限無寿限無五劫の擦り切れ海砂利水魚の\n")

def list_fonts():
    if not FONT_DIR.exists():
        return []
    return [f.name for f in FONT_DIR.iterdir() if f.suffix.lower() == ".ttf"]


def get_default_font(local_mode=True):
    return (FONT_DIR / "NotoSansJP-Medium.ttf").as_posix()


def get_font_weight_name(font_path: str) -> str | None:
    font = TTFont(font_path)
    name_table = font['name']
    for record in name_table.names:
        if record.nameID == 2:  # Subfamily（例：Bold, Regular）
            return record.toStr()
    return None


def draw_fixed_width_text(dwg, text, font, font_weight, y, area_x, base_area_width, font_color, min_scale):
    text_parts = text.split(" ")
    num_spaces = len(text_parts) - 1
    merged = "".join(text_parts)
    num_chars = len(merged)
    if num_chars == 0:
        return
    font_family = font.getname()[0]
    dont_weight_map = {
        "regular": "normal",
        "medium": "normal",
        "bold": "bold",
        "semibold": "bold",
        "extrabold": "bold",
        "black": "bold"
    }
    font_weight = dont_weight_map.get(font_weight.lower(), "normal")

    # 1文字ずつフォントの幅を計算するためのダミー画像を作成
    dummy_img = Image.new('RGB', (1000, 100), color='white')
    draw = ImageDraw.Draw(dummy_img)
    char_widths = [draw.textbbox((0, 0), c, font=font)[2] for c in text if c != ' ']

    MID = "middle"
    LFT = "start"
    RGT = "end"
    L_POS = area_x
    R_POS = area_x + base_area_width
    C_POS = area_x + base_area_width * 0.5
    if font_color.startswith("rgba"):
        # ex) rgba(200.73281250000002, 39.618318256578945, 39.618318256578945, 1)
        mo = re.match(r'rgba\((.+),\s*(.+),\s*(.+),\s*(.+)\)', font_color)
        if mo:
            font_color = svgwrite.rgb(float(mo.group(1)), float(mo.group(2)), float(mo.group(3)))
        else:
            font_color = "black"

    def put_text(texts, xx, yy, anchor, text_xscale=1.0):
        if texts == "_":
            # アンダースコアはスペースに置換
            texts = " "
        if text_xscale != 1.0:
            transform_str = f"translate({xx}, {y}) scale({text_xscale}, 1) translate({-text_xscale}, {-y})"
            text_group = dwg.g(transform=transform_str)
            text_group.add(dwg.text(
                texts,
                insert=(0, yy),
                text_anchor=anchor,
                font_size=font.size,
                font_family=font_family,
                font_weight=font_weight,
                fill=font_color
            ))
            dwg.add(text_group)
        else:
            dwg.add(dwg.text(
                texts, insert=(xx, yy), text_anchor=anchor, font_size=font.size,
                font_weight=font_weight,
                font_family=font_family, fill=font_color
            ))

    if num_chars == 1:
        put_text(text, C_POS, y, MID)
        return

    if num_chars == 2:
        put_text(merged[0], L_POS, y, LFT)
        put_text(merged[1], R_POS, y, RGT)
        return

    if num_chars == 3:
        put_text(merged[0], L_POS, y, LFT)
        put_text(merged[2], R_POS, y, RGT)
        if num_spaces == 1:
            if len(text_parts[0]) < len(text_parts[1]):
                # 名前の方が2文字 真ん中は右に寄せる
                put_text(merged[1], C_POS, y, LFT)
            else:
                # 苗字の方が2文字 真ん中は左に寄せる
                put_text(merged[1], C_POS, y,RGT)
        else:
            # 等間隔配置
            put_text(merged[1], C_POS, y, MID)
        return

    first_w = char_widths[0]
    last_w = char_widths[-1]
    total_char_width = sum(char_widths)
    margin_rest = base_area_width - total_char_width
    step = (R_POS - L_POS) / (num_chars - 1)

    if num_chars == 4:
        if num_spaces == 1:
            if len(text_parts[0]) == len(text_parts[1]):
                # 1文字目と4文字目の位置は固定
                put_text(merged[0], L_POS, y, LFT)
                put_text(merged[-1], R_POS, y, RGT)
                # 苗字も名前も2文字 すこしそれzれに寄せる
                for i in range(1, num_chars - 1):
                    pos = L_POS + step * i
                    put_text(merged[i], pos, y, MID)
                return
            else:
                # 苗字と名前の間に全角スペースを入れて5文字ぴったりにする
                put_text(text_parts[0] + "　" + text_parts[1], L_POS, y, LFT)
                return
        else:
            # num_spaces が 1 以外の場合は均等に配置
            pos = L_POS
            for i in range(num_chars):
                put_text(merged[i], pos, y, LFT)
                pos += (margin_rest / (num_chars - 1) + char_widths[i])
            return

    if num_chars == 5:
        # 5文字の場合は普通に均等配置
        pos = L_POS
        for i in range(num_chars):
            put_text(merged[i], pos, y, LFT)
            pos += (margin_rest / (num_chars - 1) + char_widths[i])
        return

    # 6文字以上の場合 文字幅を縮める
    spacer = 1.0
    # text_xscale = max(min_scale, 5 / num_chars)
    text_xscale = base_area_width / (total_char_width + spacer * (num_chars - 1))
    text_xscale = max(text_xscale, min_scale)
    # print(f"文字数: {num_chars}, 縮小率: {text_xscale} {min_scale}")
    pos = L_POS + 0.5 * (base_area_width - total_char_width * text_xscale - spacer * (num_chars  - 1))
    for i in range(num_chars):
        put_text(merged[i], pos, y, LFT, text_xscale=text_xscale)
        pos += spacer + char_widths[i] * text_xscale


def render_text_to_svg(
        text, font_path, font_size, font_space, min_scale,
        line_height, space_line_height, svg_width, output_file: str | None, font_color, debug=False):
    font = ImageFont.truetype(str(font_path), font_size)
    lines = text.split('\n')
    svg_height = 0
    heights = []
    regex = re.compile(r'^\s*(.+)\s*$')

    font_weight = get_font_weight_name(font_path)
    # print(f"フォント: {font_path.name} ({font_weight})")

    for line in lines:
        # 頭にスペースがあれば除去
        mo = regex.match(line)
        if mo:
            line = regex.match(line).group(1)
        if line == "":
            heights.append(space_line_height)
            svg_height += space_line_height
        else:
            heights.append(line_height)
            svg_height += line_height
    dwg = svgwrite.Drawing(output_file, size=(svg_width, svg_height))

    # 基準となる5文字分の合計幅を計算（スペースを除外）
    dummy_five = "あいうえお"
    dummy_img = Image.new('RGB', (1000, 100), color='white')
    draw = ImageDraw.Draw(dummy_img)
    base_widths = [draw.textbbox((0, 0), c, font=font)[2] for c in dummy_five]
    base_area_width = sum(base_widths) + font_space * 4
    area_x = (svg_width - base_area_width) / 2

    if debug:
        # 位置確認用の罫線の描画
        dwg.add(dwg.line(
            start=(svg_width / 2, 0), end=(svg_width / 2, svg_height), stroke="lightblue", stroke_dasharray="5,5"))
        dwg.add(dwg.line(start=(area_x, 0), end=(area_x, svg_height), stroke="lightblue"))
        dwg.add(dwg.line(
            start=(area_x + base_area_width, 0), end=(area_x + base_area_width, svg_height), stroke="lightblue"))

        dwg.add(dwg.line(start=(0, 0), end=(0, svg_height), stroke="lightblue"))
        dwg.add(dwg.line(start=(svg_width, 0), end=(svg_width, svg_height), stroke="lightblue"))

    y_cursor = 0
    for line, h in zip(lines, heights):
        draw_fixed_width_text(
            dwg, line, font, font_weight, y=y_cursor + font_size, area_x=area_x,
            base_area_width=base_area_width, font_color=font_color, min_scale=min_scale
        )
        y_cursor += h
    if output_file:
        dwg.save()
    return dwg.tostring()


def run_ui(args):
    font_files = list_fonts()
    font_choices = font_files if font_files else ["(フォントなし)"]
    # NotoSansJPが含まれるものを前に持ってくる
    font_choices.sort(key=lambda x: "NotoSansJP" not in x)

    def generate_svg(text, font_name, font_size, font_space, min_scale, line_height, space_line_height,
                     svg_width, text_color, debug, scale):
        output_filename = args.output
        font_path = FONT_DIR / font_name
        if not font_path.exists():
            with open("error.txt", "w", encoding="utf-8") as f:
                f.write("フォントが見つかりませんでした。")
            return "エラー: フォントが見つかりません。", None
        svg_content = render_text_to_svg(
            text, font_path, int(font_size), int(font_space), float(min_scale), int(line_height), int(space_line_height),
            int(svg_width), None, text_color, debug
        )
        # print(f"SVG: {svg_content[:100]}...")
        scale = scale or "0.25"
        scale_float = float(scale)
        width_style = f"width: {int(int(svg_width) * scale_float)}px;"
        scaled_svg = \
            f'<div style="transform: scale({scale}); transform-origin: top left; {width_style}">{svg_content}</div>'
        with tempfile.NamedTemporaryFile(delete=False, suffix=".svg", mode="w", encoding="utf-8") as f:
            f.write(svg_content)
            output_filename = f.name
        return output_filename, scaled_svg
    default_text = args.input or ""
    iface = gr.Interface(
        fn=generate_svg,
        inputs=[
            gr.Textbox(label="テキスト入力", lines=8, value=default_text, placeholder="各行に人名 '苗字 名前'"),
            gr.Dropdown(
                choices=font_choices, label="フォント選択",
                value=os.path.basename(
                    args.font) if args.font and os.path.basename(args.font) in font_choices else font_choices[0]),
            gr.Number(label="フォントサイズ", value=args.font_size),
            gr.Number(label="フォントスペース", value=args.font_space),
            gr.Number(label="最小縮小率", value=args.min_scale),
            gr.Number(label="行の高さ", value=args.line_height),
            gr.Number(label="スペースのみの行の高さ", value=args.space_line_height),
            gr.Number(label="SVGの横幅", value=args.width),
            gr.ColorPicker(label="文字色", value=args.font_color),
            gr.Checkbox(label="デバッグ表示（ガイド線）", value=args.debug),
            gr.Dropdown(label="表示倍率", choices=["0.1", "0.25", "0.33", "0.5", "0.75", "1.0"], value="0.5")
        ],
        outputs=[
            gr.File(label="SVGファイル ダウンロード"),
            gr.HTML(label="プレビュー")
        ],
        title="＊５文字取り＊ スタッフロールSVG作成ツール",
        description="５文字取りルールに則り、入力されたスタッフロールテキストをSVGファイルに変換します。"
    )
    iface.launch()


def get_arg_parser():
    parser = argparse.ArgumentParser(description='５文字取りルールで入力スタッフロールテキストをSVGに変換する')
    parser.add_argument('-f', '--font', default=get_default_font(), help='フォントファイル（ttf）のパス')
    parser.add_argument('-s', '--font-size', type=int, default=50, help='フォントサイズ')
    parser.add_argument('-sp', '--font-space', type=int, default=2, help='フォントスペース')
    parser.add_argument('-ms', '--min-scale', type=float, default=0.55, help='最小縮小スケール')
    parser.add_argument('-c', '--font-color', type=str, default="#000000", help='フォントカラー')
    parser.add_argument('-l', '--line-height', type=int, default=80, help='行の高さ')
    parser.add_argument('--space-line-height', type=int, default=40, help='スペースのみの行の高さ')
    parser.add_argument('-w', '--width', type=int, default=1280, help='SVGの横幅')
    parser.add_argument('-i', '--input', help='入力テキストファイル')
    parser.add_argument('-o', '--output', help='出力SVGファイル名', default="")
    parser.add_argument('--debug', action='store_true', help='デバッグ表示（中央線・ガイド）')
    parser.add_argument('--ui', action='store_true', help='GradioによるUIを表示する')
    return parser


def main():
    parser = get_arg_parser()
    args = parser.parse_args()
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as file:
            args.input = file.read()
    else:
        args.input = DEFAULT_INPUT
    if args.ui:
        run_ui(args)
    else:
        if not args.output:
            input_basename = os.path.splitext(os.path.basename(args.input))[0]
            args.output = f"{input_basename}.svg"
        regex_color = r'^#[0-9a-fA-F]{6}$'
        assert re.match(regex_color, args.font_color) is not None, "フォントカラーは #RRGGBB 形式で指定してください"
        if args.font:
            assert os.path.exists(args.font), "フォントファイルが見つかりません"
        render_text_to_svg(
            text=args.input,
            font_path=args.font,
            font_size=args.font_size,
            font_space=args.font_space,
            min_scale=args.min_scale,
            line_height=args.line_height,
            space_line_height=args.space_line_height,
            svg_width=args.width,
            output_file=args.output,
            font_color=args.font_color,
            debug=args.debug
        )


if __name__ == '__main__':
    main()
