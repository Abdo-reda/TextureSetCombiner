import os
import platform

def register_bundled_assimp():
    lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libs", "assimp")
    system = platform.system()
    if system == "Windows" and hasattr(os, "add_dll_directory"):
        os.environ["PATH"] = lib_dir + os.pathsep + os.environ.get("PATH", "")
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(lib_dir)
    elif system == "Darwin":
        os.environ["DYLD_LIBRARY_PATH"] = lib_dir + os.pathsep + os.environ.get("DYLD_LIBRARY_PATH", "")
    elif system == "Linux":
        os.environ["LD_LIBRARY_PATH"] = lib_dir + os.pathsep + os.environ.get("LD_LIBRARY_PATH", "")

 
register_bundled_assimp()

from texture_set_combiner.app import TextureSetCombinerApp

def main() -> None:
    app = TextureSetCombinerApp()
    app.run()

if __name__ == "__main__":
    main()
