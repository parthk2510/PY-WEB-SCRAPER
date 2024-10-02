import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class WebCrawler:
    def __init__(self, start_url, max_pages=10):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited_pages = set()

    def crawl(self):
        pages_to_visit = [self.start_url]

        while pages_to_visit and len(self.visited_pages) < self.max_pages:
            current_url = pages_to_visit.pop(0)
            if current_url in self.visited_pages:
                continue

            print(f"Visiting: {current_url}")
            try:
                response = requests.get(current_url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')
                self.visited_pages.add(current_url)

                for link in soup.find_all('a', href=True):
                    url = urljoin(current_url, link['href'])
                    if url not in self.visited_pages:
                        pages_to_visit.append(url)

            except requests.RequestException as e:
                print(f"Failed to fetch {current_url}: {e}")

        print(f"Visited {len(self.visited_pages)} pages.")


if __name__ == "__main__":
    start_url = "https://example.com"  # Default URL
    crawler = WebCrawler(start_url)
    crawler.crawl()
