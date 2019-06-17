from src.cli_executor import CliExecutor
from src.commands import Cat
from src.commands import Echo
from src.commands import External
from src.commands import BinaryOperator
from src.commands import Pwd
from src.commands import Signal
from src.commands import Wc

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
