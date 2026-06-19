from __future__ import annotations

import numpy as np
import pyassimp

from texture_set_combiner.core.mesh import _material_name

DEFAULT_UV_PREVIEW_SIZE = 512


def _black_rgba_floats(size: int) -> list[float]:
    rgba = np.zeros((size, size, 4), dtype=np.float32)
    rgba[:, :, 3] = 1.0
    return rgba.flatten().tolist()


def _material_index(scene, material_name: str) -> int | None:
    for index, material in enumerate(scene.materials):
        if _material_name(material, index) == material_name:
            return index
    return None


def _collect_uv_triangles(scene, material_index: int) -> list[tuple[tuple[float, float], tuple[float, float], tuple[float, float]]]:
    """Returns a list of triangles, each a tuple of 3 (u, v) points, in raw mesh UV space."""
    triangles: list[tuple[tuple[float, float], tuple[float, float], tuple[float, float]]] = []

    for mesh in scene.meshes:
        if mesh.materialindex != material_index:
            continue

        texture_coords = getattr(mesh, "texturecoords", None)
        if texture_coords is None or len(texture_coords) == 0:
            continue

        uvs = texture_coords[0]
        if uvs is None or len(uvs) == 0:
            continue

        faces = mesh.faces
        for face in faces:
            if len(face) != 3:
                # Skip non-triangular faces (shouldn't normally occur post-import,
                # but guards against malformed data instead of crashing).
                continue

            triangle_uvs = tuple(
                (float(uvs[vertex_index][0]), float(uvs[vertex_index][1]))
                for vertex_index in face
            )
            triangles.append(triangle_uvs)  # type: ignore[arg-type]

    return triangles


def _uv_to_pixel(u: float, v: float, size: int) -> tuple[float, float]:
    """Maps raw UV space (0,0)-(1,1) directly to pixel space, preserving original
    position. (0,0) is bottom-left in UV convention -> top-left flip for image space."""
    x = u * size
    y = (1.0 - v) * size
    return x, y


def _fill_triangle(pixels: np.ndarray, p0: tuple[float, float], p1: tuple[float, float], p2: tuple[float, float]) -> None:
    """Rasterizes a filled triangle (solid white) using barycentric coordinates.
    Points are in pixel space and may lie outside the canvas (clamped via bbox)."""
    height, width = pixels.shape[:2]

    min_x = max(int(np.floor(min(p0[0], p1[0], p2[0]))), 0)
    max_x = min(int(np.ceil(max(p0[0], p1[0], p2[0]))), width - 1)
    min_y = max(int(np.floor(min(p0[1], p1[1], p2[1]))), 0)
    max_y = min(int(np.ceil(max(p0[1], p1[1], p2[1]))), height - 1)

    if min_x > max_x or min_y > max_y:
        return  # Triangle is fully outside the canvas

    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2

    denom = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if abs(denom) < 1e-10:
        return  # Degenerate (zero-area) triangle

    for py in range(min_y, max_y + 1):
        for px in range(min_x, max_x + 1):
            # Sample at pixel center for slightly cleaner edges
            sx = px + 0.5
            sy = py + 0.5

            w0 = ((y1 - y2) * (sx - x2) + (x2 - x1) * (sy - y2)) / denom
            w1 = ((y2 - y0) * (sx - x2) + (x0 - x2) * (sy - y2)) / denom
            w2 = 1.0 - w0 - w1

            if w0 >= 0 and w1 >= 0 and w2 >= 0:
                pixels[py, px] = (255, 255, 255, 255)


def render_material_uv_rgba(
    model_path: str,
    material_name: str,
    size: int = DEFAULT_UV_PREVIEW_SIZE,
) -> np.ndarray:
    """Render a black UV preview image with filled white UV islands for one material.
    UV coordinates are mapped directly (no per-material normalization), so islands
    keep their original position within 0-1 UV space."""
    pixels = np.zeros((size, size, 4), dtype=np.uint8)
    pixels[:, :, 3] = 255

    with pyassimp.load(model_path) as scene:
        material_index = _material_index(scene, material_name)
        if material_index is None:
            return pixels

        triangles = _collect_uv_triangles(scene, material_index)
        if not triangles:
            return pixels

        for triangle in triangles:
            p0 = _uv_to_pixel(*triangle[0], size)
            p1 = _uv_to_pixel(*triangle[1], size)
            p2 = _uv_to_pixel(*triangle[2], size)
            _fill_triangle(pixels, p0, p1, p2)

    return pixels


def render_material_uv_flat(
    model_path: str,
    material_name: str,
    size: int = DEFAULT_UV_PREVIEW_SIZE,
) -> list[float]:
    """Return flattened RGBA float data for Dear PyGui dynamic textures."""
    pixels = render_material_uv_rgba(model_path, material_name, size)
    rgba = pixels.astype(np.float32) / 255.0
    return rgba.flatten().tolist()


def empty_uv_preview_flat(size: int = DEFAULT_UV_PREVIEW_SIZE) -> list[float]:
    return _black_rgba_floats(size)