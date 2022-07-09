from typing import Dict, List

from tkdnd import DND_FILES

from ftg.config import FtgConfig
from ftg.filename_generator import FilenameGeneratorImpl
from ftg.ftg_window_view import FtgWindowView


class FtgWindowController:

    def __init__(self,
                 config: FtgConfig,
                 categories: Dict[str, List[str]]):

        self.__config = config
        self.__tags = self.__get_sorted_tags(categories)

        self.__filename_generator = FilenameGeneratorImpl(config.get_filename_config())

        self.__view = self.__create_view(categories)
        self.__configure_view(self.__view)

    def start(self):
        self.__view.as_tk().mainloop()

    def __get_sorted_tags(self,
                          categories_dict: Dict) -> List[str]:
        result = []

        for tag_list in categories_dict.values():
            for tag in tag_list:
                if tag not in result:
                    result.append(tag)
        return sorted(result)

    def __create_view(self,
                      categories: Dict[str, List[str]]) -> FtgWindowView:

        return FtgWindowView(self.__config.get_ui_config(),
                             categories,
                             self.__tags)

    def __configure_view(self,
                         view: FtgWindowView):

        view.as_tk().drop_target_register(DND_FILES)
        view.as_tk().dnd_bind('<<Drop>>', lambda event: self.__drop_file(event))

        view.revert_button.configure(command=lambda: self.__revert())
        view.generate_button.configure(command=lambda: self.__generate())
        view.apply_button.configure(command=lambda: self.__apply())
        view.clear_button.configure(command=lambda: self.__clear())

    def __revert(self):

        filename = self.__view.filename_result_string_var.get()

        revert_result = self.__filename_generator.revert(filename)

        self.__clear_checkboxes()

        self.__view.extension_string_var.set(revert_result.extension)

        self.__view.basename_string_var.set(revert_result.basename)

        for tag in revert_result.tags:
            if tag in self.__view.checkbox_values.keys():
                self.__view.checkbox_values[tag].set(True)

    def __clear_checkboxes(self):
        for boolean_var in self.__view.checkbox_values.values():
            boolean_var.set(False)

    def __clear(self):
        self.__clear_checkboxes()
        self.__view.filename_result_string_var.set("")
        self.__view.search_result_string_var.set("")
        self.__view.path_to_selected_file_var.set("")
        self.__view.hide_selected_file_widgets()

    def __generate(self):
        result = self.__filename_generator.generate_filename(
            self.__view.basename_string_var.get(),
            self.__get_checked_tags(),
            self.__view.extension_string_var.get())
        self.__view.filename_result_string_var.set(result)

    def __get_checked_tags(self):
        result = []

        for tag in self.__view.checkbox_values.keys():
            if self.__view.checkbox_values[tag].get():
                result.append(tag)

        return result

    def __drop_file(self,
                    event):

        self.__view.show_selected_file_widgets()
        self.__view.path_to_selected_file_var.set(event.data)
        print(event.data)

    def __apply(self):
        print("OOF")
