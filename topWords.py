import requests
from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt

def fetch_text(url):
    response = requests.get(url)
    response.raise_for_status()  # Перевірка на успішний запит
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()

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

if __name__ == "__main__":
    url = 'https://en.wikipedia.org/wiki/JavaScript'
    text = fetch_text(url)
    word_counts = map_reduce(text)
    visualize_top_words(word_counts, top_n=20)
