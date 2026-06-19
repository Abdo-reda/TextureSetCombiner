import dearpygui.dearpygui as dpg

from texture_set_combiner.core.state import AppState
from texture_set_combiner.ui.tabs import (
    build_mesh_import_tab,
    build_textures_export_tab,
    build_textures_import_tab,
)

WINDOW_TAG = "main_window"


def build_main_window(state: AppState) -> None:
    """Create the primary application window and tab bar."""

    with dpg.window(tag=WINDOW_TAG):
        with dpg.tab_bar():
            build_mesh_import_tab(state)
            build_textures_import_tab(state)
            build_textures_export_tab(state)

    dpg.set_primary_window(WINDOW_TAG, True)
