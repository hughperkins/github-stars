#!/home/ubuntu/env/bin/python
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
    # print('page', page)
    nodesfound = False
    r = requests.get('https://github.com/%s?tab=repositories&page=%s' % (config['github_username'], page))
    c = r.content

    d = PyQuery(c)
    # d = d('.repo-list-item')
    d = d('.source')
    for thing in d:
        nodesfound = True
        # print('thing', thing)
        repo_name = PyQuery(thing)('.d-table')('.d-table-cell')('.f4')('a').text().lower()
        # print('repo_name', repo_name)
        count = 0
        countanode = PyQuery(thing)('.d-table')('.col-1')('a')
        # print('countanode', countanode)
        count = int(countanode.text())
        # si = PyQuery(statItem)
        # href = si.attr('href')
        # if href.endswith('/stargazers'):
        #   count = int(si.text())
        # print('count', count)
        if count > 0:
            countByName[repo_name] = count
    page += 1

print('Content-type: text/plain')
print('')
sortedKeys = list(countByName.keys())
sortedKeys.sort()
for name in sortedKeys:
    print(name, countByName[name])
