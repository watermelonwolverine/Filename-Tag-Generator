from typing import List, Dict

from ftg.utils.tag import Tag
from ftg.view.ftg_window import FtgWindow


class FtgWindowControllerContext:

    def __init__(self,
                 tags: List[Tag],
                 view: FtgWindow):
        self.tags = tags
        self.view = view
        self.selected_files = []
        self.tags_for_selected_files: Dict[str, List[str]] = {}
