#!/usr/bin/env python
import requests
import yaml
from os import path
from os.path import join
from pyquery import PyQuery


def parse_page(page_html):
    d = PyQuery(page_html)
    res = {}
    nodes_found = False
    for a_node in d('a').items():
        if a_node.attr['aria-label'] == 'Stargazers' or a_node.find('svg').attr['aria-label'] == 'star':
            nodes_found = True
            href = a_node.attr['href']
            repo_name = href.split('/')[2]
            stars = int(a_node.text().strip())
            if stars > 0:
                res[repo_name] = stars
    return res, nodes_found


if __name__ == '__main__':
    script_dir = path.dirname(path.realpath(__file__))
    with open(join(script_dir, 'config.yaml'), 'r') as f:
        config = yaml.load(f)

    page = 1
    nodes_found = True
    countByName = {}
    while nodes_found:
        r = requests.get('https://github.com/%s?tab=repositories&page=%s' % (config['github_username'], page))
        c = r.content.decode('utf-8').replace('\u00ae', '(R)').replace('\u2122', '(TM)')

        res, nodes_found = parse_page(c)
        for repo, count in res.items():
            countByName[repo] = count

        page += 1
        if page > 20:
            print('pages went off end...')
            break

    print('Content-type: text/plain')
    print('')
    sortedKeys = list(countByName.keys())
    sortedKeys.sort(key=lambda x: x.lower())
    for name in sortedKeys:
        print('%s %s' % (name, countByName[name]))
