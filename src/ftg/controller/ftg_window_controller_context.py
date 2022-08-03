from typing import List, Dict

from ftg.config.tags import Tags
from ftg.view.ftg_window import FtgWindow


class FtgWindowControllerContext:

    def __init__(self,
                 tags: Tags,
                 view: FtgWindow):
        self.changes_are_pending = False
        self.tags: Tags = tags
        self.view: FtgWindow = view
        self.selected_files: List[str] = []
        self.tags_for_selected_files: Dict[str, List[str]] = {}
