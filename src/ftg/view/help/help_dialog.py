import logging
import os.path
import traceback
import urllib.request
import webbrowser
from tkinter import Tk, BOTH, Toplevel
from typing import Callable

import markdown
from tkinterweb.htmlwidgets import HtmlFrame

from ftg.__help_text import help_table_of_contents, sections, sections_by_link
from ftg.view.styles import Styles
from ftg.view.ui_config import UIConfig


class FtgHelpDialog:

    def __init__(self,
                 parent: Tk,
                 config: UIConfig,
                 styles: Styles):
        self.__root = Toplevel(parent)
        self.__root.title("Help")
        self.__root.minsize(400, 400)
        self.__config = config
        self.__styles = styles

        self.__build_ui()

        self.__show_markdown(help_table_of_contents)

    def __build_ui(self):
        self.html_frame = HtmlFrame(self.__root,
                                    messages_enabled=False,
                                    vertical_scrollbar="auto",
                                    horizontal_scrollbar="auto")

        def open_url(url: str):
            self.__open_url(url)

        self.html_frame.html.link_click_func = open_url
        self.html_frame.html.form_submit_func = lambda: None

        self.html_frame.pack(fill=BOTH,
                             expand=True)

    def __show_markdown(self,
                        markdown_text):

        html_text = markdown.markdown(markdown_text)

        self.html_frame.load_html(html_text)

    # tkinterweb just swallows exceptions...
    def __wrap_with_logger(self,
                           fun: Callable):

        try:
            fun()
        except Exception:
            logging.warning(traceback.format_exc())

    def __open_url(self,
                   url):

        self.__wrap_with_logger(lambda: self.__try_open_url(url))

    def __try_open_url(self,
                       url):

        if url.startswith("https://"):
            webbrowser.open(url)
            return

        if url.startswith("file://"):

            filename = url.split("/")[-1]

            if filename.startswith("#"):

                if filename == "#home":
                    self.__show_markdown(help_table_of_contents)
                    return

                if filename in sections_by_link.keys():

                    section = sections_by_link[filename]

                    section_markdown_text = section.text

                    navigation_links = "[Home](#home)"

                    index = sections.index(section)

                    if index > 0:
                        navigation_links += F'  [Previous]({sections[index - 1].link})'

                    if index < len(sections) - 1:
                        navigation_links += F'  [Next]({sections[index + 1].link})'

                    self.__show_markdown(navigation_links + "\n\n" + section_markdown_text)
                return

            try:
                path = urllib.request.url2pathname(url)
            except OSError as ex:
                # urls aren't conforming
                # get rid of file://
                path = url[7:]

            if os.path.exists(path):
                if os.path.isdir(path):
                    os.startfile(path)
                elif os.path.isfile(path):
                    os.startfile(os.path.dirname(path))
                return
