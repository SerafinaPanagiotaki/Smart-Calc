from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import time
import datetime
import locale
from pygame import mixer
import speech_recognition
import pyaudio
import math
import sys


#δηλώσεις μεταβλητών
#προεπιλεγμένη γλώσσα: Ελληνικά (στην πρώτη γραμμή) και στην ώρα (δεύτερη γραμμή)
lang = 'gr'
locale.setlocale(locale.LC_ALL, "en_GB.utf8")
#locale.setlocale(locale.LC_ALL, "el_GR.utf8")

#τρέχουσα κατάσταση του calculator (προεπιλογή: on)
#global power
power = 'on'

#καθολική μεταβλητή (χρώμα background)
bg_color = "#e1e1ea"

#λίστα με τις φωτογραφίες του προγ/τος
photo = ['calc.ico', 'eap_logo2.png', 'smartcalc.jpg', 'serafina.jpg', 'xenakis.jpg', 'microphone.png', 'greek_flag.png', 'uk_flag.png', 'sound_on.jpg', 'sound_off.jpg']

#λίστα με τα Frames που εναλλάσσονται    
frames_list = ['MainFrame',  'AboutFrame', 'CalcFrame', 'InfoFrame']

#λίστα με τα ονόματα του κουμπιών του calculator (οι κενές τιμές τοποθετήθηκαν
#εσκεμμένα, για να πάρουν πάρουν index - στη θέση τους θα βάλω εικονίδιο στα κουμπιά -)
#global buttons_names_list
buttons_names_list = ['ON/OFF', 'sinθ', 'cosθ', 'tanθ', u'\u221A', 'MR', 'MC', 'M+', 'CE', u'\u00F7',
                      'Themes', 'asinθ', 'acosθ', 'atanθ', u'\u207F'+u'\u221A', '1', '2', '3', 'C', u'\u00D7',
                      'log' + u'\u2081' + u'\u2080', 'sinh', 'cosh', 'tanh', 'x'+u'\u00B2', '4', '5', '6', '=', '-',
                      'ln', 'asinh', 'acosh', 'atanh', 'x'+ u'\u207F', '7', '8', '9', '0', '+',
                      'e', 'deg', u'\u33AD', u'\u03C0', 'n!', '1'+u'\u00F7'+'x', u'\u2213', '.', '(', ')']    #Degrees: u'\u00B0'                                          

#λίστα με τα διαθέσιμα themes για τον calculator
theme_list = ['default', 'light', 'dark']

#τρέχον theme (προεπιλογή: default)
theme = theme_list[0]

#λίστα με τους διαθέσιμους ήχους
sounds = ["[Non Copyrighted Music] Carl Storm - With You In The Morning [Pop].mp3", "beep.mp3"]

#λεξικό με τις χρωματικές αποχρώσεις του calculator
colors = {'default': [["#f3e6ff", "#4f0099", "#a94dff"], ["#ffffff", "#000000"]],          
          'light': [["#ffddcc", "#ff661a", "#ffaa80"], ["#ffffff", "#000000"]],
          'dark':[["#e0e0eb", "#5a5a8c", "#a2a2c3"], ["#ffffff", "#000000"]]
        }

#λεξικό με την αντιστοίχιση θέσεων των πλήκτρων και τιμών τους για το calculator
numbers_dict = {'15': 1, '16': 2, '17': 3, '25': 4, '26': 5, '27': 6, '35': 7, '36': 8, '37': 9, '38': 0}

#μεταβλητή για τον ήχο έναρξης
intro_music = False

#βοηθητική μεταβλητή για να παίξει intro sound μόνο κατά την έναρξη (μετά έλεγχος από χρήστη)
start = True

#καθολική (βοηθητική) μεταβλητή που χρησιμοποιείται για έλεγχο
#global section
section = None

#καθολική μεταβλητή που χρησιμοποιείται για τον υπολογισμό του συνολικού αποτελέσματος (MR)
#global total_memory
total_memory = ''

#καθολική μεταβλητή ποτ δηλώνει αν οι υπολογισμοί κρατούνται - ή όχι - στην μνήμη
#global memory_on
#default τιμή: μη ενεργή
memory_on = False

#καθολικές μεταβλητές που χρησιμοποιούνται για τον έλεγχο των παρενθέσεων
left_parenthesis = 0

right_parenthesis = 0

#βοηθητική μεταβλητή που χρησιμοποιείται για τον υπολογισμό της n-οστής ρίζα
global n_root
n_root = False

#καθολική μεταβλητή που χρησιμοποιείται για την αναζήτηση τελεστών (αμυντικός προγ/μός)
operator = None

