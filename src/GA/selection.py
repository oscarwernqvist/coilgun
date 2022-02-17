from .DNA import DNA

from random import sample


def versus(gen_score: list[tuple[DNA, float]]) -> DNA:
	"""Return a parent after a 1v1 duel (the highest fitness wins)"""
	combatants = sample(gen_score, 2)

	# Return the combatant with the highest fittness
	return max(combatants, key=lambda x: x[1])[0]

