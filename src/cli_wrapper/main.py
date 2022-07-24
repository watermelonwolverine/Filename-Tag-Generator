from ftg.controller.ftg_window_controller import FtgWindowController
from ftg.utils.program_config import ProgramConfigImpl
from ftg.utils.tags import Tags


def main(path_to_config_file,
         path_to_tags_file):
    config = ProgramConfigImpl.parse_file(path_to_config_file)

    tags: Tags = Tags.parse_file(path_to_tags_file)

    ftg_window_controller = FtgWindowController(config,
                                                tags)
    ftg_window_controller.start()