#dictionary που περιλαμβάνει τα μηνύματα προς τον χρήστη
#global messages_dict
messages_dict = {'gr':['Τίτλος Project: Ανάπτυξη scientific calculator με τη βιβλιοθήκη tkinter','''

Το scientific calculator είναι μια αριθμομηχανή που εκτός από τις βασικές πράξεις (πρόσθεση, αφαίρεση, πολλαπλασιασμός, διαίρεση) εκτελεί και μερικές
πιο προχωρημένες μαθηματικές πράξεις, όπως: τετραγωνική ρίζα, ύψωση σε δύναμη, τριγωνομετρικές πράξεις, λογάριθμοι, παραγοντικό, σταθερές (π, e), κλπ.

Το Smart Calc μπορεί να υπολογίζει:
1. Τις 4 βασικές πράξεις (+, -, x, /) για ακέραιους και πραγματικούς αριθμούς 
2. Τετραγωνική ρίζα και νιοστή ρίζα αριθμού
3. Ύψωση σε δύναμη n√
4. Δεκαδικό και φυσικό λογάριθμο
5. Παραγοντικό 
6. Ημίτονο, συνημίτονο, εφαπτομένη, τόξο ημιτόνου, τόξο συνημιτόνου, τόξο εφαπτομένης
7. Υπερβολικό ημίτονο, υπερβολικό συνημίτονο, υπερβολική εφαπτομένη, υπερβολικό τόξο ημιτόνου, υπερβολικό τόξο συνημιτόνου, υπερβολικό τόξο εφαπτομένης
8. Υολογισμός σε μοίρες ή ακτίνια
9. Σταθερές π και e
10. Αλλαγή προσήμου +/- 
11. Αντίστροφο 1/x

Διαθέτει πλήκτρα καθαρισμού (C, AC) και πλήκτρα μνήμης (MC, MR, M+), ενώ με <Esc> μπορείτε να τερματίσετε την εφαρμογή.

Το Smart Calc διαθέτει επίσης δυνατότητα εκτέλεσης πράξεων με φωνητική αναγνώριση.''',
'''[ΠΛΗΠΡΟ - ΗΛΕ52] 2023 - 2024, Ομάδα_5_Project

Τίτλος Project: Ανάπτυξη scientific calculator με τη βιβλιοθήκη tkinter
ID Project: 46

Για την υλοποίηση του Project χρησιμοποιήθηκε:
- Python v.3.12.2

Φοιτήτρια: Σεραφίνα Παναγιωτάκη
Σύμβουλος Καθηγητής/Επιβλέπων: Απόστολος Ξενάκης
''', 'Προειδοποίηση:', 'Δεν ανιχνεύθηκε συσκευή εισόδου ήχου.',
("Τερματισμός προγράμματος", "Θέλετε σίγουρα να τερματίσετε το πρόγραμμα;"),
("Επιβεβαίωση τερματισμού", "Ευχαριστούμε που χρησιμοποιήσατε το Smart Calc!\n\n [ΠΛΗΠΡΟ - ΗΛΕ52] 2023 - 2024\nΟμάδα_5_Project\n\nΠιέστε ΟΚ για τερματισμό.")],
                    
                'uk': ['Project Title: Scientific calculator build with tkinter library', '''

Scientific calculator is a calculating device which, besides basic operations (addition, abstraction, multiplication, division) it also performs some
more advanced mathematical operations, such as: square root, exponents, trigonometrical calculations, logarithms, factorial, constants (π, e), etc.

Smart calc can calculate:
1. The four basic mathematical operations (+, -, x, /) for integer and float numbers
2. Numbers square and nth root
3. Rise to n exponent
4. Decimal and physical logarithm
5. Factorial
6. Sin, cos, tan, arc sin, arc cos, arc tan
7. Hyperbolic sin, cos, tan, arc sin, arc cos, arc tan
8. Conversion to degrees or radians
9. Constants π and e
10. Sign inversion +/- 
11. Number reverse 1/x

It has clear buttons (C, AC) and memory buttons (MC, MR, M+) and with the <Esc> button the program terminates.

Smart calc also can perform operations with voice call assistance.''',
'''[ΠΛΗΠΡΟ - ΗΛΕ52] 2023 - 2024, Team_5_Project

Project Title: Scientific calculator build with tkinter library
ID Project: 46

This application is powered by:
- Python v.3.12.2

Student: Serafina Panagiotaki
Professor/Assistance coach and Supervisor: Apostolos Xenakis
''', 'Warning:', 'No input device was detected.',
("Exit program", "Are you sure that you want to exit program?"),
("Exit confirmation", "Thank you for using Smart Calc!\n\n[ΠΛΗΠΡΟ - ΗΛΕ52] 2023 - 2024\nTeam_5_Project\n\nPress OK to exit.")]                      
                }

#Συναρτήσεις
def terminate(event):
    '''
        Συνάρτηση που τερματίζει το πρόγραμμα.
        Ρωτάει πρώτα τον χρήστη αν επιμένει στον τερματισμό,
        και αν λάβει θετική απάντηση κλεινει το παράθυρο
        τερματίζοντας το πρόγραμμα.

        Ενεργοποιείται με το πλήκτρο <Esc>.
    '''
    #print(terminate.__doc__)
    verification = messagebox.askquestion(messages_dict[str(lang)][5][0], messages_dict[str(lang)][5][1])        
    if verification == 'yes':
        messagebox.showinfo(messages_dict[str(lang)][6][0], messages_dict[str(lang)][6][1])        
        start_window.destroy()

def change_locale():
    '''αλλαγή της γλώσσας κειμένου ανάλογα με την επιλογή του χρήστη'''
    #print(change_locale.__doc__())
    
    #match case
    match (lang):
        case 'uk':
            locale.setlocale(locale.LC_ALL, "en_GB.utf8")
        case 'gr':
            locale.setlocale(locale.LC_ALL, "el_GR.utf8")        

def change_language(var):
    ''' Συνάρτηση που αλλάζει τη γλώσσα των μηνυμάτων προς τον χρήστη, ανάλογα με την επιλογή του.
Διαθέσιμες γλώσσες σε αυτή την έκδοση: 1. Ελληνικά 2. Αγγλικά'''
    #print change_language.__doc__()
    
    global lang
    lang = var

    #χειροκίνητη αλλαγή της γλώσσας κειμένου μόνο για την αρχική σελίδα
    change_locale()
    #αμυντικός προγ/μός (για να μην "χτυπήσει σφάλμα" στην περίπτωση που
    #αλλάξει ο χρήστης τη γλώσσα (μόνο ένα από τα Frames είναι ενεργό κάθε
    #φορα, για τα υπόλοιπα το πρόγραμμα κάνει exception χωρίς το try...except)
    try:
        global introLabel1
        introLabel1.config(text = messages_dict[str(lang)][0])
        global about_label
        about_label.config(text = messages_dict[str(lang)][1])
        global info_label
        info_label .config(text = messages_dict[str(lang)][2])        
    except: pass        

def addition(a, b):
    '''
        Συνάρτηση πρόσθεσης για τη φωνητική κλήση.
    '''
    #print(addition.__doc__)
    return a + b

def abstruct(a, b):
    '''
        Συνάρτηση αφαίρεσης για τη φωνητική κλήση.
    '''
    #print(addition.__doc__)
    return a - b

def multiply(a, b):
    '''
        Συνάρτηση πολλαπλασιασμού για τη φωνητική κλήση.
    '''
    #print(addition.__doc__)
    return a * b

def division(a, b):
    '''
        Συνάρτηση πρόσθεσης για τη φωνητική κλήση.
    '''
    #print(addition.__doc__)
    #αμυντικός προγ/μός
    if b == 0: return 'Error'
    else: return a / b

#λεξικό με τις λέξεις - κλειδιά που αποθηκεύονται για τη φωνητική αναγνώριση
words_dict = {'ΠΡΟΣΘΕΣΗ':addition, 'ΠΡΟΣΘΕΣΕ':addition, 'ΣΥΝ':addition, 'ΚΑΙ':addition,
              'ΑΦΑΙΡΕΣΗ':abstruct, 'ΑΦΑΙΡΕΣΕ':abstruct, 'ΠΛΗΝ':abstruct, 'ΜΕΙΟΝ':abstruct,
              'ΠΟΛΛΑΠΛΑΣΙΑΜΟΣ': multiply, 'ΠΟΛΛΑΠΛΑΣΙΑΣΕ': multiply, 'ΕΠΙ': multiply, 'ΦΟΡΕΣ': multiply,
              'ΔΙΑΡΕΣΗ': division, 'ΔΙΑΡΕΣΕ': division, 'ΔΙΑ': division,
              'ADD':addition, 'ADDITION':addition, 'PLUS':addition, 
              'ABSTRUCT':abstruct, 'REMOVE':abstruct, 'MINUS':abstruct, 
              'MULTIPLY': multiply, 'TIMES': multiply, 'MULTIPLICATION': multiply,
              'DIVIDE': division, 'DIVISION': division, 'BY': division, 
            }

