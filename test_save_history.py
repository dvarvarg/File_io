import os
import json


def save_history(file_save, link,file): # где сохраняем, что сохраняем, имя файла, который получаем
    history=[] #создали пустой список
    if os.path.exists(file_save):  # если файл существует
        with open(file_save,'r') as f: # и дополняем его новым
            history=json.load(f) # то мы загружаем в него все данные из этого файла
    history.append({'name_file' : os.path.basename(file), # имя файла
                    'save_file_history':os.path.basename(file_save), # куда мы сохраняем
                    'link': link}) # сгенерированная ссылка
    with open(file_save, 'w') as f:
        json.dump(history, f,indent=4) # загрузить данные (какие, куда, с каким отступом)


def test_save_history():
    file_save='test_file.json'
    link='https://file.io/GWfznANXTqHv'
    file_name='reminder.mp3'
    save_history(file_save, link, file_name)
    with open('test_file.json','r') as test_file:
        content=json.load(test_file)
        assert len(content)==1

    os.remove('test_file.json')


test_save_history()
