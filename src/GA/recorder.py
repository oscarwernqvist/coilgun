import os

from datetime import datetime
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable
from math import floor

import matplotlib.pyplot as plt


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


class CLIInformationRecorder(Recorder):
	"""Print information to the command line during evolution"""

	def __init__(self, print_every: int=1):
		self.print_every = print_every
		self.start_time = None

	def setup(self, evolution):
		self.start_time = datetime.now()
		print("Generation\tProgress\tAverage fitness\tBest fitness\tElapsed time (H:M:S)\tEstimated time left(H:M:S)")

	def record(self, evolution):
		gen = evolution.current_gen
		gens = evolution.last_gen

		# Generation
		generation_report = f"{gen}/{gens}"

		# Progress bar
		progressbar_width = 20
		fill = floor(progressbar_width * gen / gens)
		progressbar = ('#'*fill).ljust(progressbar_width, "-")

		# Fitness report
		average_fitness = f"{evolution.average_score():.4f}"
		best_fitness = f"{evolution.best_score:.4f}"

		# Time eleapsed
		duration = datetime.now() - self.start_time
		total_seconds = duration.total_seconds()
		hours, minutes_rest = divmod(total_seconds, 3600)
		minutes, seconds_rest = divmod(minutes_rest, 60)
		seconds = round(seconds_rest)

		time_elapsed = f"{hours:.0f}:{minutes:.0f}:{seconds:.0f}"

		# Time left
		average_duration = total_seconds / gen
		seconds_left = average_duration * (gens - gen)
		hours, minutes_rest = divmod(seconds_left, 3600)
		minutes, seconds_rest = divmod(minutes_rest, 60)
		seconds = round(seconds_rest)

		time_left = f"{hours:.0f}:{minutes:.0f}:{seconds:.0f}"

		print("\t".join([generation_report, progressbar, average_fitness, best_fitness, time_elapsed, time_left]))

	def summary(self, evolution):
		pass


class FitnessRecorder(CLIInformationRecorder):
	"""Record statistics about the evolution"""

	def __init__(self):
		self.data = []

	def setup(self, evolution):
		super().setup(evolution)

	def record(self, evolution):
		super().record(evolution)

		average_score = evolution.average_score()
		best_score = evolution.best_score
		self.data.append((average_score, best_score))

	def summary(self, evolution):
		# TODO: Matlab plot and save data
		super().summary(evolution)

		plt.plot(range(1, evolution.last_gen+1), self.data, label=["Average fitness", "Best fitness"])

		plt.ylim([0, max(1, evolution.best_score*1.2)])
		plt.xlabel("Generation")
		plt.ylabel("Efficiency")
		plt.legend()
		plt.show()


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

