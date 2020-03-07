from FileInterpreter import FileInterpreter


def main():
    fp = "tests/test1"
    fi = FileInterpreter(fp)
    fi.parse()


if __name__ == "__main__":
    main()