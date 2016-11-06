from .app import app
import logging

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level='DEBUG')
    app.run()


if __name__ == '__main__':
    main()
