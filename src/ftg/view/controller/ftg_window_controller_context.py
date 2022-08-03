from typing import List, Dict

from ftg.config.tags import Tags
from ftg.view.ui.ftg_widget import FtgWidget


class FtgWindowControllerContext:

    def __init__(self,
                 tags: Tags,
                 view: FtgWidget):
        self.changes_are_pending = False
        self.tags: Tags = tags
        self.view: FtgWidget = view
        self.selected_files: List[str] = []
        self.tags_for_selected_files: Dict[str, List[str]] = {}
