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
    nodesfound = False
    r = requests.get('https://github.com/%s?tab=repositories&page=%s' % (config['github_username'], page))
    c = r.content.decode('utf-8').replace('\u00ae', '(R)').replace('\u2122', '(TM)')

    d = PyQuery(c)
    d = d('.source')
    for thing in d:
        nodesfound = True
        repo_name = PyQuery(thing)('.f4')('a').text().lower()
        count = 0
        countanode = PyQuery(thing)('.col-1')('a')
        if countanode.text() == '':
            continue
        count = int(countanode.text())
        if count > 0:
            countByName[repo_name] = count
    page += 1

print('Content-type: text/plain')
print('')
sortedKeys = list(countByName.keys())
sortedKeys.sort()
for name in sortedKeys:
    print('%s %s' % (name, countByName[name]))
