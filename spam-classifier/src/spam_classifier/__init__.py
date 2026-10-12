import logging

from doc_processor.core.logging import configure_logging

logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging()
    logger.info("spam-classifier command started")