def find_numbers(list_):
    #αρχικοποιηση λίστας
    numbers_list = []

    #εντοπισμός των αριθμών στη λίστα κειμένου και καταχώρησή τους
    #στην νέα λίστα (αριθμών) - χρήση αμυντικού προγ/μού
    for number in list_:
        try: numbers_list.append(float(number))
        except ValueError: pass
    return numbers_list
        

def voice_call():
    '''
        Συνάρτηση που εκτελεί πράξεις με φωνητικές εντολές.
    '''
    #print(voice_call.__doc__)
    #ήχος ('beep.mp3') που ακούγεται στο πάτημα κουμπιού του μικροφώνου
    mixer.music.load(sounds[1])
    mixer.music.play()

    #δημιουργία αντικειμένου της κλάσης Recognizer
    listener = speech_recognition.Recognizer()

    try:    
        #δημιουργία αντικειμένου της κλάσης Microphone
        with speech_recognition.Microphone() as mic:
            try:        
                #... αν υπάρξει κενό (παύση) μεγαλύτερη από 0.2 secs, ο listener
                #θα το αναγνωρίσει ως επόμενη φράση
                listener.adjust_for_ambient_noise(mic, duration = 0.2)

                #μεταβλητή στην οποία αποθηκεύουμε τη φωνή
                voice = listener.listen(mic)

                #μετατροπή σε κείμενο
                text_from_voice = listener.recognize_google(voice)

                #####################
                # TESTING.......... #
                #####################
                print(text_from_voice)

                #ήχος ('beep.mp3') που ακούγεται μετά την ολοκλήρωση της φράσης του χρήστη
                mixer.music.load(sounds[1])
                mixer.music.play()

                #διαχωρισμός των λέξεων του κειμένου και τοποθέτησή τους σε λίστα
                text_list = text_from_voice.split(' ')

                #εντοπισμός των λέξεων κλειδιών που υποδηλώνουν πράξη (ή τελεστή)
                for word in text_list:
                    #εντοπισμός των τελεστέων και καταχώρισή τους σε λίστα
                    if word.upper() in words_dict.keys():
                        numbers_list = find_numbers(text_list)
                        print(numbers_list)

                        global digit
                        digit = words_dict[word.upper()](numbers_list[0], numbers_list[1])
                        show_to_screen(digit)
                    #αμυντικός προγ/μός ('οριακή' περίπτωση κατά την οποία ο χρήστης δεν
                    #έδωσε τελεστή ή το πρόγραμμα δεν τον αναγνώρισε μέσω της φωνής του χρήστη)
                    else: pass
            #περιπτώσεις όπου ο listener δεν αναγνωρίζει τη φωνή (και θα προέκυπτε σφάλμα)
            except:
                print("Coudn't hear you")
                #####pass 

    #περίπτωση να μην αναγνωρίσει το μικρόφωνο(φιλικό μήνυμα προς τον χρήστη)
    except OSError:
        messagebox.showwarning(messages_dict[str(lang)][3], messages_dict[str(lang)][4])      

def change(frame_name):
    '''
        Συνάρτηση που εναλλάσσει Frames (ορίζονται από την καθολική μεταβλητή section).
        Εκτελεί τις εξής ενέργειες:

        1. Eξετάζει ποιο Frame είναι ενεργό
        2. Το καταργεί και κάνει ενεργό το Frame που έλαβε ως όρισμα.
    '''
    #print(change.__doc__)

    #αν ο χρήστης δεν επέλεξε την τρέχουσα επιλογή... (αμυντικός προγ/μός)    
    if section != frame_name:
        #...match case (έλεγχος ποιο Frame είναι ενεργό και κατάργησή του)
        match(section):
            case 'MainFrame':
                global MainFrame
                MainFrame.grid_remove()
            case 'AboutFrame':
                global AboutFrame
                AboutFrame.grid_remove()
            case 'CalcFrame':
                global CalcFramemake
                CalcFrame.grid_remove()
            case 'InfoFrame':
                global InfoFrame
                InfoFrame.grid_remove()
        #...match case (έλεγχος ποια υποσελίδα επιλέγει ο χρήστης και
        #ενεργοποίηση του αντίστοιχου Frame)
        match(frame_name):
            case 'MainFrame':
                main()
            case 'AboutFrame':
                make_about_frame()
            case 'CalcFrame':
                make_calc_frame()
            case 'InfoFrame':
                make_info_frame()
                
def delay_time():
    '''Συνάρτηση που "κάνει όλη τη δουλειά" για την επόμενη (display_time), μόνο που κάνει τη διαδικασία μία φορά. Ουσιαστικά "σπάσαμε" τη διαδικασία σε μία μοναδιαία
και ένα ατέρμονα βρόχο που την εκτελεί, διότι πιο κάτω στον κώδικα θέλουμε να τρέξει πεπερασμένες φορές.'''
    #print(delay_time.__doc__())

    #χρονοκαθυστέρηση ("πάγωμα") ενός δευτερολέπτου
    time.sleep(1)

    #τρέχουσα ώρα 
    current_time = datetime.datetime.now()

    #μορφοποίηση ώρας
    display_new_time = f"{current_time: %A, %d %B %Y - %H:%M:%S}"

    #αλλαγή της ώρας μέσα στο ρολόι
    clock.config(text = display_new_time)

    #ανανέωση του αρχικού παραθύρου (για να εφαρμοστεί η αλλαγή)
    start_window.update()
    

