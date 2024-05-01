import requests
from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

def map_reduce(text):
    words = text.split()
    map_results = map(lambda word: (word.lower().strip('.,!;:"\'()[]{}'), 1), words)
    reduce_results = Counter()
    for word, count in map_results:
        reduce_results[word] += count
    return reduce_results

def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)
    plt.figure(figsize=(10, 8))
    plt.bar(words, counts)
    plt.xlabel('Слова')
    plt.ylabel('Частота')
    plt.title('Топ-слова за частотою використання')
    plt.xticks(rotation=45)
    plt.show()

def main(urls, top_n=20):
    texts = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(fetch_text, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                text = future.result()
                texts.append(text)
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")

    combined_text = " ".join(texts)
    word_counts = map_reduce(combined_text)
    visualize_top_words(word_counts, top_n=top_n)

if __name__ == "__main__":
    urls = [
        'https://en.wikipedia.org/wiki/JavaScript',
        'https://en.wikipedia.org/wiki/Python_(programming_language)',
        'https://en.wikipedia.org/wiki/Java_(programming_language)'
    ]
    main(urls, top_n=20)
