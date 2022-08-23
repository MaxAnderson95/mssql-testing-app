import logging
from dynaconf import Dynaconf, Validator, ValidationError

settings = Dynaconf(
    settings_files=['settings.toml'],
    validators=[
        Validator("logging.level", default=logging.INFO, must_exist=True),
        Validator("sql.connectionstring", must_exist=True)
    ]
)
