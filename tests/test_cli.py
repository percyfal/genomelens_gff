"""Test CLI."""

import re

from genomelens_gff import main


def test_cli_help(runner):
    result = runner.invoke(main, ["--help"])
    assert not result.exception
    assert re.search(
        r"\s+Parse GFF file and convert all records to a gene.",
        result.output,
    )
    assert re.search(r"--help\s+Show this message and exit.", result.output)


def test_cli_run(runner, gff_file):
    result = runner.invoke(main, [str(gff_file)])
    assert not result.exception
    data = result.output.splitlines()
    assert len(data) > 0
    for line in data:
        if line.startswith("#"):
            continue
        fields = re.split(r"\s+", line.strip())
        assert len(fields) == 9
        assert fields[2] == "gene"
        assert fields[8].startswith("GL_Type=")
