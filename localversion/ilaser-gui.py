from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import re
#from laser import * 
#put a laser folder beneath current directory and put all non-views files from transducer there
#will need to create a specific code_gen file which can handle the get_code method inside views
#without  using HTML/Django code. 

#also need to put all FAdo files in a subfolder of laser folder. 

class ResultFrame(ttk.Frame):
    def __init__(self, parent, row, result):
        resultFrame = ttk.Frame(parent, relief="solid", borderwidth=2)
        if result is not None:
            resultFrame.grid(column=0, row=row)
            resultFrame.columnconfigure(0, weight=1)
            resultLabel = ttk.Label(resultFrame, text=result)
            resultLabel.grid(column=0, row=0)
    

class QuestionFrame(ttk.Frame):
    choices = ["-Please Select-", "Satisfaction", "Maximality", "Construction", "Approximate Maximality"]  
    #chosenQuestion = StringVar(value="-Please Select-")
    #chosenQuestionSave = chosenQuestion.get() #shenanigans to keep the variable alive for default selection


    def __init__(self, root, row):
        questionFrame = ttk.Frame(root, relief="raised", borderwidth=2)
        questionFrame.grid(column=0, row=row, sticky=(EW)) #result is above it, though if result doesn't exist, it doesn't take up space
        questionFrame.columnconfigure(0, weight=1)
        questionLabel = ttk.Label(questionFrame, text="What question would you like to solve?")
        questionLabel.grid(row=0, column=0)
        self.questionPicker = ttk.Combobox(questionFrame, justify="center")
        self.questionPicker['state'] = 'readonly'
        self.questionPicker['values'] = self.choices
        self.questionPicker.current(newindex=0)
        self.questionPicker.grid(row=1, column=0)

    def getQuestionNumber():
        return self.questionPicker.current()
        
        

class LargeEntryFrame(ttk.Frame):
#used for automaton, transducer, and theta. has a file upload button on the left, and
#a textbox on the right. tries to validate inputs but still allows submission of 
#invalid inputs. 
    
  userinput = None
  validation = None

  def validate(self):
    for pattern in self.validation:
        if re.match(pattern, self.get_data(), re.IGNORECASE):
            print("Input validates")
            return True
    print("Input does not validate")
    return False
    
  def get_data(self):
    return self.userinput.get(0, "end")

  def get_file_to_data(self,windowTitle="Select File..."):
    self.userinput.delete(0, "end")
    with fd.askopenfile(mode="r", title=windowTitle) as input_file:
        self.userinput.insert(0, input_file.read())


  def __init__(self, root, row, file_request_text, file_button_text, textbox_label, validation_regex):
    self.validation = validation_regex
    aut_frame = ttk.Frame(root, relief="solid", borderwidth=2)
    aut_frame.grid(column=0, row=row, sticky=(EW))
    aut_frame.columnconfigure(0, weight=1)
    ttk.Label(aut_frame, text=file_request_text).grid(column=0, row=0)
    ttk.Button(aut_frame, text=file_button_text, command=self.get_file_to_data).grid(column=0, row=1)
    ttk.Label(aut_frame, text=textbox_label).grid(column=1, row=0)
    self.userinput = Text(aut_frame, width=40, height=10, wrap="none")
    self.userinput.grid(column=1, row=1)
    self.userinput.tag_bind("important", "<<Modified>>", self.validate)
  
  

class AutomatonFrame(LargeEntryFrame):
    REGEX_PATTERN = r"^[0-9A-Za-z()+*]+$" #for the user to input a regex in the NFA area
    #a single unrestricted line. balanced brackets is not possible and the handler will error
    #anyways if it cannot parse the regex. 
    GRAIL_PATTERN = r"^\(START\) +\|- +\d+(?:(?:\r?\n\d+ [0-9A-Za-z] \d)|(?:\r?\n\d+ +-\| +\(FINAL\)))+$"
    FADO_PATTERN = r"^@[ND]FA(?: +\d+)+(?:\r?\n\d+ +[0-9A-Za-z] +\d+)+$"
              
    def __init__(self, root, row):
        super().__init__(root, row, "Choose an automaton file", "Select Automaton File", "Or enter an automaton or regex in this text area.", (self.REGEX_PATTERN, self.GRAIL_PATTERN, self.FADO_PATTERN))

