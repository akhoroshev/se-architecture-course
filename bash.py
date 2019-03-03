from src.cli_executor import CliExecutor
from src.commands.echo import Echo
from src.commands.cat import Cat
from src.commands.callback import Callback
from src.commands.pwd import Pwd
from src.commands.wc import Wc
from src.commands.external import External
from src.commands.grep import Grep
from functools import partial


if __name__ == "__main__":
    cli = CliExecutor()
    cli.add_command(Echo, "echo", False)
    cli.add_command(Cat, "cat", False)
    cli.add_command(Pwd, "pwd", False)
    cli.add_command(Wc, "wc", False)
    cli.add_command(partial(Callback, cli.stop, None), "exit", False)
    cli.add_command(partial(Callback, cli.add_environment_variable, 2), "=", True)
    cli.add_command(Grep, "grep", False)

    cli.set_default_command(External)

    cli.run()
