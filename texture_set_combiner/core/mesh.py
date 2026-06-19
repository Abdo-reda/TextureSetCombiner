import pyassimp
from texture_set_combiner.core.state import AppState


def load_mesh(state: AppState, file_path: str) -> None:
    """Load a mesh file and update application state. Implementation TBD."""
    get_materials(state, file_path)
    print("---- is this working?", file_path)
    pass


def get_materials(state: AppState, model_path: str) -> list[str]:
    """Return detected materials / texture sets for the loaded mesh."""
    with pyassimp.load(model_path) as scene:
        for i, material in enumerate(scene.materials):
            props = material.properties
            name = props.get("name", f"Material_{i}")
            print(f"\nMaterial {i}: {name}")
 
            for key, value in props.items():
                # texture file paths usually show up under keys like
                # 'file' / 'file.diffuse' / 'file.normals' depending on the build
                if "file" in key.lower():
                    print(f"  Texture ({key}): {value}")
                else:
                    print(f"  {key}: {value}")

    return state.materials
