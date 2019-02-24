from src.command import ICommand, CommandArgumentCountError


class Callback(ICommand):
    def __init__(self, action, number_of_params, name, *args):
        super().__init__(name, *args)
        self.m_action = action
        self.m_number_of_params = number_of_params
        if number_of_params and len(args) != number_of_params:
            raise CommandArgumentCountError(self.m_name)

    def execute(self) -> None:
        if self.m_number_of_params:
            self.m_action(*self.m_args[:self.m_number_of_params])
        else:
            self.m_action()
