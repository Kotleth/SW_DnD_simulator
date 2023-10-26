from character import Unit
from additions import ColorText


def perform_attack(attack_result: Unit.melee_attack):
    # TODO include 1 and 20 as a critical failure and a critical success respectively
    # A math here is fine, you just need to include things like a character's strength bonus.
    attack_roll: int = attack_result[0]
    damage_dealt: int = attack_result[1]
    damage_dice_result_list: list[int] = attack_result[2]
    participants: tuple[str] = attack_result[3]
    if damage_dealt == 0:
        print(f"\n{participants[0].title()} rolled {attack_roll} and missed!"
              f"\n{participants[1].title()} is unscathed!")
    else:
        damage_rolls_str = ''
        if len(damage_dice_result_list) == 1:
            damage_rolls_str = damage_dice_result_list[0]
        elif len(damage_dice_result_list) >= 2:
            for damage in damage_dice_result_list[:-2]:
                damage_rolls_str += str(damage) + ', '
            damage_rolls_str += f"{damage_dice_result_list[-2]} and {damage_dice_result_list[-1]}"
        else:
            raise Exception("No damage rolls has been made!")
        print(f"{participants[0].title()} rolled {ColorText.green if attack_roll == 20 else ''}{attack_roll}{ColorText.end if attack_roll == 20 else ''} and hit!"
              f"\n{participants[0].title()} rolled for damage", damage_rolls_str,
              f"dealing {participants[1].title()} {ColorText.red if damage_dealt >= 10 else ''}"
              f"{damage_dealt}{ColorText.end if damage_dealt >= 10 else ''} damage!")