from FileInterpreter import FileInterpreter
from Simulation import Simulation


def main():
    fp = "tests/test1"
    sim = Simulation()
    FileInterpreter(fp, sim).parse()
    sim.run()


if __name__ == "__main__":
    main()