from dataclasses import dataclass, field


@dataclass
class AppState:
    """Shared application state. Populate via core logic, read by the UI."""

    mesh_file_path: str = ""
    materials: list[str] = field(default_factory=list)
    selected_material: str = ""
