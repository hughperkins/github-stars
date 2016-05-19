#!/home/ubuntu/env/bin/python
import requests
import sys
import os
import yaml
from os import path
from os.path import join
from docopt import docopt
from pyquery import PyQuery

script_dir = path.dirname(path.realpath(__file__))
with open(join(script_dir, 'config.yaml'), 'r') as f:
  config = yaml.load(f)

r = requests.get('https://github.com/%s?tab=repositories' % config['github_username'])
c = r.content

print('Content-type: text/plain')
print('')
d = PyQuery(c)
d = d('.repo-list-item')
countByName = {}
for thing in d:
  repo_name = PyQuery(thing)('.repo-list-name')('a').text().lower()
  count = 0
  for statItem in PyQuery(thing)('.repo-list-stat-item'):
    si = PyQuery(statItem)
    href = si.attr('href')
    if href.endswith('/stargazers'):
      count = int(si.text())
  if count > 0:
    countByName[repo_name] = count

sortedKeys = list(countByName.keys())
sortedKeys.sort()
for name in sortedKeys:
  print(name, countByName[name])

