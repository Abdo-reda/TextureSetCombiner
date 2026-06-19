import dearpygui.dearpygui as dpg

from texture_set_combiner.core import mesh as mesh_core
from texture_set_combiner.core.state import AppState
from texture_set_combiner.ui.native_dialog import pick_mesh_file

TAG_FILE_PATH = "mesh_import_file_path"
TAG_MATERIAL_LIST = "mesh_import_material_list"
TAG_UV_PREVIEW = "mesh_import_uv_preview"
TAG_UV_PREVIEW_HINT = "mesh_import_uv_preview_hint"


def build_mesh_import_tab(state: AppState) -> None:
    """Build the Mesh Import tab wireframe."""

    def on_browse_clicked() -> None:
        file_path = pick_mesh_file()
        if not file_path:
            return

        materials = mesh_core.load_mesh(state, file_path)
        dpg.set_value(TAG_FILE_PATH, file_path)
        dpg.configure_item(TAG_MATERIAL_LIST, items=materials)
        dpg.set_value(TAG_UV_PREVIEW_HINT, "Select a material to preview UVs")

    def on_material_selected(sender, app_data) -> None:
        state.selected_material = app_data or ""
        if state.selected_material:
            dpg.set_value(
                TAG_UV_PREVIEW_HINT,
                f"Selected: {state.selected_material}",
            )
        else:
            dpg.set_value(TAG_UV_PREVIEW_HINT, "Select a material to preview UVs")

    with dpg.tab(label="Mesh Import"):
        with dpg.group(horizontal=True):
            # Left panel — file picker and material list
            with dpg.child_window(width=360, height=-1, border=True):
                dpg.add_text("Mesh File")
                with dpg.group(horizontal=True):
                    dpg.add_input_text(
                        tag=TAG_FILE_PATH,
                        width=260,
                        readonly=True,
                        hint="No file selected",
                    )
                    dpg.add_button(label="Browse...", callback=on_browse_clicked)

                dpg.add_spacer(height=8)
                dpg.add_separator()
                dpg.add_spacer(height=4)
                dpg.add_text("Materials / Texture Sets")
                dpg.add_listbox(
                    tag=TAG_MATERIAL_LIST,
                    items=[],
                    num_items=12,
                    width=-1,
                    callback=on_material_selected,
                )

            # Right panel — UV preview placeholder
            with dpg.child_window(tag=TAG_UV_PREVIEW, width=-1, height=-1, border=True):
                dpg.add_text("UV Preview")
                dpg.add_spacer(height=4)
                with dpg.child_window(width=-1, height=-1, border=True):
                    dpg.add_text(
                        "UV layout preview will appear here",
                        tag=TAG_UV_PREVIEW_HINT,
                        color=(140, 140, 140),
                    )
