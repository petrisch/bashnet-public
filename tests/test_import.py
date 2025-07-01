import os
import pytest
from bashnet.cli_core import BashnetCLI

def test_import_data_creates_knowledge_net(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()

  
    (data_dir / "commands.json").write_text("""[
        {
            "id": "cmd_echo",
            "label": "echo",
            "type": "command",
            "description": "Prints a string to stdout.",
            "related": ["opt_n"]
        }
    ]""", encoding="utf-8")

    (data_dir / "options.json").write_text("""[
        {
            "id": "opt_n",
            "label": "-n",
            "type": "option",
            "description": "Do not output the trailing newline."
        }
    ]""", encoding="utf-8")

  
    (data_dir / "concepts.json").write_text("[]", encoding="utf-8")
    (data_dir / "scripting.json").write_text("[]", encoding="utf-8")

    
    cli = BashnetCLI()
    cli.data_dir = str(data_dir)
    cli.knowledge_file = str(data_dir / "knowledge_net.json")

    cli.import_data()

  
    assert os.path.exists(cli.knowledge_file)
    assert cli.net.has_node("cmd_echo")
    assert cli.net.has_node("opt_n")
    assert any(
        source == "cmd_echo" and target == "opt_n" and relation == "related"
        for source, target, relation in cli.net.graph.edges.data("relation")
    )
