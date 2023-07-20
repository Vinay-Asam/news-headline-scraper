import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error getting content from {url}: {e}")
        return None

    return response.content

def extract_headlines(content, source):
    try:
        soup = BeautifulSoup(content, 'html.parser')
    except Exception as e:
        print(f"Error parsing content for {source}: {e}")
        return []

    headlines = []

    if source == 'CNN':
        for headline in soup.find_all('span', attrs={'data-editable': 'headline'}):
            headlines.append(headline.get_text(strip=True))
    elif source == 'BBC':
        for headline in soup.find_all('a', class_='gs-c-promo-heading'):
            headlines.append(headline.get_text(strip=True))
    else:
        print(f"Unsupported source: {source}")

    return headlines

def main():
    sources = [
        {'name': 'CNN', 'url': 'https://edition.cnn.com/world'},
        {'name': 'BBC', 'url': 'https://www.bbc.com/news/world'}
    ]

    all_headlines = []
    for source in sources:
        print(f"Getting content from {source['name']}...")
        content = get_page_content(source['url'])
        if content is None:
            print(f"Skipping {source['name']} due to error getting content.")
            continue

        print(f"Extracting headlines from {source['name']}...")
        headlines = extract_headlines(content, source['name'])
        if not headlines:
            print(f"No headlines found for {source['name']}.")
            continue

        for headline in headlines:
            all_headlines.append({
                'headline': headline,
                'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                'source': source['name'],
            })

    df = pd.DataFrame(all_headlines)
    print(df)

    # Save the DataFrame to a CSV file
    df.to_csv('news_headlines.csv', index=False)

if __name__ == '__main__':
    main()