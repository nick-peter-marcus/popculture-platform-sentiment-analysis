import argparse
import asyncio
import aiohttp as aiohttp
import pandas as pd
import time
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm.asyncio import tqdm


# Parse number of pages / page range to be scraped from cmd
parser = argparse.ArgumentParser()
parser.add_argument('-p', action='store', 
                    dest='pages_to_scrape',
                    default=1,
                    help='Store numbers of pages that should be scraped')
parser.add_argument('-ps', action='store', 
                    dest='page_start',
                    default=1,
                    help='Store page number scraping should start')
parser.add_argument('-pe', action='store', 
                    dest='page_end',
                    default=1,
                    help='Store page number scraping should end')

args = parser.parse_args()
N_PAGES = int(args.pages_to_scrape)
PAGE_START = int(args.page_start)
PAGE_END = int(args.page_end)

if N_PAGES > 1:
    PAGE_RANGE = range(1, N_PAGES)
else:
    PAGE_RANGE = range(PAGE_START, PAGE_END+1)


HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/131.0.0.0 Safari/537.36')
}


async def fetch(url):
    """ Sends GET request to URL, returns response as str """
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        try:
            async with session.get(url, max_redirects=30) as resp:
                return await resp.text()
        except asyncio.TimeoutError:
                return None


async def scrape_main_page(link, posts_dict):
    """ Scrapes content from main page where posts are listed """

    content = await fetch(link)
    # If content is None due to exception error in fetch(),
    #  return posts_dict unchanged.
    if not content:
        return posts_dict
    
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


async def scrape_posts(id, link, posts_dict):
    """ Scrapes content from individual post pages """

    content = await fetch(link)
    # If content is None due to exception error in fetch(),
    #  return updated posts_dict depicting error.
    if not content:
        posts_dict[id].update({"error_occured": True})
        return posts_dict
    
    soup = BeautifulSoup(content, 'html.parser')

    post_categories_date = soup.find("div", class_="categories-list")
    if post_categories_date:
        post_categories = post_categories_date.find("div", class_="categories").text.strip()
        post_date = post_categories_date.find("div", class_="post-dates").text.strip()
        error_occured = False
    else:
        post_categories, post_date = (None, None)
        error_occured = True

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
       "error_occured": error_occured,
    }}

    posts_dict[id].update(post_detail_dict[id])

    return posts_dict


async def main():
    start_time = time.time()

    BASE_URL = "https://www.boredpanda.com/page/"
    
    main_page_urls = [f"{BASE_URL}{p}/" for p in PAGE_RANGE]

    posts_dict = {}

    print("Start scraping main pages")
    main_page_tasks = []
    for link in main_page_urls:
        main_page_tasks.append(scrape_main_page(link, posts_dict))
    await tqdm.gather(*main_page_tasks)
    print("Scraping main pages completed")

    print("Start scraping individual post pages")
    post_page_urls = {key: values["link"] for key, values in posts_dict.items()}
    posts_page_tasks = []
    for id, link in post_page_urls.items():
        posts_page_tasks.append(scrape_posts(id, link, posts_dict))
    await tqdm.gather(*posts_page_tasks)
    print("Scraping individual post pages completed")
    
    # Store data as dataframe in csv and excel formats.
    df = pd.DataFrame(posts_dict).T
    time_created = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if len(PAGE_RANGE) > 1:
        pages = f"pages_{PAGE_RANGE[0]}-{PAGE_RANGE[-1]}"
    else: 
        pages = f"page_{PAGE_RANGE[0]}"
    file_name = f"scraping_result_{pages}_{time_created}"
    df.to_excel(f"excel/{file_name}.xlsx", header=True, index=True)
    df.to_csv(f"csv/{file_name}.csv", header=True, index=True)

    end_time = time.time()
    time_past = round(end_time - start_time)
    print(f"Total execution time: {time_past} seconds")


if __name__ == '__main__':
    asyncio.run(main())