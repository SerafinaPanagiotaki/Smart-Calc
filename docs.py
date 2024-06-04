from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import webbrowser

#λίστα με τις φωτογραφίες του προγ/τος
photo = ['docs_ico.ico', 'greek_flag.png', 'uk_flag.png']

#λεξικό με τα μηνύματα σφαλμάτων (ανάλογα με τη γλώσσα επιλογής από τον χρήστη)
errors = {
            'gr': ['Σφάλμα:', 'Δε βρέθηκε το αρχείο τεκμηρίωσης.'] ,
            'uk': ['Error:', 'Documentation file not found.']
            }            
          
def open_documentation(lang):
    '''
        Διαδικασία που ανοίγει (url) σε μορφή ιστοσελίδας το documentation της εφαρμογής.
    '''
    #print(open_documentation.__doc__)

    #άνοιγμα σε νέα καρτέλα του browser (new = 2). Άλλες διαθέσιμες επιλογές:
    # - άνοιγμα στον ίδιο (ανοιχτό) browser: new = 0
    # - άνοιγμα σε νέο browser: new = 1

    #match case
    match(lang):
        #ο έλεγχος ύπαρξης του αρχείου τεκμηρίωσης γίνεται με if... else αντί για try... except,
        #διότι με try... excpet ΑΝΟΙΓΕΙ καρτέλα στον φυλλομετρητή και εμφανίζει εκεί σφάλμα, ενώ
        #εμείς θέλουμε να εμφανιστεί στην οθόνη φιλικό μήνυμα προς τον χρήστη και ΝΑ ΜΗΝ ΑΝΟΙΞΕΙ
        #το URL αν δε βρεθεί το αρχείο τεκμηρίωσης
        case 'gr':
            if os.path.isfile("documentation_gr.html"): webbrowser.open("documentation_gr.html", new = 2, autoraise = True)
            #FileNotFoundError
            else: messagebox.showerror(errors['gr'][0], errors['gr'][1])
        case 'uk':
            if os.path.isfile("documentation_uk.html"): webbrowser.open("documentation_uk.html", new = 2, autoraise = True)
            #FileNotFoundError
            else: messagebox.showerror(errors['uk'][0], errors['uk'][1])

def place_buttons():
    '''
        Συνάρτηση που τοποθετεί στο παράθυρο (εμφανίζει)
        τα κουμπιά τυης εφαρμογής.
    '''
    #print(place_buttons.__doc__)
    
    global greek_btn
    global greek_img
    greek_btn.grid(row = 15, column = 4, padx = 10, pady = 10)

    global uk_btn
    global uk_img
    uk_btn.grid(row = 15, column = 5, padx = 30, pady = 10)

def terminate(event):
    '''
        Συνάρτηση που καταστρέφει το παράθυρο της εφαρμογής και την κλείνει.
    '''
    #print(termninate.__doc__)
    
    start_window.destroy()

def main():
    '''
        Κύρια συνάρτηση.
    '''
    #print(main.__doc__)
    
    #εικονίδιο (πάνω αριστερά)    
    start_window.iconbitmap(str(photo[0]))

    #εικονίδιο ελληνικής σημαίας
    global greek_btn
    global greek_img
    greek_img = ImageTk.PhotoImage(Image.open(str(photo[1])))
    greek_btn = Button(start_window, image = greek_img, relief = RAISED, cursor = 'hand2', command = lambda: open_documentation('gr')) 
    
    #εικονίδιο αγγλικής σημαίας
    global uk_btn
    global uk_img
    uk_img = ImageTk.PhotoImage(Image.open(str(photo[2])))
    uk_btn = Button(start_window, image = uk_img, relief = RAISED, cursor = 'hand2', command = lambda: open_documentation('uk'))     
    
    #τίτλος
    start_window.title('Smart Calc - Documentation')    
    start_window.geometry('400x200+500+400')    

    user_choice1 = Label(start_window, text = "Τεκμηρίωση προγράμματος (Documentation)", font = ('Helvetica', 11, 'bold'), fg = "#4f0099", padx = 40)
    user_choice1.grid(row = 5, column = 0, columnspan = 10, sticky = N + S + E + W, pady = 5)
    user_choice2 = Label(start_window, text = "Επιλογή γλώσσας (Select language):", font = ('Helvetica', 8, 'bold'), justify = CENTER, fg = "#4f0099", padx = 55)
    user_choice2.grid(row = 10, column = 0, columnspan = 10, sticky = N + S + E + W, pady = 10)

    place_buttons()

    #κλείσιμο της εφαρμογής με <Esc>
    start_window.bind("<Escape>", terminate)
    
    start_window.mainloop()
    
#δημιουργία αρχικού παράθυρου για το πρόγραμμα
start_window = Tk()
main()
