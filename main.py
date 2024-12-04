from nicegui import ui
import numpy as np
from tasker import Tasker

tasker = Tasker()
simulations = 1000
# N = 100
# mutation_rate = 0.01
# migration_rate = 0.1
# generations = 100

intro = ui.markdown('''
    # **GPOP 05/12/2024** 🗣️🗣️\n
    */ The population is formed by N haploid individuals, each one carrying one allele for a given locus.\n
    */ The population evolves with constant population size and discrete non-overlapping generations.\n
    */ Each individual in generation t+1 is a copy of a randomly selected individual in generation t.\n
''')
# N_input = ''
# mutation_rate_input = ''
# migration_rate_input = ''
# generations_input = ''
with ui.row() as input_buttons:
    N = ui.number(label='input N', value=100, placeholder='wanna change value of N?',)#.bind_value_to(globals(), N)
    mutation_rate = ui.number(label='input mutation_rate', value=0.01, placeholder='wanna change value of mutation rate?')
    migration_rate = ui.number(label='input migration_rate', value=0.1, placeholder='wanna change value of migration rate?')
    generations = ui.number(label='input generations', value=100, placeholder='wanna change value of generations?')
def task1(p, N):
    with ui.row() as task1_row:
        with ui.card().classes('w-[1300px] mx-auto'):
            ui.markdown('## Genetic Drift')
            with ui.matplotlib(figsize=(12, 6)).figure as fig:
                ax = fig.gca()
                for i in range(5):
                    gen_drift = tasker.task_1(p=p, N=N)
                    ax.plot(gen_drift, label=f"pop {i}")
                ax.set_ylim(ymin=0, ymax=1)
                ax.set_xlim(xmin=0, xmax=2*N)
                ax.set_xlabel('Generations')
                ax.set_ylabel('p: frequency of allele A')
                ax.legend()
        with ui.card().classes('w-[500px] mx-auto'):
            ui.markdown('##### Cheatsheet')
            ui.button('mr. clean', on_click=lambda: (task1_row.delete()))
            fixations = 0
            times = []            
            for i in range(simulations):
                gen_drift = tasker.task_1(p=p, N=N)
                if gen_drift[-1] == 1 or 0:
                    fixations += 1
                times.append(len(gen_drift) - 1)
            ui.markdown(f'The fixation probability of allele A with pA=**{p}** over {simulations} simulations:\
                         **{round(fixations/simulations, 2)}**')
            ui.markdown("""Fixation probability of allele A in pop = initial allele frequency pA.                        
                        For pA = 0.2, fixation probability of allele A is in range(0.12, 0.17)""")
            ui.markdown(f'The expected fixation time (number of generations): {round(np.mean(times), 2)}')
            ui.markdown(r'''
                            Harmonic mean of actual pop size:
                            $$Ne = (\frac{1}{t}\sum_{i=0}^{t-1} \frac{1}{Ni})^-1$$
                        ''', extras=['latex'])
            ui.markdown('Theoretically, with N = 100 and generations = 200, Ne ~ 100')
            
