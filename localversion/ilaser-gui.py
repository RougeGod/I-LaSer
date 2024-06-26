from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import re
from laser import handlers
#put a laser folder beneath current directory and put all non-views files from transducer there
#will need to create a specific code_gen file which can handle the get_code method inside views
#without  using HTML/Django code. 

#also need to put all FAdo files in a subfolder of laser folder to be locally imported with no need
#for extra installations on user's computer. 


LIGHTGREEN = "#d5fc99"
LIGHTRED = "#ff7979"




class ResultFrame(ttk.Frame):

    def __init__(self, parent, row):
        self.styling = ttk.Style()
        self.styling.configure("Error.TFrame", background=LIGHTRED)
        self.styling.configure("Error.TLabel", background=LIGHTRED)

        self.result = StringVar()
        self.resultFrame = ttk.Frame(parent, relief="solid", borderwidth=2)
        self.resultFrame.grid(column=0, row=row, sticky="NEW")
        self.resultFrame.columnconfigure(0, weight=1)
        self.resultLabel = ttk.Label(self.resultFrame, text="", textvariable=self.result, wraplength=777)
        self.resultLabel.grid(column=0, row=0)
    
    def hide(self):
        self.resultFrame.grid_remove()
        self.resultLabel.text = ""
    
    def show(self, row=1):
        self.resultFrame.grid()
        
    def setResult(self, result):
        if (type(result) == str): #The "calculating... " message (all other messages will be in dictionaries)
            self.resultFrame["style"] = 'TFrame' #remove all errors
            self.resultLabel["style"] = "TLabel"
            self.result.set(result)
        elif (result.get('error_message')):
            self.result.set(result["error_message"])     
            self.resultFrame["style"] = "Error.TFrame"
            self.resultLabel["style"] = "Error.TLabel"
            self.resultLabel.text = result
        elif (result.get("result")):
            self.resultFrame["style"] = 'TFrame' #default TFrame
            self.resultLabel["style"] = "TLabel"
            if (result.get("proof")):
                self.result.set(result["result"] + "\n" + result["proof"])
            else:
                self.result.set(result.get("result"))
        self.show()
        self.resultLabel.text = self.result #don't think this line is necessary

class QuestionFrame(ttk.Frame):
    choices = ["-Please Select-", "Satisfaction", "Maximality", "Construction", "Approximate Maximality"]  

    def __init__(self, root, row, question, questionChangeFunc):
        self.questionVar = question
        self.questionReact = questionChangeFunc
        self.questionVar.trace_add("write", self.questionReact)        
        
        questionFrame = ttk.Frame(root, relief="raised", borderwidth=2)
        questionFrame.grid(column=0, row=row, sticky="NEW") #result is above it, though if result doesn't exist, it doesn't take up space
        questionFrame.columnconfigure(0, weight=1)
        questionLabel = ttk.Label(questionFrame, text="What question would you like to solve?")
        questionLabel.grid(row=0, column=0)
        self.questionPicker = ttk.Combobox(questionFrame, justify="center", textvariable=self.questionVar)
        self.questionPicker['state'] = 'readonly'
        self.questionPicker['values'] = self.choices
        self.questionPicker.current(newindex=0)
        self.questionPicker.grid(row=1, column=0)

    def getQuestionNumber(self):
        return self.questionPicker.current()

    def hide(self):
        self.grid_remove()
    
    def show(self, row=2):
        self.grid()
        
        

