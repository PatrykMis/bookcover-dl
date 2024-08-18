#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BookCover-DL Module to obtain cover URL from Legimi service
# Copyright (C) 2024 Patryk Mis
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import re
import requests

from bs4 import BeautifulSoup


def get_book_cover(url):
    """
    Extracts URL of the best possible book cover and book title from the given Legimi URL.

    Args:
    url (str): URL of the book on the Legimi page.

    Returns:
    tuple: A tuple containing the URL of the cover image and the title of the book.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")

            h1_element = soup.find("h1", {"class": "title-text"})
            for child in h1_element.find_all(recursive=True):
                child.extract()
            book_title = h1_element.get_text(strip=True)

            book_cover_images = soup.find_all("img", {"data-test": "book-cover"})

            if not book_cover_images:
                return None, None

            cover_url = None
            max_width = 0

            for image in book_cover_images:
                srcset_attr = image.get("data-srcset")

                if srcset_attr:
                    urls_and_sizes = re.findall(r"([^\s,]+)\s+(\d+)w", srcset_attr)

                    for url, size in urls_and_sizes:
                        width = int(size)
                        if width > max_width:
                            max_width = width
                            cover_url = url

                # Check if the current image has a higher width than the previous best image
                width_attr = image.get("data-width")
                if width_attr and int(width_attr) > max_width:
                    max_width = int(width_attr)
                    cover_url = image.get('data-src')

            return cover_url, book_title
        else:
            print("Failed to fetch URL:", url)
            return None, None
    except Exception as e:
        print("An error occurred:", e)
        return None, None
