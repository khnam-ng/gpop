from nicegui import ui
import numpy as np
from tasker import Tasker

tasker = Tasker()
simulations = 1000
N = 100
mutation_rate = 0.1

intro = ui.markdown('''
    # **GPOP 05/12/2024** 🗣️🗣️
''')
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
    with ui.row() as task_row:
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
                ax.set_xlabel("Sample size n = [2, 3, 4, 5]")
                ax.set_ylabel("Generations to First Coalescent Event")
                ax.set_title("Empirical / Theoretical")
                ax.legend()
        with ui.card().classes('w-[500px] mx-auto'):
            ui.markdown('##### Cheatsheet')
            ui.button('mr. clean', on_click=lambda: (task_row.delete()))
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
            
with ui.row():
    ui.button('Task 1', on_click=lambda: (task1(p=0.2, N=N)))
            # badge1 = ui.badge('!', color='red').props('floating')
        
    ui.button('Task 2', on_click=lambda: (task2(N=N)))
        # badge2 = ui.badge('!', color='red').props('floating')
    # ui.button('Task 3', on_click=lambda: (tasker.task_3(p=1, N=100, mutation_rate=0.1), card_label.set_content('## Mutations')))
    # ui.button('Task 4', on_click=lambda: (tasker.task_4(), card_label.set_content('## Selection')))
    # ui.button('Task 5', on_click=lambda: (tasker.task_5(), card_label.set_content('## Clonal inference')))
    # ui.button('Task 6', on_click=lambda: (tasker.task_6(), card_label.set_content('## Population structure')))
    # ui.button('Task 7', on_click=lambda: (tasker.task_7(), card_label.set_content('## Migration')))

url = 'https://github.com/khnam-ng/gpop'
ui.button('Open GitHub', on_click=lambda: ui.navigate.to(url, new_tab=True))

ui.dark_mode().enable()
ui.run(title='give me 20', favicon='🗣️')