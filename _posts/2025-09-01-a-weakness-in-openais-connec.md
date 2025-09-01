---
title: "Prompt injection and early 2000s blogging"
author: "Monsur"
author_handle: "monsur.hossa.in"
date: 2025-09-01 06:08:04 +0000
source_url: "https://bsky.app/profile/monsur.hossa.in/post/3lxqwsxh6gs2h"
source_uri: "at://monsur.hossa.in/app.bsky.feed.post/3lxqwsxh6gs2h"
platform: "Bluesky"
layout: post
---

_"A weakness in OpenAI’s Connectors allowed sensitive information to be extracted from a Google Drive account using an indirect prompt injection attack."_ ([source](https://www.wired.com/story/poisoned-document-could-leak-secret-data-chatgpt/))

These prompt injection attacks remind me of Javascript injection attacks on blogging sites from the early 2000s

Early social media sites like Xanga and MySpace allowed users to add Javascript directly to their page. I worked at Xanga in the early 2000s, and mitigating these attacks was a challenging game of one-upmanship.

Embedding JS started as a fun way for users to customize their site. Javascript was relatively new, and you could do things like change fonts, colors, cursors, mouseovers, etc (this was even before CSS). JS code snippets were a form of currency that allowed your site to stand out from others.

But then users got more creative. Using exec(), document.cookie or XMLHttpRequest could lead to bad things.

So we'd regex those out.

But users can get even more creative and escape strings, concat strings, or spread commands across multiple script tags.

It became untenable to parse everything safely.

I see a similar trend playing out with AI. So long as all the data is in the same prompt, users can get ever more creative with how they inject prompts.

@simonwillison.net makes the [same point](https://simonwillison.net/2025/Aug/25/agentic-browser-security/):

_"to an LLM the trusted instructions and untrusted content are concatenated together into the same stream of tokens, and... nobody has demonstrated a convincing and effective way of distinguishing between the two."_

In hindsight, and with years of wisdom, its obvious that giving users the power to run Javascript was not a good idea. A more constrained set of customizations would have been better.

But hey, it was the early days of the internet, we were young, and this shit was so cool (just like AI is today)!

<!--more-->

---

*Originally posted on [Bluesky](https://bsky.app/profile/monsur.hossa.in/post/3lxqwsxh6gs2h) by [@monsur.hossa.in](https://bsky.app/profile/monsur.hossa.in)*
*Source: [https://bsky.app/profile/monsur.hossa.in/post/3lxqwsxh6gs2h](https://bsky.app/profile/monsur.hossa.in/post/3lxqwsxh6gs2h)*
