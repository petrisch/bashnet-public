from bashnet.cli_core import BashnetCLI
from bashnet.node import Node
from bashnet.edge import Edge


sample_command = {
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

sample_option = {
    "id": "opt_a",
        "label": "-a",
        "type": "option",
        "description": "Includes all entries, even those that are normally hidden, such as dotfiles or user processes.",
        "tags": [
            "all",
            "hidden",
            "dotfiles",
            "visibility"
        ],
        "links": [
            "https://man7.org/linux/man-pages/man1/ls.1.html",
            "https://man7.org/linux/man-pages/man1/ps.1.html"
        ]
}

sample_concept = {
    "id": "con_file",
    "label": "File",
    "type": "concept",
    "description": "A file is a data object stored in the filesystem. It can contain text, binary data, or be executable.",
    "category": "filesystem",
    "tags": ["data", "object", "text", "binary", "executable"],
    "examples": ["readme.txt", "script.sh", "/etc/passwd"],
    "related": ["cmd_ls", "cmd_rm"],
    "links": ["https://en.wikipedia.org/wiki/Computer_file"]
}

sample_scripting = {
    "id": "scr_if",
        "label": "if",
        "type": "scripting",
        "description": "Evaluates a condition and executes a block of code if the condition is true.",
        "category": "control structure",
        "tags": [
            "condition",
            "branch",
            "logic"
        ],
        "examples": [
            {
                "command": "if [ $x -eq 1 ]; then echo 'Equal'; fi",
                "expected_output": "Equal",
                "explanation": "Executes the code block because x equals 1."
            },
            {
                "command": "if [ $x -eq 2 ]; then echo 'Yes'; else echo 'No'; fi",
                "expected_output": "No",
                "explanation": "The else block runs because the condition is false."
            }
        ],
        "related": [
            "scr_then",
            "scr_else"
        ],
        "links": [
            "https://www.gnu.org/software/bash/manual/bash.html#Conditional-Constructs"
        ]
}

class DummyCLI(BashnetCLI):
    def __init__(self, nodes):
        super().__init__()
        self.net.graph.clear() 
        for node in nodes:
            self.net.add_node(Node(
                node_id=node["id"],
                label=node["label"],
                node_type=node["type"],
                **{k: v for k, v in node.items() if k not in {"id", "label", "type"}}
            ))

def test_simple_search_command():
    cli = DummyCLI([sample_command])
    result = cli.simple_search("cd")
    assert result is not None
    assert result["id"] == "cmd_cd"

def test_simple_search_option():
    cli = DummyCLI([sample_option])
    result = cli.simple_search("-a")
    assert result is not None
    assert result["id"] == "opt_a"

def test_simple_search_concept():
    cli = DummyCLI([sample_concept])
    result = cli.simple_search("File")
    assert result is not None
    assert result["id"] == "con_file"

def test_simple_search_scripting():
    cli = DummyCLI([sample_scripting])
    result = cli.simple_search("if")
    assert result is not None
    assert result["id"] == "scr_if"

def test_simple_search_term():
    cli = DummyCLI([])
    result = cli.simple_search("nonexistent")
    assert result is None

def test_deep_search_command():
    cli = DummyCLI([sample_command])
    node, context = cli.deep_search("cd")
    assert node is not None
    assert node["id"] == "cmd_cd"
    assert isinstance(context, dict)

def test_deep_search_option():
    cli = DummyCLI([sample_command, sample_option])
    cli.net.add_edge(Edge("cmd_cd", "opt_a", "options"))
    node, context = cli.deep_search("-a")
    assert node is not None
    assert node["id"] == "opt_a"
    assert "commands" in context

def test_deep_search_concept():
    cli = DummyCLI([sample_concept])
    node, context = cli.deep_search("File")
    assert node is not None
    assert node["id"] == "con_file"
    assert "commands" in context or "options" in context or "others" in context

def test_deep_search_scripting():
    cli = DummyCLI([sample_scripting])
    node, context = cli.deep_search("if")
    assert node is not None
    assert node["id"] == "scr_if"
    assert "related" in context

def test_deep_search_term():
    cli = DummyCLI([sample_command])
    node, context = cli.deep_search("cd")
    assert node is not None
    assert node["id"] == "cmd_cd"

def test_deep_search_non_existing():
    cli = DummyCLI([])
    node, context = cli.deep_search("unknown_term")
    assert node is None
    assert "fallback" in context