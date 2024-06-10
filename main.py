import typing

from src.graphics_engine import GraphicsEngine


def main() -> typing.NoReturn:
    app = GraphicsEngine()
    app.run()


if __name__ == "__main__":
    main()
