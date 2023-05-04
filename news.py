import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def get_page_content(url):
    response = requests.get(url)
    return response.content

def extract_headlines(content, source):
    soup = BeautifulSoup(content, 'html.parser')
    headlines = []

    if source == 'CNN':
        for headline in soup.find_all('span', attrs={'data-editable': 'headline'}):
            headlines.append(headline.get_text(strip=True))
    elif source == 'BBC':
        for headline in soup.find_all('a', class_='gs-c-promo-heading'):
            headlines.append(headline.get_text(strip=True))
    else:
        print("Unsupported source")
    
    return headlines
def main():
    sources = [
        {'name': 'CNN', 'url': 'https://edition.cnn.com/world'},
        {'name': 'BBC', 'url': 'https://www.bbc.com/news/world'}
    ]

    all_headlines = []
    for source in sources:
        content = get_page_content(source['url'])
        headlines = extract_headlines(content, source['name'])

        for headline in headlines:
            all_headlines.append({
                'headline': headline,
                'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                'source': source['name'],
            })

    df = pd.DataFrame(all_headlines)
    print(df)

    # Save the DataFrame to a CSV file
    df.to_csv('news_headlines.cs', index=False)


if __name__ == '__main__':
    main()