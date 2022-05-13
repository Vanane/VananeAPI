class Item:
    name:str
    modifiers:dict

    def __init__(self) -> None:
        self.name = ""


    def addModifier(self, name:str, detail:str):
        if not hasattr(self, "modifiers"):
            self.modifiers = dict()            
        self.modifiers[name] = detail
        # TODO : For modifiers that appear 2 times, make them double the bonuses