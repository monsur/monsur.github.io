---
title: "I used Gemini CLI to update a GitHub project I hav"
author: "Monsur"
author_handle: "monsur.hossa.in"
date: 2025-07-24 04:00:29 +0000
source_url: "https://bsky.app/profile/monsur.hossa.in/post/3luonivshps23"
source_uri: "at://monsur.hossa.in/app.bsky.feed.post/3luonivshps23"
platform: "Bluesky"
layout: post
---

I used Gemini CLI to update a GitHub project I haven't touched in 14 years: https://github.com/monsur/echo-server

I actually tried this a few weeks back using IDE integration, and it got stuck on unit tests. This time it worked much better (and I think I've gotten better at prompthing).

It was able to uncover functionality I forgot I added (e.g. conditional support), and then updated the README so I wouldn't forget.

It even fixed a security bug:

"I made a significant security improvement. The original server used new Function(), which could execute arbitrary JavaScript from a URL parameter—a major security risk. The modernized version replaces this with a safer, more specific conditional logic"

My key takeaway is the time savings. This was less than an hour of messing around on a weeknight. While I understood all the changes being made, it would have taken SO much longer to do them all myself.

Here's the full conversation if you're curious: https://docs.google.com/document/d/1MeCSzXR5MmUbBjG0wXhlj9y7V9zj7QgYHAjfLY35wCU/edit?usp=sharing

<!--more-->

---

*Originally posted on [Bluesky](https://bsky.app/profile/monsur.hossa.in/post/3luonivshps23) by [@monsur.hossa.in](https://bsky.app/profile/monsur.hossa.in)*
*Source: `at://monsur.hossa.in/app.bsky.feed.post/3luonivshps23`*
