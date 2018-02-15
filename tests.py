import logging
from logging import config

from unittest import TestCase


class FormatterTest(TestCase):
    def setUp(self):
        config.dictConfig({
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'graylog': {
                    '()': 'graylog_json_formatter.GrayLogJSONFormatter',
                    'format': '({levelname}) | {name} | [{asctime}]: '
                              'File {pathname}:{lineno}" - {funcName}() | '
                              '{message}',
                    'style': '{',
                    'source': 'test',
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

        self.logger = logging.getLogger('test')

    def test_message(self):
        self.logger.debug(
            'test message',
            extra={'data': {'str_key': 'value1', 'int_key': 1}}
        )

    def test_message_and_args(self):
        self.logger.debug(
            'test message: %s | %s', 1, 2,
            extra={'data': {'str_key': 'value2', 'int_key': 2}}
        )

    def test_message_and_exc(self):
        try:
            int('test')
        except Exception as exc:
            self.logger.error(
                'test message',
                extra={'data': {'str_key': 'value3', 'int_key': 3}},
                exc_info=exc,
            )


class EncoderFormatterTest(TestCase):
    def setUp(self):
        config.dictConfig({
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'graylog': {
                    '()': 'graylog_json_formatter.GrayLogJSONFormatter',
                    'format': '({levelname}) | {name} | [{asctime}]: '
                              'File {pathname}:{lineno}" - {funcName}() | '
                              '{message}',
                    'style': '{',
                    'source': 'test',
                    'encoder': 'json.JSONEncoder',
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

        self.logger = logging.getLogger('test')

    def test_message(self):
        self.logger.debug(
            'test message',
            extra={'data': {'str_key': 'value1', 'int_key': 1}}
        )
