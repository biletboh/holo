"""
This module process introduces CLI for article analysis.
"""

import argparse
import logging
import sys


from analyze import (
    gather_statistics,
    aggregate_statistics,
    create_plot,
)


__author__ = "Bohdan Biletskyi"
__copyright__ = "Bohdan Biletskyi"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


from analyze import gather_statistics, aggregate_statistics


def parse_args(args):
    """Parse command line parameters
    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).
    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Analyze articles data and gather statistics"
    )
    parser.add_argument(
        "-f", "--file", help="Path to the initial data csv file.", type=str
    )
    parser.add_argument(
        "-l",
        "--language",
        help="Language code: pl or ua",
        type=str,
        default="ua",
    )
    parser.add_argument(
        "-w",
        "--words",
        help="Key words to analyze.",
        type=str,
    )
    parser.add_argument(
        "-a",
        "--aggregate",
        help="Only aggregate statistics",
        type=bool,
        default=False,
    )
    parser.add_argument(
        "-p",
        "--plot",
        help="Create plot",
        type=bool,
        default=False,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging
    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel,
        stream=sys.stdout,
        format=logformat,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion
    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formated message.
    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting script...")

    if args.plot:
        create_plot()
    elif args.words:
        if args.aggregate:
            aggregate_statistics(args.language, args.words)
        else:
            gather_statistics(args.file, args.language, args.words)
    else:
        print("Please, provide words to analyze (-w)")

    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`
    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
