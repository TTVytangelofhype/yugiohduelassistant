"""Deck-agnostic, conservative Yu-Gi-Oh study helpers (not a full game solver)."""
import json
from pathlib import Path

def read_deck(path):
    deck = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(deck, dict):
        raise ValueError("Deck must be a JSON object")
    for zone in ("main", "extra", "side"):
        cards = deck.get(zone, {})
        if not isinstance(cards, dict):
            raise ValueError(zone + " must map names to counts")
        for name, count in cards.items():
            if not isinstance(name, str) or not name.strip() or type(count) is not int or not 0 <= count <= 3:
                raise ValueError("Each card needs a name and count 0–3")
    return deck

def deck_statistics(deck):
    totals = {z: sum(deck.get(z, {}).values()) for z in ("main", "extra", "side")}
    totals["main_in_range"] = 40 <= totals["main"] <= 60
    totals["extra_in_range"] = totals["extra"] <= 15
    return totals

def battle_damage(attack, opposing_stat=0, position="Attack", direct=False):
    if min(attack, opposing_stat) < 0:
        raise ValueError("Stats cannot be negative")
    if direct:
        return {"opponent": attack, "you": 0}
    if position == "Attack":
        return {"opponent": max(attack-opposing_stat, 0), "you": max(opposing_stat-attack, 0)}
    return {"opponent": 0, "you": max(opposing_stat-attack, 0)}

def checklist(hand, field, grave, extra, opponent, phase, deck=None):
    data = ["NEXUS DUEL AI — OFFLINE STUDY CHECKLIST", "This is not a legal-move solver.", "Phase: " + phase]
    for label, value in (("Hand",hand),("Your field",field),("Graveyard",grave),("Available extra-deck cards",extra),("Known opponent cards",opponent)):
        data.append(label + ": " + (value.strip() or "(unknown)"))
    if deck:
        data.append("Deck: " + str(deck.get("name","Unnamed")) + " | " + str(deck_statistics(deck)))
    data.extend(["Verify normal summon/once-per-turn usage, exact card effect text, costs and targeting.",
                 "Check summon locks, chain timing, battle positions and opponent interruptions.",
                 "Unknown face-down/hand cards must remain unknown.",
                 "For additional *unverified* ideas, use optional local screenshot AI."])
    return "\n".join(data)
