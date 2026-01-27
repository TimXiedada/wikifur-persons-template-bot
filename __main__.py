# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2026 Xie Youtian
import mwclient
import os
import sys
import configparser
import argparse
import difflib
import logging

from get import get_page_list
from convert import get_pinyinized_page_list, generate_template
from send import send_template

def init_site():
    """初始化并登录到WikiFur站点"""
    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")
    
    site = mwclient.Site(config["Location"]["domain"])
    site.login(username=config["Credential"]["username"], password=config["Credential"]["password"])
    return site

def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="生成并可选地推送人物模板到WikiFur")
    parser.add_argument("--send", action="store_true", help="推送模板到WikiFur（默认为仅输出到stdout）")
    parser.add_argument("--dry-run", action="store_true", help="显示与当前页面内容的差异但不推送")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细日志")
    parser.add_argument("-q", "--quiet", action="store_true", help="只显示错误日志")
    parser.add_argument("--page", default="模板:人物", help="目标页面标题（默认为'模板:人物'）")
    parser.add_argument("--summary", help="编辑摘要（默认为自动生成）")
    
    # 检查是否需要显示帮助
    if "--help" in argv or "-h" in argv:
        parser.parse_args(argv[1:])  # 这会打印帮助信息并退出
        return 0
    
    args = parser.parse_args(argv[1:])
    
    # 配置日志
    if args.verbose:
        level = logging.DEBUG
    elif args.quiet:
        level = logging.WARNING
    else:
        level = logging.INFO
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s'
    )
    
    logging.info("【第1步】正在初始化与WikiFur站点的连接...")
    # 初始化站点连接
    try:
        site = init_site()
        logging.info("【第1步】站点连接初始化完成")
    except Exception as e:
        logging.error(f"无法连接到WikiFur: {e}")
        logging.error("请检查config.ini文件中的凭证和网络连接。")
        return 1
    
    logging.info("【第2步】开始获取人物页面列表...")
    page_list_tagged = get_page_list(site)
    logging.info(f"【第2步】已获取 {len(page_list_tagged)} 个人物页面信息")
    
    logging.info("【第3步】开始将页面标题转换为拼音...")
    page_list_pinyinized = get_pinyinized_page_list(page_list_tagged)
    logging.info("【第3步】页面标题拼音转换完成")
    
    logging.info("【第4步】正在生成人物模板...")
    template = generate_template(page_list_pinyinized)
    logging.info("【第4步】人物模板生成完成")
    
    # 干运行模式：显示差异但不推送
    if args.dry_run and args.send:
        logging.warning("--dry-run 与 --send 同时指定，将忽略 --dry-run 并推送更新。")
    
    # 干运行模式：显示差异但不推送
    if args.dry_run and not args.send:
        logging.info(f"【第5步】正在获取当前页面内容 '{args.page}'...")
        try:
            current_content = site.pages[args.page].text()
        except Exception as e:
            logging.error(f"无法获取当前页面内容: {e}")
            return 1
        if current_content == template:
            logging.info("当前页面内容与生成的模板相同，无需更新。")
        else:
            logging.info("差异如下（--- 当前页面，+++ 生成模板）:")
            diff = difflib.unified_diff(
                current_content.splitlines(keepends=True),
                template.splitlines(keepends=True),
                fromfile='当前页面',
                tofile='生成模板',
                lineterm=''
            )
            sys.stdout.writelines(diff)
        return 0

    if args.send:
        logging.info("【第5步】正在推送模板到WikiFur...")
        success = send_template(site, template, page_title=args.page, summary=args.summary)
        if success:
            logging.info("【第5步】模板推送完成")
            return 0
        else:
            logging.error("模板推送失败")
            return 1
    else:
        # 默认行为：输出到stdout
        logging.info("【第5步】输出生成的模板到控制台")
        print(template)
        return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))