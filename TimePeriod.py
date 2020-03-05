class FileInterpreter:
    file_path: str
    mode: str

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.mode = None

    def __check_syntax(self, line: str, line_num: int) -> None:
        string_list = line.split(" ")
        for string in string_list:
            if type(string) is not str:
                raise Exception("line ", line_num, " contains non string element")
            elif string == "":
                raise Exception("line ", line_num, " contains additional whitespaces")
            else



    def parse(self) -> None:
        f = open(self.file_path, "r")
        line_num = 0
        for line in f:
            self.__check_syntax(line, line_num)
            line_num = line_num + 1


class InitialConditions:
    def __init__(self):
        pass


class TimePeriod:
    def __init__(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')

    def read(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')

    def calculate(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')

    def write(self):
        raise Exception(type(self), ' ', __name__, ' is not implemented')
