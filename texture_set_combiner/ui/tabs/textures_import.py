import dearpygui.dearpygui as dpg

from texture_set_combiner.core.state import AppState


def build_textures_import_tab(state: AppState) -> None:
    """Build the Textures Import tab wireframe."""

    with dpg.tab(label="Textures Import"):
        dpg.add_text("Textures Import")
        dpg.add_spacer(height=8)
        dpg.add_text(
            "Texture import controls will go here.",
            color=(140, 140, 140),
        )
