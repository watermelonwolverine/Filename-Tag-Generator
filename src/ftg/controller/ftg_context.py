from typing import List, Dict

from ftg.view.ftg_window_view import FtgWindowView


class FtgContext:

    def __init__(self,
                 tags: List[str],
                 view: FtgWindowView):
        self.tags = tags
        self.view = view
        self.selected_files = []
        self.tags_for_selected_files: Dict[str, List[str]] = {}

    def clear(self):
        self.selected_files = []
        self.tags_for_selected_files = {}