def display_time():
    '''Συνάρτηση που προβάλλει καθόλη τη διάρκεια του προγράμματος την τρέχουσα ημερομηνία και ώρα. Είναι απαραίτητο να υλοοποιηθεί πρώτη από όλες τις συναρτήσεις, καθώς όσες
από τις υπόλοιπες περιέχουν εναλλαγές Frames η χρονοκαθυστέρηση πρέπει να την καλέσουν (αν δεν υλοποιηθεί πρώτη από όλες και κάποια συνάρτηση που προηγείται στον κώδικα συμβεί
να την καλέσει, τότε θα παραχθεί σφάλμα'''
    #print(dispay_time.__doc__())
    
    #τρέχουσα ώρα
    current_time = datetime.datetime.now()
    
    #μορφοποιηση της ώρας προτού εμφανιστεί στην οθόνη
    display_new_time = f"{current_time:%A, %d %B %Y - %H:%M:%S}"

    #δημιουργία του ψηφιακού ρολογιού στην οθόνη
    global clock
    clock = Label(start_window, text = display_new_time, font = ('Helventica', 8, 'bold'), fg = '#000000', bg = bg_color, width = 35, anchor = 'e')
    clock.grid(row = 0, column = 17, columnspan = 3, sticky = W + E, padx = 20)

    #αλλαγή της ώρας ανά δευτερόλεπτο
    while True:
        delay_time()

def turn_on_off():
    '''
        Συνάρτηση που αναβοσβήνει τον calculator.

        Προεπιλογή: on.
    '''
    #print(turn_on_off.__doc__)
    global power
    global screen
    if power == 'on':
        screen.delete(0, END)
        power = 'off'
        make_calc_frame()        
        screen.config(state = DISABLED)                
    else:        
        screen.config(state = NORMAL)
        power = 'on'
        make_calc_frame()
    
def change_theme():
    '''
        Συνάρτηση που αλλάζει τα χρώματα του calculator.

        Οι εναλλαγές γίνονται κυκλικά (default - light - dark).
        Προεπιλογή: default.
    '''
    #print(change_theme.__doc__)
    global theme
    for i in range(len(theme_list)):        
        if theme == theme_list[i]:
            if theme != theme_list[-1]:
                theme = theme_list[i + 1]            
                break
            else: theme = theme_list[0]
    user_input = screen.get()
    make_calc_frame()
    screen.insert(0, user_input)

def add_digit(digit):
    '''
        Συνάρτηση που προσθέτει ψηφία στην οθόνη του calculator.

        Παίρνει ως όρισμα την είσοδο του χρήστη (από το πληκτρολόγιο
        ή το ποντίκι), ελέγχει το πλήθος των χαρακτήρων και, εφόσον
        πληροί τις προϋποθέσεις, τοποθετεί το ψηφίο στα δεξιά της οθόνης.
    '''
    #print(add_digit.__doc__)    
    global user_input
    #έλεγχος αν το μηδέν είναι πρώτο ψηφίο και ΔΕΝ ακολούθησε υποδιαστολή
    if user_input != '0':
        #σε περίπτωση πράξεων με μνήμης, αφαιρούμε το 'Μ' για να ξαναβάλει ο χρήστης αριθμούς
        if u'\u1D39' in user_input: user_input = user_input[1:]
        digit = user_input + str(digit)        
        show_to_screen(digit)    

def dot():
    '''
        Συνάρτηση που ελέγχει αν μπορεί να τοποθετηθεί υποδιαστολή και,
        εφόσον πληροί τις προϋποθέσεις, την προσθέτει.
    '''
    #print(dot.__doc__)
    
    global allow_dot
    allow_dot = False
    user_input = screen.get()
    #έλεγχος αν υπάρχει υποδιαστολή νωρίτερα...
    previous_dot = user_input.rfind('.')
    if previous_dot == -1: allow_dot = True
    else:
        #... αν δεν υπάρχει τελεστής μετά την τελευταία υποδιαστολή
        #δεν μπορεί να χρησιμοποιηθεί ξανά η υποδιαστολή
        #Ο ΕΛΕΓΧΟΣ ΓΙΝΕΤΑΙ ΜΕ ΑΝΑΠΟΔΗ ΦΟΡΑ
        check_characters = user_input[previous_dot:]
        print('check_characters[::-1]:', check_characters[::-1])
        for character in check_characters[::-1]:
            if character in ['+', '-', '*', '/', '**']:
                allow_dot = True
                break
    #εμφάνιση υποδιαστολής   
    if allow_dot:
        clear_all()
        user_input += '.'
        screen.insert(0, user_input)

def clear_all():
    '''
        Συνάρτηση που καθαρίζει την οθόνη του calculator.
    '''
    #print(clear_all.__doc__)
    screen.delete(0, END)

def clear_last():
    '''
        Συνάρτηση που διαγράφει το τελευταίο χαρακτήρα που εισήγαγε ο χρήστης.
    '''
    #print(clear_last.__doc__)
    user_input = screen.get()
    clear_all()
    screen.insert(0, user_input[:-1])
    
def show_to_screen(result):
    '''
        Συνάρτηση που εμφανίζει το αποτέλεσμα.
    '''
    #print(show_to_screen.__doc__)
    #καθάρισμα οθόνης
    clear_all()
        
    #προβολή αποτελέσματος
    if len(str(result)) >= 20: result = '%e'%float(result)
    screen.insert(0, result)




        
    
def reverse_operator():
    '''
        Συνάρτηση που αντιστρέφει το πρόσημο.

        Λειτουργει και μέσα σε παραστάσεις (πχ παρενθέσεις, δυνάμεις κλπ) και
        αντιστρέφει το τελευταίο πρόσημο (ή προσθέτει, αν αυτό έχει παραλειφθεί).
    '''
    #print(reverse_operator.__doc__)
    global operator
    user_input = screen.get()
    digit = user_input
    #περίπτωση αλλαγής προσήμου σε ολόκληρη παρένθεση
    if digit[-1] == ')':
        #βοηθητική μεταβλητή που μετράει τις "κλειστές" παρενθέσεις
        closed = 1
        #έρευνα αν υπάρχουν και άλλες "κλειστές" παρενθέσεις εντός αυτής
        #...εύρεση της τελευταίας αριστερής παρένθεσης...
        start = digit.rfind('(')

        look_up = digit[start : -1].rfind(')')

        while look_up != -1 and start != -1:
            #...ψάξε και για άλλες αριστερές παρενθέσεις, αριστερότερα
            #από την προηγούμενη
            start = digit[:start].rfind('(')
            look_up = digit[start : look_up].rfind(')')
            
        #...εύρεση προσήμου εκτός της αριστερής παρένθεσης...
        if start > 0: operator = digit[start - 1 : start - 1]
        else: operator = ''        
        #...και αντιστροφή του
        #match case
        match(operator):
            case '-':
                if start > 1: digit = digit[:start - 1] + '+' + digit[start:]
                #αν πρέπει να αντιστρέψουμε το πρόσημο στην αρχή και πρέπει να
                #γίνει '+', τότε το παραλείπουμε
                else: digit = digit[:start - 1] + digit[start:]
            case '+':
                digit = digit[:start - 1] + '-' + digit[start:]
            #η default περίπτωση "πιάνει" και τις περιπτώσεις όπου δεν
            #υπάρχει '+' ή '-' πριν από την αριστερή παρένθεση, πχ '*', '/', '**'
            case _:
                if start > 1: digit = digit[:start] + '-' + digit[start:]
                else: digit = '-' + digit
    #περίπτωση αλλαγής προσήμου στον τελευταίο αριθμό (δεν υπάρχει παρένθεση)...
    else:                
        #...εύρεση του τελευταίου τελεστή ή παρένθεσης (ψάχνουμε από το τέλος)...                
        for i in range(len(digit)-1, -1, -1):
            if digit[i] in ['+', '-', '*', '/', '**']:
                operator = digit[i]                        
                #...και αντιστροφή του
                #match case
                if i>0:
                    match(operator):
                        case '-':
                            digit = digit[:i] + '+' + digit[i + 1:]
                        case '+':
                            digit = digit[:i] + '-' + digit[i + 1:]
                        #η default περίπτωση "πιάνει" και τις περιπτώσεις όπου δεν
                        #υπάρχει + 'η - πριν από την αριστερή παρένθεση, πχ '*', '/', '**'
                        case _:
                            digit = digit[:i + 1] + '-' + digit[i + 1:]
                    show_to_screen(digit)
                    return
        #...περίπτωση να υπάρχει ένας μόνο - θετικός - αριθμός στην οθόνη (αλλαγή προσήμου στην αρχή)...                                
        else:
            #match case
            match(digit[0]):
                case '-':
                    digit = digit[1:]
                case _:
                    digit = '-' + digit                                
    show_to_screen(digit)