def task2(N):
    with ui.row() as task2_row:
        with ui.card().classes('w-[1300px] mx-auto'):
            ui.markdown('## Coalescent model')
            with ui.matplotlib(figsize=(12, 6)).figure as fig:
                ax = fig.gca()
                generation, freq = tasker.task_2_identicalByDescent(N = N)
                ax.plot(freq, label='frequency of an allele from 1/N to 1')
                ax.set_ylim(ymin=0, ymax=1)
                ax.set_xlim(xmin=0, xmax=2*N)
                ax.set_xlabel('Generations')
                ax.set_ylabel('Frequency of an allele')
                ax.legend()
                ax.set_title('All alleles are identical by descent')
            with ui.matplotlib(figsize=(12, 6)).figure as fig2:
                sample_size = [2, 3, 4, 5]
                E_Tn = []
                generations_arr = []
                for n in sample_size:
                    E_Tn.append(2 * N / (n * (n - 1)))
                    generationsForEachN = []
                    for i in range(simulations):
                        generationsForEachN.append(tasker.task_2_firstCoalescentEvent(n=n, N=N))
                    generations_arr.append(np.mean(generationsForEachN))
                ax = fig2.gca()
                ax.plot(sample_size, E_Tn, label='Theoretical', marker='o', color='green')
                ax.plot(sample_size, generations_arr, label='Empirical', marker='x', color='red')
                ax.set_yticks(np.arange(0, 110, 5))
                ax.set_xlabel("Sample size n = [2, 3, 4, 5]")
                ax.set_ylabel("Generations to First Coalescent Event")
                ax.set_title("Empirical / Theoretical")
                ax.legend()
            with ui.matplotlib(figsize=(12, 6)).figure as fig2:
                sample_size = [2, 3, 4, 5]
                E_Tn = []
                generations_arr = []
                for n in sample_size:
                    E_Tn.append(2 * N / (n * (n - 1)))
                    generationsForEachN = []
                    for i in range(simulations):
                        generationsForEachN.append(tasker.task_2_coalescentModel(n=n, N=N))
                    generations_arr.append(np.mean(generationsForEachN))
                ax = fig2.gca()
                ax.plot(sample_size, E_Tn, label='Theoretical', marker='o', color='green')
                ax.plot(sample_size, generations_arr, label='Empirical', marker='x', color='red')
                ax.set_xlabel("Sample size n = [2, 3, 4, 5]")
                ax.set_ylabel("Generations of Coalescent Model")
                ax.set_title("Empirical / Theoretical")
                ax.legend()
        with ui.card().classes('w-[500px] mx-auto'):
            ui.markdown('##### Cheatsheet')
            ui.button('mr. clean', on_click=lambda: (task2_row.delete()))
            ui.markdown('Tracking a population of N = 100 individuals until all alleles are identical by descent\
                        is like tracking genetic drift.')
            ui.markdown('A population has N alleles with first frequency of each allele = 1/N. \
                        To count generations until frequency of an allele reach 1. \
                        That means this population has 1 allele left.')
            ui.markdown(r'''
                            Expected generations to the first coalescent event:
                            $$E\{Tn\} = \frac{4N}{n(n-1)}$$
                            $$E\{T2\} = 100  $$
                            $$E\{T3\} = 33.34$$
                            $$E\{T4\} = 16.67$$
                            $$E\{T5\} = 10   $$
                        ''', extras=['latex'])
            ui.markdown('To the first coalescent event, number of generations in empirical experiment and theory are the same.\
                         But in case of running the model until the number of lineages = 1, number of generations in empirical experiment is far away from theory.\
                        because the assumption n ≪ N is violated.')

def task3(N, mutation_rate, generations):
    # print(N, mutation_rate, generations)
    with ui.row() as task3_row:
        with ui.card().classes('w-[1300px] mx-auto'):
            ui.markdown('## Mutation and drift')
            with ui.matplotlib(figsize=(12, 6)).figure as fig:
                ax = fig.gca()
                equilibrium = 1 / (1+2*N*mutation_rate)
                fixation = tasker.task_3(N = N, mutation_rate = mutation_rate, generations = generations)
                # print(fixation)
                ax.plot(fixation, label='fixation index')
                ax.set_ylim(ymin=0, ymax=1)
                ax.hlines(y = equilibrium, xmin=0, xmax=generations, color='red', linestyle='--', label='Equilibrium')
                ax.hlines(y = np.mean(fixation), xmin=0, xmax=generations, color='green', linestyle='--', label='mean value of fixation index')
                ax.set_xlim(xmin=0, xmax=generations)
                ax.set_xlabel('Generations')
                ax.set_ylabel('Fixation index')
                ax.legend()
                ax.set_title('The fixation index (probability that two randomly chosen alleles are identical) over time')
        with ui.card().classes('w-[500px] mx-auto'):
            ui.markdown('##### Cheatsheet')
            ui.button('mr. clean', on_click=lambda: (task3_row.delete()))
            ui.markdown(r'''
                            The fixation index: the value of $\mathcal{G}$ after one round of random mating and mutation
                            $$\mathcal{G'} = (1-\mu)^2[\frac{1}{2N} + (1 - \frac{1}{2N})\mathcal{G}]$$
                        
                            With G and $\mathcal{G}$ are "almost the same" + the total frequency of homozygotes is given by:
                            $$G = \sum_{i=1}^{k}p_i^2$$
                        
                            At equilibrium, the probability that 2 alleles different by origin are identical by state is given by:
                            $$\hat{\mathcal{G}} = \frac{1}{1+2N\mu}$$
                        ''', extras=['latex'])
            ui.markdown(f'For this example, the equilibrium = {round(equilibrium, 2)} which is smaller the mean value of fixation index = {round(np.mean(fixation), 2)}')
            ui.markdown(r'''Genetic drift increases fixation index $\mathcal{G}$ while **mutation decreases $\mathcal{G}$.**
                        ''', extras=['latex'])
            ui.markdown(f'Run the experiment for several times until 1000 generations. \
                        Most of the plots have peaks that reach the equilibrium and then return, with a few times that can surpass the equilibrium. \
                        Anyway, equilibrium =/= static -> new mutations/alleles appear, drift happens.')
