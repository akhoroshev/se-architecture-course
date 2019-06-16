from src.cli_executor import CliExecutor
from src.commands.cat import Cat
from src.commands.echo import Echo
from src.commands.external import External
from src.commands.operators import BinaryOperator
from src.commands.pwd import Pwd
from src.commands.signal import Signal
from src.commands.wc import Wc

if __name__ == "__main__":
    cli = CliExecutor()
    cli.add_command(Echo, "echo", False)
    cli.add_command(Cat, "cat", False)
    cli.add_command(Pwd, "pwd", False)
    cli.add_command(Wc, "wc", False)
    cli.add_command(lambda name, *_: Signal(cli.stop, name), "exit", False)
    cli.add_command(lambda name, lhs, rhs: BinaryOperator(cli.add_environment_variable, name, lhs, rhs), "=", True)
    cli.set_default_command(External)

    cli.run()
