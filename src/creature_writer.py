from writer import Writer
from os.path import join
import re

class Creature_Writer(Writer):
    def __init__(self, path, source, license, creature: dict):
        super().__init__(path, source, license)
        self.description = creature
    
    def write_properties(self):
        with open(self.path, 'w') as prop_path:
            prop_path.write("---\n")
            prop_path.write(f"title: \"{self.description.get("title")}\"\n")
            prop_path.write(f"obsidianUIMode: preview\n")
            prop_path.write(f"notetype: pf2eMonster\n")
            prop_path.write(f"cssClasses:\n  - pf2e\n")
            prop_path.write(f"tags:\n")
            for tag in self.description.get("tags"):
                prop_path.write(f"  - {tag}\n")
            prop_path.write(f"statblock: inline\n")
            prop_path.write(f"name: \"{self.description.get("name")}\"\n")
            prop_path.write(f"level: {self.description.get("level")}\n")
            prop_path.write(f"license: {self.license}\n")
            prop_path.write("---\n\n")

    def get_signed_number(self, number):
        sign = "+"
        if number < 0:
            sign = "-"
        return sign + str(number)

