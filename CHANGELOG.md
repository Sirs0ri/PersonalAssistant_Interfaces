Date       | Version | Changes
-----------|---------|----------------------------------------------------------
2016-04-11 |   0.2.1 | Switched from a FileHandler to a TimedRotatingFileHandler that starts a new logfile every day.
2016-04-11 |   0.2.1 | Don't start the AutoRemoteHandler if it's not configured properly
2016-04-11 |   0.2.1 | Add warning if `simple_cli/__init__.py` is executed manually
2016-04-11 |   0.2.1 | Create Loggers always via `LOGGER = logging.getLogger(__name__)`
2016-04-10 |     0.2 | Added Logging and a bunch of comments
2016-04-09 |     0.1 | Moved the first, almost finished interface over from https://github.com/Sirs0ri/PersonalAssistant.
2016-04-06 |         | Initial commit for SAM2. Began working on the interface in https://github.com/Sirs0ri/PersonalAssistant.
