from GeneticAlgorithm.GaAlgo import Population
import time
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import logging
import argparse
import textwrap


logging.basicConfig(
		filename='log.log',
        format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
        level=logging.INFO,
        datefmt="%H:%M:%S",
)
# Create a logger object.
logger = logging.getLogger(__file__.split('.')[0])
logging.getLogger("chardet.charsetprober").disabled = True


def main(args):
	target_name = args.target
	population_size = args.population
	target = list(target_name)
	start = time.time()
	p = Population(population_size, target)
	fitness = []
	gen = 1
	while True:
		f = p.proba_of_importance()
		fitness_max = np.max(f)
		fitness.append(fitness_max)
		if fitness_max == 1:
			break
		else:
			p.create_new_generation()
			gen += 1
	end = time.time()
	logger.info(f'found the target passeword in generation: {gen} with Time: {end - start:.2f} s')
	logger.info(f'Generation: {gen}')
	for entitie in p.entities:
		logger.info(f'<Entity: {entitie}> | fitness score: {entitie.fitness_score(target)}')
	current_dir = os.path.realpath(os.path.dirname(__file__))
	figures_dir = os.path.join(current_dir, 'figures')
	if not os.path.exists(figures_dir):
		os.mkdir(figures_dir)
	plt.plot(range(gen), fitness)
	plt.xlabel('generations')
	plt.ylabel('max fitness over generation')
	plt.title(target_name)
	plt.savefig(os.path.join(figures_dir, 'FitnessOverGeneration.png'))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		prog = "CrackPassword",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent("""\


██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗      ██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗    ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║    ██║     ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║    ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝    ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝      ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                                                               


Run simulations with differents passwords targets and differents size of the population
to crack the password with genetic algorithm.
"""
			),
		epilog=textwrap.dedent("""\
			Example usage:
			--------------
			- Run the simulation with population size 150 and password target GeneticAlgorithm@23:
			  	$ python crack_code.py -p 150 -t GeneticAlgorithm@23

			"""
			)
		)
	parser.add_argument(
		'-p', '--population', type=int, default=150,
		help="""\
			choose the population size for the genetic algorithm.
		"""
		)
	parser.add_argument(
		'-t', '--target', type=str, required=True,
		help="""\
			choose the target passeword to crack
		"""
	)
	args = parser.parse_args()
	main(args)