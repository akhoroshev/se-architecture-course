from src.command import IFsCommand
from os.path import join, isdir, split


class Cd(IFsCommand):
    """
    Cd command
    """
    def execute(self) -> None:
        """

        :return:
        """
        if len(self.m_args) > 1:
            print("too many arguments fo cd", file=self.m_out_stream)
            return
        new_dir = self.m_args[0]
        if new_dir == ".":
            return
        if new_dir == "..":
            IFsCommand.m_current_dir = split(IFsCommand.m_current_dir)[0]
            return
        if new_dir[0] != "/":
            new_dir = join(IFsCommand.m_current_dir, new_dir)
        if isdir(new_dir):
            IFsCommand.m_current_dir = new_dir
        else:
            print("Directory " + self.m_args[0] + " do not exists", file=self.m_out_stream)
