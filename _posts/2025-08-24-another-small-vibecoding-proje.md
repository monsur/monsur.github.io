---
title: "Vibecoding on a Sunday afternoon"
author: "Monsur"
author_handle: "monsur.hossa.in"
date: 2025-08-24 23:38:41 +0000
source_url: "https://bsky.app/profile/monsur.hossa.in/post/3lx6nsaottk2n"
source_uri: "at://monsur.hossa.in/app.bsky.feed.post/3lx6nsaottk2n"
platform: "Bluesky"
layout: post
---

Another small vibecoding project from a Sunday afternoon: mirroring my BlueSky posts to a Jekyll blog [http://monsur.hossa.in/blog](http://monsur.hossa.in/blog). I've been posting here more (I can get into the why in the future), and I wanted to have my own archive of this content.

Even though BlueSky captures bite-sized content, I envision a BlueSky thread as a single coherent blog post.

[This Python script](https://github.com/monsur/monsur.github.io/blob/master/scripts/bsky_to_blog.py) concatenates a BlueSky thread into a Markdown file which serves as a single blog post.

It was built using Claude Code. I was dipping in and out throughout the afternoon, but it was maybe an hour, hour and a half of work in total.

While the script could automatically run when there's a new post, I'm running it manually for now so I can inspect the output.

Claude used the public BlueSky API, no authentication required. I assumed I'd have to authenticate given how locked-down APIs tend to be these days. Yay for open APIs!

Claude also had a clever solution for ensuring all the posts are mine. I would have just hardcoded my username directly in the script. Claude saves the username of the first post, and then ensures the user is the same for subsequent posts. This is a much more scalable approach!

<!--more-->

---

*Originally posted on [Bluesky](https://bsky.app/profile/monsur.hossa.in/post/3lx6nsaottk2n) by [@monsur.hossa.in](https://bsky.app/profile/monsur.hossa.in)*
*Source: [https://bsky.app/profile/monsur.hossa.in/post/3lx6nsaottk2n](https://bsky.app/profile/monsur.hossa.in/post/3lx6nsaottk2n)*