class LargeEntryFrame(ttk.Frame):
#used for automaton, transducer, and theta. has a file upload button on the left, and
#a textbox on the right. tries to validate inputs but still allows submission of 
#invalid inputs. 
    
  userinput = None
  validation = None

  def remove_comments(self, enteredString):
    enteredString = re.sub(r'\r', '', enteredString)
    enteredString = re.sub(r'\n#.+\n', '\n', enteredString)
    enteredString = re.sub(r'#.*', '', enteredString)
    return enteredString

  def validate(self, *uselessArgs):
    self.userinput.edit_modified(False) #clear the modified flag so it can fire again
    for pattern in self.validation: 
        #make sure that you put an iterable in the validation_regex argument
        #even if there is only one regex pattern to be matched
        try: 
            if re.match(pattern, self.remove_comments(self.get_data()), re.IGNORECASE):
                self.userinput["bg"] = LIGHTGREEN #text is OK so make the background light green
                return True
        except TypeError: #caused by the string being empty and the regex parser complaining
            print(self.get_data())
    self.userinput["bg"] = "white" #text is not OK, remove colour
    return False
    
  def get_data(self):
    return self.userinput.get(1.0, "end").strip()

  def get_file_to_data(self,windowTitle="Select File..."):
    try: 
        with fd.askopenfile(mode="r", title=windowTitle) as input_file:
            self.userinput.delete(1.0, "end")
            self.userinput.insert(1.0, input_file.read())
    except AttributeError: #file selection cancelled
        pass

  def __init__(self, root, row, file_request_text, file_button_text, textbox_label, validation_regex):
    self.validation = validation_regex
    self.aut_frame = ttk.Frame(root, relief="solid", borderwidth=2)
    self.aut_frame.grid(column=0, row=row, sticky=(EW))
    self.aut_frame.columnconfigure(0, weight=1)
    ttk.Label(self.aut_frame, text=file_request_text).grid(column=0, row=0)
    ttk.Button(self.aut_frame, text=file_button_text, command=self.get_file_to_data).grid(column=0, row=1)
    ttk.Label(self.aut_frame, text=textbox_label).grid(column=1, row=0)
    self.userinput = Text(self.aut_frame, width=40, height=10, wrap="none")
    self.userinput["bg"] = "white"
    self.userinput["fg"] = "black"
    self.userinput.grid(column=1, row=1)
    self.userinput.bind("<<Modified>>", self.validate)

  def hide(self):
        self.aut_frame.grid_remove()
    
  def show(self, *useless):
    self.aut_frame.grid()
  
  

class AutomatonFrame(LargeEntryFrame):
    REGEX_PATTERN = r"^[0-9A-Za-z()+*]+$" #for the user to input a regex in the NFA area
    #a single unrestricted line. balanced brackets is not possible and the handler will error
    #anyways if it cannot parse the regex. 
    GRAIL_PATTERN = r"^\(START\) +\|- +\d+(?:(?:\r?\n\d+ [0-9A-Za-z] \d)|(?:\r?\n\d+ +-\| +\(FINAL\)))+$"
    FADO_PATTERN = r"^@[ND]FA(?: +\d+)+(?:\r?\n\d+ +[0-9A-Za-z] +\d+)+$"
              
    def __init__(self, root, row):
        super().__init__(root, row, "Choose an automaton file", "Select Automaton File", "Or enter an automaton or regex in this text area.", (self.REGEX_PATTERN, self.GRAIL_PATTERN, self.FADO_PATTERN))
    
    #@Override
    def show(self):
        super().show(self)

class TransducerFrame(LargeEntryFrame):
    TRANS_PATTERN = r"^(?:(@InputAltering|@ErrorDetecting|@ErrorCorrecting)\r?\n)?@Transducer(?: \d+)+(?:\r?\n\d+ +[0-9A-Za-z] +[0-9A-Za-z] +\d+)+$"
    TRAJ_PATTERN = r"^[01*+)( ]+$"

    def __init__(self, root, row):
        super().__init__(root, row, "Choose a transducer file", "Select Transducer File", "Or enter a transducer or trajectory in that text area.", (self.TRANS_PATTERN, self.TRAJ_PATTERN))
    #@Override
    def show(self):
        super().show(self)
