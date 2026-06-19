import dearpygui.dearpygui as dpg

from texture_set_combiner.core import mesh as mesh_core
from texture_set_combiner.core.state import AppState

TAG_FILE_PATH = "mesh_import_file_path"
TAG_MATERIAL_LIST = "mesh_import_material_list"
TAG_FILE_DIALOG = "mesh_import_file_dialog"
TAG_UV_PREVIEW = "mesh_import_uv_preview"


def build_mesh_import_tab(state: AppState) -> None:
    """Build the Mesh Import tab wireframe."""

    def on_browse_clicked() -> None:
        dpg.show_item(TAG_FILE_DIALOG)

    def on_file_selected(sender, app_data) -> None:
        file_path = app_data["file_path_name"]
        dpg.set_value(TAG_FILE_PATH, file_path)
        mesh_core.load_mesh(state, file_path)

    def on_material_selected(sender, app_data) -> None:
        state.selected_material = app_data
        # UV preview update will be wired here later.

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
                        color=(140, 140, 140),
                    )

    with dpg.file_dialog(
        tag=TAG_FILE_DIALOG,
        directory_selector=False,
        show=False,
        callback=on_file_selected,
        width=700,
        height=400,
        default_path=".",
    ):
        dpg.add_file_extension(
            "Mesh files (*.obj, *.fbx){.obj,.fbx}",
            color=(100, 200, 100),
        )
