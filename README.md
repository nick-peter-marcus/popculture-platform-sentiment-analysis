# Introduction
In this project, I explore the sentiment of post titles from a pop culture/meme website called Bored Panda.

According to the [page’s meta description](https://www.boredpanda.com/):
<blockquote>"Bored Panda is a leading art and pop culture magazine which is viewed nearly 100 million times every month. Our mission is to spread good news and highlight top artists from around the world."</blockquote>

In a [New York Times article](https://www.nytimes.com/2017/11/30/technology/facebook-bored-panda.html), the site has further been described as a website that 
<blockquote>"[publishes] user-generated content from Reddit, Instagram, Twitter and other social platforms and repackage[s] it with tempting headlines. But by focusing on art, photography and other creative pursuits, and by studiously sticking to the kind of apolitical content that few people object to, Bored Panda has steadily built a feel-good, escapist empire."</blockquote>

I personally found myself visiting this website frequently for amusement and killing time. However, I noticed that despite the described "feel-good" nature of this site, posts and their respective titles became more negative and provocative over time. While there still exist many positive posts about cute animals and funny memes, it seemed that most posts nowadays focus on frustrating topics of family disputes and AITA-posts.

This can potentially be drawn back to the theory, that provoking stories yield more interaction with the posts in form of comments and likes, and thus generate more traffic on the website.

In order to quantitatively investigate the feeling of this website's perceived steady decline in positiveness, I decided to analyze the postings for their sentiment.

# Project Scope
This project spans the following steps:

## 0. Forming hypotheses
My hypotheses are that postings with provoking or negatively associated titles yield:
- a) more comments and
- b) more negative voting

## 1. Data retrieval
The data was collected on 01/27/2025 by scraping titles from the first 100 pages of boredpanda.com. The associated posts were individually accessed to gather voting, the number of comments, posting date, as well as authorships. Scraping was performed by asyncio and parsed with BeautifulSoup.

## 2. Data Cleaning
From the originally 2135 posts scraped, 119 were flagged as duplicates and dropped from the data. Additionally, 132 posts were removed for being advertisements, resulting in 1884 posts used for this analysis.

## 3. Data Analysis
**Sentiment**<br>
The Vader sentiment analyzer yielded the following share of sentiment groups based on compound:
- Positive sentiment (compound > 0): n=833 (44%)
- Negative sentiment (compound < 0): n=769 (41%)
- Neutral sentiment (compound = 0): n=282 (15%)
<p align="center">
  <img src="https://github.com/nick-peter-marcus/popculture-platform-sentiment-analysis/blob/main/images/sentiment.png" alt="sentiment" width="200"/>
</p>

**Voting, number of comments, number of authors and number of postings**<br>
An F-Test showed that the three groups significantly differ in terms of community voting, the number of comments, the number of authors, and the number of postings within a single post (e.g. compilations).

Exploring differences between the individual groups, Tukey's HSD Test concluded that positive and negative posts significantly differ in all abovementioned variables.
<p align="center">
  <img src="https://github.com/nick-peter-marcus/popculture-platform-sentiment-analysis/blob/main/images/tukeys_hsd_test.png" alt="tukeys_hsd_test" width="500"/>
</p>
<p align="center">
  <img src="https://github.com/nick-peter-marcus/popculture-platform-sentiment-analysis/blob/main/images/num_cols.png" alt="num_cols" width="500"/>
</p>

**Categories**<br>
Amongst the categories with the largest share of positive posts are Jokes, Comics, Funny Memes, Dogs/Animals and Wholesome. In terms of total frequency, those categories are rather low in numbers. 
On the bottom of the positivity-share we find the categories Relationship, Social Issues, Entitled people and Family. For those categories, we observe higher numbers of occurrence.
<p align="center">
  <img src="https://github.com/nick-peter-marcus/popculture-platform-sentiment-analysis/blob/main/images/categories.png" alt="categories" width="500"/>
</p>

**Date**<br>
Visually, no distinct trend can be found for postings over time. This is a potential shortcoming of this analysis. The dates of upload that are provided on the posts' pages only go back as far as 10/31/2024. Including more data from posts before that date could gain further insights of the distribution over time.
<p align="center">
  <img src="https://github.com/nick-peter-marcus/popculture-platform-sentiment-analysis/blob/main/images/date.png" alt="date" width="500"/>
</p>

**Titles**<br>
Looking at a word cloud depicting the most common words present in the posts' titles, we find some substantial differences. Titles classified as having positive sentiment contain words describing humor as well as animals: Comic, Memes, Hilarious, Share, Funny, Christmas, Cat, Dog.
Titles with negative sentiment, however, contain words associated with family/members (Family, Kid, Mom, Wife, Husband, MIL) and provocative behavior (Refuse, Leave)
<p align="center">
  <img src="https://github.com/nick-peter-marcus/popculture-platform-sentiment-analysis/blob/main/images/wordclouds.png" alt="wordclouds" width="700"/>
</p>

## 4. Conclusion
The statistical analyses show proof of the defined hypotheses: Positive and negative postings significantly differ in terms of community voting and the number of comments.