def reverse_number():
    '''
        Συνάρτηση που αντιστρέφει την είσοδο του χρήστη (1/x).
    '''
    #print(reverse_number.__doc__)
    try: digit = 1/eval(user_input)
    except ZeroDivisionError: digit = 'Error'
    finally: show_to_screen(digit)

def parenthesis(action):
    '''
        Συνάρτηση που ελέγχει και - εφόσον ικανοποιούνται οι συνθήκες -
        ανοίγει αριστερή παρένθεση.
    '''
    #print(open_parenthesis.__doc__)
    #match case
    match(action):        
        #άνοιγμα παρένθεσης
        case 'open':    
            digit = user_input
            global left_parenthesis
            #αν η αριστερή παρένθεση είναι πρώτος χαρακτήρας ή ακολουθεί
            #τελεστή, τότε ανοίγει
            if len(digit) == 0 or digit[-1] in ['+', '-', '*', '/', '**', '(']:                
                left_parenthesis += 1
                digit += '('
        #κλείσιμο παρένθεσης
        case 'close':
            digit = user_input
            global right_parenthesis
            #αν οι δεξιές παρενθέσεις στην παράσταση είναι λιγότερες από τις αριστερές
            #(δεν εχουν "κλείσει" δηλαδή) και δεν προηγείται τελεστής ή αριστερή παρένθεση,
            #τότε κλείνει
            if left_parenthesis > right_parenthesis and digit[-1] not in ['(', '+', '-', '*', '/', '**']:
                right_parenthesis += 1
                digit += ')'
                #αν έχουν "κλείσει" όλα τα ζευγάρια παρενθέσεων, τότε μηδενίζουμε τους μετρητές
                if left_parenthesis == right_parenthesis:
                    left_parenthesis = 0
                    right_parenthesis = 0            
    show_to_screen(digit)

def add_to_memory(expression):
    '''
        Συνάρτηση που προσθέτει στην μνήμη (Μ+).
    '''
    #print(add_to_memory.__doc__)
    
    global total_memory    
    global memory_on
    memory_on = True
    print('user_input:', user_input)
    digit = eval(user_input)    
    total_memory += '+' + str(digit)
    print('total_memory:', total_memory)
    clear_all()
    screen.insert(END, u'\u1D39')    
    
def what_to_do(number):
    '''
        Συνάρτηση που ελέγχει το πλήκτρο που πατήθηκε στον calculator και ανάλογα καλεί
        την αντίστοιχη συνάρτηση.
    '''
    #print(what_to_do.__doc__)

    #έλεγχος εγκυρότητας της εισόδου του χρήστη
    #είσοδος χρήστη
    global user_input
    user_input = screen.get()

    #αμυντικός προγ/μός (ο χρήστης πληκτρολογήσει υπολογισμό χωρίς είσοδο)
    #εξαιρούνται: σταθερές (π, e), η '(', η υποδιαστολή ο τελεστής '-',
    #το κουμπί ON/OFF, η αλλαγή themes και τα ψηφία (0-9)
    if len(user_input) == 0 and number not in [0, 10, 15, 16, 17, 25, 26, 27, 29, 35, 36, 37, 38, 40, 43, 47, 48]: return
    
    global total_memory
    global digit
    
    #αν έχουμε υπολογισμούς με μνήμη, αφαιρούμε το 'Μ'
