import os
from myClick import Cli

if __name__ == "__main__":
    current = os.getcwd()
    ui = Cli(current)
    cli = ui.create_cli()
    cli()