class ThetaFrame(LargeEntryFrame):
    THETA_PATTERN = r"^@Theta\r?(?:\n[A-Za-z0-9]\s+[A-Za-z0-9])+$"
    
    def __init__(self, root, row):
        super().__init__(root, row, "Choose a Theta File", "Select Theta File", "Or enter an antimorphism here", (self.THETA_PATTERN,))

    #@Override
    def show(self):
        super().show(self)

class ConstructionFrame(ttk.Frame):
  s_entry = None
  n_entry = None
  l_entry = None   
    
  

  def __init__(self, root, row):
    self.styling = ttk.Style()
    self.styling.configure("Valid.TEntry", fieldbackground=LIGHTGREEN)
    self.styling.configure("Invalid.TEntry", fieldbackground="white")
    

    self.s_int = StringVar(value="")
    self.s_int.trace_add("write", self.validate)
    self.n_int = StringVar(value="")
    self.n_int.trace_add("write", self.validate)
    self.l_int = StringVar(value="")
    self.l_int.trace_add("write", self.validate)
    self.constructionFrame = ttk.Frame(root, relief="solid", borderwidth=2)
    self.constructionFrame.grid(column=0, row=row, sticky=(EW))
    self.constructionFrame.columnconfigure(0, weight=1)
    ttk.Label(self.constructionFrame, text="Please input the integers for Construction:").grid(column=0, row=0, sticky='EW', columnspan=2)
    ttk.Label(self.constructionFrame, text="S (# of digits in the alphabet)").grid(column=0, row=1)
    self.s_entry = ttk.Entry(self.constructionFrame, textvariable=self.s_int)
    self.s_entry.grid(column=1, row=1)
    ttk.Label(self.constructionFrame, text="N (# of words to Construct)").grid(column=0, row=2)
    self.n_entry = ttk.Entry(self.constructionFrame, textvariable=self.n_int)
    self.n_entry.grid(column=1, row=2)
    ttk.Label(self.constructionFrame, text="L (length of the words to construct)").grid(column=0, row=3)
    self.l_entry = ttk.Entry(self.constructionFrame, textvariable=self.l_int)
    self.l_entry.grid(column=1, row=3)

  def getS(self):
    try: 
        return int(self.s_entry.get()) #note: this will error and return None on floating-point strings like "1.5"
    except (TypeError, ValueError):
        return None
  def getN(self):
    try:
        return int(self.n_entry.get())
    except (TypeError, ValueError): 
        return None
  def getL(self):
    try: 
        return int(self.l_entry.get())
    except (TypeError, ValueError):
        return None
  def getConstructionValues(self):
    return ({"s_int": self.getS(), "n_int": self.getN(), "l_int": self.getL()})

  def hide(self):
        self.constructionFrame.grid_remove()
    
  def show(self):
        self.constructionFrame.grid()

  def set_backgrounds(self, valid):
    if valid:
        self.n_entry["style"] = "Valid.TEntry"
        self.l_entry["style"] = "Valid.TEntry"
        self.s_entry["style"] = "Valid.TEntry"
    else:
        self.n_entry["style"] = "Invalid.TEntry"
        self.l_entry["style"] = "Invalid.TEntry"
        self.s_entry["style"] = "Invalid.TEntry"

  def validate(self, *uselessArgs):
        try: 
            if ((2 <= self.getS() <= 10) and (self.getS() <= self.getL()) and (self.getL() >= 1) and (self.getN() >= 1)):
                self.set_backgrounds(True)
                return True
        except TypeError:
            self.set_backgrounds(False)
            return False
        self.set_backgrounds(False)
        return False

