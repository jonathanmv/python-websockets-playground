import logging
from app import utils


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Application started")
    # Your application logic here
    utils.some_function()
    logger.info("Application finished")


if __name__ == "__main__":
    main()
