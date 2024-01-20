import os

import PySimpleGUI as sg

layout = [
    [
        sg.Text('Current Directory: '), sg.Text(size=(60, 1), key='current_directory'),
        sg.Button('Home', key='home'),
        sg.Button('Back', key='back'),
        sg.Checkbox('Show Hidden Files', key='show_hidden_files'),
    ],
    [sg.Table(key='table', values=[], size=(400, 100), headings=['file_name_full_path', 'linecount'], enable_events=True)],
]

window = sg.Window('LC File Explorer', layout, resizable=True, finalize=True, font=('Helvetica', 18))
window.Maximize()


def show_files_in_dir(selected_dir, window):
    window['current_directory'].update(selected_dir)
    print(selected_dir)
    files = os.listdir(selected_dir)
    if not window.show_hidden_files:
        files = [file for file in files if not file.startswith('.')]
    files = sorted(files)
    file_paths = [os.path.join(selected_dir, file) for file in files]
    # line_count = [' ' if not os.path.isfile(file) else str(len(open(file).readlines())) for file in files]
    line_count = []
    for file in file_paths:
        if os.path.isfile(file):
            try:
                line_count.append(str(len(open(file).readlines())))
            except Exception:
                line_count.append(' ')
        else:
            line_count.append(' ')

    window.current_files = list(zip(files, line_count))
    window.current_directory = selected_dir
    window['table'].update(values=window.current_files)


home_dir = os.path.expanduser('~')
window.show_hidden_files = False
show_files_in_dir(home_dir, window)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == 'table':
        try:
            file = values['table'][0]
            file_name = window.current_files[file][0]
            selected_dir = os.path.join(window.current_directory, file_name)
            if os.path.isdir(selected_dir):
                show_files_in_dir(selected_dir, window)
        except IndexError:
            pass

    if event == 'back':
        directory = os.path.dirname(window.current_directory)
        show_files_in_dir(directory, window)

    if event == 'show_hidden_files':
        window.show_hidden_files = values['show_hidden_files']
        show_files_in_dir(window.current_directory, window)

    if event == 'home':
        show_files_in_dir(home_dir, window)
