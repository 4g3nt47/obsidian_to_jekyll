#!/usr/bin/python3
#--------------------------------------------------------------
# A program for converting Obsidian writeups into Jekyll posts.
#                                               Author: 4g3nt47
#--------------------------------------------------------------

import sys, os, time

def obsidian_to_jekyll(jekyll_root, img_src_path, name, title, categories, tags, body):
  jekyll_img_path = "/assets/img"
  img_dst_path = f"{jekyll_root}{jekyll_img_path}"
  name = name.replace(" ", "_")
  body = body.strip()
  output = ""
  day = time.strftime("%d")
  month = time.strftime("%m")
  year = time.strftime("%Y")
  post_fname = f"{year}-{month}-{day}-{name}.md"
  print(f"[+] Creating blog post: {post_fname}")
  print("[*] Building header...")
  header = """---
layout: post
date: %s-%s-%s
title: "%s"
categories: [%s]
tags: [%s]
---

<br>

""" %(year, month, day, title, categories, tags)
  output += header
  # Extract images
  print("[*] Extracting images...")
  in_codeblock = False
  for line in body.splitlines():
    if line.startswith("```") or line.endswith("```"):
      in_codeblock = not in_codeblock
    if not in_codeblock and line.startswith("![[") and line.endswith("]]"):
      img_name = line[3:-2]
      if not img_name[-3:] in ["png", "jpg"]: continue
      src_fname = f"{img_src_path}/{img_name}"
      dst_fname = f"{img_dst_path}/{img_name}"
      if not os.path.isfile(src_fname):
        print(f"[-] Invalid file: {src_fname}")
        output += line + "\n"
        continue
      if os.path.isfile(dst_fname):
        print(f"[-] File already exists: {dst_fname}")
        output += line + "\n"
        continue
      rfo = open(src_fname, "rb")
      wfo = open(dst_fname, "wb")
      wfo.write(rfo.read())
      wfo.close()
      rfo.close()
      line = f"![]({jekyll_img_path}/{img_name})"
      print(f"[+] {img_name}")
    output += line + "\n"
  print("[*] Saving post...")
  wfo = open(f"{jekyll_root}/_posts/{post_fname}", "w")
  wfo.write(output)
  wfo.close()
  print("[+] Post saved successfully!")

if __name__ == '__main__':
  try:
    if len(sys.argv) < 4:
      print(f"[-] Usage: {os.path.basename(sys.argv[0])} <writeup.md> <obsidian_imgs_dir> <jekyll_root>")
      exit(1)
    body = open(sys.argv[1]).read()
    name = input("[?] Post name: ").strip()
    if not name: exit(1)
    title = input("[?] Post title: ").strip()
    categories = input("[?] Categories (comma separated): ").strip()
    tags = input("[?] Tags (comma separated): ").strip()
    obsidian_to_jekyll(sys.argv[3], sys.argv[2], name, title, categories, tags, body)
  except KeyboardInterrupt:
    exit(2)
