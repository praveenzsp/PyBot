from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox, filedialog
import wolframalpha
import threading
import wikipedia as wik


class PyBot:
    def __init__(self, root):
        self.root = root

        self.font = ('arial', 12)
        self.background_color = '#000000'
        self.text_color = '#ffffff'

        # Add Widgets ....
        # Add menu ....
        menubar = Menu(self.root)
        option_menu = Menu(menubar, tearoff=0)
        option_menu.add_command(label="Clear Chat", command=self.clear_chat)
        option_menu.add_command(label="Save Chat", command=self.save_chat)
        option_menu.add_command(label="Change Font", command=None)
        option_menu.add_separator()
        option_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Options", menu=option_menu)
        self.root.config(menu=menubar)

        self.text_area = ScrolledText(self.root, font=self.font,
                                      bg=self.background_color,
                                      fg=self.text_color,
                                      undo=True,
                                      wrap=WORD, bd=3, relief=RAISED)
        self.text_area.config(spacing1=5)
        self.text_area.config(spacing2=5)
        self.text_area.config(spacing1=5)
        self.text_area.place(x=10, y=10, width=480, height=440)

        frame = Frame(self.root, bg=self.background_color,
                      bd=2, relief=RAISED)
        frame.place(x=10, y=460, width=480, height=50)

        self.entry_box = Entry(frame,
                               font=('arial', 14),
                               bd=1, relief=RAISED,
                               width=35)
        self.entry_box.grid(row=0, column=0, pady=9, padx=5)

        self.send_button = Button(frame, text="Send", width=6, command=self.human_input)
        self.send_button.grid(row=0, column=1, pady=9, padx=5)

    def human_input(self):
        input = self.entry_box.get()
        if input:
            self.text_area.insert(END, "You : " + input)
            self.entry_box.delete(0, END)
            self.call_bot(input)

    def bot_output(self, input):
        appid = "V9JA54-7YWULJ89TH"
        client = wolframalpha.Client(appid)
        res = client.query(input)
        # if input == 'who are you':
        #     self.text_area.insert(END, "\nJarvis : My name is Jarvis" + '\n')
        # if input == 'who made you' or 'who created you' or 'who invented you':
        #     self.text_area.insert(END, "\nJarvis : I was created by Praveen." + '\n')
        try:
            answer = next(res.results).text
            if answer:
                self.text_area.insert(END, "\nJarvis : " + answer + '\n')
        except:
            try:
                answer = wik.summary(input, sentences=2)
            except:
                self.text_area.insert(END, "\nJarvis : uhoh....please enter your query more clearly" + '\n')
            self.text_area.insert(END, "\nJarvis : " + answer + '\n')


    def call_bot(self, input):
        x = threading.Thread(target=self.bot_output, args=(input,))
        x.start()

    def save_chat(self):
        filename = filedialog.asksaveasfile()
        if filename:
            with open(filename, "w") as f:
                f.write(self.text_area.get(0.0, END))

    def clear_chat(self):
        if messagebox.askyesno("JARVIS Says", "Do you really want ot delete recent Chats"):
            self.text_area.delete(0.0, END)


if __name__ == "__main__":
    root = Tk()
    root.title("JARVIS-Just A Rather Very Intelligent System")
    root.geometry("500x520")
    root.config(bg="grey")
    root.resizable(0, 0)
    PyBot(root)
    root.mainloop()