##    global memory_on
##    if memory_on == True:
##        user_input = ''
##        clear_all()
    
    #match case (number: index κουμπιών calculator)
    match(number):
        #power on/off
        case 0: turn_on_off()
        #αλλαγή theme (κυκλική εναλλαγή: default - light - dark)
        case 10: change_theme()
        #ημίτονο 
        case 1:
            digit = math.sin(eval(user_input))
            show_to_screen(digit)
        #συνημίτονο 
        case 2:
            digit = math.cos(eval(user_input))
            show_to_screen(digit)
        #εφαπτομένη 
        case 3:
            digit = math.tan(eval(user_input))
            show_to_screen(digit)
        #τετραγωνική ρίζα
        case 4:
            digit = math.sqrt(eval(user_input))
            show_to_screen(digit)
        #MR (συνολικό αποτέλεσμα μνήμης -> user-defined function)
        case 5:
            digit = eval(total_memory)
            clear_all()
            screen.insert(0, str(digit) + ' ' + u'\u1D39')
            #####total_memory = ''            
        #MC (καθαρισμός μνήμης -> user-defined function)
        case 6:            
            total_memory = ''
            clear_all()
            #####show_to_screen(digit)
            memory_on = False            
        #M+ (πρόσθεση στην μνήμη -> user-defined function)
        case 7:
            digit = user_input
            print('@716, user_input:', user_input)
            add_to_memory(digit)
        #καθαρισμός οθόνης
        case 8: clear_all()
        #διαίρεση (user-defined function)
        case 9:
            digit = user_input + '/'
            show_to_screen(digit)
        #τόξο ημιτόνου
        case 11:
            digit = math.asin(eval(user_input))
            show_to_screen(digit)
        #τόξο συνημιτόνου
        case 12:
            digit = math.acos(eval(user_input))
            show_to_screen(digit)
        #τόξο εφαπτομένης
        case 13:
            digit = math.atan(eval(user_input))
            show_to_screen(digit)
        #ν-οστή ρίζα
        case 14:
            digit = user_input + '**1/'
            global n_root
            n_root = True
            show_to_screen(digit)
        #C (διαγραφή τελευταίου ψηφίου -> user-defined function)
        case 18: clear_last()
        #πολλαπλασιασμός (user-defined function))
        case 19:
            digit = user_input + '*'
            show_to_screen(digit)
        #δεκαδικός λογάριθμος
        case 20:
            digit = math.log10(eval(user_input))
            show_to_screen(digit)
        #υπερβολικό ημίτονο
        case 21:
            digit = math.sinh(eval(user_input))
            show_to_screen(digit)
        #υπερβολικό συνημίτονο
        case 22:
            digit = math.cosh(eval(user_input))
            show_to_screen(digit)
        #υπερβολική εφαπτομένη
        case 23:
            digit = math.tanh(eval(user_input))
            show_to_screen(digit)
        #τετράγωνο αριθμού
        case 24:
            digit = eval(user_input + '**2')
            show_to_screen(digit)
        # = (user-defined function))
        case 28:
            if n_root:
                number = user_input.rfind('^')
                #αμυντικός προγ/μός                
                try:
                    digit = eval(str(pow(float(user_input[:number]), 1/int(user_input[number + 3:]))))                                
                except ValueError: digit = 'Error'
                except ZeroDivisionError: digit = 'Error'
                finally: 
                    n_root = False
                    show_to_screen(digit)
            else:
                try:
                    digit = eval(user_input)
                #except ValueError: digit = 'Error'
                except ZeroDivisionError: digit = 'Error'
                finally: show_to_screen(digit)
        # αφαίρεση (user-defined function))
        case 29:
            digit = user_input + '-'
            show_to_screen(digit)
        #λογάριθμος με βάση το 2
        case 30:
            digit = math.log2(eval(user_input))
            show_to_screen(digit)
        #υπερβολικό τόξο ημιτόνου
        case 31:
            digit = math.asinh(eval(user_input))
            show_to_screen(digit)
        #υπερβολικό τόξο συνημιτόνου
        case 32:
            digit = math.acosh(eval(user_input))
            show_to_screen(digit)
        #υπερβολικό τόξο εφαπτομένης
        case 33:
            digit = math.atanh(eval(user_input))
            show_to_screen(digit)
        #ν-οστή δύναμη
        case 34:            
            digit = user_input + '**'
            show_to_screen(digit)
        #πρόσθεση (user-defined function))
        case 39:
            digit = user_input + '+'
            show_to_screen(digit)
        #αριθμός e
        case 40:
            digit = user_input + str(math.e)
            show_to_screen(digit)
        #μετατροπή από ακτίνια σε μοίρες
        case 41:
            digit = math.degrees(eval(user_input))
            show_to_screen(digit)
        #μετατροπή από μοίρες σε ακτίνια
        case 42:
            digit = math.radians(eval(user_input))
            show_to_screen(digit)
        #αριθμός π
        case 43:
            digit = user_input + str(math.pi)
            show_to_screen(digit)
        #παραγοντικό
        case 44:
            digit = math.factorial(eval(user_input))
            show_to_screen(digit)
        # αντιστροφή αριθμου (1 / x)
        case 45: reverse_number()
        #αντιστροφή προσήμου (user-defined function))
        case 46: reverse_operator()
        #υποδιαστολή (user-defined function))
        case 47: dot()
        #αριστερή παρένθεση (user-defined function))
        case 48: parenthesis('open')
        #δεξιά παρένθεση (user-defined function))
        case 49: parenthesis('close')
        # ψηφία 0 - 9 (user-defined function))
        case _:
##            if memory_on: clear_all()
            add_digit(numbers_dict[str(number)])                                   

def make_main_frame():
    '''
        Συνάρτηση που δημιουργεί το περιβάλλον της αρχικής σελίδας.
    '''
    #print(make_main_frame.__doc__)

    #header
    headerTitle = Label(start_window, text = "   Smart Calc", font = ("Helvetica", 40, "bold"), bg = bg_color, fg = "#000000", padx = 165, anchor = 'center')
    headerTitle.grid(row = 0, column = 10, columnspan = 3, sticky =  E + W)
    headerSubTitle = Label(start_window, text = "Scientific Calculator", font = ("Helvetica", 11, "bold"), bg=bg_color, fg = "#000000", padx = 0, anchor = 'center')
    headerSubTitle.grid(row = 1, column = 0, columnspan = 20, sticky =  E + W)

    #χρησιμοποιώ κενά Labels για να με βοηθήσουν στη διαταξη (καλύτερη στοίχιση)
    blank_label1 = Label(start_window, text = "", font = ("Helvetica", 40, "bold"), bg = bg_color, fg = "#000000", padx = 80, anchor = 'center')
    blank_label1.grid(row = 0, column = 1, columnspan = 4, sticky =  E + W, padx = 5)

    global eap_label
    #εικονίδιο ΕΑΠ (πάνω αριστερά)
    eap_label.grid(row = 0, column = 0, padx = 5, sticky = W)

    #buttons κεντρικού μενού
    menuBtnsList = ["Home", "About", "Calculator", "Info"]    
    buttonsFrame = Frame(start_window, bg = bg_color, padx = 0)
    buttonsFrame.grid(row = 2, column = 0, rowspan = 3, columnspan = 20, sticky = E + W)
    blankLabel3 = Label(buttonsFrame, text = "", bg = bg_color, fg = "#000000", padx = 85, anchor = 'center')
    blankLabel3.grid(row = 2, column = 0, columnspan = 2, sticky =  E + W)    
    for i in range(len(menuBtnsList)):
        menuBtn = Button(buttonsFrame, text = menuBtnsList[i], fg = bg_color, bg = "#8787ab", width = 20, pady = 15, font = ('Helvetica', 9, 'bold'), anchor = 'center', command = lambda i = i: change(frames_list[i]))
        menuBtn.grid(row = 4, column = 3 + 4 * i, columnspan = 2, padx = 30)
    
    global introLabel1    
    introLabel1 = Label(buttonsFrame, text = messages_dict[str(lang)][0], font = ('Helvetica', 8, 'bold'), bg = bg_color, fg = "#000000", anchor = 'center', pady = 10)    
    introLabel1.grid(row = 10, column = 0, columnspan = 20, sticky =  E + W)

    #εικονίδιο speaker
    global speaker_on
    global speaker_btn
    if start or intro_music: photo = speaker_on
    else: photo = speaker_off
    speaker_btn = Button(buttonsFrame, image = photo, bg = bg_color, relief = FLAT, activebackground = bg_color, command = play_music) 
    speaker_btn.grid(row = 4, column = 1, sticky = W, padx = 20)
    
    #εικονίδια γλώσσας
    global greek_img
    greek_label = Button(buttonsFrame, image = greek_img, bg = bg_color, relief = FLAT, activebackground = bg_color, command = lambda: change_language('gr')) 
    greek_label.grid(row = 4, column = 18, padx =25)
    global uk_img
    uk_label = Button(buttonsFrame, image = uk_img, bg = bg_color, relief = FLAT, activebackground = bg_color, command = lambda: change_language('uk') )
    uk_label.grid(row = 4, column = 19)
    
    #εικόνα κεντρικής οθόνης
    calc_label.grid(row = 20, column = 5)

    #ενημέρωση καθολικής μεταβλητής section
    global section
    section = "MainFrame"

