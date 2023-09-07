import logging
from dynaconf import Dynaconf, Validator, ValidationError

logger = logging.getLogger(__name__)

settings = Dynaconf(
    envvar_prefix=False,
    settings_files=['settings.toml'],
)

settings.validators.register(
    Validator("logging_level", default=logging.INFO, must_exist=True),
    Validator("username", must_exist=True),
    Validator("password", must_exist=True),
    Validator("database", must_exist=True),
    Validator("host", must_exist=True),
    Validator("port", must_exist=True),
    Validator("encrypt", must_exist=True, default="no"),
    Validator("connect_timeout", must_exist=True, default=30),
    Validator("sleep_between_inserts", must_exist=True, default=2),
    Validator("multisubnetfailover", must_exist=True, default="no"),   
)

try:
    settings.validators.validate_all()
except ValidationError as e:
    accumulative_errors = e.details
    logger.critical("FATAL ERROR: The following required settings are missing:")
    for error in accumulative_errors:
        logger.critical(f"{error[1]}")
    logger.critical("Exiting...")
    raise SystemExit(1)