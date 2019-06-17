from src.command import ICommand


class Cat(ICommand):
    """
    Cat command
    """
    def execute(self) -> None:
        if self.m_args:
            for filename in self.m_args:
                with open(filename, "rb") as file:
                    print(file.read().decode(encoding='utf-8'),
                          flush=True,
                          end='',
                          file=self.m_out_stream)
        else:
            line = self.m_inp_stream.readline()
            while line:
                print(line, file=self.m_out_stream, end='')
                line = self.m_inp_stream.readline()
