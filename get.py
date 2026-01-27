# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2026 Xie Youtian
import mwclient
from typing import TypedDict, NotRequired

class PageInfo(TypedDict):
    page_id: int
    page_title: str
    user_page: bool
    deceased: NotRequired[bool]

def get_page_list(site: mwclient.Site) -> list[PageInfo]:
    import logging
    logging.info("  正在获取'人物'分类中的页面列表...")
    
    page_list_tagged: list = []
    cat = site.categories["人物"]
    cat_deceased = site.categories["逝世的人物"]

    # Collect deceased pages first and store them
    deceased_pages_info = {}  # Dictionary to store page info by (title, user_page)

    logging.info("  正在处理'逝世的人物'分类...")
    for page in cat_deceased:
        # Skip subpages (pages with "/" in the title)
        if page.namespace in [0, 2] and "/" not in page.page_title:
            user_page = page.namespace == 2
            key = (page.page_title, user_page)
            deceased_pages_info[key] = {
                "page_id": page.pageid,
                "page_title": page.page_title,
                "user_page": user_page,
                "deceased": True
            }

    existing_pages = set()  # (title, user_page)

    # Process all person pages
    logging.info("  正在处理'人物'分类中的所有页面...")
    for page in cat:
        # Skip subpages (pages with "/" in the title)
        if page.namespace in [0, 2] and "/" not in page.page_title:
            user_page = page.namespace == 2
            key = (page.page_title, user_page)
            if key in existing_pages:
                continue  # 已经处理过，跳过重复
            is_deceased = key in deceased_pages_info
            page_info: PageInfo = {
                "page_id": page.pageid,
                "page_title": page.page_title,
                "user_page": user_page,
                "deceased": is_deceased
            }
            page_list_tagged.append(page_info)
            existing_pages.add(key)

    # Add any deceased pages that weren't in the main category
    for key, page_info in deceased_pages_info.items():
        if key not in existing_pages:
            page_list_tagged.append(page_info)
            existing_pages.add(key)

    logging.info(f"  成功获取 {len(page_list_tagged)} 个页面信息")
    return page_list_tagged