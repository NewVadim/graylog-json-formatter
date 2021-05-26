# coding=utf-8
import logging.config

from unittest import TestCase


class BaseTestCase(TestCase):
    base_config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'graylog': {
                '()': 'graylog_json_formatter.GrayLogJSONFormatter',
                'format': '{message} | %(message)s',
                'style': '{',
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'source': 'test',
                'environment': 'testing',
                'keys': {
                    'name', 'levelno', 'levelname',
                    'pathname', 'filename', 'module', 'lineno', 'funcName',
                    'created', 'asctime', 'msecs', 'relativeCreated',
                    'thread', 'threadName', 'process',
                    'message', 'data',
                    'exc_text', 'stack_info',
                }
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
    }


class FormatterTest(BaseTestCase):
    def setUp(self):
        logging.config.dictConfig(self.base_config)

        self.logger = logging.getLogger('test')

    def test_message(self):
        self.logger.debug(
            'FormatterTest.test_message(не аски)',
            extra={'data': {'str_key': 'value1', 'int_key': 1}}
        )
        self.logger.debug(
            'не аски',
        )

    def test_message_and_args(self):
        self.logger.debug(
            'FormatterTest.test_message_and_args: %s | %s', 1, 2,
            extra={'data': {'str_key': 'value2', 'int_key': 2}}
        )

    def test_message_and_exc(self):
        try:
            int('test')
        except Exception as exc:
            self.logger.error(
                'FormatterTest.test_message_and_exc',
                extra={'data': {'str_key': 'value3', 'int_key': 3}},
                exc_info=exc,
            )


class EncoderFormatterTest(BaseTestCase):
    def setUp(self):
        config = {key: value for key, value in self.base_config.items()}
        config.update({
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
        })
        logging.config.dictConfig(config)

        self.logger = logging.getLogger('test')

    def test_message(self):
        self.logger.debug(
            'EncoderFormatterTest.test_message',
            extra={'data': {'str_key': 'value1', 'int_key': 1}}
        )


class ExtraDictTest(BaseTestCase):
    def setUp(self):
        config = {key: value for key, value in self.base_config.items()}
        config.update({
            'formatters': {
                'graylog': {
                    '()': 'graylog_json_formatter.GrayLogJSONFormatter',
                    'format': '({levelname}) | {name} | [{asctime}]: '
                              'File {pathname}:{lineno}" - {funcName}() | '
                              '{message}',
                    'style': '{',
                    'source': 'test',
                    'extra': {'service': 'service-dict'}
                }
            },
        })
        logging.config.dictConfig(config)

        self.logger = logging.getLogger('test')

    def test_message(self):
        self.logger.debug('ExtraDictTest.test_message')


class ExtraFuncTest(BaseTestCase):
    def setUp(self):
        config = {key: value for key, value in self.base_config.items()}
        config.update({
            'formatters': {
                'graylog': {
                    '()': 'graylog_json_formatter.GrayLogJSONFormatter',
                    'format': '({levelname}) | {name} | [{asctime}]: '
                              'File {pathname}:{lineno}" - {funcName}() | '
                              '{message}',
                    'style': '{',
                    'source': 'test',
                    'extra': lambda record: {'service': 'service-func'}
                }
            },
        })
        logging.config.dictConfig(config)

        self.logger = logging.getLogger('test')

    def test_message(self):
        self.logger.debug('ExtraFuncTest.test_message')


class ExtraFuncPathTest(BaseTestCase):
    def setUp(self):
        config = {key: value for key, value in self.base_config.items()}
        config.update({
            'formatters': {
                'graylog': {
                    '()': 'graylog_json_formatter.GrayLogJSONFormatter',
                    'format': '({levelname}) | {name} | [{asctime}]: '
                              'File {pathname}:{lineno}" - {funcName}() | '
                              '{message}',
                    'style': '{',
                    'source': 'test',
                    'extra': 'tests.ExtraFuncPathTest.extra_func'
                }
            },
        })
        logging.config.dictConfig(config)

        self.logger = logging.getLogger('test')

    @staticmethod
    def extra_func(record):
        return {'service': 'service-func-path'}

    def test_message(self):
        self.logger.debug('ExtraFuncPathTest.test_message')
