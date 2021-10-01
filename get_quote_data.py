import requests
import json
import re
from unidecode import unidecode
from bs4 import BeautifulSoup as bs


def get_raw_data(name, page=1):
    url = f"https://www.goodreads.com/quotes/search?commit=Search&page={page}&q={name.replace(' ', '+')}&utf8=%E2%9C%93"
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    quotes = soup.find(class_="leftContainer")
    raw_quote_data = quotes.find_all(class_="quoteDetails")

    return raw_quote_data


def extract_quotes_metadata(raw_quote_data):
    quote_list = []
    for raw_quote in raw_quote_data:
        quote_data = {}

        # get quote
        quote = raw_quote.find("div", class_="quoteText")
        quote = unidecode(quote.text.strip())
        quote = re.match('\"(.+?)\"', quote)

        # get author
        author = raw_quote.find(class_="authorOrTitle").text.replace(
            ",", "").strip()

        # get title
        title = raw_quote.find(class_="authorOrTitle")
        title = title.nextSibling.nextSibling.text

        # append data to list
        quote_data['title'] = title.strip()
        quote_data['author'] = author.strip()
        quote_data['quote'] = quote.group(1).strip()

        quote_list.append(quote_data)

    return quote_list


def main():

    # for testing
    name = 'golden son'
    data = get_raw_data(name)
    lst = extract_quotes_metadata(data)
    with open('test.txt', 'w') as f:
        for entry in lst:
            if name.lower().strip() == entry['title'].lower().strip():
                f.write(json.dumps(entry, indent=2) + '\n')


if __name__ == "__main__":
    main()
