"""OS-native file dialogs via crossfiledialog."""

import crossfiledialog

MESH_FILE_FILTER = {"Mesh files": ["*.fbx", "*.obj"]}


def pick_mesh_file() -> str:
    """Open the OS file picker for a single mesh file.

    Returns the selected path, or an empty string if cancelled.
    """
    return crossfiledialog.open_file(
        title="Select mesh file",
        filter=MESH_FILE_FILTER,
    )