class ApproximationFrame(ttk.Frame): #should have made ApproximationFrame and ConstructionFrame subclasses of a larger class. Perhaps I should do that in the future if there's time
    epsi = None
    disp = None
    dirichletT = None

    def validate(self, *useless):
        if self.getEpsi() is None:
            self.epsi["style"] = "Invalid.TEntry"
        else:   
            self.epsi["style"] = "Valid.TEntry"
        if self.getDisp() is None:
            self.disp["style"] = "Invalid.TEntry"
        else:   
            self.disp["style"] = "Valid.TEntry"
        if self.getT() is None:
            self.dirichletT["style"] = "Invalid.TEntry"
        else:   
            self.dirichletT["style"] = "Valid.TEntry"
        
            
    def __init__(self, root, row):
        self.styling = ttk.Style()
        self.styling.configure("Valid.TEntry", fieldbackground=LIGHTGREEN)
        self.styling.configure("Invalid.TEntry", fieldbackground="white")

        self.epsi_value= StringVar(value="0.01")
        self.epsi_value.trace_add("write", self.validate)

        self.t_value = StringVar(value="2.001")
        self.t_value.trace_add("write", self.validate)

        self.disp_value = StringVar(value="1")
        self.disp_value.trace_add("write", self.validate)

        self.approximationFrame = ttk.Frame(root, relief="solid", borderwidth=2)
        self.approximationFrame.grid(column=0, row=row, sticky=(EW))
        self.approximationFrame.columnconfigure(0, weight=1)
        ttk.Label(self.approximationFrame, text="Please input the parameters for approximation:").grid(column=0, row=0, columnspan=2, sticky='EW')

        ttk.Label(self.approximationFrame, text="Epsilon").grid(column=0, row=1, sticky=E)
        self.epsi = ttk.Entry(self.approximationFrame, textvariable=self.epsi_value)
        self.epsi.grid(column=1, row=1)

        ttk.Label(self.approximationFrame, text="t (Dirichlet distribution parameter)").grid(column=0, row=2, sticky=E)
        self.dirichletT = ttk.Entry(self.approximationFrame, textvariable=self.t_value)
        self.dirichletT.grid(column=1, row=2, sticky=W)

        ttk.Label(self.approximationFrame, text="Displacement").grid(column=0, row=3, sticky=E)
        self.disp = ttk.Entry(self.approximationFrame, textvariable=self.disp_value)
        self.disp.grid(column=1, row=3, sticky=W)

        self.validate()


    def getEpsi(self):
        try:
            val = float(self.epsi_value.get())
            if (val > 0 and val < 1):
                return val
            else: 
                raise ValueError("Epsilon must be between 0 and 1")
        except (TypeError, ValueError):
            return None

    def getDisp(self):
        try: 
            d = int(self.disp_value.get())
            if (d < 0):
                raise ValueError("Displacement cannot be negative")
            return d
        except (TypeError, ValueError):   
            return None

    def getT(self):
        try: 
            val = float(self.t_value.get())
            if val <= 1.0:
                raise ValueError("T must be greater than 1")
            else: 
                return val
        except (TypeError, ValueError):
            return None

    def getApproximationValues(self):
        return ({"epsilon": self.getEpsi(), "displacement": self.getDisp(), "dirichletT": self.getT()})

    def hide(self):
        self.approximationFrame.grid_remove()
    
    def show(self):
        self.approximationFrame.grid()
        


