import os
import unittest
from ..core.utils.env_utils import EnvImporter


class Test1(unittest.TestCase):

    def setUp(self) -> None:
        self.testEnvs = [
            'TEST_ENV',
            'TEST_ENV1',
            'TEST_ENV2',
            'TEST_ENV3',
            'TEST_ENV4',
        ]
        self.testValues = [
            'test_value_0',
            'test_value_1',
            'test_value_2',
            'test_value_3',
            'test_value_4',
        ]
        return super().setUp()

    def tearDown(self) -> None:
        for env in self.testEnvs:
            os.environ.pop(env, None)
        return super().tearDown()

    def assertEnv(self, env: str, value: str):
        self.assertIn(env, os.environ)
        self.assertEqual(os.environ[env], value)

    def assertNotEnv(self, env: str):
        self.assertNotIn(env, os.environ)


    def test_1_importEnv(self):
        self.assertNotEnv(self.testEnvs[0])

        envImporter = EnvImporter()
        self.assertNotEnv(self.testEnvs[0])
        envImporter.importEnv(self.testEnvs[0], self.testValues[0])
        self.assertEnv(self.testEnvs[0], self.testValues[0])
        envImporter.importEnv(self.testEnvs[0], self.testValues[1])
        self.assertEnv(self.testEnvs[0], self.testValues[1])
        del envImporter
        self.assertNotEnv(self.testEnvs[0])

        os.environ[self.testEnvs[0]] = self.testValues[1]
        self.assertEnv(self.testEnvs[0], self.testValues[1])
        envImporter = EnvImporter()
        envImporter.importEnv(self.testEnvs[0], self.testValues[0])
        self.assertEnv(self.testEnvs[0], self.testValues[0])
        del envImporter
        self.assertEnv(self.testEnvs[0], self.testValues[1])

    def test_2_popEnv(self):
        self.assertNotEnv(self.testEnvs[0])

        envImporter = EnvImporter()
        self.assertNotEnv(self.testEnvs[0])
        envImporter.importEnv(self.testEnvs[0], self.testValues[0])
        self.assertEnv(self.testEnvs[0], self.testValues[0])
        envImporter.popEnv(self.testEnvs[0])
        self.assertNotEnv(self.testEnvs[0])
        del envImporter
        self.assertNotEnv(self.testEnvs[0])

        os.environ[self.testEnvs[0]] = self.testValues[1]
        self.assertEnv(self.testEnvs[0], self.testValues[1])
        envImporter = EnvImporter()
        envImporter.popEnv(self.testEnvs[0])
        self.assertNotEnv(self.testEnvs[0])
        del envImporter
        self.assertEnv(self.testEnvs[0], self.testValues[1])

    def test_3_importEnvs(self):
        for i in range(5):
            self.assertNotEnv(self.testEnvs[i])
        
        envImporter = EnvImporter()
        for i in range(5):
            self.assertNotEnv(self.testEnvs[i])
        envImporter.importEnvs(**dict(zip(self.testEnvs, self.testValues)))
        for i in range(5):
            self.assertEnv(self.testEnvs[i], self.testValues[i])
        del envImporter
        for i in range(5):
            self.assertNotEnv(self.testEnvs[i])

        envImporter = EnvImporter()
        for i in range(5):
            self.assertNotEnv(self.testEnvs[i])
        envImporter.importEnvs(**dict(zip(self.testEnvs, self.testValues)))
        for i in range(5):
            self.assertEnv(self.testEnvs[i], self.testValues[i])
        d2 = {
            self.testEnvs[0] : None,
            self.testEnvs[1] : self.testValues[2],
        }
        envImporter.importEnvs(**d2)
        self.assertNotEnv(self.testEnvs[0])
        self.assertEnv(self.testEnvs[1], self.testValues[2])
        for i in range(2, 5):
            self.assertEnv(self.testEnvs[i], self.testValues[i])
        del envImporter
        for i in range(5):
            self.assertNotEnv(self.testEnvs[i])

    def test_4_importEnvironFromShell(self):
        self.assertNotEnv(self.testEnvs[0])

        envImporter = EnvImporter()
        envImporter.importEnvironFromShell(['echo'])
        self.assertNotEnv(self.testEnvs[0])
        envImporter.importEnvironFromShell(
            ['set', f'{self.testEnvs[0]}={self.testValues[0]}'],
            importNew=False)
        self.assertNotEnv(self.testEnvs[0])
        envImporter.importEnvironFromShell(['set', f'{self.testEnvs[0]}={self.testValues[0]}'])
        self.assertEnv(self.testEnvs[0], self.testValues[0])
        del envImporter
        self.assertNotEnv(self.testEnvs[0])



        os.environ[self.testEnvs[0]] = self.testValues[1]
        self.assertEnv(self.testEnvs[0], self.testValues[1])
        envImporter = EnvImporter()
        envImporter.importEnvironFromShell(['set', f'{self.testEnvs[0]}={self.testValues[0]}'])
        self.assertEnv(self.testEnvs[0], self.testValues[1])
        del envImporter
        self.assertEnv(self.testEnvs[0], self.testValues[1])

        envImporter = EnvImporter()
        envImporter.importEnvironFromShell(
            ['set', f'{self.testEnvs[0]}={self.testValues[0]}'],
            importEnvs = [self.testEnvs[0]])
        self.assertEnv(self.testEnvs[0], self.testValues[0])
        del envImporter
        self.assertEnv(self.testEnvs[0], self.testValues[1])

        pathValue = os.environ['PATH']
        self.assertEqual(pathValue, os.environ['PATH'])
        envImporter = EnvImporter()
        envImporter.importEnvironFromShell(
            ['set', f'PATH={self.testValues[0]}'],
            importPath = False)
        self.assertEqual(pathValue, os.environ['PATH'])
        envImporter.importEnvironFromShell(['set', f'PATH={self.testValues[0]}'])
        self.assertNotEqual(pathValue, os.environ['PATH'])
        del envImporter
        self.assertEqual(pathValue, os.environ['PATH'])


if __name__ == '__main__':
    unittest.main()