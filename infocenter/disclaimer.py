# SPDX-License-Identifier: GPL-2.0-or-later

import gi
import re

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk  # noqa E402


def replace_urls(text):
    url_pattern = re.compile(r"https?://\S+|www\.\S+")
    urls = url_pattern.findall(text)

    for url in urls:
        text = text.replace(url, '<a href="' + url + '">' + url + "</a>")

    return text


@Gtk.Template(resource_path="/de/volkswagen/infocenter/gtk/disclaimer.ui")
class Disclaimer(Gtk.Box):
    __gtype_name__ = "Disclaimer"

    title_label = Gtk.Template.Child()
    content_label = Gtk.Template.Child()

    def __init__(self, title="", content="", **kwargs):
        super().__init__(**kwargs)
        self.title_label.set_markup("<b>" + title + "</b>")
        self.content_label.set_markup(replace_urls(content))
        self.content_label.add_css_class("dim-label")
