import argparse
import os
import os.path as osp
from urllib.request import urlopen
import bs4
import hashlib
import json
import re

def parse_config_file(config_file):
    with open(f'{config_file}', 'r') as f:
        config_json = json.load(f)
        return config_json['urls']

def get_page_source(url, cache_dir):
    movie_hash = hashlib.sha1(url.encode("UTF-8")).hexdigest()

    if osp.isdir(cache_dir):
        movie_file_path = osp.join(cache_dir, movie_hash)
        if osp.isfile(movie_file_path):
            cache_file = open(movie_file_path, 'r')
            return cache_file
        else:
            return get_html_file(url, cache_dir)
    else:
        os.makedirs(cache_dir)
        return get_html_file(url, cache_dir)

def get_html_file(url, cache_dir):
    review_page = urlopen(url).read()

    movie_hash = hashlib.sha1(url.encode("UTF-8")).hexdigest()
    movie_file_path = osp.join(cache_dir, movie_hash)

    with open(movie_file_path, 'wb') as f:
        f.write(review_page)

    return review_page

def get_reviews(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    reviews = soup.findAll('div', 'imdb-user-review')

    result = []

    for review in reviews:
        review_div = review.find('div', 'text show-more__control')
        helpfulness_div = review.find('div', 'actions text-muted')

        helpfulness_array = helpfulness_div.text.split()
        helpful = re.sub(',', '', helpfulness_array[0])
        total = re.sub(',', '', helpfulness_array[3])

        if float(total) == 0:
            continue

        helpfulness = float(helpful) / float(total)

        result.append({
            'review': review_div.text,
            'helpfulness': helpfulness
        })

    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_file')
    parser.add_argument('-o', '--output_file')

    args = parser.parse_args()

    urls = parse_config_file(args.config_file)
    count = 0

    with open(args.output_file, 'w') as f:
        for url in urls:
            html_file = get_page_source(url, 'cache')
            json_file = get_reviews(html_file)
            count += len(json_file)

            for entry in json_file:
                json.dump(entry, f)
                f.write('\n')

    print(count)

if __name__ == '__main__':
    main()
