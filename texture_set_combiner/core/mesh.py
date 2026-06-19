import pyassimp

from texture_set_combiner.core.state import AppState


def _material_name(material, index: int) -> str:
    props = material.properties
    try:
        name = str(props["name"]).strip()
        if name:
            return name
    except (KeyError, TypeError):
        pass
    return f"Material_{index}"


def get_materials(state: AppState, model_path: str) -> list[str]:
    """Read material names from a mesh file and store them on state."""
    materials: list[str] = []

    with pyassimp.load(model_path) as scene:
        for index, material in enumerate(scene.materials):
            name = _material_name(material, index)
            if name not in materials:
                materials.append(name)

    state.materials = materials
    return materials


def load_mesh(state: AppState, file_path: str) -> list[str]:
    """Load a mesh file and return detected material names."""
    state.mesh_file_path = file_path
    state.selected_material = ""
    return get_materials(state, file_path)
