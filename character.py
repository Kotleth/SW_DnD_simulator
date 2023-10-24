import random as r
from weaponry import *
from additions import *
from typing import Type


class Unit:
    name: str
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    armor_class: int
    vitality_points: int
    proficiency: int
    resistances: list[str] = []
    weapon: Weapon

    def __init__(self, name, strength, dexterity, constitution, intelligence, wisdom, charisma, armor_class,
                 vitality_points, proficiency):
        self.name = name
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.armor_class = armor_class
        self.vitality_points = vitality_points
        self.proficiency = proficiency

    def add_resistance(self, resistance):
        self.resistances.append(resistance)

    def reset_armor(self):
        self.armor_class = 10 + self.dexterity

    def put_on_weapon(self, weapon: Weapon):
        self.weapon = weapon

    def show_resistances(self):
        print(f"RESISTANCES OF {self.name}\n")
        for _resistance in self.resistances:
            print(_resistance)
        print(f"\n{'*'*10}")

    def get_damage(self, hit_bonus, damage_instance: DamageInstance, attack_type):
        if r.randint(0, 20) + hit_bonus >= self.armor_class:
            for damage_type, damage in damage_instance.damage_dict.items():
                if damage_type in self.resistances:
                    self.vitality_points -= round(damage/2)
                else:
                    self.vitality_points -= damage

    def deal_melee_damage(self, target: Type['Unit'], weapon: Weapon = None):
        if weapon is None:
            weapon = self.weapon
        print(weapon)
        damage = DamageInstance()

