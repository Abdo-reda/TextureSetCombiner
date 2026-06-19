"""OS-native file dialogs (tkinter-backed, no Dear PyGui file dialog)."""

import tkinter as tk
from tkinter import filedialog


def pick_mesh_file() -> str:
    """Open the OS file picker for mesh files. Returns a path or an empty string."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    root.update()

    file_path = filedialog.askopenfilename(
        title="Select mesh file",
        filetypes=[
            ("Mesh files", "*.fbx *.obj"),
            ("FBX files", "*.fbx"),
            ("OBJ files", "*.obj"),
            ("All files", "*.*"),
        ],
    )

    root.destroy()
    return file_path or ""
