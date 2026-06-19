import dearpygui.dearpygui as dpg

from texture_set_combiner.core.state import AppState
from texture_set_combiner.ui import build_main_window

APP_TITLE = "Texture Set Combiner"
VIEWPORT_WIDTH = 960
VIEWPORT_HEIGHT = 640


class TextureSetCombinerApp:
    """Application entry point — owns state and Dear PyGui lifecycle."""

    def __init__(self) -> None:
        self.state = AppState()

    def run(self) -> None:
        dpg.create_context()
        build_main_window(self.state)

        dpg.create_viewport(
            title=APP_TITLE,
            width=VIEWPORT_WIDTH,
            height=VIEWPORT_HEIGHT,
        )
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
