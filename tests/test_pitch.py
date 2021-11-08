import unittest
from app.models import Pitch

class PitchTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Pitch class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_pitch = Pitch(1234,'Pickup','Pickup Lines','Superb idea',6/11/2021,3)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch,Pitch))