def make_calc_frame():
    '''
        Συνάρτηση που δημιουργει το περιβάλλον του scientific calculator.
    '''
    #print(make_calc_frame.__doc__)
    
    global section
    section = "CalcFrame"
    global CalcFrame    
    CalcFrame.grid(row = 5, column = 0, columnspan = 20, sticky =  N + S + E + W)

    #δημιουργία "κενών" Frames για καλύτερη στοίχιση
    blankFrame = Frame(CalcFrame, bg = bg_color)
    blankFrame.grid(row = 7, column = 5, rowspan = 10, pady = 0, padx = 128)
    
    global calculator
    #αναγκαίο να γίνει εκ νέου config (ΔΕΝ αλλάζει κάτι στην σύνταξη) ώστε να πάρει
    #το περίγραμμα του calculator τη νέα απόχρωση σε περίπτωση αλλαγής theme
    calculator.config(bg = colors[theme][0][1])
    calculator.grid(row = 7, column = 6, rowspan = 10, columnspan = 12, pady = 0)
    
    #εικονίδο ΕΑΠ
    eap_label_calc.grid(row = 7, column = 6, padx = 5, sticky = W + N)
    eap_label_calc.config(bg = colors[theme][0][1])

    #κουμπί μικροφώνου    
    microphone.grid(row = 7, column = 17, padx = 5, sticky = E + N)
    microphone.config(bg = colors[theme][0][1])
    microphone.config(activebackground = colors[theme][0][1])

    #τίτλος calculator
    calc_title = Label (CalcFrame, text = "Smart Calc", fg = "#ffffff", font = ("Helvetica", 15, "bold"), bg = colors[theme][0][1], pady = 5)
    calc_title.grid(row = 7, column = 6, columnspan = 12, pady = 0, sticky = N)

    #δημιουργία οθόνης calculator
    global screen
    screen = Entry(calculator, width = 77, relief = SUNKEN, bd = 5, bg = "#ffffff", fg = "#ff0000", font = ("Helvetica", 10), justify = RIGHT)
    screen.grid(row = 8, column = 6, rowspan = 4, columnspan = 10, pady = 10)
    
    #δημιουργία κουμπιών calculator
    next_line = 0
    next_column = 0

    #προεπιλογή: ENABLED
    status = 'ENABLED'
    #επιλογή χρωμάτων (foreground, background0
    for i in range(len(buttons_names_list)):
        
        #όλα τα υπόλοιπα πλήκτρα
        if i not in [5, 6, 7, 8, 15, 16, 17, 18, 25, 26, 27, 28, 35, 36, 37, 38]:
            bg_selected = colors[theme][0][2]
            fg_selected = colors[theme][1][0]
            
        #πλήκτρα καθαρισμού, μνήμης και ισότητας
        elif i in [5, 6, 7, 8, 18, 28]:
            bg_selected = colors[theme][0][1]
            fg_selected = colors[theme][1][0]
            
        #αριθμοί (0-9)
        else:
            bg_selected = colors[theme][0][0]
            fg_selected = colors[theme][1][1]                        

        global calc_btn        
        calc_btn = Button(calculator, text = buttons_names_list[i], bg = bg_selected, fg = fg_selected, width = 6, padx = 0, pady = 10, command = lambda i = i : what_to_do(i))

        #δυνατότητας πληκτρολόγησης και πατήματος ποντικιού
        if i in [15, 16, 17, 25, 26, 27, 35, 36, 37, 38]:            
            calc_btn.bind(str(numbers_dict[str(i)]), lambda i = i: what_to_do(i))
            
        #αλλαγή γραμμής κάθε 10 πλήκτρα (διαταξη: 5x10)
        if i%10 == 0:
            next_column = 0
            next_line += 1
        calc_btn.grid(row = 15 + next_line, column = 6 + next_column, pady = 4, padx = 3)
        next_column += 1
        #ενεργοποίηση/απενεργοποίηση πλήκτρων αριθμομηχανής
        if power == 'off' and i != 0: calc_btn.config(state = 'disabled')
        else: calc_btn.config(state = 'normal')

def make_about_frame():
    '''
        Διαδικασία (οδηγίες σχετικά με τη χρήση του scientific calculator).
    '''
    #print(make_about_frame.__doc__)

    global AboutFrame
    global section
    global about_label
    section = "AboutFrame"
    AboutFrame = Frame(start_window, bg = bg_color, highlightthickness = 0)
    AboutFrame.grid(row = 5, column = 0, columnspan = 20, sticky =  N + S + E + W)
    blank_label = Label(AboutFrame, text = "", fg = "#000000", padx = 70, bg = bg_color)
    blank_label.grid(row = 10, column = 0)
    about_label = Label(AboutFrame, text = str(messages_dict[str(lang)][1]), fg = "#000000", bg = bg_color, width = 130, justify = LEFT)
    about_label.grid(row = 10, column = 5, columnspan = 10, sticky = E + W)
    

        
    
