Graylog JSON formatter
======================

GrayLogJSONFormatter formatted LogRecord as JSON object for graylog JSON extractor.
JSON object include LogRecord attributes as default_keys and include extra attributes:
``source``, ``message``, ``asctime`` and ``data``.

Example
-------
configure::

    from logging import config

    config.dictConfig({
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'graylog': {
                    '()': 'graylog_json_formatter.GrayLogJSONFormatter',
                    'format': '({levelname}) | {name} | [{asctime}]: '
                              'File {pathname}:{lineno}" - {funcName}() | {message}',
                    'style': '{',
                    'source': 'test',
                    'environment': 'testing',
                    'keys': {
                        'name', 'levelno', 'levelname',
                        'pathname', 'filename', 'module', 'lineno', 'funcName',
                        'created', 'asctime', 'msecs', 'relativeCreated',
                        'thread', 'threadName', 'process',
                        'message', 'data',
                        'exc_text', 'stack_info',
                    },
                    'extra': {'service': 'my-service'},
                }
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'graylog',
                },
                'graylog': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.SysLogHandler',
                    'formatter': 'graylog',
                    'address': ('localhost', 10000),
                }
            },
            'loggers': {
                'test': {
                    'level': 'DEBUG',
                    'handlers': ['console', 'graylog'],
                    'propagate': False,
                },
            }
        })

        logger = logging.getLogger('test')

logging::

    # extra usage
    logger.debug('test message: % | %s', 1, 2, extra={'data': {'key': 'value', 'int_key': 12})


Graylog extract extra as ``data-key`` and ``data-int_key`` fields.

``extra`` argument may be callable or string with dotted path to callable attribute::

    'extra': lambda record: {'service': 'service-func'}

