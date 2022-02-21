import os


def test_cross_breeding(gen_score, breeding_vs):
	"""Test the cross breeding"""
	dna_A = gen_score[0][0]
	dna_B = gen_score[1][0]
	# This is the worst DNA
	# It should never give any genes
	dna_C = gen_score[2][0]

	for _ in range(1000):
		new_dna = breeding_vs.breed(gen_score)

		for key in new_dna.DNA.keys():
			# Make sure the DNA only has genes from A or B
			assert not new_dna.DNA[key] == dna_C.DNA[key]
			assert new_dna.DNA[key] == dna_A.DNA[key] or new_dna.DNA[key] == dna_B.DNA[key]

def test_evolution(test_evolution):
	"""
	Test the evolution algorithm with a simple DNA.
	The DNA only has one gene, one float between 0 and 1,
	and the fitness function will try to maximize this
	"""
	# Evaluate the current population score
	start_score = sum([dna_score[1] for dna_score in test_evolution.evaluate_gen()])

	# Do the evolution
	test_evolution.evolve()

	# New population score
	end_score = sum([dna_score[1] for dna_score in test_evolution.evaluate_gen()])

	# The population score should be higher now
	assert end_score > start_score

def test_checkpoint_saving(tmp_path, test_evolution):
	"""Try to save a checkpoint"""
	checkpoint_dir = test_evolution.save_checkpoint(tmp_path)

	# Check that all the DNA has been saved
	assert len(os.listdir(checkpoint_dir)) == 100



