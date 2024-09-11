from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os

# Global variable to track visited sites
visited_sites = set()


def get_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    try:
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')

        links = []
        for link in soup.find_all('a'):
            link_url = link.get('href')
            print(link_url)

            if link_url is not None:
                # Convert relative URLs to absolute URLs
                absolute_url = urljoin(url, link_url)
                if ('docs.oracle.com/en/cloud/saas/transportation/planning' in absolute_url and
                        absolute_url not in visited_sites):
                    links.append(absolute_url + '\n')
                    visited_sites.add(absolute_url)

        write_to_file(links)
        return links
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return []


def write_to_file(links):
    try:
        with open('./data_doc/data5.txt', 'a') as f:
            f.writelines(links)
    except Exception as e:
        print(f"Error writing to file: {e}")


def get_all_links(url, depth=1):
    if depth > 3:  # Limit the recursion depth to avoid infinite loops
        return
    for link in get_links(url):
        get_all_links(link.strip(), depth + 1)


if __name__ == "__main__":
    if not os.path.exists('links.txt'):
        print("links.txt file not found.")
        exit()

    with open('links.txt', 'r') as file:
        urls = file.readlines()

    for r in urls:
        r = r.strip().split('#')[0]
        if r:
            write_to_file([r + '\n'])
            visited_sites.add(r)
            get_all_links(r)

    print("Processing completed.")
