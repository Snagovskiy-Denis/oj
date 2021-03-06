from .fixture_files  import FixtureFiles
from .fixture_system import FixtureSystem


class TestEnvironment(FixtureFiles, FixtureSystem):
    '''Creates test environment to satisfy external dependencies

    List of external dependencies:

        * files: config, template (optionally destination file)
        * today's date
        * environment variables
        * system arguments
        * file writing
        * process running

    Class creates test files for path-resolving functional and
    patch Configurator._get_config_path to read created config.
    Afterwards it patchs todas date, env variables, sysargv etc

    List of patched enteties:

        FixtureSystem:

            * oj.chdir (os.chdir)
            * oj.getenv (os.getenv)
            * pathlib.Path.write_text
            * subprocess.run
            * sys.argv

        FixtureFiles:

            * configurator.Configurator._get_config_path
            * oj.date (datetime.date)
    '''
    config_file_required      = True
    template_file_required    = True
    destination_file_required = False

    def initiate_test_environment(self):
        self.create_files()
        self.isolate_from_system()

    def clear_test_environment(self):
        self.stop_system_isolation()
        self.delete_files()