def make_info_frame():
    '''
        Διαδικασία (οδηγίες σχετικά με την υλοποίηση του scientific calculator).
    '''
    #print(make_info_frame.__doc__)
    
    global section
    global InfroFrame
    global info_label
    section = "InfoFrame"    
    InfoFrame.grid(row = 10, column = 0, columnspan = 20, sticky =  N + S + E + W)
    blank2_label = Label(InfoFrame, text = "", fg = "#000000", padx = 200, bg = bg_color)
    blank2_label.grid(row = 11, column = 0, pady = 0)
    info_label = Label(InfoFrame, text = str(messages_dict[str(lang)][2]), fg = "#000000", bg = bg_color, justify = LEFT)
    info_label.grid(row = 12, column = 5, columnspan = 10)

    #φωτογραφία δική μου
    serafina_label.grid(row = 20, column = 5, padx = 50, pady = 10)

    #φωτογραφία Καθηγητή
    xenakis_label.grid(row = 20, column = 6, padx = 50, pady = 10)

def play_music():
    '''
        Συνάρτηση που ενεργοποιεί ήχο με την έναρξη της εφαρμογής και τον διαχειρίζεται
        στην συνέχεια με επιλογή του χρήστη.
    '''
    #print(intro_music.__doc__)

    global start
    global speaker_btn
    global intro_music
    #έναρξη εφαρμογής (play)
    if start:
        intro_music = True
        mixer.music.load(sounds[0])
        #loop playing --> (-1)    
        mixer.music.play(-1)
        speaker_btn.config(image = speaker_on)
        start = False        
    else:
        #εναλλαγές (pause/unpause κατά τη διάρκεια που τρέχει η εφαρμογή) με επιλογή του χρήστη       
        if not intro_music:
            intro_music = True            
            mixer.music.unpause()
            speaker_btn.config(image = speaker_on)                   
        else:
            mixer.music.pause()
            speaker_btn.config(image = speaker_off)
            intro_music = False           

#if __name__ =="__main__":
def main():    
    global calc_label
    global imageFrame
    global eap_label
    
    #τίτλος
    start_window.title("[ΠΛΗΠΡΟ - ΗΛΕ52] 2023 - 2024 Ομάδα_5_Project    Smart Calc v.2.0.0")
    
    #εικονίδιο (πάνω αριστερά)    
    start_window.iconbitmap(str(photo[0]))
        
    start_window.geometry('1200x700+0+0')
    start_window.option_add("*Button.cursor", "hand2")  #attribute για όλα τα Buttons, cursor="hand2" 
    start_window.configure(bg=bg_color)    

    #εικονίδιο ΕΑΠ (πάνω αριστερά)
    eap_img = ImageTk.PhotoImage(Image.open(str(photo[1])))    
    eap_label = Label(start_window, image = eap_img, bg = bg_color)

    global MainFrame
    MainFrame = Frame(start_window, bg = bg_color, highlightthickness = 0)
    MainFrame.grid(row = 10, column = 0, columnspan = 20, sticky =  N + S + E + W)
    imageFrame = Frame(MainFrame, bg = bg_color, pady = 10, padx = 436)
    imageFrame.grid(row = 20, column = 0, columnspan = 20, sticky = E + W, pady = 10)

    #εικονίδιο speaker 
    global speaker_label
    global speaker_on
    global speaker_off
    speaker_on = ImageTk.PhotoImage(Image.open(str(photo[8])))
    speaker_off = ImageTk.PhotoImage(Image.open(str(photo[9])))

    #εικονίδιο ελληνικής σημαίας
    global greek_label
    global greek_img
    greek_img = ImageTk.PhotoImage(Image.open(str(photo[6])))
    
    #εικονίδιο αγγλικής σημαίας
    global uk_label
    global uk_img
    uk_img = ImageTk.PhotoImage(Image.open(str(photo[7])))   
    
    #εικόνα αρχικής οθόνης
    calc_img = ImageTk.PhotoImage(Image.open(str(photo[2])))
    calc_label = Label(imageFrame, image = calc_img, bg = bg_color)

    #δημιουργία initializer ήχου
    mixer.init()

    #κατασκευή των Frames εδώ και τοποθέτησής τους (.grid) όποτε χρειαστεί. Αυτό το
    #επιλέγουμε για να μπορουμε να κατασκευάσουμε τις εικόνες, οι οποιες χρειαζεται
    #να τοποθετηθουν στα ανάλογα Frames (αν δεν ειναι δηλωμένα σε αυτό το σημείο τα
    #Frames, o compiler χτυπάει σφάλμα (δηλώνονται ως καθολικές - global - μεταβλητές)
    global InfoFrame
    InfoFrame = Frame(start_window, bg = bg_color, highlightthickness = 0)

    global CalcFrame
    CalcFrame = Frame(start_window, bg = bg_color, highlightthickness = 0)

    global calculator
    calculator = Frame(CalcFrame, bg = colors[theme][0][1], padx = 60, pady = 30)
    
    #εικόνα δική μου
    global serafina_label
    serafina_img = ImageTk.PhotoImage(Image.open(str(photo[3])))
    serafina_label = Label(InfoFrame, image = serafina_img, bg = bg_color)

    #εικόνα Καθηγητή
    global xenakis_label
    xenakis_img = ImageTk.PhotoImage(Image.open(str(photo[4])))
    xenakis_label = Label(InfoFrame, image = xenakis_img, bg = bg_color)

    #εικονίδιο μικροφώνου
    global microphone
    microphone_img = ImageTk.PhotoImage(Image.open(str(photo[5])))    
    microphone = Button(CalcFrame, image =  microphone_img, bd = 0, bg = colors[theme][0][1], activebackground = colors[theme][0][1], command = voice_call)    
    
    #εικονίδιο ΕΑΠ (αριστερά στο calculator)
    global eap_label_calc
    eap_img_calc = ImageTk.PhotoImage(Image.open(str(photo[1])))    
    eap_label_calc = Label(CalcFrame, image = eap_img_calc, bg = colors[theme][0][1])
       
    #δημιουργία αρχικής οθόνης
    make_main_frame()

    ##################
    #   TESTING...   #
    ##################    
    change('CalcFrame')

    #σύνδεση του <Escape> με τον τερματισμό του προγράμματος
    start_window.bind("<Escape>", terminate)

    #μουσικό χαλί με την έναρξη της εφαρμογής
    global start
    if start :
        play_music()
        start = False
    
    #ρολόι (θα εμφανίζεται σε ολα τα Frames, για αυτό θα το τοποθετήσω
    #στο αρχικό παράθυρο και όχι σε κάποιο Frame, ώστε κάθε φορά που θα
    #γίνεται εναλλαγή στα Frames, το ρολόι θα παραμένει ανεπηρέαστο
    display_time()

    start_window.mainloop()
    
#δημιουργία αρχικού παράθυρου για το πρόγραμμα
start_window = Tk()
main()
