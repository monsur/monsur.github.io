#!/usr/bin/env python3
"""
Bluesky Thread to Blog Post Converter

Fetches a threaded Bluesky post from a URL and converts it to a Jekyll-compatible markdown file.
"""

import requests
import json
import re
from datetime import datetime
import argparse
import os


def extract_uri_from_url(bsky_url):
    """Extract AT-URI from Bluesky post URL"""
    # Example URL: https://bsky.app/profile/monsur.hossa.in/post/3lwzcq42rdc22
    pattern = r"https://bsky\.app/profile/([^/]+)/post/([^/]+)"
    match = re.match(pattern, bsky_url)
    
    if not match:
        raise ValueError(f"Invalid Bluesky URL format: {bsky_url}\nExpected format: https://bsky.app/profile/handle/post/postid")
    
    handle, post_id = match.groups()
    # Convert to AT-URI format
    at_uri = f"at://{handle}/app.bsky.feed.post/{post_id}"
    return at_uri


def validate_at_uri(at_uri):
    """Validate AT-URI format"""
    # AT-URI format: at://handle/app.bsky.feed.post/postid
    pattern = r"^at://[^/]+/app\.bsky\.feed\.post/[^/]+$"
    if not re.match(pattern, at_uri):
        raise ValueError(f"Invalid AT-URI format: {at_uri}\nExpected format: at://handle/app.bsky.feed.post/postid")
    return at_uri


