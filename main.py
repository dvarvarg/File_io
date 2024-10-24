from tkinter import *
import requests
from tkinter import filedialog as fd
#from tkinter import ttk
from tkinter import messagebox as mb
import pyperclip
import os
import json


file_save='history_link.json'


def save_history(file_save, link,file): # куда и что сохраняем
    history=[] #создали пустой список
    if os.path.exists(file_save):  # если файл существует
        with open(file_save,'r') as f: # и дополняем его новым
            history=json.load(f) # то мы загружаем в него все данные из этого файла
    history.append({'name_file' : os.path.basename(file), # имя файла
                    'save_file_history':os.path.basename(file_save), # куда мы сохраняем
                    'link': link}) # сгенерированная ссылка
    with open(file_save, 'w') as f:
        json.dump(history,f,indent=4) # загрузить данные (какие, куда, с каким отступом)


def get_response():
    try:
        file=fd.askopenfilename()
        if file:
            with open (file,'rb') as fi:  # rb-чтение файла побитно
                f={'file':fi}
                answer_json=requests.post('https://file.io',files=f)
                #print(answer_json.json())
                if answer_json.status_code == 200:
                    link=answer_json.json()['link']
                    e.delete(0,END)
                    e.insert(0,link)
                    pyperclip.copy(link) #сохранение в буфер обмена, как только получили ссылку, то она у нас уже скопирована и ее можно уже вставлять
                    save_history(file_save, link,file)
                else:
                     mb.showerror('Ошибка', 'Неверно указанный путь к сайту')
    except Exception as e:
        mb.showerror('Ошибка',f'Произошла ошибка: {e}')


def show_history():
    if not os.path.exists(file_save):
        mb.showinfo('Информация','История пуста')
        return
    window_history=Toplevel()
    window_history.title('История')

    name_listbox=Listbox(window_history,width=50)
    name_listbox.pack(side=LEFT)

    link_listbox=Listbox(window_history,width=50)
    link_listbox.pack(side=LEFT)

    with open(file_save,'r') as file:
        content=json.load(file)
        for i in content:
            name_listbox.insert(END,i['name_file'])
            link_listbox.insert(END, i['link'])




window=Tk()
window.title('Отправка файлов в file.io')
window.geometry(f'400x300+{window.winfo_screenwidth()//2-200}+{window.winfo_screenheight()//2-150}')

btn=Button(window, text='Выбрать файл',font=('Arial',16), command=get_response)
btn.pack(pady=10)

e=Entry(window,width=30, font=('Arial',16))
e.pack(pady=10)

btn_history=Button(window,text='Посмотреть историю',font=('Arial',16), command=show_history)
btn_history.pack()

window.mainloop()