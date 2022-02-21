import os

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable


class Recorder(ABC):
	"""Record details about the evolution"""

	@abstractmethod
	def setup(self, evolution):
		"""This function called before the start of the evolution"""

	@abstractmethod
	def record(self, evolution):
		"""This function is called every step in the evolution"""

	@abstractmethod
	def summary(self, evolution):
		"""This function is called after an evolution is complete"""	

class RecordFunc(Recorder):
	"""Custom record function"""

	def __init__(self, record_func: Callable, summary_func: Callable, setup_func: Callable):
		self.record_func = record_func
		self.data = data
		self.summary_func = summary_func
		self.setup_func = setup_func

	def setup(self, evolution):
		self.setup_func(evolution)

	def record(self, evolution):
		self.data.append(self.record_func(evolution))

	def summary(self, evolution):
		self.summary_func(evolution)


class FitnessRecorder(Recorder):
	"""Record statistics about the evolution"""

	def __init__(self):
		self.data = []

	def setup(self, evolution):
		pass

	def record(self, evolution):
		average_score = evolution.population_score()
		best_score = evolution.best_score
		self.data.append((average_score, best_score))

	def summary(self, evolution):
		# TODO: Matlab plot
		print(self.data)


class CheckpointRecorder(FitnessRecorder):
	"""Saves a checkpoint of the evolution"""

	def __init__(self, save_every: int, output_folder: Path):
		super().__init__()

		# How often should a checkpoint be made
		self.save_every = save_every
		self.output_folder = output_folder

	def setup(self, evolution):
		super().setup(evolution)
		
		# Create the directory to save the evolution data
		os.makedirs(self.output_folder)

		# Save the rules so they can be reused
		evolution.mutation_rules.save_rules(self.output_folder / "rules.yaml")

	def record(self, evolution):
		super().record(evolution)

		if evolution.current_gen % self.save_every == 0 and not evolution.current_gen == 0:
			evolution.save_checkpoint(self.output_folder)

	def summary(self, evolution):
		super().summary(evolution)

		# Save the best DNA
		evolution.best_DNA.save_DNA(self.output_folder / 'best_DNA.yaml')