def fetch_thread(post_uri):
    """Fetch thread data from Bluesky API"""
    api_url = "https://public.api.bsky.app/xrpc/app.bsky.feed.getPostThread"
    params = {
        'uri': post_uri,
        'depth': 1000,  # Get full thread depth
        'parentHeight': 1000  # Get full parent chain
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch thread: {e}")


def remove_thread_markers(text):
    """Remove thread number markers like '1/ ', '2/ ' from the beginning of text"""
    # Pattern matches: number + slash + whitespace at the start of text
    pattern = r'^\d+/\s+'
    return re.sub(pattern, '', text)


def reconstruct_text_with_links(text, facets):
    """Reconstruct text with full URLs from facets data"""
    if not facets:
        return text
    
    # Convert text to bytes for accurate positioning
    text_bytes = text.encode('utf-8')
    
    # Sort facets by byte start position in reverse order to avoid offset issues
    sorted_facets = sorted(facets, key=lambda f: f.get('index', {}).get('byteStart', 0), reverse=True)
    
    for facet in sorted_facets:
        features = facet.get('features', [])
        index = facet.get('index', {})
        byte_start = index.get('byteStart')
        byte_end = index.get('byteEnd')
        
        if byte_start is None or byte_end is None:
            continue
            
        for feature in features:
            if feature.get('$type') == 'app.bsky.richtext.facet#link':
                full_url = feature.get('uri', '')
                if full_url:
                    # Replace the truncated text with the full URL using byte positions
                    text_bytes = text_bytes[:byte_start] + full_url.encode('utf-8') + text_bytes[byte_end:]
                    break
    
    # Convert back to string
    return text_bytes.decode('utf-8')


def extract_posts_from_thread(thread_data):
    """Extract and order posts from thread data"""
    posts = []
    
    def process_post(post_item):
        """Process a single post item"""
        if post_item.get('$type') == 'app.bsky.feed.defs#threadViewPost':
            post = post_item.get('post', {})
            record = post.get('record', {})
            author = post.get('author', {})
            
            # Get the original text
            text = record.get('text', '')
            facets = record.get('facets', [])
            
            # Reconstruct text with full URLs from facets
            if facets:
                text = reconstruct_text_with_links(text, facets)
            
            # Remove thread markers like "1/ ", "2/ " etc.
            text = remove_thread_markers(text)
            
            post_data = {
                'text': text,
                'created_at': record.get('createdAt', ''),
                'author': author.get('displayName', author.get('handle', '')),
                'handle': author.get('handle', ''),
                'uri': post.get('uri', ''),
                'cid': post.get('cid', '')
            }
            return post_data
        return None
    
    def collect_posts(thread_item):
        """Recursively collect posts from thread structure"""
        # Process current post
        post_data = process_post(thread_item)
        if post_data:
            posts.append(post_data)
        
        # Process replies
        replies = thread_item.get('replies', [])
        for reply in replies:
            collect_posts(reply)
    
    # Start with the main thread
    thread = thread_data.get('thread', {})
    
    # Collect parent posts first
    parent_posts = []
    current = thread.get('parent')
    while current:
        parent_data = process_post(current)
        if parent_data:
            parent_posts.insert(0, parent_data)  # Insert at beginning for correct order
        current = current.get('parent')
    
    # Add parent posts to main list
    posts.extend(parent_posts)
    
    # Collect main thread posts
    collect_posts(thread)
    
    return posts


def merge_posts_to_markdown(posts, original_url, at_uri, custom_title=None):
    """Merge posts into a single markdown blog post"""
    if not posts:
        return ""
    
    # Get metadata from first post
    first_post = posts[0]
    author = first_post['author']
    handle = first_post['handle']
    created_at = first_post['created_at']
    
    # Parse date for Jekyll front matter
    try:
        post_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        date_str = post_date.strftime('%Y-%m-%d')
        datetime_str = post_date.strftime('%Y-%m-%d %H:%M:%S %z')
    except:
        date_str = datetime.now().strftime('%Y-%m-%d')
        datetime_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S %z')
    
    # Use custom title if provided, otherwise generate from first post
    if custom_title:
        title_text = custom_title
    else:
        # Generate title from first post (first 50 chars, cleaned up)
        title_text = posts[0]['text'][:50].strip()
        title_text = re.sub(r'[^\w\s-]', '', title_text).strip()
        if not title_text:
            title_text = f"Bluesky Thread by {author}"
    
    # Jekyll front matter
    front_matter = f"""---
title: "{title_text}"
author: "{author}"
author_handle: "{handle}"
date: {datetime_str}
source_url: "{original_url}"
source_uri: "{at_uri}"
platform: "Bluesky"
layout: post
---

"""
    
    # Merge post content
    content_parts = []
    
    for i, post in enumerate(posts):
        text = post['text'].strip()
        if text:
            if i == 0:
                # First post - no special formatting
                content_parts.append(text)
            else:
                # Subsequent posts - add some separation
                content_parts.append(f"\n{text}")
    
    # Combine everything
    full_content = front_matter + "\n".join(content_parts)
    
    # Add source attribution at the end
    full_content += f"\n\n---\n\n*Originally posted on [Bluesky]({original_url}) by [@{handle}](https://bsky.app/profile/{handle})*\n*Source: `{at_uri}`*\n"
    
    return full_content


def generate_filename(posts, date_str, custom_title=None):
    """Generate Jekyll-compatible filename"""
    if custom_title:
        # Use custom title for slug generation
        slug_text = custom_title
    elif posts:
        # Create slug from first post
        slug_text = posts[0]['text'][:30].strip()
    else:
        return f"{date_str}-bluesky-post.md"
    
    slug = re.sub(r'[^\w\s-]', '', slug_text).strip()
    slug = re.sub(r'\s+', '-', slug).lower()
    
    if not slug:
        slug = "bluesky-thread"
    
    return f"{date_str}-{slug}.md"


def main():
    parser = argparse.ArgumentParser(description='Convert Bluesky thread to Jekyll blog post')
    parser.add_argument('url', help='Bluesky post URL (format: https://bsky.app/profile/handle/post/postid)')
    parser.add_argument('-o', '--output', help='Output filename (optional)')
    parser.add_argument('-d', '--output-dir', default='.', help='Output directory (default: current directory)')
    parser.add_argument('--title', help='Custom title for the blog post (optional)')
    
    args = parser.parse_args()
    
    try:
        # Extract AT-URI from URL
        post_uri = extract_uri_from_url(args.url)
        print(f"Extracted AT-URI: {post_uri}")
        
        # Validate the extracted AT-URI
        validate_at_uri(post_uri)
        
        # Fetch thread data
        print("Fetching thread data...")
        thread_data = fetch_thread(post_uri)
        
        # Extract posts
        posts = extract_posts_from_thread(thread_data)
        print(f"Found {len(posts)} posts in thread")
        
        if not posts:
            print("No posts found in thread")
            return
        
        # Generate markdown content
        markdown_content = merge_posts_to_markdown(posts, args.url, post_uri, args.title)
        
        # Generate filename
        if args.output:
            filename = args.output
        else:
            try:
                post_date = datetime.fromisoformat(posts[0]['created_at'].replace('Z', '+00:00'))
                date_str = post_date.strftime('%Y-%m-%d')
            except:
                date_str = datetime.now().strftime('%Y-%m-%d')
            
            filename = generate_filename(posts, date_str, args.title)
        
        # Ensure output directory exists
        output_path = os.path.join(args.output_dir, filename)
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Write markdown file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Blog post written to: {output_path}")
        print(f"Title: {posts[0]['text'][:50]}...")
        print(f"Author: {posts[0]['author']} (@{posts[0]['handle']})")
        print(f"Posts in thread: {len(posts)}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())