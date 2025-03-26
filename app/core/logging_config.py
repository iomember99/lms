import logging


def init_logging():
    logging.basicConfig(
        filename="logs/app.log",  # save to file
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    # Optional: set log level for third-party libs if needed
    logging.getLogger("zeep").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