class PropertySelectorFrame(ttk.Frame):
    choices = ["-Please Select-", "Fixed (UD Code, Prefix Code, Suffix Code...)", "Trajectory or Input-Altering Transducer", "Error-Detection via Input-Preserving Transducer", "Error-Correction via Input-Preserving Transducer", "Theta-Transducer Property via Transducer and Antimorphic Permutation"]  
    
    def __init__(self, root, row, property, propertyChangeFunc):

        self.propertyVar = property
        self.propChanger = propertyChangeFunc
        self.propertyVar.trace_add("write", self.propChanger)

        self.propertyFrame = ttk.Frame(root, relief="solid", borderwidth=2)
        self.propertyFrame.grid(column=0, row=row, sticky=(EW))
        self.propertyFrame.columnconfigure(0, weight=1)
        propertyLabel = ttk.Label(self.propertyFrame, text="Please Select a Property")
        propertyLabel.grid(row=0, column=0)
        self.propertyPicker = ttk.Combobox(self.propertyFrame, justify="center", width=58, textvariable=self.propertyVar)
        self.propertyPicker['state'] = 'readonly'
        self.propertyPicker['values'] = self.choices
        self.propertyPicker.current(newindex=0)
        self.propertyPicker.grid(row=1, column=0)

    def updateOptions(self, question):
        if (question == 1):
            self.propertyPicker["values"] = self.choices
        elif (question == 2):
            if (self.getProperty() == 5):
                self.resetProperty()
            self.propertyPicker["values"] = self.choices[0:5]
        elif (question == 3):
            if (self.getProperty() in [4,5]):
                self.resetProperty()
            self.propertyPicker["values"] = self.choices[0:4]
        elif (question == 4):
            if (self.getProperty() == 5):
                self.resetProperty()
            self.propertyPicker["values"] = self.choices[0:5]
        elif (question == 0):
            self.hide()

    def getProperty(self):
        return self.propertyPicker.current()

    def setProperty(self, newProp):
        self.propertyPicker.current(newindex=newProp)

    def resetProperty(self):
        self.setProperty(0)

    def hide(self):
        self.propertyFrame.grid_remove()
    
    def show(self):
        self.propertyFrame.grid()


class FixedTypeSelectorFrame(ttk.Frame):
    choices = ["Prefix", "Suffix", "Infix", "Outfix", "HyperCode", "Code"]  
    #chosenfixedType = StringVar(value="-Please Select-")
    #chosenTypeSave = chosenfixedType.get()
    
    def __init__(self, root, row):
        self.fixedTypeFrame = ttk.Frame(root, relief="solid", borderwidth=2)
        self.fixedTypeFrame.grid(column=0, row=7, sticky=(EW))
        self.fixedTypeFrame.columnconfigure(0, weight=1)
        fixedTypeLabel = ttk.Label(self.fixedTypeFrame, text="Please Select a Fixed Type")
        fixedTypeLabel.grid(row=0, column=0)
        self.fixedTypePicker = ttk.Combobox(self.fixedTypeFrame, justify="center", width=15)
        self.fixedTypePicker['state'] = 'readonly'
        self.fixedTypePicker['values'] = self.choices
        self.fixedTypePicker.current(newindex=0)
        self.fixedTypePicker.grid(row=1, column=0)

    def getFixedType(self):
        return self.fixedTypePicker.current() + 1
    def hide(self):
        self.fixedTypeFrame.grid_remove()
    
    def show(self):
        self.fixedTypeFrame.grid()

#class handling non-interactive instructional parts of the application


class InstructionFrame(ttk.Frame):
    
    def __init__(self, root, message):
        self.mainFrame = ttk.Frame(root, relief="solid")
        self.mainFrame.grid(column=0, row=1, sticky="EWS")
        self.mainFrame.columnconfigure(0, weight=1)
        messageLabel = ttk.Label(self.mainFrame, wraplength=777, text=message)
        messageLabel.grid(row=0, column=0, columnspan=2, sticky=(EW))

    def show(self):
        self.mainFrame.grid()
    def hide(self):
        self.mainFrame.grid_remove()

