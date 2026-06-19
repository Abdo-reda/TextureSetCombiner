import dearpygui.dearpygui as dpg

from texture_set_combiner.core import mesh as mesh_core
from texture_set_combiner.core import uv_preview as uv_preview_core
from texture_set_combiner.core.state import AppState
from texture_set_combiner.ui.native_dialog import pick_mesh_file

TAG_FILE_PATH = "mesh_import_file_path"
TAG_MATERIAL_LIST = "mesh_import_material_list"
TAG_UV_PREVIEW = "mesh_import_uv_preview"
TAG_SELECTED_MATERIAL = "mesh_import_selected_material"
TAG_UV_TEXTURE = "mesh_import_uv_texture"
TAG_UV_IMAGE = "mesh_import_uv_image"

UV_PREVIEW_SIZE = uv_preview_core.DEFAULT_UV_PREVIEW_SIZE


def build_mesh_import_tab(state: AppState) -> None:
    """Build the Mesh Import tab."""

    def refresh_uv_preview() -> None:
        if not state.mesh_file_path or not state.selected_material:
            dpg.set_value(TAG_SELECTED_MATERIAL, "")
            dpg.set_value(
                TAG_UV_TEXTURE,
                uv_preview_core.empty_uv_preview_flat(UV_PREVIEW_SIZE),
            )
            return

        dpg.set_value(TAG_SELECTED_MATERIAL, state.selected_material)
        texture_data = uv_preview_core.render_material_uv_flat(
            state.mesh_file_path,
            state.selected_material,
            UV_PREVIEW_SIZE,
        )
        dpg.set_value(TAG_UV_TEXTURE, texture_data)

    def on_browse_clicked() -> None:
        file_path = pick_mesh_file()
        if not file_path:
            return

        materials = mesh_core.load_mesh(state, file_path)
        dpg.set_value(TAG_FILE_PATH, file_path)
        dpg.configure_item(TAG_MATERIAL_LIST, items=materials)
        refresh_uv_preview()

    def on_material_selected(sender, app_data) -> None:
        state.selected_material = app_data or ""
        refresh_uv_preview()

    with dpg.tab(label="Mesh Import"):
        with dpg.group(horizontal=True):
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

            with dpg.child_window(tag=TAG_UV_PREVIEW, width=-1, height=-1, border=True):
                dpg.add_text("UV Preview")
                dpg.add_text("", tag=TAG_SELECTED_MATERIAL, color=(180, 180, 180))
                dpg.add_spacer(height=4)
                with dpg.child_window(width=-1, height=-1, border=True):
                    with dpg.texture_registry():
                        dpg.add_dynamic_texture(
                            UV_PREVIEW_SIZE,
                            UV_PREVIEW_SIZE,
                            uv_preview_core.empty_uv_preview_flat(UV_PREVIEW_SIZE),
                            tag=TAG_UV_TEXTURE,
                        )
                    dpg.add_image(TAG_UV_TEXTURE, tag=TAG_UV_IMAGE)
