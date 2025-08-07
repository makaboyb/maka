diff --git a//dev/null b/harrypotter_duel.py
index 0000000000000000000000000000000000000000..4b5a4edf09726d9acf039a87625351edd82c49ba 100644
--- a//dev/null
+++ b/harrypotter_duel.py
@@ -0,0 +1,322 @@
+import argparse
+import random
+from dataclasses import dataclass
+from typing import Callable, Dict, Optional
+
+
+def default_log(message: str) -> None:
+    print(message)
+
+
+log: Callable[[str], None] = default_log
+
+
+@dataclass
+class Wizard:
+    name: str
+    health: int = 100
+    stunned: bool = False
+    shield: int = 0
+    bleeding: int = 0
+
+    def alive(self) -> bool:
+        return self.health > 0
+
+
+def apply_damage(target: "Wizard", amount: int) -> None:
+    """Inflict damage taking shields into account."""
+    if target.shield > 0:
+        absorbed = min(target.shield, amount)
+        target.shield -= absorbed
+        amount -= absorbed
+        if absorbed:
+            log(f"{target.name}'s shield absorbs {absorbed} damage!")
+    if amount > 0:
+        target.health -= amount
+        log(f"{target.name} takes {amount} damage.")
+
+
+def apply_heal(target: "Wizard", amount: int) -> None:
+    old = target.health
+    target.health = min(100, target.health + amount)
+    healed = target.health - old
+    if healed:
+        log(f"{target.name} heals {healed} hp.")
+
+
+def apply_shield(target: "Wizard", amount: int) -> None:
+    target.shield += amount
+    log(f"{target.name} gains a shield of {amount} hp.")
+
+
+def damage_spell(amount: int) -> Callable[[Wizard, Wizard], None]:
+    def effect(caster: Wizard, target: Wizard) -> None:
+        apply_damage(target, amount)
+
+    return effect
+
+
+def heal_spell(amount: int) -> Callable[[Wizard, Wizard], None]:
+    def effect(caster: Wizard, target: Wizard) -> None:
+        apply_heal(caster, amount)
+
+    return effect
+
+
+def shield_spell(amount: int) -> Callable[[Wizard, Wizard], None]:
+    def effect(caster: Wizard, target: Wizard) -> None:
+        apply_shield(caster, amount)
+
+    return effect
+
+
+def damage_stun_spell(amount: int) -> Callable[[Wizard, Wizard], None]:
+    def effect(caster: Wizard, target: Wizard) -> None:
+        apply_damage(target, amount)
+        target.stunned = True
+        log(f"{target.name} is stunned!")
+
+    return effect
+
+
+def damage_heal_spell(damage: int, heal: int) -> Callable[[Wizard, Wizard], None]:
+    def effect(caster: Wizard, target: Wizard) -> None:
+        apply_damage(target, damage)
+        apply_heal(caster, heal)
+
+    return effect
+
+
+def remove_shield_spell() -> Callable[[Wizard, Wizard], None]:
+    def effect(caster: Wizard, target: Wizard) -> None:
+        if target.shield > 0:
+            log(f"{target.name}'s shield is removed!")
+        else:
+            log(f"{target.name} has no shield to remove.")
+        target.shield = 0
+
+    return effect
+
+
+def damage_remove_shield_spell(amount: int) -> Callable[[Wizard, Wizard], None]:
+    def effect(caster: Wizard, target: Wizard) -> None:
+        apply_damage(target, amount)
+        if target.shield > 0:
+            log(f"{target.name}'s shield is shattered!")
+        target.shield = 0
+
+    return effect
+
+
+def damage_bleed_spell(damage: int, bleed: int) -> Callable[[Wizard, Wizard], None]:
+    def effect(caster: Wizard, target: Wizard) -> None:
+        apply_damage(target, damage)
+        target.bleeding = bleed
+        log(f"{target.name} starts bleeding for {bleed} damage next turn!")
+
+    return effect
+
+
+def damage_shield_spell(damage: int, shield: int) -> Callable[[Wizard, Wizard], None]:
+    def effect(caster: Wizard, target: Wizard) -> None:
+        apply_damage(target, damage)
+        apply_shield(caster, shield)
+
+    return effect
+
+
+def confringo_spell(caster: Wizard, target: Wizard) -> None:
+    apply_damage(target, 45)
+    apply_damage(caster, 5)
+
+
+def ennervate_spell(caster: Wizard, target: Wizard) -> None:
+    caster.stunned = False
+    apply_heal(caster, 10)
+    log(f"{caster.name} shakes off all stunning effects!")
+
+
+def avada_kedavra(caster: Wizard, target: Wizard) -> None:
+    target.health = 0
+    log(f"{target.name} is struck by the Killing Curse!")
+
+
+SPELLS: Dict[str, Callable[[Wizard, Wizard], None]] = {
+    "Accio": heal_spell(5),
+    "Aguamenti": damage_spell(5),
+    "Alohomora": remove_shield_spell(),
+    "Arresto Momentum": damage_stun_spell(10),
+    "Bombarda": damage_spell(40),
+    "Carpe Retractum": damage_heal_spell(15, 5),
+    "Colloportus": shield_spell(15),
+    "Confundo": damage_stun_spell(0),
+    "Confringo": confringo_spell,
+    "Crucio": damage_stun_spell(30),
+    "Diffindo": damage_spell(25),
+    "Ennervate": ennervate_spell,
+    "Expelliarmus": damage_remove_shield_spell(15),
+    "Expulso": damage_spell(30),
+    "Flipendo": damage_remove_shield_spell(10),
+    "Imperio": damage_heal_spell(20, 20),
+    "Impedimenta": damage_stun_spell(20),
+    "Incendio": damage_spell(30),
+    "Langlock": damage_stun_spell(15),
+    "Locomotor Mortis": damage_stun_spell(25),
+    "Lumos Solem": damage_remove_shield_spell(10),
+    "Morsmordre": damage_spell(35),
+    "Obliviate": damage_heal_spell(15, 10),
+    "Obscuro": damage_shield_spell(10, 5),
+    "Orchideous": heal_spell(10),
+    "Petrificus Totalus": damage_stun_spell(10),
+    "Protego": shield_spell(30),
+    "Reducto": damage_spell(35),
+    "Relashio": damage_remove_shield_spell(20),
+    "Rictusempra": damage_stun_spell(10),
+    "Salvio Hexia": shield_spell(20),
+    "Scourgify": damage_heal_spell(5, 5),
+    "Sectumsempra": damage_bleed_spell(25, 5),
+    "Stupefy": damage_stun_spell(20),
+    "Tarantallegra": damage_stun_spell(15),
+    "Wingardium Leviosa": damage_shield_spell(5, 5),
+    "Avada Kedavra": avada_kedavra,
+}
+
+
+def cast_spell(caster: Wizard, target: Wizard, choice: str) -> None:
+    """Apply the effects of a spell from caster to target."""
+    log(f"{caster.name} casts {choice}!")
+    effect = SPELLS[choice]
+    effect(caster, target)
+
+
+def choose_spell(name: str) -> str:
+    options = ", ".join(SPELLS.keys())
+    choice = input(f"{name}, choose your spell ({options}): ")
+    while choice not in SPELLS:
+        choice = input(f"Invalid spell. Choose again ({options}): ")
+    return choice
+
+
+def take_turn(attacker: Wizard, defender: Wizard, spell: Optional[str] = None, auto: bool = False) -> None:
+    """Process a single turn for attacker against defender."""
+    if attacker.bleeding:
+        log(f"{attacker.name} bleeds for {attacker.bleeding} damage!")
+        apply_damage(attacker, attacker.bleeding)
+        attacker.bleeding = 0
+        if not attacker.alive():
+            return
+    if attacker.stunned:
+        log(f"{attacker.name} is stunned and skips the turn!")
+        attacker.stunned = False
+        return
+    if spell is None:
+        if auto:
+            spell = random.choice(list(SPELLS.keys()))
+        else:
+            spell = choose_spell(attacker.name)
+    cast_spell(attacker, defender, spell)
+
+
+def duel(player: Wizard, enemy: Wizard, auto: bool = False) -> None:
+    """Run a duel between two wizards."""
+    turn = 0
+    while player.alive() and enemy.alive():
+        attacker, defender = (player, enemy) if turn % 2 == 0 else (enemy, player)
+        take_turn(attacker, defender, auto=auto or attacker is enemy)
+        log(
+            f"\n{player.name}: {player.health} hp (shield {player.shield}) | "
+            f"{enemy.name}: {enemy.health} hp (shield {enemy.shield})\n"
+        )
+        turn += 1
+    winner = player if player.alive() else enemy
+    log(f"{winner.name} wins the duel!")
+
+
+class DuelGUI:
+    """Tkinter-based interface for the duel."""
+
+    def __init__(self) -> None:
+        import tkinter as tk
+
+        self.tk = tk
+        self.root = tk.Tk()
+        self.root.title("Wizard Duel")
+
+        self.player = Wizard("Harry")
+        self.enemy = Wizard("Voldemort")
+
+        # logging
+        global log
+        log = self.gui_log
+
+        self.player_label = tk.Label(self.root)
+        self.player_label.pack()
+        self.enemy_label = tk.Label(self.root)
+        self.enemy_label.pack()
+
+        self.text = tk.Text(self.root, height=10, width=60, state=tk.DISABLED)
+        self.text.pack()
+
+        self.spell_var = tk.StringVar(value=list(SPELLS.keys())[0])
+        self.spell_menu = tk.OptionMenu(self.root, self.spell_var, *SPELLS.keys())
+        self.spell_menu.pack()
+
+        self.cast_button = tk.Button(self.root, text="Cast Spell", command=self.player_cast)
+        self.cast_button.pack()
+
+        self.update_labels()
+
+    def gui_log(self, message: str) -> None:
+        self.text.config(state=self.tk.NORMAL)
+        self.text.insert(self.tk.END, message + "\n")
+        self.text.see(self.tk.END)
+        self.text.config(state=self.tk.DISABLED)
+
+    def update_labels(self) -> None:
+        self.player_label.config(
+            text=f"{self.player.name}: {self.player.health} hp (shield {self.player.shield})"
+        )
+        self.enemy_label.config(
+            text=f"{self.enemy.name}: {self.enemy.health} hp (shield {self.enemy.shield})"
+        )
+
+    def player_cast(self) -> None:
+        spell = self.spell_var.get()
+        take_turn(self.player, self.enemy, spell)
+        self.update_labels()
+        if not self.check_winner():
+            self.root.after(1000, self.enemy_turn)
+
+    def enemy_turn(self) -> None:
+        take_turn(self.enemy, self.player, auto=True)
+        self.update_labels()
+        self.check_winner()
+
+    def check_winner(self) -> bool:
+        if not self.player.alive() or not self.enemy.alive():
+            winner = self.player if self.player.alive() else self.enemy
+            log(f"{winner.name} wins the duel!")
+            self.cast_button.config(state=self.tk.DISABLED)
+            return True
+        return False
+
+    def start(self) -> None:
+        self.root.mainloop()
+
+
+def main() -> None:
+    parser = argparse.ArgumentParser(description="Harry Potter themed duel game")
+    parser.add_argument("--auto", action="store_true", help="simulate duel without user input")
+    parser.add_argument("--gui", action="store_true", help="launch graphical interface")
+    args = parser.parse_args()
+
+    if args.gui:
+        DuelGUI().start()
+    else:
+        player = Wizard("Harry")
+        enemy = Wizard("Voldemort")
+        duel(player, enemy, auto=args.auto)
+
+
+if __name__ == "__main__":
+    main()
