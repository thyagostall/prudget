class UIPrinter:
    def __init__(self):
        self._length = 0

    def _get_title(self, title):
        length = self._get_line_length()
        return '|{:^{length}}|\n'.format(title, length=length - 2)

    def _get_line_length(self):
        raise NotImplementedError

    def _get_separator(self):
        return '-' * self._get_line_length() + '\n'

    def _get_length(self):
        raise NotImplementedError

    def print(self):
        self._length = self._get_length()
