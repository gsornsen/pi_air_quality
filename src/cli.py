import argparse

async def get_cli_args():
    parser = argparse.ArgumentParser(description="""
        Start the air-quality application
    """)
    parser.add_argument(
        "--mode",
        help="simulation or normal mode?",
        default="normal"
    )
    parser.add_argument(
        "--verbose",
        help="Settings this flag will log data in stdout",
        action="store_true"
    )
    parser.add_argument(
        "--write",
        help="Setting this flag will write data to the DB",
        action="store_true"
    )
    args = parser.parse_args()
    return args