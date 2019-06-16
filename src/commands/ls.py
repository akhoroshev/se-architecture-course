from src.command import IFsCommand
from os import listdir
from os.path import abspath, isdir, join


class Ls(IFsCommand):
    """
    Ls command
    """
    def execute(self) -> None:
        if len(self.m_args) == 0:
            res = [file for file in listdir(IFsCommand.m_current_dir)]
        elif len(self.m_args) == 1:
            if self.m_args[0][0] == "/":
                dir = abspath(self.m_args[0])
            else:
                dir = abspath(join(IFsCommand.m_current_dir , self.m_args[0]))
            if isdir(dir):
                res = [file for file in listdir(dir)]
            else:
                print("Directory " + self.m_args[0] + " do not exists", file=self.m_out_stream)
                return
        print("\n".join(res), file=self.m_out_stream)
