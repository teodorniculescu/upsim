import TimePeriod


def main():
    fp = "tests/test1"
    fi = TimePeriod.FileInterpreter(fp)
    fi.parse()


if __name__ == "__main__":
    main()