class AutomataFormatFrame(InstructionFrame):
    
    def __init__(self, root):
        text= "You can use either the Grail or FAdo formats for nondeterministic finite automata" \
        "(those with non-empty transitions). Some points to take into account when"\
        "writing files in either format:\n\n"\
        "1. '#' begins a single-line comment\n"\
        "2. Transitions are written one per line and consist of three space-separated fields: "\
        "(start state) (symbol) (next state)\n\n"\
        "How to write files in the FAdo format:\n"\
        "1. '@NFA' or '@DFA' starts an automaton and determines its type."\
        "It must be followed by a space-separated list of final states on the same line. \n"\
        "2. The initial state of the automaton is the start state of the first transition. \n"\
        "How to write files in the Grail format:\n"\
        "1. The start state is specified using the line (START) |- X "\
        "where X is the number of the start state. " \
        "Only one start state is permitted per automaton.\n"\
        "2. End states are specified using the line Y -| (FINAL). Multiple end states are permitted.\n\n"\
        "Below are some examples of automata in both formats\n"
        super().__init__(root, text)

        #examples for ab*
        Example1Intro = ttk.Label(self.mainFrame, text="Automaton accepting an a followed by 0 or more b's (a*b):")
        FAdoExample1  = ttk.Label(self.mainFrame, text="FAdo:\n@NFA 2\n1 a 2\n2 b 2")
        GrailExample1 = ttk.Label(self.mainFrame, anchor="center", text="Grail:\n(START) |- 1\n1 a 2\n2 b 2")
        Example2Intro = ttk.Label(self.mainFrame, text="Automaton accepting 0 or more a's followed by one or two nines (a*(9+(99))):")
        FAdoExample2  = ttk.Label(self.mainFrame, 
            text="FAdo:\n@NFA 2 3\n1 a 1\n1 9 2\n2 9 3\n2 a 4\n3 a 4\n3 9 4")
        GrailExample2 = ttk.Label(self.mainFrame,
         text="Grail:\n(START) |- 1\n2 -| (FINAL)\n3 -| (FINAL)\n1 a 1\n1 9 2\n2 9 3\n2 a 4\n3 a 4\n3 9 4")
        AdditionalInfo = ttk.Label(self.mainFrame, text="For more examples, please see the instruction manual.")
        Example1Intro.grid(row=1, column=0, columnspan=2)
        FAdoExample1.grid(row=2, column=0)
        GrailExample1.grid(row=2, column=1)
        Example2Intro.grid(row=3, column=0, columnspan=2)
        FAdoExample2.grid(row=4, column=0)
        GrailExample2.grid(row=4, column=1)
        AdditionalInfo.grid(row=5, column=0, columnspan=2)
        for count in range(6):
            self.mainFrame.columnconfigure(count, weight=1)


class TransducerFormatFrame(InstructionFrame):
    text = "The only transducer format accepted is the FAdo tarnsducer format. Complete " \
           "details are available at fado.dcc.fc.up.pt, below are concise formatting instructions.\n\n" \
           "1. '#' begins a single-line comment.\n" \
           "2. '@Transducer' begins the transducer, and this must be followed by a space-separated " \
           "list of final states.\n" \
           "3. Transitions are given one per line and must be in the form " \
           "(start state) (input) (output) (next state)\n" \
           "4. The initial state is the start state of the first transition.\n\n"
           
    

