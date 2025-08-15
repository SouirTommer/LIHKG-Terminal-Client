import requests
import json
import re

BASE_URL = "https://lihkg.com/api_v2/"
HEADERS = {
    "X-LI-DEVICE": "a1b2c3d4e5f6789012345678901234567890abcd",
    "X-LI-DEVICE-TYPE": "android",
    "User-Agent": "LIHKG/16.0.4 Android/9.0.0 Google/Pixel XL",
    "orginal": "https://lihkg.com",
    "referer": "https://lihkg.com/category/1"
}

def clean_html(raw_html):
    # Remove HTML tags from the message
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_property():
    url = BASE_URL + "system/property"
    resp = requests.get(url, headers=HEADERS)
    data = resp.json()
    categories = data["response"]["category_list"]
    print("Category List:")
    # Print two categories per line
    for i in range(0, len(categories), 2):
        left = f"{categories[i]['cat_id']} - {categories[i]['name']}"
        right = ""
        if i + 1 < len(categories):
            right = f"{categories[i+1]['cat_id']} - {categories[i+1]['name']}"
        print(f"{left:<25} {right}")
    return categories

def get_thread_list(cat_id, page=1, count=10):
    url = BASE_URL + f"thread/latest?cat_id={cat_id}&page={page}&count={count}&type=now"
    resp = requests.get(url, headers=HEADERS)
    data = resp.json()
    threads = data["response"]["items"]
    print("\nThread List:")
    for idx, thread in enumerate(threads):
        print(f"[{idx}] Thread ID: {thread['thread_id']} Title: {thread['title']}")
    return threads

def get_thread_content(thread_id, page=1, order='reply_time'):
    url = BASE_URL + f"thread/{thread_id}/page/{page}?order={order}"
    resp = requests.get(url, headers=HEADERS)
    data = resp.json()
    print("\nPost Content:")
    posts = data["response"]["item_data"]
    if not posts:
        print("No post found")
        return []
    for post in posts:
        nickname = post.get('user_nickname', '')
        raw_msg = post.get("msg", "[No content]")
        text_msg = clean_html(raw_msg)
        print("-" * 40)
        print(f"{nickname}: \n{text_msg}")
    print("-" * 40)
    return posts

def main():
    categories = get_property()
    cat_id = input("Enter category ID: ")
    threads = get_thread_list(cat_id)
    idx = input("\nEnter thread index (e.g. 0): ")
    try:
        idx = int(idx)
        thread_id = threads[idx]['thread_id']
        get_thread_content(thread_id)
    except (ValueError, IndexError):
        print("Invalid index, please try again.")

if __name__ == "__main__":
    main()