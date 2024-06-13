from tkinter import *
from tkinter import ttk
#from laser import * 
#put a laser folder beneath current directory and put all non-views files from transducer there
#will need to create a specific code_gen file which can handle the get_code method inside views
#without  using HTML/Django code. 





def createMenuFrame(root):
    menuFrame = ttk.Frame(root)
    menuFrame.grid(column=0, row=0, sticky=(N))

    #initialize all of the buttons in the same order as I-LaSer website. 
    #they currently have no styling
    ttk.Button(menuFrame, text="Home").grid(column=0, row=0, sticky=(N)) #home button
    ttk.Button(menuFrame, text="Automata Format").grid(column=1, row=0, sticky=(N))
    ttk.Button(menuFrame, text="Transducer Format").grid(column=2, row=0, sticky=(N))
    ttk.Button(menuFrame, text="Trajectory Format").grid(column=3, row=0, sticky=(N))
    ttk.Button(menuFrame, text="Antimorphism Format").grid(column=4, row=0, sticky=(N))
    ttk.Button(menuFrame, text="Technical Notes").grid(column=5, row=0, sticky=(N))
    ttk.Button(menuFrame, text="Credits").grid(column=6, row=0, sticky=(N))

def createResultFrame(root, result=None):
    resultFrame = ttk.Frame(root)
    if result is not None:
        resultFrame.grid(column=0, row=1)
        resultLabel = ttk.Label(resultFrame, text=result)
        resultLabel.grid(column=0, row=0)
    

def createQuestionFrame(root):
    choices = ["-Please Select-", "Satisfaction", "Maximality", "Construction", "Approximate Maximality"]  
    chosenQuestion = StringVar(value="-Please Select-")
    chosenQuestionSave = chosenQuestion.get() #shenanigans to keep the variable alive for default selection
    
    questionFrame = ttk.Frame(root)
    questionFrame.grid(column=0, row=2) #result is above it, though if result doesn't exist, it doesn't take up space
    questionLabel = ttk.Label(questionFrame, text="What question would you like to solve?")
    questionLabel.grid(row=0, column=0)
    questionPicker = ttk.Combobox(questionFrame, justify="center")
    questionPicker['state'] = 'readonly'
    questionPicker['values'] = choices
    questionPicker.current(newindex=0)
    questionPicker.grid(row=1, column=0)

def createAutomatonFrame(root):
    aut_frame = ttk.Frame(root)
    aut_frame.grid(column=0, row=3)
    ttk.Label(aut_frame, text="Provide a Language File via\nautomaton or Regular Expression").grid(column=0, row=0)
    ttk.Button(aut_frame, text="Select Automaton File").grid(column=0, row=1)
    ttk.Label(aut_frame, text="Or enter an automaton or Regular Expression here").grid(column=1, row=0)
    Text(aut_frame, width=40, height=10).grid(column=1, row=1)

def createConstructionFrame(root):
    constructionFrame = ttk.Frame(root)
    constructionFrame.grid(column=0, row=4)
    ttk.Label(constructionFrame, text="Please input the integers for Construction:").grid(column=0, row=0, sticky='EW')
    ttk.Label(constructionFrame, text="S (# of digits in the alphabet)").grid(column=0, row=1)
    ttk.Entry(constructionFrame).grid(column=1, row=1)
    ttk.Label(constructionFrame, text="N (# of words to Construct)").grid(column=0, row=2)
    ttk.Entry(constructionFrame).grid(column=1, row=2)
    ttk.Label(constructionFrame, text="L (length of the words to construct)").grid(column=0, row=3)
    ttk.Entry(constructionFrame).grid(column=1, row=3)
    

def createApproximationFrame(root):
    approximationFrame = ttk.Frame(root)
    approximationFrame.grid(column=0, row=4)
    ttk.Label(approximationFrame, text="Please input the integers for approximation:").grid(column=0, row=0, sticky='EW')
    ttk.Label(approximationFrame, text="Epsilon").grid(column=0, row=1)
    ttk.Entry(approximationFrame).grid(column=1, row=1)
    ttk.Label(approximationFrame, text="t (Dirichlet distribution parameter)").grid(column=0, row=2)
    ttk.Entry(approximationFrame).grid(column=1, row=2)
    ttk.Label(approximationFrame, text="Displacement").grid(column=0, row=3)
    ttk.Entry(approximationFrame).grid(column=1, row=3)

def createPropSelectorFrame(root):
    choices = ["-Please Select-", "Fixed (UD Code, Prefix Code, Suffix Code...)", "Trajectory or Input-Altering Transducer", "Error-Detection via Input-Preserving Transducer", "Error-Correction via Input-Preserving Transducer", "Theta-Transducer Property via Transducer and Antimorphic Permutation"]  
    chosenProperty = StringVar(value="-Please Select-")
    chosenPropSave = chosenProperty.get() #shenanigans to keep the variable alive for default selection
    
    propertyFrame = ttk.Frame(root)
    propertyFrame.grid(column=0, row=5)
    propertyLabel = ttk.Label(propertyFrame, text="Please Select a Property")
    propertyLabel.grid(row=0, column=0)
    propertyPicker = ttk.Combobox(propertyFrame, justify="center", width=58)
    propertyPicker['state'] = 'readonly'
    propertyPicker['values'] = choices
    propertyPicker.current(newindex=0)
    propertyPicker.grid(row=1, column=0)

def createFixedTypeSelectorFrame(root):
    choices = ["-Please Select-", "Prefix", "Suffix", "Infix", "Outfix", "HyperCode", "Code"]  
    chosenfixedType = StringVar(value="-Please Select-")
    chosenTypeSave = chosenfixedType.get()
    
    fixedTypeFrame = ttk.Frame(root)
    fixedTypeFrame.grid(column=0, row=6)
    fixedTypeLabel = ttk.Label(fixedTypeFrame, text="Please Select a Fixed Type")
    fixedTypeLabel.grid(row=0, column=0)
    fixedTypePicker = ttk.Combobox(fixedTypeFrame, justify="center", width=15)
    fixedTypePicker['state'] = 'readonly'
    fixedTypePicker['values'] = choices
    fixedTypePicker.current(newindex=0)
    fixedTypePicker.grid(row=1, column=0)
    

#code that gets run when the python file runs
root = Tk()
root.title("I-LaSer")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
createMenuFrame(root)
createQuestionFrame(root)
createAutomatonFrame(root)
createConstructionFrame(root)
createApproximationFrame(root)
createPropSelectorFrame(root)
createFixedTypeSelectorFrame(root)

root.mainloop() #open the actual GUI window


