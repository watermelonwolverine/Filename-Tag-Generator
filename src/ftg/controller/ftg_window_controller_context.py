from typing import List, Dict

from ftg.utils.tag import Tag
from ftg.view.ftg_window import FtgWindow


class FtgWindowControllerContext:

    def __init__(self,
                 tags: List[Tag],
                 view: FtgWindow):
        self.changes_are_pending = False
        self.tags: List[Tag] = tags
        self.view: FtgWindow = view
        self.selected_files: List[str] = []
        self.tags_for_selected_files: Dict[str, List[str]] = {}
