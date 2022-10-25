import logging
from dynaconf import Dynaconf, Validator, ValidationError

settings = Dynaconf(
    envvar_prefix=False,
    settings_files=['settings.toml'],
    validators=[
        Validator("logging_level", default=logging.INFO, must_exist=True),
        Validator("sql_connectionstring", must_exist=True)
    ]
)
