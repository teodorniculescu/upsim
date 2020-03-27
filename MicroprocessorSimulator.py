from FileInterpreter import FileInterpreter
from Simulation import Simulation


def main():
    file_in = "tests/test1"
    file_out = ""
    sim = Simulation()
    FileInterpreter(file_in, file_out, sim).parse()
    sim.run()


if __name__ == "__main__":
    main()