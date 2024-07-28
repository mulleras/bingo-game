from tkinter import *
import datetime
from threading import Thread
import random
from time import sleep as nap
import threading
from playAudios import play_sound as play
from playsound import playsound

		




class BINGO:
    def __init__(self, method, napTime):
        self.need_to_stop = False
        self.need_to_restart = False
        self.method = method
        self.napTime = napTime
        self.numbersof = 0
        if self.method == 'nap':
            self.th = threading.Thread(target=self.key_waiting, daemon=True)
            self.th.start()

    def key_waiting(self):
        # Placeholder method for thread
        pass

    def start_playing_cmd(self):
        num = [i for i in range(1, 76)]
        done = []
        B, I, N, G, O = ([] for _ in range(5))

        for _ in range(1, 76):
            if self.method == 'input':
                input("Press enter to get num")
            else:
                nap(self.napTime)
                while self.need_to_stop:
                    nap(1)

            if num:
                a = random.choice(num)
                num.remove(a)
                
                print(a)
                
                done.insert(0, a)
                done.sort()

                if a <= 15:
                    B.append(a)
                    B.sort()
                elif a <= 30:
                    I.append(a)
                    I.sort()
                elif a <= 45:
                    N.append(a)
                    N.sort()
                elif a <= 60:
                    G.append(a)
                    G.sort()
                elif a <= 75:
                    O.append(a)
                    O.sort()

                print('line  B', B)
                print('line  I', I)
                print('line  N', N)
                print('line  G', G)
                print('line  O', O)
                
                print()
                play(f'sounds/{a}.mp3')

    def start_playing_gui(self):
        if not self.need_to_restart:
            num = [i for i in range(1, 76)]
            for _ in range(1, 76):
                while self.need_to_stop:
                    nap(3)

                a = random.choice(num)
                num.remove(a)
                yield a
        else:
            yield 0

    @classmethod
    def player(cls, method, napTime=2.5):
        pla = cls(method, napTime)
        pla.start_playing_cmd()

