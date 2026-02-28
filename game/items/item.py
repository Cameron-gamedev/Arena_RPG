class Item:
    def __init__(
        self,
        name,
        item_type,
        effect=None,
        stackable=False,
        quantity=1,
        attack_bonus=0,
        defense_bonus=0,
        crit_bonus=0,
        modifiers=None
    ):
        self.name = name
        self.item_type = item_type
        self.effect = effect
        self.stackable = stackable
        self.quantity = quantity
        self.max_stacks = 10

        # Basic stat bonuses
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.crit_bonus = crit_bonus

        self.modifiers = modifiers or {}
