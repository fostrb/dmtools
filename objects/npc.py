

class Npc(object):
    def __init__(self):
        self.name = ''

        # stats
        self.strength       = 10
        self.dexterity      = 10
        self.constitution   = 10
        self.intelligence   = 10
        self.wisdom         = 10
        self.charisma       = 10

    def get_ability_mod(self, ability):
        try:
            ab = self.__getattribute__(ability)
            mod = int((ab-10)/2)
            return mod
        except:
            return None


if __name__ == '__main__':
    n = Npc()
    print(n.get_ability_mod("strength"))
