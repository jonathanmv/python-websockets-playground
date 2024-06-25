import logging
from app import check_network_packages


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Application started")

    # Your application logic here
    check_network_packages.run_websocket_listener()

    logger.info("Application finished")


if __name__ == "__main__":
    main()
