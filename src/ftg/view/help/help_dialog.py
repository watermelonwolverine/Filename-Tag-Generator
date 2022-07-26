import webbrowser
from tkinter import Tk, BOTH, Toplevel

import markdown
from tkinterweb.htmlwidgets import HtmlFrame

from ftg.__help_text import help_text
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

    def __build_ui(self):
        text = HtmlFrame(self.__root,
                         messages_enabled=False,
                         vertical_scrollbar="auto",
                         horizontal_scrollbar="auto")

        def open_url(url:str):
            if url.startswith("https://"):
                webbrowser.open(url)

        text.html.link_click_func = open_url
        text.html.form_submit_func = lambda: None

        text.pack(fill=BOTH,
                  expand=True)

        html_help_text = markdown.markdown(help_text)

        text.load_html(html_help_text)
