#!/usr/bin/env python
import requests
import yaml
from os import path
from os.path import join
from pyquery import PyQuery

script_dir = path.dirname(path.realpath(__file__))
with open(join(script_dir, 'config.yaml'), 'r') as f:
    config = yaml.load(f)

page = 1
nodesfound = True
countByName = {}
while nodesfound:
    nodesfound = False
    r = requests.get('https://github.com/%s?tab=repositories&page=%s' % (config['github_username'], page))
    c = r.content.decode('utf-8').replace('\u00ae', '(R)').replace('\u2122', '(TM)')

    d = PyQuery(c)
    for a_node in d('a'):
        if 'aria-label' not in a_node.keys():
            continue
        ariaLabel = a_node.get('aria-label')
        if ariaLabel != 'Stargazers':
            continue
        nodesfound = True
        href = a_node.get('href')
        repo_name = href.split('/')[2]
        stars = int(a_node.text_content().strip())
        if stars > 0:
            countByName[repo_name] = stars
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
