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

    def write_statblock(self):
        with open(self.path, mode="a") as stat_path:
            stat_path.write(f"```statblock\n")
            stat_path.write(f"columns: 2\n")
            stat_path.write(f"forcecolumns: true\n")
            stat_path.write(f"layout: Basic Pathfinder 2e Layout\n")
            stat_path.write(f"source: \"{self.source}\"\n")
            stat_path.write(f"name: \"{self.description.get("name")}\"\n")
            level = self.description.get("level", 0)
            stat_path.write(f"level: \"Creature {level}\"\n")
            if self.description.get("rarity") is not None:
                stat_path.write(f"rare_03: [[{self.description.get("rarity")}]]\n")
            stat_path.write(f"alignment: \"\"\n")
            stat_path.write(f"size: \"{self.description.get("size")}\"\n")
            for i, trait in enumerate(self.description.get("traits"), 1):
                trait_nr = str(i)
                if len(trait_nr) == 1:
                    trait_nr = "0" + trait_nr
                stat_path.write(f"trait_{trait_nr}: [[{trait}]]\n")
            perception = self.description.get("perception", 0)
            signed_perception = self.get_signed_number(perception)
            stat_path.write(f"modifier: {perception}\n")
            stat_path.write(f"perception:\n")
            stat_path.write(f"  - name: \"Perception\"\n")
            stat_path.write(f"    desc: \"{signed_perception}; {self.description.get("senses","")}\"\n")
            languages_str = ""
            for language in self.description.get("languages", {}):
                languages_str += (f"{language}, ")
            stat_path.write(f"languages: \"{languages_str[:-2]}\"\n")
            stat_path.write(f"skills:\n")
            stat_path.write(f"  - name: \"Skills\"\n")
            skill_str = ""
            for skill in self.description.get("skills", {}):
                skill_str += (f"{skill}, ")
            stat_path.write(f"    desc: \"{skill_str[:-2]}\"\n")
            ability_scores = ""
            for ability in ["str", "dex", "con", "int", "wis", "cha"]:
                ability_scores += self.description.get(ability, 0) + ", "
            stat_path.write(f"abilityMods: [{ability_scores[:-2]}]\n")
            speeds = ""
            for speed in self.description.get("speed", ["0"]):
                speeds += speed + " feet, "
            stat_path.write(f"speed: {speeds[:-2]}\n")
            stat_path.write(f"sourcebook: \"_{self.source}_\"\n")
            armor_class = self.description.get("ac", 10)
            stat_path.write(f"ac: {armor_class}\n")
            stat_path.write(f"armorclass:\n")
            stat_path.write(f"  - name: AC\n")
            fort = self.description.get("fort")
            ref = self.description.get("ref")
            will = self.description.get("will")
            stat_path.write(f"    desc: \"{armor_class}; __Fort__ {fort}, __Ref__ {ref}, __Will__ {will}\"\n")
            hp = self.description.get("hp")
            stat_path.write(f"hp: {hp}\n")
            stat_path.write(f"health:\n")
            stat_path.write(f" - name: \"\"\n")
            stat_path.write(f" - name: HP\n")
            immunities_str = ""
            immunities = self.description.get("immunities")
            if immunities is not None and immunities != []:
                immunities_str = "__Immunities__ "
                for immunity in immunities:
                    immunities_str += immunity + ", "
                immunities_str = immunities_str[:-2] + "; "
            resistances_str = ""
            resistances = self.description.get("resistances")
            if resistances is not None and resistances != []:
                resistances_str = "__Resistances__ "
                for resistance in self.description.get("resistances"):
                    resistances_str += resistance + ", "
                resistances_str = resistances_str[:-2] + "; "
            stat_path.write(f"   desc: \"{hp}; {immunities_str}{resistances_str}\"\n")
            stat_path.write(f"abilities_top:\n")
            stat_path.write(f"  - name: \"\"\n")
            stat_path.write(f"\n")
            for ability in self.description.get("abilities_top"):
                stat_path.write(f"  - name: \"{ability.get("name")}\"\n")
                description_str = ""
                descriptions = ability.get("desc")
                for description in descriptions:
                    multiple = re.search('[(][0-9]+[)]$', description)
                    if multiple:
                        description_str += f"{multiple.group()[1:-1]}x "
                        description = description[:-len(multiple.group())-1]
                    description_str += description + ", "
                stat_path.write(f"    desc: \" {description_str[:-2]}\"\n\n")
            stat_path.write(f"abilities_mid:\n")
            stat_path.write(f"  - name: \"\"\n")
            for ability in self.description.get("abilities_mid"):
                stat_path.write(f"  - name: \"{ability.get("name")}\"\n")
                stat_path.write(f"    desc: \" {ability.get("desc")}\"\n\n")
            stat_path.write(f"attacks:\n")
            stat_path.write(f"  - name: \"\"\n")
            attacks = self.description.get("attacks", [])
            for attack in attacks:
                name = attack.get("name")
                desc = attack.get("desc")
                damage = attack.get("damage")
                stat_path.write(f"\n  - name: \"{name}\"\n")
                stat_path.write(f"    desc: \"{desc}\\n__Damage__ {damage}\"\n")
            stat_path.write(f"```\n\n")

    def write_encounter(self):
        with open(self.path, mode="a") as encounter_path:
            encounter_path.write("```encounter-table\n")
            encounter_path.write(f"name: {self.description.get("name")}\n")
            encounter_path.write(f"creatures:\n")
            encounter_path.write(f"  - 1: {self.description.get("name")}\n")
            encounter_path.write(f"\n```\n")
            encounter_path.write(f"\n\n{self.description.get("description text")}\n\n")

            

            






