import os
import unittest
from ..core.lr_environments import LREnvironments
from ..core.lr_environments import LREnvironmentsOverride


class TestEnvironments(LREnvironments):

    @LREnvironments.setCategory('Test')
    @LREnvironments.setEnv(PROJ_DESC='Just for test.')

    @LREnvironments.addEnv(ENV1='environment1')
    @LREnvironments.addEnv(ENV2='environment2')
    @LREnvironments.addEnv(ENV3='environment3')
    @LREnvironments.addEnv(ENV4=None)
    @LREnvironments.addEnv(ENV5=None)
    @LREnvironments.exportEnv('ENV2', 'ENV4')
    def initialize(self):
        pass


class testLEO1(LREnvironmentsOverride):
    @LREnvironmentsOverride.overrideEnv(ENV3='testLEO1_environment3')
    @LREnvironmentsOverride.overrideEnv(ENV4='testLEO1_environment4')
    @LREnvironmentsOverride.overrideExportEnv('ENV1')
    def initialize(self):
        pass


class testLEO2(LREnvironmentsOverride):
    @LREnvironmentsOverride.overrideEnv(ENV3='testLEO2_environment3')
    @LREnvironmentsOverride.overrideEnv(ENV4='testLEO2_environment4')
    @LREnvironmentsOverride.overrideEnv(ENV5='testLEO2_environment5')
    @LREnvironmentsOverride.overrideExportEnv('ENV1', 'ENV3')
    def initialize(self):
        pass


class Test1(unittest.TestCase):

    def assertOriginalEnv(self):
        self.assertEqual(LREnvironments.ENV1, 'environment1')
        self.assertEqual(LREnvironments.ENV2, 'environment2')
        self.assertEqual(LREnvironments.ENV3, 'environment3')
        with self.assertRaises(AssertionError):
            LREnvironments.ENV4
        with self.assertRaises(AssertionError):
            LREnvironments.ENV5

    def assertOverriddenEnv_1(self):
        self.assertEqual(LREnvironments.ENV1, 'environment1')
        self.assertEqual(LREnvironments.ENV2, 'environment2')
        self.assertEqual(LREnvironments.ENV3, 'testLEO1_environment3')
        self.assertEqual(LREnvironments.ENV4, 'testLEO1_environment4')
        with self.assertRaises(AssertionError):
            LREnvironments.ENV5

    def assertOverriddenEnv_1_2(self):
        self.assertEqual(LREnvironments.ENV1, 'environment1')
        self.assertEqual(LREnvironments.ENV2, 'environment2')
        self.assertEqual(LREnvironments.ENV3, 'testLEO2_environment3')
        self.assertEqual(LREnvironments.ENV4, 'testLEO2_environment4')
        self.assertEqual(LREnvironments.ENV5, 'testLEO2_environment5')

    def assertOriginalExportEnv(self):
        self.assertNotIn('ENV1', os.environ)        
        self.assertIn('ENV2', os.environ)
        self.assertEqual(LREnvironments.ENV2, os.environ['ENV2'])
        self.assertNotIn('ENV3', os.environ)
        self.assertNotIn('ENV4', os.environ)
        self.assertNotIn('ENV5', os.environ)

    def assertOriginalExportEnv_1(self):
        self.assertIn('ENV1', os.environ)
        self.assertEqual(LREnvironments.ENV1, os.environ['ENV1'])
        self.assertIn('ENV2', os.environ)
        self.assertEqual(LREnvironments.ENV2, os.environ['ENV2'])
        self.assertNotIn('ENV3', os.environ)
        self.assertIn('ENV4', os.environ)
        self.assertEqual(LREnvironments.ENV4, os.environ['ENV4'])
        self.assertNotIn('ENV5', os.environ)

    def assertOriginalExportEnv_1_2(self):
        self.assertIn('ENV1', os.environ)
        self.assertEqual(LREnvironments.ENV1, os.environ['ENV1'])
        self.assertIn('ENV2', os.environ)
        self.assertEqual(LREnvironments.ENV2, os.environ['ENV2'])
        self.assertIn('ENV3', os.environ)
        self.assertEqual(LREnvironments.ENV3, os.environ['ENV3'])
        self.assertIn('ENV4', os.environ)
        self.assertEqual(LREnvironments.ENV4, os.environ['ENV4'])
        self.assertNotIn('ENV5', os.environ)


    def test_1_originalEnv(self):
        self.assertOriginalEnv()
        self.assertOriginalExportEnv()

    def test_2_overrideEnv(self):
        LREnvironments.sApplyOverride('testLEO1')
        self.assertOverriddenEnv_1()
        self.assertOriginalExportEnv_1()
        LREnvironments.sClearOverrides()
        self.assertOriginalEnv()
        self.assertOriginalExportEnv()

        LREnvironments.sApplyOverride('testLEO1')
        self.assertOverriddenEnv_1()
        self.assertOriginalExportEnv_1()
        LREnvironments.sApplyOverride('testLEO2')
        self.assertOverriddenEnv_1_2()
        LREnvironments.sClearOverrides()
        self.assertOriginalEnv()
        

if __name__ == '__main__':
    unittest.main()