class TransducerFrame(LargeEntryFrame):
    TRANS_PATTERN = r"^(?:(@InputAltering|@ErrorDetecting|@ErrorCorrecting)\r?\n)?@Transducer(?: \d+)+(?:\r?\n\d+ +[0-9A-Za-z] +[0-9A-Za-z] +\d+)+$"
    TRAJ_PATTERN = r"^[01*+)( ]+$"

    def __init__(self, root, row):
        super().__init__(root, row, "Choose a transducer file", "Select Transducer File", "Or enter a transducer or trajectory in that text area.", (self.TRANS_PATTERN, self.TRAJ_PATTERN))

class ThetaFrame(LargeEntryFrame):
    THETA_PATTERN = r"^@Theta\r?(?:\n[A-Za-z0-9]\s+[A-Za-z0-9])+$"
    
    def __init__(self, root, row):
        super().__init__(root, row, "Choose a Theta File", "Select Theta File", "Or enter an antimorphism here", (self.THETA_PATTERN,))


class ConstructionFrame(ttk.Frame):
  s_entry = None
  n_entry = None
  l_entry = None   

  def __init__(self, root, row):
    constructionFrame = ttk.Frame(root, relief="solid", borderwidth=2)
    constructionFrame.grid(column=0, row=row, sticky=(EW))
    constructionFrame.columnconfigure(0, weight=1)
    ttk.Label(constructionFrame, text="Please input the integers for Construction:").grid(column=0, row=0, sticky='EW')
    ttk.Label(constructionFrame, text="S (# of digits in the alphabet)").grid(column=0, row=1)
    self.s_entry = ttk.Entry(constructionFrame)
    self.s_entry.grid(column=1, row=1)
    ttk.Label(constructionFrame, text="N (# of words to Construct)").grid(column=0, row=2)
    self.n_entry = ttk.Entry(constructionFrame)
    self.n_entry.grid(column=1, row=2)
    ttk.Label(constructionFrame, text="L (length of the words to construct)").grid(column=0, row=3)
    self.l_entry = ttk.Entry(constructionFrame)
    self.l_entry.grid(column=1, row=3)

  def getS(self):
    return int(self.s_entry.get())
  def getN(self):
    return int(self.n_entry.get())
  def getL(self):
    return int(self.l_entry.get())
  def getConstructionValues(self):
    return (self.getS(), self.getN(), self.getL())

class ApproximationFrame(ttk.Frame):
    epsi = None
    disp = None
    dirichletT = None
            
    def __init__(self, root, row):
        approximationFrame = ttk.Frame(root, relief="solid", borderwidth=2)
        approximationFrame.grid(column=0, row=row, sticky=(EW))
        approximationFrame.columnconfigure(0, weight=1)
        ttk.Label(approximationFrame, text="Please input the parameters for approximation:").grid(column=0, row=0, sticky='EW')
        ttk.Label(approximationFrame, text="Epsilon").grid(column=0, row=1, sticky=E)
        self.epsi = ttk.Entry(approximationFrame)
        self.epsi.grid(column=1, row=1)
        self.epsi.insert(0, "0.01")
        ttk.Label(approximationFrame, text="t (Dirichlet distribution parameter)").grid(column=0, row=2, sticky=E)
        self.dirichletT = ttk.Entry(approximationFrame)
        self.dirichletT.grid(column=1, row=2, sticky=W)
        self.dirichletT.insert(0, "2.001")
        ttk.Label(approximationFrame, text="Displacement").grid(column=0, row=3, sticky=E)
        self.disp = ttk.Entry(approximationFrame)
        self.disp.grid(column=1, row=3, sticky=W)
        self.disp.insert(0, "1")

    def getEpsi(self):
        try:
            return float(self.epsi.get())
        except ValueError:
            return 0.01
    def getDisp(self):
        try: 
            return int(self.disp.get())
        except ValueError:   
            return 1
    def getT(self):
        try: 
            return float(self.dirichletT.get())
        except ValueError:
            return 2.001
    def getApproximationValues(self):
        return (self.getEpsi(), self.getDisp(), self.getT())
        


