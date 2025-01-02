from enum import Enum


class LoggerError(Exception): ...


class LevelLogging(str, Enum):
    INFO = "info"


def build_log_message(message_type: str, messages: dict[str, str], **kwargs) -> str:
    if message_type in messages:
        return messages[message_type].format(**kwargs)
    raise LoggerError(f"Неизвестный тип сообщения: {message_type}")


def log_message(
    message_type: str,
    messages: dict[str, str],
    logger,
    level: str = LevelLogging.INFO.value,
    **kwargs,
) -> None:
    message = build_log_message(message_type, messages, **kwargs)
    getattr(logger, level)(message)


def show_free_shipping_icon(messages: dict[str, str], logger):
    log_message("free_shipping", messages, logger)


def hide_free_shipping_icon(messages: dict[str, str], logger):
    log_message("paid_shipping", messages, logger)
