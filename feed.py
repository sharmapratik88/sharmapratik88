import time
import re
from os import path
import requests
from bs4 import BeautifulSoup


def open_readme():
    directory = path.abspath(path.dirname(__file__))
    with open(path.join(directory, 'README.md'), encoding='utf-8') as f:
        readme = f.read()
    return readme


def write_readme(updated):
    directory = path.abspath(path.dirname(__file__))
    with open(path.join(directory, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(updated)


def modify_readme(readme, text, identifier=''):
    start_tag = f'{identifier}_START'
    end_tag = f'{identifier}_END'
    return re.sub(f'(?<=<!-- {start_tag} -->).*?(?=<!-- {end_tag} -->)', text, readme, flags=re.DOTALL)


def fetch_posts_from_sitemap(feed):
    # Fetch and parse the sitemap
    response = requests.get(feed)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract URLs and last modified dates
    posts = []
    for url_tag in soup.find_all('url'):
        loc = url_tag.find('loc').text
        lastmod = url_tag.find('lastmod').text if url_tag.find('lastmod') else 'Not provided'

        # Fetch the page and extract the H1 tag
        page_response = requests.get(loc)
        page_soup = BeautifulSoup(page_response.content, 'html.parser')
        h1_tag = page_soup.find('h1')
        title = h1_tag.text.strip() if h1_tag else 'No H1 tag found'

        # Append formatted string to posts list
        posts.append(f"- [{title}]({loc}) ({lastmod})")

    # Return formatted string of posts
    return '\n' + '\n'.join(posts) + '\n'


def main():
    site_url = 'https://pratikdsharma.com/sitemap-posts.xml'
    posts = fetch_posts_from_sitemap(site_url)
    original = open_readme()
    updated = modify_readme(original, posts, identifier='BLOG')
    write_readme(updated)


if __name__ == '__main__':
    main()