#code that gets run when the python file runs
class MainApplication(Tk):
      
    def collect_data(self):
        data = {}
        data["question"] = self.Question.getQuestionNumber()
        data["automata_text"] = self.AutomatonInput.get_data()
        data |= self.Approximation.getApproximationValues()
        data['property_type'] = self.PropSelector.getProperty()
        data |= self.ConstructionIntegers.getConstructionValues()
        data["fixed_type"] = self.FixedSelector.getFixedType()
        data["theta_text"] = self.ThetaInput.get_data()
        data["transducer_text"] = self.TransInput.get_data()
        try:
            data["time_limit"] = float(self.timeLimit.get())
            if data["time_limit"] <= 0:
                data["time_limit"] = None
        except ValueError:
            data["time_limit"] = None
        self.Result.setResult("Calculating... this may take a while")
        Tk.update(self) #force the "Calculating..." text to appear
        self.Result.setResult(handlers.get_response(data))

    def __init__(self):
        super().__init__()
        self.title("I-LaSer Local Version")


        #these need to be class variables so that they persist
        self.question = StringVar()
        self.property_type = StringVar()
        self.fixed_type = StringVar()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.minsize(800,300)

        root = ttk.Frame(self)
        root.grid(column=0, row=0, sticky="nesw")
        root.columnconfigure(0, weight=1)
            

        menuFrame = ttk.Frame(root, relief="solid", borderwidth=2)
        menuFrame.grid(column=0, row=0, sticky="NEW")
        menuFrame.columnconfigure(0, weight=1)

        #initialize all of the buttons in the same order as I-LaSer website. 
        #they currently have no styling
        ttk.Button(menuFrame, text="Home").grid(column=0, row=0, sticky=(N)) #home button
        ttk.Button(menuFrame, text="Automata Format").grid(column=1, row=0, sticky=(N))
        ttk.Button(menuFrame, text="Transducer Format").grid(column=2, row=0, sticky=(N))
        ttk.Button(menuFrame, text="Trajectory Format").grid(column=3, row=0, sticky=(N))
        ttk.Button(menuFrame, text="Antimorphism Format").grid(column=4, row=0, sticky=(N))
        ttk.Button(menuFrame, text="Technical Notes").grid(column=5, row=0, sticky=(N))
        ttk.Button(menuFrame, text="Credits").grid(column=6, row=0, sticky=(N))
        
        #self.AutomatonInstructions = AutomataFormatFrame(root)

        
        self.Result = ResultFrame(root, 1)
        self.Question = QuestionFrame(root, 2, self.question, self.reactToQuestionChange)
        self.AutomatonInput = AutomatonFrame(root, 3)
        self.ConstructionIntegers = ConstructionFrame(root, 4)
        self.Approximation = ApproximationFrame(root, 5)
        self.PropSelector = PropertySelectorFrame(root, 6, self.property_type, self.reactToPropChange)
        self.FixedSelector = FixedTypeSelectorFrame(root, 7)
        self.TransInput = TransducerFrame(root, 8)
        self.ThetaInput = ThetaFrame(root, 9)
        

        #submit button and time limit
        self.submitFrame = ttk.Frame(root, relief="solid", borderwidth=2)
        self.submitFrame.grid(column=0, row=10, sticky=(EW))
        self.submitFrame.columnconfigure(0, weight=1)
        ttk.Button(self.submitFrame, text="Submit Request", default="active", command=self.collect_data).grid(column=0, row=0)
        ttk.Label(self.submitFrame, text="Time Limit in Seconds:", borderwidth=2).grid(column=1, row=0, sticky=E)
        self.timeLimit = ttk.Entry(self.submitFrame)
        self.timeLimit.grid(column=2, row=0, sticky=W)
        self.timeLimit.insert(0, "60")

        for count in range(11):
            menuFrame.rowconfigure(count, weight=1)

        self.reactToQuestionChange()
        self.reactToPropChange()
        

    def reactToQuestionChange(self, *useless):
        #called whenever the shared variable "question" is modified, to update which 
        #pieces of the program are shown and hidden
        question = self.Question.getQuestionNumber()
        self.AutomatonInput.hide() #always hide first so there is no chance of a double-frame
        if (question in [1,2,4]):
            self.AutomatonInput.show()
        self.ConstructionIntegers.hide()
        if (question == 3):
            self.ConstructionIntegers.show()
        self.PropSelector.hide()
        if (question != 0):
            self.PropSelector.show()
            self.PropSelector.updateOptions(question)
        self.Approximation.hide()
        if (question == 4):
            self.Approximation.show()
        self.submitFrame.grid_remove()
        if (question != 0): #do not show the submit button if no question selected
            self.submitFrame.grid()
        self.Result.hide()
    
    def reactToPropChange(self, *useless):
        property_type = self.PropSelector.getProperty()
        self.FixedSelector.hide()
        if (property_type == 1):
            self.FixedSelector.show()
        self.TransInput.hide()
        if (property_type in [2,3,4,5]):
            self.TransInput.show()
        self.ThetaInput.hide()
        if (property_type == 5):
            self.ThetaInput.show()
        self.Result.hide()
        
        


window = MainApplication()
window.resizable(width=False, height=True)
window.mainloop() #open the actual GUI window and start responding to inputs