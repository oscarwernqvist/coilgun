from GA.DNA import DNA
from GA.selection import versus

def test_versus():
	"""Test that the versus selcection returns the best of the combatants"""
	good_DNA = DNA()
	bad_DNA = DNA()

	gen_score = [(good_DNA, 1), (bad_DNA, 0)]

	assert versus(gen_score) is good_DNA
	assert versus(gen_score) is not bad_DNA
