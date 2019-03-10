from src.command import IFsCommand
from os import listdir


class Ls(IFsCommand):
    def execute(self) -> None:
        res = [file for file in listdir(IFsCommand.m_current_dir)]
        print(" ".join(res), file=self.m_out_stream)
