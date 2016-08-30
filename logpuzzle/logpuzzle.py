#!/usr/bin/python
# Copyright 2010 Google Inc.
# Copyright 2016 Cassiano Rocha Kuplich
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib.request

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg \
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; \
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def url_idx(url):
    match = re.search(r'-\w+-(\w+)\.jpg', url)
    if match:
        return match.group(1)
    else:
        return url


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    # Extract the hostname.
    match = re.search(r'_(.+)', filename)
    if match:
        hostname = 'http://' + match.group(1)
    else:
        sys.stderr.write("log file name doesn't contain hostname\n")
        sys.exit(1)

    # Extract the puzzle urls from the log file.
    urls = []
    f = open(filename, 'r')
    text = f.read()
    f.close()
    tuples = re.findall(r'GET\s(\S*puzzle\S*)\sHTTP', text)
    for path in tuples:
        url = hostname + path
        if url not in urls:
            urls.append(url)
    return sorted(urls, key=url_idx)


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # Create the given directory if necessary.
    os.makedirs(dest_dir, exist_ok=True)

    # Create the index.html file.
    f = open(os.path.join(dest_dir, 'index.html'), 'w')
    f.write('<html>\n<body>\n')
    for i in range(len(img_urls)):
        url = img_urls[i]
        print('Retrieving ' + url + ' ...')
        img_filename = 'img%d' % i
        # Download the image of the current url.
        urllib.request.urlretrieve(url, os.path.join(dest_dir, img_filename))
        f.write('<img src="%s">' % img_filename)
    f.write('\n</body>\n</html>')
    f.close()


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--todir dir] logfile ')
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main()
