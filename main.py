#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is the main application module of BookCover-DL, a simple GUI application for downloading book covers.
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

import application
import builtins
import gettext
import isbnlib
import mimetypes
import re
import requests
import sys, os
import validators
import webbrowser
import wx
import wx.adv

from datetime import datetime
from pathvalidate import sanitize_filename
from services import legimi_service, lubimyczytac_service, isbn_service
from unidecode import unidecode
from urllib.parse import urlparse, urlunparse

builtins.__dict__['_'] = wx.GetTranslation
bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
locales_dir = os.path.abspath(os.path.join(bundle_dir, 'locales'))

class main(wx.App):
    def init_language(self):
        wx.Locale.AddCatalogLookupPathPrefix(locales_dir)
        self.locale = wx.Locale()
        # locale = wx.Locale()
        # if self.locale.GetSystemLanguage() == wx.LANGUAGE_ENGLISH:
            # return  # Code already in english, so don't initialize.
        # if not self.locale.Init():
        if not self.locale.Init(self.locale.GetSystemLanguage()):
            wx.LogWarning("This language is not supported by the system.")
        if not self.locale.AddCatalog("BookCover-DL"):
            wx.LogError("Couldn't find/load the 'BookCover-DL' catalog for locale '" + self.locale.GetCanonicalName() + "'.")

    def OnInit(self):
        print(f"Running wxPython {wx.version()}")
        self.init_language()
        main_dlg = BookCoverDL(None)
        main_dlg.ShowModal()
        main_dlg.Destroy()
        return True

