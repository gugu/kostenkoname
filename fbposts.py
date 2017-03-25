import json
import datetime
import requests
FORMAT="""+++
title = "FB post"
date = "%(created_time)s"
+++

%(message)s


%(link_block)s
"""
token = json.load(open('private.json'))["token"]
posts = requests.get('https://graph.facebook.com/me/posts?date_format=U&limit=200&access_token=' + token).json()
for post in posts["data"]:
    if post["privacy"]["value"] != 'EVERYONE':
        continue
    post_file = open("content/posts/p" + post["id"] + ".md", "w")
    post["link_block"] = 'Link: %(link)s' % post if post.get("link")  else ""
    post["created_time"] = datetime.datetime.utcfromtimestamp(post["created_time"]).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    if "picture" in post:
        post["message"] = post.get('message', '') + '\n\n![Photo](%(picture)s)' % post
    if "message" not in post:
        continue
    post_file.write((FORMAT % post).encode('UTF-8'))
    post_file.close()
