# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2026 Xie Youtian
import pypinyin
import logging
from get import PageInfo
from typing import List, TypedDict

def _kana_to_romaji(text: str) -> List[str]:
    """将假名文本转换为罗马字，用于pypinyin的errors回调"""
    # 平假名到罗马字映射
    hiragana_map = {
        'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
        'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
        'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
        'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
        'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
        'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
        'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
        'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
        'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
        'わ': 'wa', 'を': 'wo', 'ん': 'n',
        'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
        'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
        'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
        'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
        'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
        'きゃ': 'kya', 'きゅ': 'kyu', 'きょ': 'kyo',
        'しゃ': 'sha', 'しゅ': 'shu', 'しょ': 'sho',
        'ちゃ': 'cha', 'ちゅ': 'chu', 'ちょ': 'cho',
        'にゃ': 'nya', 'にゅ': 'nyu', 'にょ': 'nyo',
        'ひゃ': 'hya', 'ひゅ': 'hyu', 'ひょ': 'hyo',
        'みゃ': 'mya', 'みゅ': 'myu', 'みょ': 'myo',
        'りゃ': 'rya', 'りゅ': 'ryu', 'りょ': 'ryo',
        'ぎゃ': 'gya', 'ぎゅ': 'gyu', 'ぎょ': 'gyo',
        'じゃ': 'ja', 'じゅ': 'ju', 'じょ': 'jo',
        'びゃ': 'bya', 'びゅ': 'byu', 'びょ': 'byo',
        'ぴゃ': 'pya', 'ぴゅ': 'pyu', 'ぴょ': 'pyo',
    }
    
    # 片假名到罗马字映射
    katakana_map = {
        'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
        'カ': 'ka', 'キ': 'ki', 'ク': 'ku', 'ケ': 'ke', 'コ': 'ko',
        'サ': 'sa', 'シ': 'shi', 'ス': 'su', 'セ': 'se', 'ソ': 'so',
        'タ': 'ta', 'チ': 'chi', 'ツ': 'tsu', 'テ': 'te', 'ト': 'to',
        'ナ': 'na', 'ニ': 'ni', 'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no',
        'ハ': 'ha', 'ヒ': 'hi', 'フ': 'fu', 'ヘ': 'he', 'ホ': 'ho',
        'マ': 'ma', 'ミ': 'mi', 'ム': 'mu', 'メ': 'me', 'モ': 'mo',
        'ヤ': 'ya', 'ユ': 'yu', 'ヨ': 'yo',
        'ラ': 'ra', 'リ': 'ri', 'ル': 'ru', 'レ': 're', 'ロ': 'ro',
        'ワ': 'wa', 'ヲ': 'wo', 'ン': 'n',
        'ガ': 'ga', 'ギ': 'gi', 'グ': 'gu', 'ゲ': 'ge', 'ゴ': 'go',
        'ザ': 'za', 'ジ': 'ji', 'ズ': 'zu', 'ゼ': 'ze', 'ゾ': 'zo',
        'ダ': 'da', 'ヂ': 'ji', 'ヅ': 'zu', 'デ': 'de', 'ド': 'do',
        'バ': 'ba', 'ビ': 'bi', 'ブ': 'bu', 'ベ': 'be', 'ボ': 'bo',
        'パ': 'pa', 'ピ': 'pi', 'プ': 'pu', 'ペ': 'pe', 'ポ': 'po',
        'キャ': 'kya', 'キュ': 'kyu', 'キョ': 'kyo',
        'シャ': 'sha', 'シュ': 'shu', 'ショ': 'sho',
        'チャ': 'cha', 'チュ': 'chu', 'チョ': 'cho',
        'ニャ': 'nya', 'ニュ': 'nyu', 'ニョ': 'nyo',
        'ヒャ': 'hya', 'ヒュ': 'hyu', 'ヒョ': 'hyo',
        'ミャ': 'mya', 'ミュ': 'myu', 'ミョ': 'myo',
        'リャ': 'rya', 'リュ': 'ryu', 'リョ': 'ryo',
        'ギャ': 'gya', 'ギュ': 'gyu', 'ギョ': 'gyo',
        'ジャ': 'ja', 'ジュ': 'ju', 'ジョ': 'jo',
        'ビャ': 'bya', 'ビュ': 'byu', 'ビョ': 'byo',
        'ピャ': 'pya', 'ピュ': 'pyu', 'ピョ': 'pyo',
        'ヴ': 'vu', 'ヴァ': 'va', 'ヴィ': 'vi', 'ヴェ': 've', 'ヴォ': 'vo',
        'ファ': 'fa', 'フィ': 'fi', 'フェ': 'fe', 'フォ': 'fo',
        'ティ': 'ti', 'ディ': 'di', 'トゥ': 'tu', 'ドゥ': 'du',
    }
    
    # 合并映射
    kana_map = {**hiragana_map, **katakana_map}
    
    # 处理文本：尝试将假名转换为罗马字
    result = []
    i = 0
    while i < len(text):
        # 优先尝试匹配2字符的拗音
        if i + 1 < len(text) and text[i:i+2] in kana_map:
            result.append(kana_map[text[i:i+2]])
            i += 2
        # 匹配单字符假名
        elif text[i] in kana_map:
            result.append(kana_map[text[i]])
            i += 1
        # 非假名字符，保持原样（pypinyin会处理）
        else:
            result.append(text[i])
            i += 1
    
    # pypinyin期望一个拼音列表
    return result


