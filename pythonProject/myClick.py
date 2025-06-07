
import click
from repository import Repository

class Cli:

    def __init__(self, current):
        self.repository = Repository(current)
        print(self.repository)

    def create_cli(self):

        @click.group()
        def cli():
            """Management user interface repository"""
            pass

        @cli.command()
        def init():
            try:
                self.repository.wit_init()
                click.echo("Initialized repository structure.")
            except Exception as e:
                click.echo(f"Error {e}")

        @cli.command()
        # @click.argument()
        def add():
            try:
                self.repository.wit_add()
                # click.echo(f"file {file_name} added successfully.")
            except Exception as e:
                click.echo(f"Error {e}")

        @cli.command()
        # @click.argument("message")
        def commit():
            try:
                self.repository.wit_commit()
                click.echo(f"Commited successfully.")
            except Exception as e:
                click.echo(f"Error {e}")

        @cli.command()
        def log():
            try:
                self.repository.wit_log()
            except Exception as e:
                click.echo(f"Error {e}")

        @cli.command()
        def status():
            try:
                self.repository.wit_status()
            except Exception as e:
                click.echo(f"Error {e}")

        @cli.command()
        # @click.argument("commit_hash")
        def checkout():
            try:
                self.repository.wit_checkout()
            except Exception as e:
                click.echo(f"Error {e}")

        @cli.command()
        # @click.argument("commit_hash")
        def push():
            try:
                self.repository.wit_push()
            except Exception as e:
                click.echo(f"Error {e}")

        return cli