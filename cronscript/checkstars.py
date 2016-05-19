#!/home/hughperkins/env27/bin/python

from __future__ import print_function

import requests
import os
import sys
import yaml
from os import path
from os.path import join

oldList = ""
try:
    with open('oldstars.txt', 'r') as f:
        oldList = f.read()
except:
    pass

script_dir = path.dirname(path.realpath(__file__))
with open(join(script_dir, 'config.yaml'), 'r') as f:
  config = yaml.load(f)

r = requests.get(config['scanservice_url'])
c = r.content.decode('utf-8')
# print('c', c)
newList = c
if newList != oldList:
  old = {}
  new = {}
  for line in oldList.split('\n'):
    split_line = line.split(' ')
    if len(split_line) < 2:
      continue
    repo = split_line[0]
    count = int(split_line[1])
    old[repo] = count
  for line in newList.split('\n'):
    split_line = line.split(' ')
    if len(split_line) < 2:
      continue
    repo = split_line[0]
    count = int(split_line[1])
    new[repo] = count
  for repo, count in new.items():
    oldCount = old.get(repo, 0)
    if count != oldCount:
      print('%s %s => %s' % (repo, oldCount, count))

if newList != oldList and newList != '':
    with open('oldstars.txt', 'w') as f:
        f.write(newList)

