"""GenomeLens GFF file parser.

Parse GFF file line by line and convert all records to a gene,
preserving the original type in a column feature GL_Type.

"""

from typing import Callable
import re

import click
from click.decorators import FC
import logging

__all__ = ["__version__", "main"]

from ._version import version as __version__


logger = logging.getLogger(__name__)


def verbose_option(expose_value: bool = False) -> Callable[[FC], FC]:
    """Add verbose option with callback"""

    def verbose_callback(
        ctx: click.core.Context, param: click.core.Option, value: int
    ) -> int:
        """Verbose callback"""
        log_level = max(3 - value, 0) * 10
        logging.basicConfig(
            level=log_level,
            format="%(levelname)s [%(name)s:%(funcName)s]: %(message)s",
        )
        return log_level

    verbose = click.option(
        "--verbose",
        "-v",
        help="Set the verbosity level",
        count=True,
        callback=verbose_callback,
        expose_value=expose_value,
        is_eager=True,
    )
    return verbose


CHOICES = [
    "CDS",
    "mRNA",
    "exon",
    "TF_binding_site",
    "five_prime_UTR",
    "three_prime_UTR",
    "intron",
    "repeat_region",
    "transposable_element",
    "other",
]


@click.command()
@click.argument("gff", type=click.File("r"), default="-")
@click.argument("output", type=click.File("w"), default="-")
@click.option(
    "--rewrite", type=click.Choice(CHOICES, case_sensitive=False), multiple=True
)
@verbose_option()
@click.pass_context
def main(ctx, gff, output, rewrite):
    """Parse GFF file and convert all records to a gene."""
    logger.debug("Parsing GFF")
    rewrite = list(rewrite) + ["gene"]
    for line in gff:
        line = line
        if line.startswith("#"):
            output.write(line)
            continue
        fields = re.split(r"\s+", line.strip())
        if fields[2] not in rewrite:
            continue
        if re.search("GL_Feature=", fields[8]):
            continue
        features = re.sub("Parent=", "GL_Parent=", fields[8])
        fields[8] = f"{features};GL_Feature={fields[2]}"
        fields[2] = "gene"
        output.write("\t".join(fields) + "\n")
