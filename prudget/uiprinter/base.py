class UIPrinter:
    def _get_title(self, title, length):
        length = self._get_line_length(length)
        return '|{:^{length}}|\n'.format(title, length=length - 2)

    def _get_line_length(self, widest_item_length):
        raise NotImplementedError

    def _get_separator(self, widest_item_length):
        return '-' * self._get_line_length(widest_item_length) + '\n'
