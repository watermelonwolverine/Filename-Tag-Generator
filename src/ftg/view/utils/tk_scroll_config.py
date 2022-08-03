import sys
from tkinter import Canvas, Frame, NW

from ftg.__cli_wrapper.__constants import win32, linux


# from here: https://gist.github.com/JackTheEngineer/81df334f3dcff09fd19e4169dd560c59
def configure_canvas_and_interior_vertical_scroll(canvas: Canvas,
                                                  frame: Frame) -> None:
    tag_list_frame_id = canvas.create_window(0, 0, window=frame,
                                             anchor=NW)

    def _configure_interior(_):
        # Update the scrollbars to match the size of the inner frame.
        size = (frame.winfo_reqwidth(), frame.winfo_reqheight())
        # noinspection PyTypeChecker
        canvas.config(scrollregion="0 0 %s %s" % size)
        if frame.winfo_reqwidth() != canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            canvas.config(width=frame.winfo_reqwidth())

    frame.bind('<Configure>', _configure_interior)

    def _configure_canvas(_):
        if frame.winfo_reqwidth() != canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            canvas.itemconfigure(tag_list_frame_id, width=canvas.winfo_width())

    canvas.bind('<Configure>', _configure_canvas)


def configure_canvas_and_interior_horizontal_scroll(canvas: Canvas,
                                                    frame: Frame) -> None:
    tag_list_frame_id = canvas.create_window(0, 0, window=frame,
                                             anchor=NW)

    def _configure_interior(_):
        # Update the scrollbars to match the size of the inner frame.
        size = (frame.winfo_reqwidth(), frame.winfo_reqheight())
        # noinspection PyTypeChecker
        canvas.config(scrollregion="0 0 %s %s" % size)
        if frame.winfo_reqheight() != canvas.winfo_height():
            # Update the canvas's height to fit the inner frame.
            canvas.config(height=frame.winfo_reqheight())

    frame.bind('<Configure>', _configure_interior)

    def _configure_canvas(_):
        if frame.winfo_reqheight() != canvas.winfo_height():
            # Update the inner frame's height to fill the canvas.
            canvas.itemconfigure(tag_list_frame_id, height=canvas.winfo_height())

    canvas.bind('<Configure>', _configure_canvas)


def configure_mousewheel_vertical_scrolling(canvas: Canvas,
                                            frame: Frame) -> None:
    def _scroll(delta) -> None:
        # Don't scroll when everything is visible, avoid weird behavior
        if frame.winfo_height() > canvas.winfo_height():
            canvas.yview_scroll(delta, "units")

    def _on_mousewheel(event):
        if sys.platform == win32:
            _scroll(int(-1 * (event.delta / 120)))
        else:
            raise NotImplementedError()

    def _bind_to_mousewheel(_):
        if sys.platform == win32:
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        elif sys.platform == linux:
            canvas.bind_all("<Button-4>", lambda event: _scroll(-1))
            canvas.bind_all("<Button-5>", lambda event: _scroll(1))
        else:
            raise NotImplementedError()

    def _unbind_from_mousewheel(_):
        if sys.platform == win32:
            canvas.unbind_all("<MouseWheel>")
        elif sys.platform == linux:
            canvas.bind_all("<Button-4>")
            canvas.bind_all("<Button-5>")
        else:
            raise NotImplementedError()

    canvas.bind('<Enter>', _bind_to_mousewheel)
    canvas.bind('<Leave>', _unbind_from_mousewheel)
