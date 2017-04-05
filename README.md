# github-stars

Get emailed whenever someone stars one of your github repos.  No more excuses for compulsively `F5`ing
[https://github.com](https://github.com) :-D

## Example email

```
github-stars 2 => 3
```
Shows someone starred your repo called `github-stars`, and the number of stars changed from 2 to 3.

## Installation

How this works:
- have a Ubuntu box somewhere, with `scangitstars.py` in your `/usr/lib/cgi-bin` directory, on an apache box
  - create a python virtualenv at `/home/ubuntu/env` (or tweak the path in line 1 of `scangitstars.py`):
```
sudo apt-get install -y python-virtualenv libpython3-dev libxml2-dev libxslt1-dev
virtualenv -p python3 /home/ubuntu/env
source /home/ubuntu/env/bin/activate
pip install -r webservice/requirements.txt
```
  - copy `webservice/config.yaml.templ` to `config.yaml`, in the same directory as `scangitstars.py`, and customize it
  with your github username

- on another Ubuntu box (or could be the same one):
  - create a python virtualenv, and install `cronscript/requirements.txt`
```
sudo apt-get install -y python-virtualenv libpython3-dev libxml2-dev libxslt1-dev
virtualenv -p python3 /home/ubuntu/env
source /home/ubuntu/env/bin/activate
pip install -r cronscript/requirements.txt
```
(note that python2.7 is ok too)
- add an entry to crontab, to run this every 15 minutes or so, eg:
```
crontab -e
# put a line something like:
28,45,0,15 * * * * nice /home/yourusername/git/github-stars/cronscript/checkstars.py
# at the top, put a line like:
MAILTO="youremailaddress@gmail.com"
```
- now, whenever a change in the number of stars is detected, you'll get an email :-)
- note that the first time you run the script, you'll get an email too, saying that the number of stars
for each repo changed from 0 to whatever-it-is-now

## FAQ

* why not just have one script?
  * the cron script runs on dreamhost, which handles emailing for me (I mean, anything that goes to stdout in something called from cron, gets emailed automatically. Easy :-) )
    * dreamhost doesnt allow much cpu however, so ...
  * the cpu-intensive bit, which polls github etc, runs on an aws box
    * its probably possible to set up email on an aws box, but seems like a llloootttt of effort
* do you really need to check your github stars so compulsively? :-P
  * apparently I do :-D
* it only shows stars added, not removed
  * yeah, nothing worse than getting woken up in the morning by an email to tell you someone unstarred your repository. I'd rather not know I think. It's not like someone sends you a message saying "I unstarred it because X,Y,Z, ..."
* can I see who unstarred me?
  * why? so can email them etc?  I think I'd rather not know.  Technically doable though, but I dont intend to do that myself.
* why not make a website for this, and make money off it?
  * cos if hardly any users, wont make much money
  * if lots of users, github will probably either block me, or simply implement it themselves
  * I'm 'lazy :-D
* can I make a website that uses this?
  * Sure :-)

## License

* [BSDv2](LICENSE)

## News

* Updated on 5 April 2017 to handle new github format, and add some unit-tests
