# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2026 Xie Youtian
import mwclient
import time
import logging
from typing import Optional

def send_template(site: mwclient.Site, template: str, page_title: str = "模板:人物", 
                  summary: Optional[str] = None, max_retries: int = 3) -> bool:
    """
    将生成的模板推送到WikiFur页面。
    
    Args:
        site: 已登录的mwclient.Site对象
        template: 要推送的模板内容
        page_title: 目标页面标题（默认为"模板:人物"）
        summary: 编辑摘要（默认为自动生成）
        max_retries: 最大重试次数（遇到编辑冲突时）
    
    Returns:
        bool: 推送是否成功
    """
    import logging
    logging.info(f"  正在准备推送模板到页面 '{page_title}'...")
    
    if summary is None:
        summary = "更新人物模板（自动生成）"
    
    page = site.pages[page_title]
    
    for attempt in range(max_retries):
        try:
            logging.info(f"  正在获取页面当前内容...")
            # 获取页面当前内容
            current_content = page.text()
            
            # 检查内容是否相同
            if current_content == template:
                logging.info(f"  页面 '{page_title}' 内容未更改，无需更新。")
                return True
            
            logging.info(f"  正在向页面 '{page_title}' 推送新内容...")
            # 编辑页面
            result = page.edit(template, summary=summary)
            
            if result.get('result') == 'Success':
                logging.info(f"  成功更新页面 '{page_title}'")
                return True
            else:
                logging.error(f"  更新页面 '{page_title}' 失败: {result}")
                return False
                
        except mwclient.errors.EditError as e:
            if 'editconflict' in str(e).lower() and attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                logging.warning(f"  编辑冲突，等待 {wait_time} 秒后重试 (尝试 {attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
                continue
            else:
                logging.error(f"  编辑页面 '{page_title}' 时出错: {e}")
                return False
        except Exception as e:
            logging.error(f"  更新页面 '{page_title}' 时出现意外错误: {e}")
            return False
    
    return False

def send_template_from_stdin(site: mwclient.Site) -> bool:
    """
    从标准输入读取模板内容并推送到WikiFur。
    
    Args:
        site: 已登录的mwclient.Site对象
    
    Returns:
        bool: 推送是否成功
    """
    import sys
    
    logging.info("从标准输入读取模板内容...")
    template = sys.stdin.read()
    
    if not template:
        logging.error("错误: 标准输入为空")
        return False
    
    return send_template(site, template)