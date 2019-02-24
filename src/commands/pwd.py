from src.command import IFsCommand


class Pwd(IFsCommand):
    def execute(self) -> None:
        print(IFsCommand.m_current_dir, file=self.m_out_stream)