class PropertySelectorFrame(ttk.Frame):
    choices = ["-Please Select-", "Fixed (UD Code, Prefix Code, Suffix Code...)", "Trajectory or Input-Altering Transducer", "Error-Detection via Input-Preserving Transducer", "Error-Correction via Input-Preserving Transducer", "Theta-Transducer Property via Transducer and Antimorphic Permutation"]  
    #chosenProperty = StringVar(value="-Please Select-")
    propertyPicker = None
    
    def __init__(self, root, row):
        propertyFrame = ttk.Frame(root, relief="solid", borderwidth=2)
        propertyFrame.grid(column=0, row=row, sticky=(EW))
        propertyFrame.columnconfigure(0, weight=1)
        propertyLabel = ttk.Label(propertyFrame, text="Please Select a Property")
        propertyLabel.grid(row=0, column=0)
        self.propertyPicker = ttk.Combobox(propertyFrame, justify="center", width=58)
        self.propertyPicker['state'] = 'readonly'
        self.propertyPicker['values'] = self.choices
        self.propertyPicker.current(newindex=0)
        self.propertyPicker.grid(row=1, column=0)

    def getProperty(self):
        return self.propertyPicker.current()


class FixedTypeSelectorFrame(ttk.Frame):
    choices = ["-Please Select-", "Prefix", "Suffix", "Infix", "Outfix", "HyperCode", "Code"]  
    #chosenfixedType = StringVar(value="-Please Select-")
    #chosenTypeSave = chosenfixedType.get()
    
    def __init__(self, root, row):
        fixedTypeFrame = ttk.Frame(root, relief="solid", borderwidth=2)
        fixedTypeFrame.grid(column=0, row=7, sticky=(EW))
        fixedTypeFrame.columnconfigure(0, weight=1)
        fixedTypeLabel = ttk.Label(fixedTypeFrame, text="Please Select a Fixed Type")
        fixedTypeLabel.grid(row=0, column=0)
        self.fixedTypePicker = ttk.Combobox(fixedTypeFrame, justify="center", width=15)
        self.fixedTypePicker['state'] = 'readonly'
        self.fixedTypePicker['values'] = self.choices
        self.fixedTypePicker.current(newindex=0)
        self.fixedTypePicker.grid(row=1, column=0)

    def getFixedType(self):
        return self.fixedTypePicker.current()

    


#code that gets run when the python file runs
class MainApplication(Tk):

    def __init__(self):
        super().__init__()
        self.title("I-LaSer Local Version")


        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.minsize(800,300)

        root = ttk.Frame(self)
        root.grid(column=0, row=0, sticky="nesw")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

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

        Question = QuestionFrame(root, 2)
        AutomatonInput = AutomatonFrame(root, 3)
        ConstructionIntegers = ConstructionFrame(root, 4)
        Approximation = ApproximationFrame(root, 5)
        PropSelector = PropertySelectorFrame(root, 6)
        FixedSelector = FixedTypeSelectorFrame(root, 7)
        TransInput = TransducerFrame(root, 8)
        ThetaInput = ThetaFrame(root, 9)

        #submit button and time limit
        submitFrame = ttk.Frame(root, relief="solid", borderwidth=2)
        submitFrame.grid(column=0, row=10, sticky=(EW))
        submitFrame.columnconfigure(0, weight=1)
        ttk.Button(submitFrame, text="Submit Request", default="active").grid(column=0, row=0)
        ttk.Label(submitFrame, text="Time Limit in Seconds:", borderwidth=2).grid(column=1, row=0, sticky=E)
        timeLimit = ttk.Entry(submitFrame)
        timeLimit.grid(column=2, row=0, sticky=W)
        timeLimit.insert(0, "60")



window = MainApplication()
window.mainloop() #open the actual GUI window

