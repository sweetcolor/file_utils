class Logging:
    def __init__(self, log_name: str):
        self.log_file = open(log_name, 'w')
        self._temporary_line: str = ''

    def __del__(self):
        self.log_file.close()

    def log_message(self, message: str, end: str = '\n'):
        print(message, end=end)
        if end == '\n':
            if self._temporary_line:
                self.log_file.write(self._temporary_line + message + end)
                self._temporary_line = ''
            else:
                self.log_file.write(message + end)
        else:
            self._temporary_line = message