def task4(N, p, s, generations):
    with ui.row() as task4_row:
        with ui.card().classes('w-[1300px] mx-auto'):
            ui.markdown('## Selection')
            with ui.matplotlib(figsize=(12, 6)).figure as fig:
                ax = fig.gca()
                freq = tasker.task_4(N = N, p = p, s = s, generations= generations)
                ax.plot(freq, label='Frequency of allele B')
                ax.set_ylim(ymin=0, ymax=1.1)
                ax.set_xlim(xmin=0, xmax=generations)
                ax.set_xlabel('Generations')
                ax.set_ylabel('Frequency of allele B')
                ax.legend()
                ax.set_title('The fraction of allele B over time.')
        with ui.card().classes('w-[500px] mx-auto'):
            ui.markdown('##### Cheatsheet')
            ui.button('mr. clean', on_click=lambda: (task4_row.delete()))
def task5(N, generations):
    with ui.row() as task5_row:
        with ui.card().classes('w-[1300px] mx-auto'):
            ui.markdown('## Clonal interference')
            for N in [40, 100, 300, 500, 1000, 2000]:
                with ui.matplotlib(figsize=(12, 6)).figure as fig:
                    ax = fig.gca()
                    freq_A, freq_B, freq_C = tasker.task_5(N = N, generations= generations)
                    ax.plot(freq_A, label='Frequency of allele A')
                    ax.plot(freq_B, label='Frequency of allele B')
                    ax.plot(freq_C, label='Frequency of allele C')
                    ax.set_ylim(ymin=-0.1, ymax=1.1)
                    ax.set_xlim(xmin=0, xmax=generations)
                    ax.set_xlabel(f'{generations} Generations')
                    ax.set_ylabel('Frequencies of alleles')
                    ax.legend()
                    ax.set_title(f'The fraction of alleles over time + N = {N}')
        with ui.card().classes('w-[500px] mx-auto'):
            ui.markdown('##### Cheatsheet')
            ui.button('mr. clean', on_click=lambda: (task5_row.delete()))
def task6(p, N, generations):
    with ui.row() as task6_row:
        with ui.card().classes('w-[1300px] mx-auto'):
            ui.markdown('## Population structure')
            with ui.matplotlib(figsize=(12, 6)).figure as fig:
                ax = fig.gca()
                freqs = tasker.task_6(p = p, N = N, generations= generations)
                for i in range(len(freqs)):
                    ax.plot(freqs[i], label=f'sub-population {i}')
                ax.set_ylim(ymin=-0.1, ymax=1.1)
                ax.set_xlim(xmin=0, xmax=generations)
                ax.set_xlabel(f'{generations} Generations')
                ax.set_ylabel('Frequencies of allele A with p = 0.2')
                ax.legend()
                ax.set_title(f'The evolution of the population with subpopulations')
        with ui.card().classes('w-[500px] mx-auto'):
            ui.markdown('##### Cheatsheet')
            ui.button('mr. clean', on_click=lambda: (task6_row.delete()))
def task7(p, N, generations, migration_rate):
    with ui.row() as task7_row:
        with ui.card().classes('w-[1300px] mx-auto'):
            ui.markdown('## Migration')
            with ui.matplotlib(figsize=(12, 6)).figure as fig:
                ax = fig.gca()
                freqs = tasker.task_7(p = p, N = N, generations= generations, migration_rate= migration_rate)
                for i in range(len(freqs)):
                    ax.plot(freqs[i], label=f'sub-population {i}')
                ax.set_ylim(ymin=-0.1, ymax=1.1)
                ax.set_xlim(xmin=0, xmax=generations)
                ax.set_xlabel(f'{generations} Generations')
                ax.set_ylabel(f'Frequencies of allele A with p = {p}')
                ax.legend()
                ax.set_title(f'The evolution of the population with subpopulations and migration')
        with ui.card().classes('w-[500px] mx-auto'):
            ui.markdown('##### Cheatsheet')
            ui.button('mr. clean', on_click=lambda: (task7_row.delete()))
with ui.row():
    ui.button('Task 1', on_click=lambda: (task1(p=0.2, N=int(N.value))))        
    ui.button('Task 2', on_click=lambda: (task2(N=int(N.value))))
    ui.button('Task 3', on_click=lambda: (task3(N = int(N.value), mutation_rate= mutation_rate.value, generations = int(generations.value)*10)))
    ui.button('Task 4', on_click=lambda: (task4(N=int(N.value), p=0.5, s=0.05, generations=int(generations.value))))
    ui.button('Task 5', on_click=lambda: (task5(N=int(N.value), generations=int(generations.value))))
    ui.button('Task 6', on_click=lambda: (task6(p=0.2, N=int(N.value)*10, generations=int(generations.value)*2)))
    ui.button('Task 7', on_click=lambda: (task7(p=0.5, N=int(N.value)*10, generations=int(generations.value)*2, migration_rate=migration_rate.value)))

url = 'https://github.com/khnam-ng/gpop'
ui.button('Open GitHub', on_click=lambda: ui.navigate.to(url, new_tab=True))

ui.dark_mode().enable()
ui.run(title='give me 20', favicon='🗣️')