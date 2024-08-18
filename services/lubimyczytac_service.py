#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BookCover-DL Module to obtain cover URL from Lubimyczytac service
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

import requests

from bs4 import BeautifulSoup


def get_book_cover(url):
    """
    Extracts URL of the best possible book cover and book title from the given Lubimyczytac URL.

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

            book_title = soup.find("h1", class_="book__title").get_text(strip=True)
            cover_url = soup.find("a", class_="book-cover__link")["href"]

            return cover_url, book_title
        else:
            print("Failed to fetch URL:", url)
            return None, None
    except Exception as e:
        print("An error occurred:", e)
        return None, None
