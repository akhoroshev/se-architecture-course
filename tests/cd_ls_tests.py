from src.commands.cd import Cd
from src.commands.ls import Ls
from src.command import ICommand
from unittest import TestCase
from src.stream import create_string_stream
from os import mkdir, rmdir, listdir
from os.path import abspath, join


class TestCdLs(TestCase):

    PLAYGROUND = "tmp"

    @staticmethod
    def prepare_streams(cmd: ICommand, input_stream_content=None):
        start_stream = create_string_stream()
        end_stream = create_string_stream()
        cmd.set_input_stream(start_stream)
        cmd.set_output_stream(end_stream)
        if input_stream_content:
            start_stream.write(input_stream_content)
            start_stream.seek(0, 0)
        return start_stream, end_stream

    def setUp(self) -> None:
        playground = abspath(self.PLAYGROUND)
        mkdir(playground)
        mkdir(join(playground, "1"))
        mkdir(join(playground, "1", "2"))
        mkdir(join(playground, "1", "3"))

    def test_cd_ls(self):
        cmd = Cd("cd", "tmp")
        i, o = self.prepare_streams(cmd)
        cmd.execute()
        o.seek(0, 0)
        self.assertEqual("", o.read())

        cmd = Ls("ls")
        i, o = self.prepare_streams(cmd)
        cmd.execute()
        o.seek(0, 0)
        self.assertEqual("1\n", o.read())

        cmd = Ls("ls", "1")
        i, o = self.prepare_streams(cmd)
        cmd.execute()
        o.seek(0, 0)
        self.assertEqual("2\n3\n", o.read())

        cmd = Ls("ls", "2")
        i, o = self.prepare_streams(cmd)
        cmd.execute()
        o.seek(0, 0)
        self.assertEqual("Directory 2 do not exists\n", o.read())

        cmd = Cd("cd", "2")
        i, o = self.prepare_streams(cmd)
        cmd.execute()
        o.seek(0, 0)
        self.assertEqual("Directory 2 do not exists\n", o.read())

    def tearDown(self) -> None:
        TestCdLs.recursive_rmdir(self.PLAYGROUND)

    @staticmethod
    def recursive_rmdir(directory):
        for file in listdir(directory):
            TestCdLs.recursive_rmdir(join(directory, file))
        rmdir(directory)


