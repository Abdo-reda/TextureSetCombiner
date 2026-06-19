from texture_set_combiner.core.state import AppState


def load_mesh(state: AppState, file_path: str) -> None:
    """Load a mesh file and update application state. Implementation TBD."""
    pass


def get_materials(state: AppState) -> list[str]:
    """Return detected materials / texture sets for the loaded mesh. Implementation TBD."""
    return state.materials
