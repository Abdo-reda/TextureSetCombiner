import dearpygui.dearpygui as dpg

from texture_set_combiner.core.state import AppState


def build_textures_export_tab(state: AppState) -> None:
    """Build the Textures Export tab wireframe."""

    with dpg.tab(label="Textures Export"):
        dpg.add_text("Textures Export")
        dpg.add_spacer(height=8)
        dpg.add_text(
            "Texture export controls will go here.",
            color=(140, 140, 140),
        )
