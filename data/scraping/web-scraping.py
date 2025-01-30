import pandas as pd
import requests
import time
from bs4 import BeautifulSoup


def fetch(url):
    """ Request URL, returns html document """
    resp = requests.get(url)
    return resp.text


def scrape_main_page(link, posts_dict):
    """ Scrapes content from main page where posts are listed """

    content = fetch(link)
    soup = BeautifulSoup(content, 'html.parser')

    posts = soup.find_all("article", class_="post")
            
    # Iterate through each post on the current page loaded.
    for post in posts:
        # Get post id. If already existent in dict, add suffix.
        post_id = post["data-post-id"]
        while post_id in posts_dict:
            post_id += "_2"

        current_post_dict = {post_id: {
                "title": post.find("a", class_="title").text.strip(),
                "voting": int(post.find("p", class_="votes-text").text.strip()),
                "nr_comments": (int(post.find("p", class_="comment-text").text.strip())
                                if post.find("p", class_="comment-text") else None),
                "has_experimental_title": post["data-content-experiment-enabled"],
                "page_link": link,
                "link": post.find("a")["href"]
            }}
        posts_dict.update(current_post_dict)
        
    return posts_dict


def scrape_posts(id, link, posts_dict):
    """ Scrapes content from individual post pages """

    content = fetch(link)
    soup = BeautifulSoup(content, 'html.parser')

    post_categories_date = soup.find("div", class_="categories-list")
    post_categories = post_categories_date.find("div", class_="categories").text.strip()
    post_date = post_categories_date.find("div", class_="post-dates").text.strip()

    authors_ls = soup.find_all("a", class_="author")
    authors = " | ".join([a.text for a in authors_ls])
    authors_role_ls = soup.find_all("p", class_="author-role")
    authors_role = " | ".join([ar.text for ar in authors_role_ls])

    posts_total = soup.find_all("div", class_="open-list-header")
    posts_shown = soup.find_all("div", class_="open-list-item open-list-block clearfix")
    nr_postings_total = len(posts_total)
    nr_postings_shown = len(posts_shown)
    
    post_detail_dict = {id: {
       "date_posted": post_date,
       "categories": post_categories,
       "nr_postings_total": nr_postings_total,
       "nr_postings_shown": nr_postings_shown,
       "authors": authors,
       "authors_role": authors_role,
    }}

    posts_dict[id].update(post_detail_dict[id])

    return posts_dict


def main():
    start_time = time.time()

    BASE_URL = "https://www.boredpanda.com/page/"
    pages_to_scrape = 5
    main_page_urls = [f"{BASE_URL}{p}/" for p in range(1, pages_to_scrape+1)]

    posts_dict = {}

    print("Start scraping main pages")
    for link in main_page_urls:
        scrape_main_page(link, posts_dict)
    print("Scraping main pages completed")

    print("Start scraping individual post pages")
    post_page_urls = {key: values["link"] for key, values in posts_dict.items()}
    for id, link in post_page_urls.items():
        scrape_posts(id, link, posts_dict)
    print("Scraping individual post pages completed")
    
    df = pd.DataFrame(posts_dict).T
    df.to_excel("scraping_test2.xlsx", header=True, index=True)

    end_time = time.time()
    time_past = round(end_time - start_time)
    print(f"Total execution time: {time_past} seconds")

if __name__ == '__main__':
    main()