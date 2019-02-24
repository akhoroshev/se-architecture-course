from src.environment import create_environment
from src.parser import create_parser
from src.preprocessor import create_preprocessor
from src.command import ICommand
from src.stream import IStream, \
    create_string_stream, \
    get_stdout_stream, \
    get_stdin_stream


class CliExecutor:
    def __init__(self):
        self.m_should_stop = False
        self.m_environment = create_environment()
        self.m_parser = create_parser()
        self.m_preprocessor = create_preprocessor()

    def add_command(self, command_constructor, name: str, infix: bool):
        """
        Associate a command with a name.
        :param command_constructor: callable
        :param name: str
        :param infix: bool
        """
        self.m_parser.add_command(command_constructor, name, infix)

    def set_default_command(self, command_constructor):
        """
        The default command if an unknown command has passed
        :param command_constructor: callable
        """
        self.m_parser.set_default_command(command_constructor)

    def add_environment_variable(self, env, value):
        """
        Add env variable
        :param env: str
        :param value: str
        """
        self.m_environment.add(env, value)

    def run(self):
        """
        Run main loop
        """
        while not self.m_should_stop:
            try:
                print("> ", end='', flush=True)
                line = get_stdin_stream().readline()
                token_array = self.m_preprocessor.process(line, self.m_environment)
                command_list = self.m_parser.parse(token_array)
                CliExecutor.execute_command_list(command_list,
                                                 get_stdin_stream(),
                                                 get_stdout_stream())
            except Exception as e:
                print(e)

    def stop(self):
        """
        Stop main loop
        """
        self.m_should_stop = True

    @staticmethod
    def execute_command_list(command_list: [ICommand], start_stream: IStream, end_stream: IStream):
        """
        Executing a list of commands with sequential linking of streams
        :param command_list: [ICommand]
        :param start_stream: input stream for fst command
        :param end_stream: output stream for last command
        """
        last_idx = len(command_list) - 1
        current_stream: IStream = None
        for idx, command in enumerate(command_list):
            if idx == 0:
                command.set_input_stream(start_stream)
            else:
                current_stream.seek(0, 0)
                command.set_input_stream(current_stream)
            if idx != last_idx:
                current_stream = create_string_stream()
                command.set_output_stream(current_stream)
            else:
                command.set_output_stream(end_stream)

            command.execute()
