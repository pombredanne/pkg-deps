#!/usr/bin/env python
import click

from . import collector
from . import annotators
from . import writers


@click.command()
@click.argument('packages', nargs=-1, required=True)
@click.option('--outdated', is_flag=True, help="Look for outdated packages.")
@click.option('--human', 'format', flag_value='human', default=True,
              help="Print results in simple human-readable form.")
@click.option('--dot', 'format', flag_value='dot',
              help="""Write in the GraphViz 'dot' format, for direct
              visualization.""")
@click.option('--graphml', 'format', flag_value='graphml',
              help="""Write in the XML-based GraphML format, for use with Gephi
              or other graph programs.""")
@click.option('--json', 'format', flag_value='json',
              help="""Write in a 'node-link' JSON format, for use with other
              Python tools or d3.js.""")
@click.option('--precise-pin', is_flag=True,
              help="""Annotate packages that the top-level package depends on
              directly without exactly pinning the version (xyz==N.N).""")
@click.option('--should-pin-all', is_flag=True,
              help="""Annotate packages that the top-level package depends on
              indirectly but not directly.""")
def main(packages, outdated, format, precise_pin, should_pin_all):
    """Print dependencies and latest versions available."""

    graph = None

    # Need this because e.g. PrJ_bankIt becomes prj-bankit.
    good_package_names = []
    for package in packages:
        graph, top = collector.collect_dependencies(package, graph=graph)
        good_package_names.append(top)

    if outdated:
        annotators.add_available_updates(graph)

    if precise_pin:
        annotators.should_pin_precisely(graph, good_package_names)

    if should_pin_all:
        annotators.should_pin_all(graph, good_package_names)

    getattr(writers, format)(graph)


if __name__ == '__main__':
    main()
