# RSSPrompt
A simple Python script to display news from RSS feeds in the command line

## Install
```bash
pip install pyyaml
pip install feedparser
pip install colorama
git clone https://github.com/will-peixoto/rssprompt.git
```

## Configure
```bash
cd rssprompt
cd src
```
Edit `config.yaml` file with your favorite text editor and put the RSS feed URLs into `rss_url` section.

## Change colors
You can also set your preferred colors:
![image](https://github.com/will-peixoto/rssprompt/assets/147000702/b1ae5dcf-0754-45b0-82b6-023a9bc0f207)

Use the color codes defined in the `AnsiFore` class (https://github.com/tartley/colorama/blob/master/colorama/ansi.py):
![image](https://github.com/will-peixoto/rssprompt/assets/147000702/245b2d5b-561b-48cf-b9bd-971a49899bcc)

## Run
```bash
python RSSPrompt.py
```