def main():
    creature_description = {
        "title": "Mean Orc",
        "tags": [
            "pf2e/creature/type/humanoid",
            "pf2e/creature/type/orc",
            "pf2eMonster",
            "pf2e/creature/level/2",
            "Epsilon"
        ],
        "name": "Mean Orc",
        "level": 2,
        "description text": "Having spent their lives fighting for dominace in their clan, these brutes have learned how to instill fear in their opponents. While this is effective in one on one battles, and often brings the mean orcs high into the hierachy, it presents a problem for them when they are unable to intimidate themselves to a higher position.\n\nWhen a mean orc cannot rise further within the clan, they often find themself without any skills with which to be useful. With half the clan being too terrified to work with them, they are not useful to the community, and are thus often thrown out.\n\nThus Mean Orcs are often lone figures, wandering without purpose from one robbery to the next. However, should one raise to the top of a clan, it will often lead to a short stint of terror and violence before it's subjects or a group of adventurers depose it.",
        "rarity": "Uncommon",
        "size": "medium",
        "traits": ["humanoid", "orc", "evil"],
        "perception": 5,
        "senses": "Darkvision",
        "languages": ["Common", "Orcish", "Beastial Anger"],
        "skills": ["Athletics: +7", "Intimidation: +12"],
        "str": "6",
        "dex": "-1",
        "con": "3",
        "int": "-2",
        "wis": "0",
        "cha": "3",
        "speed": ["25", "swim 10"],
        "ac": 16,
        "fort": "+9",
        "ref": "+3",
        "will": "+6",
        "hp": "36",
        "immunities": ["bleed effects"],
        "resistances": [],
        "abilities_top": [{"name": "Items", "desc": ["dog collar", "horsechopper", "dagger (2)"]},
                          {"name": "Beastial Anger", "desc": ["(visual) Using body language, the Mean Orc can choose to let all creatures which observes it know what mood it is in. The Mean Orc is always angry"]}],
        "abilities_mid": [{"name": "Frightful Whisper", "desc": "`pf2:1` (auditory, emotion, mental) The Mean Orc whispers a threat to a creature within 5 feet. If the creature understands the Mean Orc's threats, it takes minus 2 on all saves to resist fear effects from the Mean Orc's actions."}],
        "attacks": [{"name": "**Melee** `pf2:1` Horsechopper", "desc": "+10 (reach 10 feet, trip, versatile p)", "damage":  "1d8 + 6 slashing"},
                    {"name": "**Melee** `pf2:1` Fist", "desc": "+10 (agile, shove)", "damage": "1d4 + 4 bludgeoning"}]
    }

    path = join("data", "epsilon", "mean_orc.md")
    c_writer = Creature_Writer(path=path, source="My Imagination", license="ORC", creature=creature_description)
    c_writer.write_properties()
    c_writer.write_statblock()
    c_writer.write_encounter()

if __name__ == "__main__":
    main()
