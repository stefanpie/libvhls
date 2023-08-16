import logging


def configure_logging(enable_logging):
    if enable_logging:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
        )
