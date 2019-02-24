from src.command import ICommand
import subprocess
from io import TextIOWrapper, BytesIO


class External(ICommand):
    def execute(self) -> None:
        if self.m_inp_stream.isatty() and self.m_out_stream.isatty():
            self.std_std()
        elif self.m_inp_stream.isatty() and not self.m_out_stream.isatty():
            self.std_pipe()
        elif not self.m_inp_stream.isatty() and self.m_out_stream.isatty():
            self.pipe_std()
        elif not self.m_inp_stream.isatty() and not self.m_out_stream.isatty():
            self.pipe_pipe()

    def std_std(self):
        subprocess.call([self.m_name, *self.m_args], stdin=self.m_inp_stream, stdout=self.m_out_stream)

    def std_pipe(self):
        p = subprocess.Popen([self.m_name, *self.m_args],
                             stdin=self.m_inp_stream,
                             stdout=subprocess.PIPE)
        output, output_err = p.communicate()
        self.m_out_stream.write(TextIOWrapper(BytesIO(output), encoding='utf-8').read())

    def pipe_pipe(self):
        p = subprocess.Popen([self.m_name, *self.m_args],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        output, output_err = p.communicate(str.encode(self.m_inp_stream.read(), encoding='utf-8'))
        self.m_out_stream.write(TextIOWrapper(BytesIO(output), encoding='utf-8').read())

    def pipe_std(self):
        p = subprocess.Popen([self.m_name, *self.m_args],
                             stdin=subprocess.PIPE,
                             stdout=self.m_out_stream)
        p.communicate(str.encode(self.m_inp_stream.read(), encoding='utf-8'))
