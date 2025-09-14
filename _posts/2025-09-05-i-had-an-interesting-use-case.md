---
title: "Vibedebugging"
author: "Monsur"
author_handle: "monsur.hossa.in"
date: 2025-09-05 04:27:42 +0000
source_url: "https://bsky.app/profile/monsur.hossa.in/post/3ly2t35ngds2i"
source_uri: "at://monsur.hossa.in/app.bsky.feed.post/3ly2t35ngds2i"
platform: "Bluesky"
layout: post
---

I had an interesting use case where vibecoding just wasn't fixing a pesky bug. So I tried "vibedebugging" instead, and used the root cause to build the correct solution.

Context: I was messing with a React app that wasn't persisting scroll position on the page. I asked Claude to fix it but the code wouldn't work, even after multiple iterations.

So I tried a different approach. Rather than asking Claude to fix the bug, I asked it to debug what was going on.

It peppered detailed console.log statements (with pretty emojis) throughout the code. Then I'd trigger the bug and paste the console output back into the CLI.

Working iteratively with Claude, we were able to uncover multiple issues (set scrollRestoration to "manual", saving position at the right time). The default approach didn't work due to these nuances; only after truly understanding the underlying bug could Claude build the right solution.

It seems a little obvious saying it, but sound software engineering practices still apply: you have to understand an issue before you can fix it. But you can leverage AI to do both!

Oh, and this was all so much fun! It felt like a pair programming session!

<!--more-->

---

*Originally posted on [Bluesky](https://bsky.app/profile/monsur.hossa.in/post/3ly2t35ngds2i) by [@monsur.hossa.in](https://bsky.app/profile/monsur.hossa.in)*
*Source: [https://bsky.app/profile/monsur.hossa.in/post/3ly2t35ngds2i](https://bsky.app/profile/monsur.hossa.in/post/3ly2t35ngds2i)*