class PinyinPageInfo(TypedDict):
    page_id: int
    page_title: str
    pinyin: str
    pinyin_group: str
    user_page: bool
    deceased: bool



def get_pinyinized_page_list(unpinyinized_titles: List[PageInfo]) -> List[PinyinPageInfo]:
    import logging
    logging.info(f"  开始处理 {len(unpinyinized_titles)} 个页面的拼音转换...")
    
    pinyinized_titles : List[PinyinPageInfo] = []
    def get_group(pinyin_str: str) -> str:
        if not pinyin_str:
            return "#"
        first_char = pinyin_str[0].upper()
        if 'A' <= first_char <= 'Z':
            return first_char
        else:
            return "#"
    
    processed_count = 0
    for page_info in unpinyinized_titles:
        copied_page_info = page_info.copy()
        copied_page_info["pinyin"] = ''.join(
            pypinyin.lazy_pinyin(
                copied_page_info["page_title"],
                style=pypinyin.Style.NORMAL,
                errors=_kana_to_romaji
            )
        )
        copied_page_info["pinyin_group"] = get_group(copied_page_info["pinyin"])
        pinyinized_titles.append(copied_page_info)
        
        processed_count += 1
        if processed_count % 1000 == 0:  # 每处理1000个页面输出一次进度
            logging.info(f"    已处理 {processed_count}/{len(unpinyinized_titles)} 个页面")

    pinyinized_titles.sort(key=lambda x: x["pinyin"])
    logging.info(f"  拼音转换完成，共处理 {len(pinyinized_titles)} 个页面")
    return pinyinized_titles

def generate_template(
    pinyinized_titles: List[PinyinPageInfo],
    grouping_scheme: list[str] = ["A·B·C·D", "E·F·G·H", "I·J·K·L", "M·N·O·P", "Q·R·S·T", "U·V·W", "X·Y·Z", "#"]
):
    # Group pages by first letter of pinyin
    groups = {}
    for page_info in pinyinized_titles:
        if page_info["pinyin"]:
            first_char = page_info["pinyin"][0].upper()
        else:
            first_char = "#"

        # Handle non-alphabetic characters (only A-Z considered alphabetic)
        if not ('A' <= first_char <= 'Z'):
            first_char = "#"

        if first_char not in groups:
            groups[first_char] = []
        groups[first_char].append(page_info)

    # Sort groups by key
    sorted_groups = dict(sorted(groups.items()))

    # Create template string with noinclude header
    template = "<noinclude>\n"
    template += "== 编辑须知 ==\n"
    template += "# 兽圈是一个包容性非常强的群体，即便你不出名，你没有拿得出手的作品，'''甚至你认为你只是一个普通人'''，你都可以在这里创建属于你自己的词条。\n"
    template += "# 欢迎每一位毛茸茸创建属于自己的词条或修订关于自己的词条，因为'''你比任何人都要了解你自己'''。\n"
    template += "# 该模板由机器人维护。当你创建了属于你的词条后，你的名字将于次日或者当日早上7点出现在这个页面上。"
    template += "# 你可以在[[gh:TimXiedada/wikifur-persons-template-bot|这个GitHub仓库]]找到机器人的源代码（一部分模块使用Vibe Coding方式开发）。\n"
    template += "# WikiFur是一个比较专业（或者说严肃）的百科平台，请各位在编辑词条时不要使用太过主观（或随意）的语言。\n"
    template += "# WikiFur并不是一个新闻的收集仓库，除非是十分重要的事件，否则请不要加入过多的时事性内容。\n"
    # template += "# 因为精力有限，以上内容可能无法包含全部毛茸茸，需要大家修订补充。\n"
    template += "# 基于现代中文出版物的做法，该模板中，逝世的人物将会用 {{Departed|示亡号}} 标记。\n\n"
    template += "== 模板正文 == \n"
    template += "</noinclude>\n"
    template += "{{Navbox\n"
    template += "|name = 人物\n"
    template += "|title = 已收录的人物（总览）\n"
    template += "|group1 = 成员\n"
    template += "|list1=\n\n"
    template += "{{Navbox subgroup\n"

    # Create letter groups according to grouping_scheme
    for i, group_name in enumerate(grouping_scheme, 1):
        template += f"|group{i} = {group_name}\n"

        # Extract letters from group name (e.g., "A·B·C·D" -> ["A", "B", "C", "D"])
        letters_in_group = [letter for letter in group_name.split("·") if letter.isalpha() or letter == "#"]

        # Collect entries for this group
        entries = []
        for letter in letters_in_group:
            if letter in sorted_groups:
                for page_info in sorted_groups[letter]:
                    page_title = page_info["page_title"]
                    if page_info.get("user_page"):
                        link = f"[[用户:{page_title}|{page_title}]]"
                    else:
                        link = f"[[{page_title}]]"
                    if page_info.get("deceased"):
                        entries.append(f"{{{{Departed|{link}}}}}")
                    else:
                        entries.append(link)

        # Join entries with separator
        list_content = " {{·}} ".join(entries) if entries else ""
        template += f"|list{i} = {list_content}\n\n"

    # Add the未创建词条 group
    template += "|group10 = 未在 [[WikiFur]] 创建词条\n"
    template += "|list10 = >>>>>>>>请前往[[模板:人物/未创建词条人物列表]]查看。<<<<<<<<\n"

    template += "}}\n\n"
    template += "}}\n\n"
    template += "<noinclude>\n\n"
    template += "[[分類:相關內容目錄|{{PAGENAME}}]]</noinclude>\n"

    return template