# 🧠 Bashnet – Semantic Bash Learning CLI

Bashnet is a cross-platform command-line tool that helps you explore and learn Bash commands, options, and scripting structures using a semantic network.

---

## 🚀 Features

- Import modular Bash knowledge from structured JSON files  
- Deep semantic search: finds related options, concepts, commands  
- Simple search: retrieve a single concept by label  
- Export complete semantic network as `knowledge_net.json`  
- Visualize the network as interactive HTML (via pyvis)  
- Fully Docker-compatible for platform-independent execution  
- CLI interface with live terminal usage

---

## 📊 JSON File Roles

Each file defines a component of the semantic network:

- `commands.json`: Bash commands (e.g. `ls`, `cd`)
- `options.json`: CLI flags and options (e.g. `-l`, `--help`) — must be described independently of any command
- `scripting.json`: Syntax and structures like `if`, `for`, `[[ ]]`
- `concepts.json`: Abstract/contextual terms like `directory`, `stdout`
- `knowledge_net.json`: The complete, generated semantic network (nodes + relations)

All files should be placed in the `src/data/` folder to be imported correctly.

---

### 📁 Minimal Example (Extendable)

To get started, here's a small valid example:

**src/data/commands.json**
```json
[
    {
        "id": "cmd_cd",
        "label": "cd",
        "type": "command",
        "description": "Changes the current working directory to a specified path.",
        "category": "file management",
        "tags": [
            "filesystem",
            "navigation",
            "directory",
            "shell"
        ],
        "examples": [
            {
                "command": "cd /home/user",
                "expected_output": "",
                "explanation": "Changes to the absolute path '/home/user'."
            },
            {
                "command": "cd ..",
                "expected_output": "",
                "explanation": "Moves one level up to the parent directory."
            }
        ],
        "options": [],
        "related": [
            "cmd_pwd",
            "con_directory"
        ],
        "links": [
            "https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html#index-cd"
        ]
    }
]
 
```

---

## 🐳 Run with Docker (Recommended)

### 🔧 Step 1: Build the image

```bash
docker build -t bashnet .
```

### ▶ Step 2: Start the CLI

```bash
docker run --rm -it \
  -v "$PWD:/app" \
  -e RUNNING_IN_DOCKER=1 \
  bashnet
```

### 🧾 Flags explained

| Flag                     | Description                                               |
| ------------------------ | --------------------------------------------------------- |
| `--rm`                   | Automatically delete the container after exit             |
| `-it`                    | Enables interactive input/output (CLI)                    |
| `-v "$PWD:/app"`         | Mounts your working dir (so JSON & HTML stay persistent)  |
| `-e RUNNING_IN_DOCKER=1` | Disables automatic browser open for HTML inside container |

---

## 💡 CLI Commands

Run inside the container or Python shell:

```text
bashnet> import
    → Loads JSON files and builds the semantic net

bashnet> search <term>
    → Deep search including context like options, related concepts

bashnet> search <term> --simple
    → Exact search for a node only

bashnet> visualize
    → Generates semantic_net.html with interactive graph

bashnet> exit
    → Leave the Bashnet CLI
```


---

## 🧪 Run Without Docker (Local Python)

You can also run Bashnet locally if you prefer:

1. Ensure Python 3.12+ is installed
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the CLI:

```bash
python -m bashnet
```

---

## ⚙️ Requirements

Minimal:

```text
click
networkx
pyvis
```

Optionally, use [Poetry](https://python-poetry.org/) for development:

```bash
poetry install
poetry run python -m bashnet
```

---

## 📄 License

MIT License – free to use, modify, extend.
Copyright (c) 2025