from writer import Writer
from os.path import join
import re

class Creature_Writer(Writer):
    def __init__(self, path, source, license, creature: dict):
        super().__init__(path, source, license)
        self.description = creature
    
