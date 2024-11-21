from nicegui import ui
import matplotlib.pyplot as plt
from tasker import Tasker

tasker = Tasker()

intro = ui.markdown('''
    # **GPOP** 🗣️🗣️

    
''')
with ui.row():
    ui.button('Task 1', on_click=lambda: (tasker.task_1(p=1, N=100), card_label.set_content('## Genetic Drift')))
    ui.button('Task 2', on_click=lambda: (tasker.task_2(p=1), card_label.set_content('## Coalescent model')))
    ui.button('Task 3', on_click=lambda: (tasker.task_3(p=1, N=100, mutation_rate=0.1), card_label.set_content('## Mutations')))
    ui.button('Task 4', on_click=lambda: (tasker.task_4(), card_label.set_content('## Selection')))
    ui.button('Task 5', on_click=lambda: (tasker.task_5(), card_label.set_content('## Clonal inference')))
    ui.button('Task 6', on_click=lambda: (tasker.task_6(), card_label.set_content('## Population structure')))
    ui.button('Task 7', on_click=lambda: (tasker.task_7(), card_label.set_content('## Migration')))

with ui.row():
    with ui.card().classes('w-[1300px] h-[600px] mx-auto'):
        card_label = ui.markdown('')
    with ui.card().classes('w-[500px] h-[600px] mx-auto'):
        ui.markdown('##### Cheatsheet')
        ui.markdown('''''')

url = 'https://github.com/zauberzeug/nicegui/'
ui.button('Open GitHub', on_click=lambda: ui.navigate.to(url, new_tab=True))

ui.dark_mode().enable()
ui.run(title='give me 20', favicon='🗣️')