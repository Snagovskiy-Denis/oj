class ConfigReadError(Exception):
    'Config file is readeble but its properties corrupted'

    def __init__(self, *arguments, message='Can not read {}: "{}"'):
        message = message.format(*arguments)
        super().__init__(message)

class SectionReadError(ConfigReadError):
    def __init__(self, section_name):
        super().__init__('section', section_name)

class SettingReadError(ConfigReadError):
    def __init__(self, setting_name):
        super().__init__('setting', setting_name)
