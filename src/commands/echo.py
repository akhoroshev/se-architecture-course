from src.command import ICommand


class Echo(ICommand):
    def execute(self) -> None:
        print(' '.join(self.m_args), file=self.m_out_stream)
