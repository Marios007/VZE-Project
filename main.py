import sys
from VzeApp import VzeApp

def main(*args, **kwargs):
    print ("Starting VZE")

    app = VzeApp(sys.argv)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

    