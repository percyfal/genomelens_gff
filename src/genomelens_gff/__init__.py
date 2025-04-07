"""GenomeLens GFF file parser.

Parse GFF file line by line and convert all records to a gene,
preserving the original type in a column feature GL_Type.

"""

import re

import click

__all__ = ["__version__", "main"]

from ._version import version as __version__


@click.command()
@click.argument("gff", type=click.File("r"), default="-")
@click.argument("output", type=click.File("w"), default="-")
@click.pass_context
def main(ctx, gff, output):
    """Parse GFF file and convert all records to a gene."""
    for line in gff:
        line = line
        if line.startswith("#"):
            output.write(line)
            continue
        fields = re.split(r"\s+", line.strip())
        fields[8] = f"GL_Type={fields[2]};{fields[8]}"
        fields[2] = "gene"
        output.write("\t".join(fields) + "\n")