class BINGO_gui(BINGO):
    def __init__(self, root):
        super().__init__(method='nap', napTime=1.5)
        self.height = 825
        self.width = 1600

        self.head_bar_colour = '#00ffff'
        self.head_bar_height = 100
        self.footer_height = 50

        self.root = root
        self.root.title('BINGO')
        self.root.geometry(f"{self.width}x{self.height}")

        self.last_tile = None

        self.head()
        self.create_tiles(self.root)
        self.create_popup_frame(self.root)# Create the casher popup frame
        self.create_popup_label(self.root)  # Create the popup label
        self.footer()

    def head(self):
        self.head_bar = Label(self.root, bg=self.head_bar_colour)
        self.head_bar.place(height=self.head_bar_height*1.5, width=0.9 * self.width)

        status_label = Label(self.head_bar, fg='white', bg=self.head_bar_colour, padx=10, font=('arial', 40, 'bold'),
                             text='Status:')
        status_label.pack(side=LEFT)

        self.status_value = Label(self.head_bar, font=('arial', 30, 'bold'), padx=10, text='ቁሟል')
        self.status_value.pack(side=LEFT)

        self.number = Label(self.head_bar, fg='blue', bg=self.head_bar_colour, font=('arial', 20, 'bold'), padx=50, text=self.numbersof)
        self.number.pack(side=LEFT)
        self.number_player = Label(self.head_bar, fg='blue', bg=self.head_bar_colour, font=('arial', 20, 'bold'), padx=50, text='')
        self.number_player.pack(side=LEFT)

        self.time_value = Label(self.head_bar, font=('arial', 40, 'bold'), padx=1, bg=self.head_bar_colour,
                                fg='white', text=datetime.datetime.now().strftime('%I:%M:%S %p'))
        self.time_value.pack(side=RIGHT)

    def footer(self):
        footer_frame = Frame(self.root, bg=self.head_bar_colour, height=self.footer_height)
        footer_frame.pack(side=BOTTOM, fill=X)

        self.stop_button = Button(footer_frame, text="አቁም", command=self.stop_game, anchor=CENTER, font=('arial', 20, 'bold'))
        self.stop_button.pack( padx=40)

        self.start_button = Button(footer_frame, text="አስጀምር", command=self.start_game, anchor=CENTER, font=('arial', 20, 'bold'))
        self.start_button.pack( padx=40)

    def stop_game(self):
        play(f'sounds/{80}.mp3')
        self.need_to_stop = True
        self.need_to_restart = True
        self.status_value.config(text="ቁሟል")
        self.number_player.config(bg=self.head_bar_colour, text='')
        self.number.config(text='') 
        self.numbersof=0;     
        self.stop_button.config(state=DISABLED)
        self.start_button.config(state=NORMAL)
        
        self.casher_frame.lower() 

     

    def start_game(self):
        self.update_casher_info(self.last_tile)
        self.stop_button.config(state=NORMAL)
        self.start_button.config(state=DISABLED)
        
      
       
    def close(self): 
        play(f'sounds/{90}.mp3')
        self.reset_game()
        self.need_to_stop = False
        self.status_value.config(text="በጭዋታ ላይ")
        self.number.config(text=self.numbersof)
        self.number_player.config(text="ተጫዋቾች", bg='red') 
       
        self.casher_frame.lower() 
        Thread(target=self.number_gen, daemon=True).start() 
    def counter(self):
        self.numbersof=self.numbersof+1
        print(self.numbersof)
        
        

    def clock(self):
        while True:
            try:
                self.time_value['text'] = datetime.datetime.now().strftime('%I:%M:%S %p')
                nap(1)
            except Exception as e:
                print(f'Clock Ends: {e}')
                break

    def create_tiles(self, master):
        canvas = Label(master, bg='#95a5a6')
        canvas.place(y=self.head_bar_height + 5, width=self.width, height=self.height - self.head_bar_height - self.footer_height)

        tile_canvas_w = self.width - 50
        tile_canvas_h = self.height - self.head_bar_height - self.footer_height
        tile_canvas = Label(canvas, bg='#ecf0f1', pady=15)
        tile_canvas.place(x=20, width=tile_canvas_w, height=tile_canvas_h)

        count = 1
        for row in range(5):
            if count <= 75:
                for col in range(15):
                    tile_num = str(count).zfill(2)
                    Label(master=tile_canvas, name=tile_num, font=('arial', 31, 'bold'),
                          text=tile_num, borderwidth=5, highlightthickness=5, relief="solid",
                          anchor=CENTER).grid(row=row, column=col, padx=10, pady=5)
                    count += 1
            else:
                break
        
        self.tile_list = tile_canvas.winfo_children()
    def create_popup_label(self, master):
        self.popup_label = Label(master, font=('arial', 60, 'bold'), bg='#ff0000', fg='white', bd=10, relief='solid')
        self.popup_label.place(x=0, y=0)  # Initially place the popup label at the top left corner
        self.popup_label.lower()
       
    def update_tiles(self, num):
        num = str(num).zfill(2)
        for i in self.tile_list:
            if i['text'] == num:
                if self.last_tile:
                    self.last_tile['bg'] = '#f1c40f'
                    self.last_tile['fg'] = 'white'
                i['bg'] = '#3de7c5'
                i['fg'] = 'white'
                self.last_tile = i
                self.animate_popup(i['text'])
                break
        else:
            raise Exception('Unable to find the tile')

    def animate_popup(self, num):
        steps = 50
        start_x, start_y = 0, 0
        end_x = (self.root.winfo_width() - 400) // 2  # Adjusted width for the popup label
        end_y = (self.root.winfo_height() - 200) // 2  # Adjusted height for the popup label

        delta_x = (end_x - start_x) / steps
        delta_y = (end_y - start_y) / steps

        def move_label(step=0):
            if step < steps:
                new_x = start_x + step * delta_x
                new_y = start_y + step * delta_y
                self.popup_label.place(x=new_x, y=new_y)
                self.root.after(10, move_label, step + 1)
            else:
                self.popup_label.place(x=end_x, y=end_y)
                self.root.after(2000, self.popup_label.lower)

        symbol = ""
        if int(num) <= 15:
                symbol = "B"
        elif int(num) <=30:
                symbol = "I"
        elif int(num) <=45:
                symbol = "N"
        elif int(num) <= 60:
                symbol = "G"
        else:
                symbol = "O"
        symbol=symbol+' : '+num      
        self.popup_label.config(text=symbol, font=('arial', 70, 'bold')) # Adjusted font size
        self.popup_label.lift()
        move_label()    
    def create_popup_frame(self, master):
    # Create the casher frame
      self.casher_frame = Frame(master, bg='#ecf0f1', padx=10, pady=10)
      self.casher_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
      self.casher_frame.lower()  # Hide initially

    # Create the casher label
      self.casher_label = Label(self.casher_frame, font=('arial', 20, 'bold'), bg='#ecf0f1')
      self.casher_label.pack(pady=10)

    # Create the close button
 

    # Number buttons configuration
      num_buttons = 70
      rows = 10
      cols = 7

    # Create a frame to hold the number buttons
      button_frame = Frame(self.casher_frame, bg='yellow')
      button_frame.pack(pady=10)

    # Place buttons using grid
    
    
      for i in range(num_buttons):
          button_text = str(i + 1)
          row_num = i // cols
          col_num = i % cols
          Button(button_frame, text=button_text, width=5,command=self.counter).grid(row=row_num,column=col_num, padx=5, pady=5)
      self.casher_close_button = Button(self.casher_frame, text="ጨዋታውን ጀምር",command=self.close, font=('arial', 15, 'bold'))
      self.casher_close_button.pack(pady=10)
      

    def update_casher_info(self, last_tile):
        if last_tile:
            self.casher_label.config(text='መጫዎቻ ካርድ ምዝገባ')
        else:
            self.casher_label.config(text='No numbers drawn yet')
        self.casher_frame.lift()  # Show the casher frame

          # Hide the casher frame


    def reset_tiles(self):
        for tile in self.tile_list:
            tile['bg'] = '#ecf0f1'
            tile['fg'] = 'black'
        self.last_tile = None

    def reset_game(self):
        self.reset_tiles()

    def number_gen(self):
        nap(1)
        for i in self.start_playing_gui():
            if self.need_to_stop:
                break
            self.update_tiles(i)
            play(f'sounds/{i}.mp3')
            nap(self.napTime)

    @classmethod
    def tam(cls):
        root = Tk()
        clas = cls(root)
        Thread(target=clas.clock, daemon=True).start()
        root.mainloop()

if __name__ == '__main__':
    BINGO_gui.tam()
