from src.command import ICommand


class Stat:
    """
    Entry for holding statistic
    """
    def __init__(self):
        self.n_lines = 0
        self.n_words = 0
        self.n_bytes = 0

    def __iadd__(self, other):
        self.n_lines += other.n_lines
        self.n_words += other.n_words
        self.n_bytes += other.n_bytes
        return self


class Wc(ICommand):
    def execute(self) -> None:
        if self.m_args:
            total_stat = Stat()
            for filename in self.m_args:
                stat = self.handle_input(filename)
                total_stat += stat
                print("{} {} {} {}".format(
                    stat.n_lines, stat.n_words, stat.n_bytes, filename),
                    file=self.m_out_stream)
            if len(self.m_args) > 1:
                print("{} {} {} total".format(
                    total_stat.n_lines, total_stat.n_words, total_stat.n_bytes),
                    file=self.m_out_stream)
        else:
            stat = self.handle_input()
            print("{:>8} {:>7} {:>7}".format(
                stat.n_lines, stat.n_words, stat.n_bytes), file=self.m_out_stream)

    def handle_input(self, input_name=None):
        def summarize(handle):
            stat = Stat()
            for line in handle:
                stat.n_lines += 1
                stat.n_words += len(line.split())
                stat.n_bytes += len(line)
            return stat

        if input_name:
            with open(input_name, "rb") as file:
                return summarize(file)
        else:
            return summarize(self.m_inp_stream)
