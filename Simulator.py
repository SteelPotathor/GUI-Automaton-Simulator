import re
import time
import tkinter as tk
from functools import partial
from tkinter import ttk

import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage

import Functions

"""
GUI made by Thorgrimmneth
"""

# Libraries install command
"!pip install customtkinter"
"!pip install pillow"

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("themes/GhostTrain.json")


def addNotebook(notebook, frame, text):
    global nbTab, numTab
    nbTab += 1
    # Images
    img_auto = Image.open("icons/automatic.png")
    img_alphabet = Image.open("icons/alphabet.png")
    img_prune = Image.open("icons/scissors7.png")
    img_tab = Image.open("icons/board.png")
    img_see = Image.open("icons/see.png")
    img_all = Image.open("icons/all.png")
    img_intersect = Image.open("icons/intersect.png")
    img_minus = Image.open("icons/minus.png")
    img_mult = Image.open("icons/mult.png")
    img_plus = Image.open("icons/plus.png")
    # Pattern for the input
    global patternNumber, patternString
    patternNumber = r'\d+'  # Matches any digit
    patternString = r'\b[a-zA-Z]+\b'  # Matches any word

    # Test
    """Definition of the window and grid"""

    """Definition of the canvas"""
    canvas = ctk.CTkCanvas(frame, width=850, height=600, bg="gray50", borderwidth=1, relief="solid")

    """Definition and initialization of global variables"""
    global automaton, automata
    automaton = [2, ["a", "b"], {(1, "a"): [1], (1, "b"): [2], (2, "a"): [2], (2, "b"): [1]}, {1}, {1}]
    automata[nbTab] = automaton

    def initGraphismeLecture():
        """
        Description: Initialization of word reading
        :return:
        """
        global automaton
        canvas.delete("all")
        resultLabel.configure(text="")
        word = wordEntry.get()
        if word == "":
            resultLabel.configure(text="Enter a word please")
            return
        wordSize = len(word)
        squareSize = max(20, min(596 // wordSize, 80))
        triangleSize = squareSize // 2
        arrowSize = 2 * squareSize // 3
        xRect = triangleSize // 2
        yRect = 2 + 50
        xText = squareSize // 2 + triangleSize // 2
        yText = squareSize // 2 + 2 + 50
        coordsTriangle = [(4, squareSize + triangleSize + 2 + 50), (4 + squareSize // 3, squareSize + 2 + 50),
                          (4 + squareSize // 1.5, squareSize + triangleSize + 2 + 50)]
        triangle = canvas.create_polygon(coordsTriangle, fill="green")

        flag, res = readWord(word)
        showWord(word, flag, res, squareSize, triangleSize, arrowSize, triangle, xRect, yRect, xText, yText)

    def readWord(m):
        global automaton

        def closure(aut, i):
            etats, al, T, init, Ac = aut

            Cl = {i}  # The closure of state i
            L = [i]
            while L:
                j = L.pop(0)
                if (j, 'epsilon') in T:
                    for k in T[(j, 'epsilon')]:
                        if not k in Cl:
                            Cl.add(k)
                            L.append(k)
            return Cl

        (states, al, T, init, Ac) = automaton
        # Calculate all closures once
        Cl = {i: closure(automaton, i) for i in range(1, states + 1)}
        L = [init]  # A list of sets
        et = list(init)
        for c in m:
            # Calculate the set of states accessible by reading the letter c
            # from one of the current states
            et2 = set()
            for i in et:
                for e in Cl[i]:  # Calculate the transitions extended to the entire closure
                    if (e, c) in T:
                        et2 = et2.union(set(T[(e, c)]))
            L.append(et2)
            et = list(et2)
            if not et:
                return False, L
        # Don't forget to inherit the accepting character to states
        # that have an accepting state in their closure
        Ac2 = set(Ac)
        for e in range(1, states + 1):
            if Cl[e].intersection(Ac) != {} and not e in Ac2:
                Ac2.add(e)
        return et2.intersection(Ac2) != {}, L

    def showWord(word, flag, lr, squareSize, triangleSize, arrowSize, triangle, xRect, yRect, xText, yText):
        """
        Description: Reads the word entered by the user and displays the evolution of the automaton
        :param m: word to read
        :param squareSize:
        :param triangleSize:
        :param arrowSize:
        :param triangle:
        :return:
        """
        global automaton
        canvas.create_text(100, 20, text="Tape Reading", font=("Arial 25 "))
        canvas.create_text(105, 3 * squareSize + 200, text="Reading Chain", font=("Arial 25"))
        for i, j in enumerate(word):
            canvas.create_rectangle((i * squareSize) + xRect, yRect, (i + 1) * squareSize + xRect, squareSize + yRect,
                                    outline="black")
            canvas.create_text(i * squareSize + xText, yText, text=j,
                               font=("Arial", squareSize // 2))
        initState = automaton[3]
        canvas.create_text(triangleSize // 3 + (len(initState) * 2 - 2) * 8, 3 * squareSize + 250, text=initState,
                           font=("Arial", 15))
        canvas.update()
        time.sleep(0.5)
        # init of the first coords
        xLine = triangleSize // 2 + 15 + (len(initState) * 3 - 2) * 8
        yLine = 3 * squareSize + 255
        xText = squareSize // 2 + 15 + (len(initState) * 3 - 2) * 8
        yText = 3 * squareSize - squareSize // 4 + 260
        for ind, c in enumerate(word):
            canvas.move(triangle, squareSize, 0)
            canvas.create_line(xLine, yLine, xLine + arrowSize, yLine,
                               arrow=tk.LAST, fill="black", width=2)
            canvas.create_text(xText, yText, text=c, font=("Arial", 15))
            canvas.update()

            currentState = lr[ind + 1]
            stateSize = (len(currentState) * 3 - 1) * 8 + 30 + arrowSize
            if currentState:
                canvas.create_text(xText + triangleSize + 8, 3 * squareSize + 250, text=currentState,
                                   font=("Arial", 15), anchor="w")
            else:
                canvas.create_text(xText + triangleSize + 8, 3 * squareSize + 250, text="{}",
                                   font=("Arial", 15), anchor="w")
            xLine += stateSize
            xText += stateSize
            canvas.update()
            time.sleep(0.5)
            if ind < len(word) - 1 and ind + 1 == len(lr) - 1:
                resultLabel.configure(text="The word doesn't belong to the language")
                return
        if flag:
            resultLabel.configure(text="The word belongs to the language")
            return
        resultLabel.configure(text="The word doesn't belong to the language")
        return

    def setAlphabet(topAlphabet):
        """
        Description: Converts the input (where the alphabet is entered) into a list of strings, with each word separated by a comma using split.
        This updates the automaton's alphabet.
        :param topAlphabet: Tkinter window for entering the alphabet
        :return:
        """
        global alphabet, automaton, patternString
        alpha = re.findall(patternString, alphabet.get())
        alpha = list(set(alpha))
        alphabetLabel.configure(text="Σ = {" + str(alpha)[1:-1] + "}")
        automaton[1] = alpha

        # Clear the window and replace it with the table (intrusive method)
        topAlphabet.destroy()
        getTable()

    def getAlphabet():
        """
        Description: Creates the popup for entering the alphabet
        :return:
        """
        global alphabet, automaton
        topAlphabet = ctk.CTkToplevel()
        topAlphabet.title("Alphabet")
        topAlphabet.geometry("900x700")
        topAlphabet.attributes("-topmost", True)
        ctk.CTkLabel(topAlphabet, text="Enter an alphabet", font=("Arial", 15)).pack()
        alphabet_var = ctk.StringVar()
        alphabet = ctk.CTkEntry(topAlphabet, width=165, fg_color="gray85", text_color="black",
                                textvariable=alphabet_var,
                                placeholder_text_color="gray50")
        alphastring = str(automaton[1])[1:-1].replace("'", "")
        alphabet_var.set(alphastring)
        alphabet.pack()
        ctk.CTkButton(topAlphabet, text="Validate", font=("Arial", 15), command=lambda: setAlphabet(topAlphabet)).pack(
            pady=30)

    def setParameters(topParamAuto, widgetdico):
        """
        Description: Converts various inputs from the window to update the states, initial states, and accepting states of the automaton.
        :param topParamAuto: Tkinter window for states, initial states, and accepting states
        :return:
        """
        global patternNumber

        automaton[0] = int(widgetdico["state"].get())
        automaton[3] = {int(i) for i in re.findall(patternNumber, widgetdico["initial"].get())}
        automaton[4] = {int(i) for i in re.findall(patternNumber, widgetdico["accepting"].get())}
        topParamAuto.destroy()

    def getParameters():
        """
        Description: Creates the popup for entering states, initial states, and accepting states
        :return:
        """
        topParamAuto = ctk.CTkToplevel()
        topParamAuto.title("Automaton's parameters")
        topParamAuto.geometry("900x700")
        topParamAuto.attributes("-topmost", True)
        couleurEntry = "gray85"
        statevar = ctk.StringVar()
        initialvar = ctk.StringVar()
        acceptingvar = ctk.StringVar()
        statevar.set(str(automaton[0]))
        initialvar.set(str(automaton[3])[1:-1])
        acceptingvar.set(str(automaton[4])[1:-1])
        widgetdico = {"State": ctk.CTkLabel(topParamAuto, text="States", font=("Arial", 15)),
                      "state": ctk.CTkEntry(topParamAuto, width=100, fg_color=couleurEntry, text_color="black",
                                            textvariable=statevar),
                      "Initial": ctk.CTkLabel(topParamAuto, text="Initial", font=("Arial", 15)),
                      "initial": ctk.CTkEntry(topParamAuto, width=215, fg_color=couleurEntry, text_color="black",
                                              textvariable=initialvar),
                      "Accepting": ctk.CTkLabel(topParamAuto, text="Accepting", font=("Arial", 15)),
                      "accepting": ctk.CTkEntry(topParamAuto, width=150, fg_color=couleurEntry, text_color="black",
                                                textvariable=acceptingvar), }

        for i in widgetdico.values():
            i.pack()
        ctk.CTkButton(topParamAuto, text="Validate", font=("Arial", 15),
                      command=lambda: setParameters(topParamAuto, widgetdico)).pack(pady=30)

    def setTable(topTable, labeldico, epsilonEntry):
        """
        Description: Converts the graphical transition table into a dictionary (key = (current state, letter): value = next state).
        Updates the automaton.
        :param topTable: Tkinter window for the transition table modification
        :return:
        """
        global automaton, patternNumber
        states, langage, T = automaton[0], automaton[1], automaton[2]
        for i in labeldico:
            switchValue = labeldico[i].get()  # retrieves the value of the entry
            # Potential incomplete automaton
            value = [int(i) for i in re.findall(patternNumber, switchValue) if i.isdigit() and 1 <= int(i) <= states]
            T[(i // len(langage) + 1, langage[i % len(langage)])] = value
            if not value:
                resultLabel.configure(text="A state is missing in the table")
        for i in epsilonEntry:
            switchValue = epsilonEntry[i].get()
            value = [int(i) for i in re.findall(patternNumber, switchValue) if i.isdigit() and 1 <= int(i) <= states]
            T[(i, "epsilon")] = value
        automaton[2] = T
        topTable.destroy()

    def getTable():
        """
        Description: Creates the window for entering and modifying the transition table. Updates the table.
        :param topTable: Tkinter window for modifying the transition table
        :return:
        """
        global automaton
        states, langage, T = automaton[0], automaton[1], automaton[2]
        # Case where the Table button is clicked
        topTable = ctk.CTkToplevel()
        topTable.title("Table")
        topTable.geometry("900x700")
        topTable.attributes("-topmost", True)
        # With the counter, each widget in the table has a specific and easily identifiable name
        cnt = 0
        labeldico = {}
        epsilonEntry = {}
        for i in range(states + 1):
            for j in range(len(langage) + 1):
                if i == 0 and j == 0:
                    continue
                if i == 0 and j > 0:
                    ctk.CTkLabel(topTable, width=100, text_color=('black', 'gray74'), text=str(langage[j - 1]),
                                 font=('Arial', 16, 'bold')).grid(row=i, column=j)
                elif j == 0 and i > 0:
                    ctk.CTkLabel(topTable, width=100, text_color=('black', 'gray74'), text=str(i),
                                 font=('Arial', 16, 'bold')).grid(row=i, column=j)
                else:
                    labeldico[cnt] = ctk.CTkEntry(topTable, width=100, text_color='blue', fg_color="gray85",
                                                  font=('Arial', 16, 'bold'))

                    # Repositioning the table value to the right place if it already exists
                    if (i, langage[j - 1]) in T:
                        labeldico[cnt].insert(0, T[(i, langage[j - 1])])
                        labeldico[cnt].grid(row=i, column=j)
                    # Otherwise set to default value 0
                    else:
                        labeldico[cnt].insert(0, 0)
                        labeldico[cnt].grid(row=i, column=j)
                    cnt += 1
            if i == 0:
                ctk.CTkLabel(topTable, width=100, text_color=('black', 'gray74'), text="Epsilon",
                             font=('Arial', 15, 'bold')).grid(
                    row=i,
                    column=j + 1)
            else:
                epsilonEntry[i] = ctk.CTkEntry(topTable, width=100, text_color='blue', fg_color="gray85",
                                               font=('Arial', 16, 'bold'))
                val = T.get((i, "epsilon"), "X")
                if val:
                    epsilonEntry[i].insert(0, val)
                else:
                    epsilonEntry[i].insert(0, "X")
                epsilonEntry[i].grid(row=i, column=j + 1)

        ctk.CTkButton(topTable, width=100, text="Validate", font=("Arial", 15),
                      command=lambda: setTable(topTable, labeldico, epsilonEntry)).grid(row=states + 1,
                                                                                        column=len(
                                                                                            langage), pady=5)

    def showTable():
        """
        Description: Displays the transition table (without the possibility of modification)
        :return:
        """
        global automaton
        states = automaton[0]
        langage = automaton[1]
        T = automaton[2]
        top = ctk.CTkToplevel()
        top.title("Table")
        top.geometry("900x700")
        top.attributes("-topmost", True)
        if switch_var.get() == "light":
            bgcolor = "#c6ced8"
        else:
            bgcolor = "#3c5064"
        for i in range(states + 1):
            for j in range(len(langage) + 1):
                if i == 0 and j == 0:
                    continue
                if i == 0 and j > 0:
                    ctk.CTkLabel(top, width=100, text=str(langage[j - 1]),
                                 font=('Arial', 16, 'bold')).grid(row=i, column=j + 1)
                elif j == 0 and i > 0:
                    if i in automaton[3]:  # if the state is an initial state
                        canvasTemp = tk.Canvas(top, width=100, height=30, bg=bgcolor, highlightthickness=0)
                        canvasTemp.grid(row=i, column=j)
                        canvasTemp.create_line(20, 15, 80, 15, fill="green", width=5, arrow=tk.LAST)
                    if i in automaton[4]:  # if the state is an accepting state
                        canvasTemp = tk.Canvas(top, width=100, height=30, bg=bgcolor, highlightthickness=0)
                        canvasTemp.grid(row=i, column=j + 1)
                        canvasTemp.create_oval(36, 1, 64, 29, outline="green", width=2)
                        canvasTemp.create_text(50, 15, text=str(i), font=("Arial", 15), fill="red")
                    else:
                        ctk.CTkLabel(top, width=100, text=str(i),
                                     font=('Arial', 16, 'bold')).grid(row=i, column=j + 1)

                else:
                    value = T.get((i, langage[j - 1]), "X")
                    if value:
                        ctk.CTkLabel(top, width=100, text_color='#AAAAFF',
                                     font=('Arial', 16, 'bold'), text=value).grid(row=i,
                                                                                  column=j + 1)
                    else:
                        ctk.CTkLabel(top, width=100, text_color='#AAAAFF',
                                     font=('Arial', 16, 'bold'), text="X").grid(row=i,
                                                                                column=j + 1)
            if i == 0:
                ctk.CTkLabel(top, width=100, text="Epsilon", font=('Arial', 15, 'bold')).grid(row=i,
                                                                                              column=j + 2)
                ctk.CTkLabel(top, width=100, text="Closure", font=('Arial', 15, 'bold')).grid(row=i,
                                                                                              column=j + 3)
            else:
                value = T.get((i, 'epsilon'), "X")
                if value:
                    ctk.CTkLabel(top, width=100, text_color='#AAAAFF', text=value,
                                 font=('Arial', 15, 'bold')).grid(
                        row=i, column=j + 2)
                else:
                    ctk.CTkLabel(top, width=100, text_color='#AAAAFF', text="X",
                                 font=('Arial', 15, 'bold')).grid(
                        row=i, column=j + 2)
                ctk.CTkLabel(top, width=100, text_color='#AAAAFF', text=str(Functions.epsilon_closure(automaton, i)),
                             font=('Arial', 15, 'bold')).grid(
                    row=i, column=j + 3)

    def pruneAut():
        """
        Description: Prunes the automaton
        :return:
        """
        global automaton
        automaton = Functions.prune(automaton)
        resultLabel.configure(text="Automaton pruned")

    def completeAut():
        """
        Description: Completes the automaton
        :return:
        """
        global automaton
        automaton = Functions.complete_automaton(automaton)
        resultLabel.configure(text="Automaton completed")

    def determinateAut():
        """
        Description: Converts the automaton to a deterministic automaton
        :return:
        """
        global automaton
        automaton = Functions.determinate_automaton_epsilon_transition(automaton)
        resultLabel.configure(text="Automaton determinated")

    switch_var = ctk.StringVar(value=ctk.get_appearance_mode().lower())

    def switch_event():
        global nbTab
        """
        Description: Changes the theme of the widgets
        :return:
        """

        ctk.set_appearance_mode(switch_var.get())
        if switch_var.get() == "light":
            canvas.configure(bg="gray80")
        else:
            canvas.configure(bg="gray50")

    def performOperation(operation, varList, entryValue, operationTop):
        global automata, nbTab
        Ltemp = [i if varList[i - 1].get() != "0" else 0 for i in range(1, nbTab + 1)]
        L = [0 for i in range(len(Ltemp))]
        for ind, val in enumerate(entryValue):
            L[val - 1] = Ltemp[ind]
        L = [automata[i] for i in L if i != 0]
        newAut = []
        if operation == "intersect":
            resultLabel.configure(text="Operation: Intersection")
            newAut = Functions.intersect_automata(*L)
        elif operation == "difference":
            resultLabel.configure(text="Operation: Difference")
            newAut = Functions.difference_automata(*L)
        elif operation == "product":
            resultLabel.configure(text="Operation: Product")
            newAut = Functions.product_automata(*L)
        elif operation == "Sum":
            resultLabel.configure(text="Operation: Sum")
            newAut = Functions.sum_automata(*L)
        if type(newAut) == str:
            resultLabel.configure(text=newAut)
            operationTop.destroy()
            return
        addNotebook(notebook, ctk.CTkFrame(notebook), "aut" + str(nbTab + 1))
        automata[nbTab] = newAut
        notebook.select(nbTab - 1)
        operationTop.destroy()

    def setUpOperation(operation):
        """
        Description: Sets up the operation to be performed on the automaton
        :param operation: Operation to be performed
        :return:
        """
        global automaton, entryList, entryVarList, entryValue, numTab, checkList, user_action
        operationTop = ctk.CTkToplevel()
        operationTop.title("Set up operation")
        operationTop.geometry("900x700")
        operationTop.attributes("-topmost", True)
        varList = []
        checkList = []
        entryList = []
        entryVarList = []
        entryValue = []

        operationTop.columnconfigure(0, weight=0)
        operationTop.columnconfigure(1, weight=1)
        operationTop.columnconfigure(2, weight=0)
        operationTop.rowconfigure(nbTab + 1, weight=1)

        labelCheckbox = ctk.CTkLabel(operationTop, width=100, text="Select the automatons to\n perform the operation")
        labelCheckbox.grid(row=0, column=0, pady=10)
        labelEntry = ctk.CTkLabel(operationTop, text="Enter the order")
        labelEntry.grid(row=0, column=2, pady=10)
        user_action = True

        def on_checkbox_change(i):
            global entryVarList, checkList, entryValue, user_action
            user_action = False
            oldValue = entryValue[i]
            if not (entryVarList[i].get()):
                temp = [int(j.get()) for j in entryVarList if j.get()]
                temp.append(0)
                valMax = max(temp) + 1
                if valMax > nbTab:
                    user_action = True
                    entryValue[i] = 1  # setting the value to 1 to enter in the if in on_entry_change
                    entryVarList[i].set(str(nbTab))
                    entryValue[i] = nbTab
                else:
                    entryVarList[i].set(str(valMax))
                    entryValue[i] = valMax
                user_action = True
                return
            if checkList[i].get() == "0":
                entryValue[i] = 0
                entryVarList[i].set("")
                for i in range(len(entryValue)):
                    if oldValue <= entryValue[i] <= nbTab:
                        entryValue[i] -= 1
                        entryVarList[i].set(str(entryValue[i]))
                user_action = True
                return

        def on_entry_change(i, *args):
            global entryList, entryVarList, entryValue, user_action, nbTab
            if user_action:
                user_action = False
                oldValue = entryValue[i]
                try:
                    newValue = int(entryList[i].get())
                except:
                    user_action = True
                    return
                tempMax = [int(j.get()) for j in entryVarList if j.get() and int(j.get()) > 0 and j != entryVarList[i]]
                valMax = len(tempMax) + 1 if tempMax else 1
                if newValue > valMax:
                    newValue = valMax
                    entryVarList[i].set(str(newValue))
                    entryValue[i] = newValue
                if oldValue:
                    dico = {}
                    for ind in range(len(entryValue)):
                        try:
                            if ind != i and entryValue[ind]:
                                dico[entryValue[ind]] = ind
                        except:
                            user_action = True

                    if oldValue - newValue > 0:
                        L = [ind for ind in range(newValue, oldValue)]
                        ndico = {}
                        for ind in L:
                            ndico[dico[ind]] = ind + 1
                        for ind in ndico:
                            entryVarList[ind].set(str(ndico[ind]))
                            entryValue[ind] = ndico[ind]
                        entryVarList[i].set(str(newValue))
                        entryValue[i] = newValue
                        user_action = True

                    elif oldValue - newValue < 0:
                        L = [ind for ind in range(oldValue + 1, newValue + 1)]
                        ndico = {}
                        for ind in L:
                            ndico[dico[ind]] = ind - 1
                        for ind in ndico:
                            entryVarList[ind].set(str(ndico[ind]))
                            entryValue[ind] = ndico[ind]
                        entryVarList[i].set(str(newValue))
                        entryValue[i] = newValue
                        user_action = True
                    else:
                        user_action = True
                else:
                    entryValue[i] = newValue
                    user_action = True

        for i in range(1, nbTab + 1):
            varList.append(ctk.StringVar(value="0"))

            checkbox = ctk.CTkCheckBox(operationTop, text="Automaton n°" + str(i),
                                       variable=varList[i - 1], onvalue=str(i), offvalue="0",
                                       command=partial(on_checkbox_change, i - 1))
            checkList.append(checkbox)
            checkbox.grid(row=i, column=0, sticky="w", pady=10)
            entry_var = tk.StringVar()
            entry_var.trace("w", partial(on_entry_change, i - 1))

            entryVarList.append(entry_var)
            if i == numTab:
                entryValue.append(i)
                entry_var.set("1")
            else:
                entryValue.append(0)
                entry_var.set("")
            newEntry = ctk.CTkEntry(operationTop, width=100, fg_color="gray85", text_color="black",
                                    textvariable=entry_var, placeholder_text_color="gray50")
            newEntry.grid(row=i, column=2, sticky="e", pady=10)
            entryList.append(newEntry)
        checkList[numTab - 1].select()

        ctk.CTkButton(operationTop, text="Validate",
                      command=lambda: performOperation(operation, varList, entryValue, operationTop)).grid(
            row=nbTab + 1,
            column=1)

    def LplusOrStar(mode):
        global automata, numTab, nbTab
        newAut = []
        if mode == "L+":
            resultLabel.configure(text="Operation: L+")
            newAut = Functions.L_plus(automaton)
        elif mode == "L*":
            resultLabel.configure(text="Operation: L*")
            newAut = Functions.L_star(automaton)
        elif mode == "comp":
            resultLabel.configure(text="Operation: complement")
            newAut = Functions.complement_automaton(automaton)
        addNotebook(notebook, ctk.CTkFrame(notebook), "aut" + str(nbTab + 1))
        automata[nbTab] = newAut
        notebook.select(nbTab - 1)

    """Switch"""
    switchTheme = ctk.CTkSwitch(frame, text="Dark Mode", command=switch_event,
                                variable=switch_var, onvalue="dark", offvalue="light")

    """Frame"""
    frame_param = ctk.CTkFrame(frame)
    frame_determinate = ctk.CTkFrame(frame)
    frame_operations = ctk.CTkFrame(frame)

    """Labels"""
    wordEntryLabel = ctk.CTkLabel(frame, text="Enter a word : ")
    resultLabel = ctk.CTkLabel(frame, text="", font=("Arial", 35), text_color="red")
    alphabetLabel = ctk.CTkLabel(frame, text="Σ = {'a','b'}", font=("Arial", 15))

    """Entries"""
    wordEntry = ctk.CTkEntry(frame, fg_color="gray85", text_color="black")

    """Buttons"""
    validationButton = ctk.CTkButton(frame, text="Start the analysis", command=initGraphismeLecture)
    autParametersButton = ctk.CTkButton(frame_param, text="Automaton's parameters", command=getParameters,
                                        image=CTkImage(dark_image=img_auto, light_image=img_auto))
    showtableButton = ctk.CTkButton(frame_param, text="Show table", command=showTable,
                                    image=CTkImage(dark_image=img_see, light_image=img_see))
    tableButton = ctk.CTkButton(frame_param, text="Modify table", command=getTable,
                                image=CTkImage(dark_image=img_tab, light_image=img_tab))
    alphabetButton = ctk.CTkButton(frame_param, text="Alphabet", command=getAlphabet,
                                   image=CTkImage(dark_image=img_alphabet, light_image=img_alphabet))
    pruneButton = ctk.CTkButton(frame_determinate, text="Prune", command=pruneAut,
                                image=CTkImage(dark_image=img_prune, light_image=img_prune))
    completeButton = ctk.CTkButton(frame_determinate, text="Complete", command=completeAut,
                                   image=CTkImage(dark_image=img_all, light_image=img_all))
    determineButton = ctk.CTkButton(frame_determinate, text="Determinate", command=determinateAut)
    intersectButton = ctk.CTkButton(frame_operations, text="Intersect", command=lambda: setUpOperation("intersect"),
                                    image=CTkImage(dark_image=img_intersect, light_image=img_intersect))
    differenceButton = ctk.CTkButton(frame_operations, text="Difference", command=lambda: setUpOperation("difference"),
                                     image=CTkImage(dark_image=img_minus, light_image=img_minus))
    sumButton = ctk.CTkButton(frame_operations, text="Sum", command=lambda: setUpOperation("Sum"),
                              image=CTkImage(dark_image=img_plus, light_image=img_plus))
    productButton = ctk.CTkButton(frame_operations, text="Product", command=lambda: setUpOperation("product"),
                                  image=CTkImage(dark_image=img_mult, light_image=img_mult))
    lplusButton = ctk.CTkButton(frame_operations, text="L+", command=lambda: LplusOrStar("L+"))
    lstarButton = ctk.CTkButton(frame_operations, text="L*", command=lambda: LplusOrStar("L*"))
    complementButton = ctk.CTkButton(frame_operations, text="Complement", command=lambda: LplusOrStar("comp"))

    frame.grid_rowconfigure(0, weight=0)
    frame.grid_rowconfigure(1, weight=0)
    frame.grid_rowconfigure(2, weight=0)
    frame.grid_rowconfigure(3, weight=0)
    frame.grid_rowconfigure(4, weight=0)
    frame.grid_rowconfigure(5, weight=0)
    frame.grid_rowconfigure(6, weight=0)
    frame.grid_rowconfigure(7, weight=0)
    frame.grid_rowconfigure(8, weight=1)
    frame.grid_rowconfigure(9, weight=0)

    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=0)
    frame.grid_columnconfigure(2, weight=1)
    frame.grid_columnconfigure(3, weight=2)
    frame.grid_columnconfigure(4, weight=0)
    frame.grid_columnconfigure(5, weight=0)
    frame.grid_columnconfigure(6, weight=0)

    """Placing every widget in the grid"""

    """Frame"""
    frame_param.grid(row=1, column=0, rowspan=3, padx=10, pady=(15, 0), sticky="nsew")
    frame_determinate.grid(row=4, column=0, rowspan=2, padx=10, pady=(15, 0), sticky="nsew")
    frame_operations.grid(row=6, column=0, rowspan=2, padx=10, pady=(15, 0), sticky="nsew")
    """"Canvas"""
    canvas.grid(row=1, column=1, rowspan=8, columnspan=6, sticky="nsew")

    """Label"""
    wordEntryLabel.grid(row=0, column=1, sticky="nsew")
    resultLabel.grid(row=9, column=2, columnspan=4, sticky="nsew")
    alphabetLabel.grid(row=0, column=6, sticky="nsew")

    """Entry"""
    wordEntry.grid(row=0, column=2, sticky="nsew")

    """Button"""
    sizePadY = 7
    validationButton.grid(row=0, column=4, padx=10, sticky="nsew")
    alphabetButton.pack(padx=2, pady=sizePadY, fill='x')
    autParametersButton.pack(padx=2, pady=sizePadY, fill='x')
    tableButton.pack(padx=2, pady=sizePadY, fill='x')
    showtableButton.pack(padx=2, pady=sizePadY, fill='x')
    pruneButton.pack(padx=2, pady=sizePadY, fill='x')
    completeButton.pack(padx=2, pady=sizePadY, fill='x')
    determineButton.pack(padx=2, pady=sizePadY, fill='x')
    intersectButton.pack(padx=2, pady=sizePadY, fill='x')
    differenceButton.pack(padx=2, pady=sizePadY, fill='x')
    sumButton.pack(padx=2, pady=sizePadY, fill='x')
    productButton.pack(padx=2, pady=sizePadY, fill='x')
    lplusButton.pack(padx=2, pady=sizePadY, fill='x')
    lstarButton.pack(padx=2, pady=sizePadY, fill='x')
    complementButton.pack(padx=2, pady=sizePadY, fill='x')

    """Switch"""
    switchTheme.grid(row=9, column=0, sticky="nsew")

    """Add the button to add an automaton"""
    bouton = ttk.Button(frame, text="Add an automaton",
                        command=lambda: addNotebook(notebook, ctk.CTkFrame(notebook), "aut" + str(nbTab + 1)))
    bouton.grid(row=8, column=0, padx=10, pady=10, sticky="s")
    """Add the frame to the notebook"""

    frame.pack(fill='both', expand=True)
    notebook.add(frame, text=text)


root = ctk.CTk()
root.title("Automaton Simulator")
root.geometry("1200x900")

global numTab
numTab = 1
global automata, automaton
automata = {}
automaton = [2, ["a", "b"], {(1, "a"): [1], (1, "b"): [2], (2, "a"): [2], (2, "b"): [1]}, {1}, {1}]
nbTab = 0

# Create a notebook
notebook = ttk.Notebook(root)
style = ttk.Style()
style.configure('TNotebook.Tab', padding=[30, 2])
notebook.pack(fill='both', expand=True)

# Create frames
frame1 = ctk.CTkFrame(notebook)
frame1.pack(fill='both', expand=True)
addNotebook(notebook, frame1, "aut1")


def on_tab_changed(event):
    global numTab, automata, automaton
    selected_tab = event.widget.select()  # Selects the current tab
    tab_text = event.widget.tab(selected_tab, "text")  # Retrieves the text of the selected tab
    numTab = int(tab_text.split("aut")[-1])
    if numTab:
        automaton = automata[numTab]


notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

root.mainloop()
