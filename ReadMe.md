# Texture Set Combiner

A tool for combining texture sets.

The app is organized around three tabs:

- **Mesh Import** — pick a mesh file, view detected materials / texture sets, and preview UVs
- **Textures Import** — import texture files
- **Textures Export** — export combined texture sets

UI is built with [Dear PyGui](https://github.com/hoffstadt/DearPyGui). 

## Run

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python main.py
```


## AI Usage Disclaimer

Generally, I am not a big fan of AI usage for many reasons and I prefer to keep its usage limited in my personal projects espeically the ones that I care about and want to enjoy making. 

However, this project is a bit different. The only reason I made this project was because I faced an issue in my current workflows and I needed this tool to help me. So, Utimately, the project was born out of "necessity" rather than pure "curiosity". As result, I don't really mind using AI that much.

The initial project scaffold, folder structure, Dear PyGui tab wireframes, application logic, and this README used the help of AI assistance (Cursor).

Most of the code was reviewed and if needed, was modified by me.