class BookCoverDL(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="BookCover-DL")

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(wx.StaticText(self, label=_("Enter URL or ISBN:")), flag=wx.EXPAND|wx.ALL)
        self.url_text = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        sizer.Add(self.url_text, flag=wx.EXPAND|wx.ALL)

        btn_sizer = self.CreateSeparatedButtonSizer(wx.OK | wx.CANCEL | wx.HELP)

        sizer.Add(btn_sizer, flag=wx.EXPAND|wx.ALL)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Center(wx.BOTH | wx.CENTER)

        self.Bind(wx.EVT_BUTTON, self.on_ok, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.on_help, id=wx.ID_HELP)

        self.url_text.SetFocus()

        self.url_text.Bind(wx.EVT_TEXT, self.on_text_changed)
        self.ok_button = self.FindWindowById(wx.ID_OK)
        if not self.url_text.GetValue():
            self.ok_button.Disable()

    def on_ok(self, event):
        input_text = self.url_text.GetValue()
        validation_result = self.validate_input(input_text)
        if validation_result == "url":
            print("Input is a URL.")
            corrected_url = self.correct_url(input_text)
            if corrected_url:
                self.url_text.SetValue(corrected_url)
            image_path = self.download_cover_from_url(input_text)
        elif validation_result == "isbn":
            self.show_info_dialog(_("Valid ISBN number"), _("The entered number appears to be valid ISBN, but the functionality of finding the book and downloading its cover is not yet implemented."))
            self.download_cover_from_isbn
            return

        else:
            self.show_error_dialog(_("Unknown input"), _("It looks like the entered input is not a valit URL address nor ISBN number. Please enter valid URL address, including HTTP or preferably https protocol or ISBN number, with or without dashes."))
            return
        if image_path:
            self.show_info_dialog(_("Success"), _("Successfully saved cover of the book named\n\"{}\" to\n\"{}\".").format(self.book_title, image_path))

    def validate_input(self, input_text):
        if validators.url(input_text):
            return "url"

        if isbnlib.is_isbn10(input_text) or isbnlib.is_isbn13(input_text):
            return "isbn"
        return "unknown"

    def correct_url(self, url):
        parsed_url = urlparse(url)
        if parsed_url.scheme == "http":
            parsed_url = parsed_url._replace(scheme="https")
            return urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))
        return None

    def download_cover_from_url(self, url):
        parsed_url = urlparse(url)
        if "legimi.pl" in parsed_url.netloc:
            result = self.show_question_dialog(_("Warning"), _("This service provides book covers with its own branding and possibly a logo on them.\n\nAre you certain you wish to download a cover from this service?"))
            if result == wx.ID_NO:
                return
                
            service = legimi_service
        elif "lubimyczytac.pl" in parsed_url.netloc:
            service = lubimyczytac_service
        else:
            self.show_error_dialog(_("Unknown service"), _("Unfortunately, I don't know how to get cover from this service.\n\nPlease enter link from Legimi or LubimyCzytać, or enter book's ISBN."))
            return None
        
        self.cover_url, self.book_title = service.get_book_cover(url)
        if self.cover_url is not None and self.book_title is not None:
            response = requests.get(self.cover_url)
            print(self.cover_url)
            if response.status_code == 200:
                content_type = response.headers.get("content-type")
                guessed_extension = mimetypes.guess_extension(content_type) or ""
                url_path = urlparse(self.cover_url).path
                filename = os.path.basename(url_path)
                filename, ext = os.path.splitext(filename)
                if ext:
                    filename = self.book_title+ext
                else:
                    filename = self.book_title+guessed_extension

                if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
                    # Running as a PyInstaller executable
                    current_dir = os.path.dirname(sys.executable)
                else:
                    # Running as a Python script
                    current_dir = os.path.dirname(os.path.abspath(__file__))

                image_path = os.path.join(current_dir, sanitize_filename(unidecode(filename)))
                with open(image_path, "wb") as f:
                    f.write(response.content)
                return image_path
            else:
                print("Failed to download book cover.")
                return None
        else:
            self.show_error_dialog(_("Error"), _("Failed to obtain the book cover. Either the URL is wrong or there is some kind of connection error; perhaps the developer will add a specific logic to display a more precise cause of this error."))
            return None

    def download_cover_from_isbn(self, isbn):
        # Stub
        pass

    def on_help(self, event):
        menu = wx.Menu()

        item_github = menu.Append(wx.ID_ANY, _("View &Source on GitHub"))
        self.Bind(wx.EVT_MENU, self.on_view_github, item_github)
        item_license = menu.Append(wx.ID_ANY, _("View GPL v3 &License"))
        item_license.Enable(False)
        # self.Bind(wx.EVT_MENU, self.on_view_license, item_license)
        item_about = menu.Append(wx.ID_ANY, _("&About…"))
        self.Bind(wx.EVT_MENU, self.on_about, item_about)
        self.PopupMenu(menu)
        menu.Destroy()

    def on_view_github(self, event):
        url = "https://github.com/PatrykMis/BookCover-DL"
        webbrowser.open(url)

    def on_about(self, event):
        aboutInfo = wx.adv.AboutDialogInfo()
        aboutInfo.SetName(application.name)
        aboutInfo.SetVersion(application.version)
        aboutInfo.SetDescription(application.description)
        aboutInfo.SetCopyright(application.copyright)
        aboutInfo.SetWebSite(application.website)
        aboutInfo.AddDeveloper(application.developer)
        wx.adv.AboutBox(aboutInfo)

    def show_error_dialog(self, title, message):
        dlg = wx.MessageDialog(self, message, title, wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        self.url_text.SetFocus()

    def show_info_dialog(self, title, message):
        dlg = wx.MessageDialog(self, message, title, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        self.url_text.SetFocus()

    def show_question_dialog(self, title, message):
        dlg = wx.MessageDialog(self, message, title, wx.YES_NO | wx.ICON_WARNING)
        result = dlg.ShowModal()
        dlg.Destroy()
        self.url_text.SetFocus()
        return result

    def on_text_changed(self, event):
        if self.url_text.GetValue():
            self.ok_button.Enable()
        else:
            self.ok_button.Disable()

if __name__ == "__main__":
    app = main(False)
    app.ExitMainLoop()
    # locale = wx.Locale(wx.LANGUAGE_DEFAULT)
    # locale.AddCatalogLookupPathPrefix("locale")
    # locale.AddCatalog("BookCover-DL")
    #language_code = wx.Locale.GetSystemLanguage()
    # language_name = wx.Locale.GetLanguageName(language_code)
    # print("System language:", language_name)
