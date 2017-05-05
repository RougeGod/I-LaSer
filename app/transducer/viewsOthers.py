from forms import UploadFileForm
from django.shortcuts import render_to_response
from django.shortcuts import render

from FAdo.codes import exponentialDensityP, editDistanceW
from laserShared import construct_automaton, IncorrectFormat, isLimitExceedForEditDist



#@login_required
def upload_file(request):
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        try:
            choice = request.POST['choice']
        except Exception, ex:
            decision = "Please choose an option."
            return render(request, 'upload_others.html', {'form':form, 'result': decision})



        try:
            autStr = request.FILES['automata_file'].read()
        except Exception:
            decision = "Please provide an automaton file."
            return {'form':form, 'result': decision}
        automatonName = "Language: " + request.FILES['automata_file'].name

        try:
            automaton = construct_automaton(autStr)
        except IncorrectFormat:
            decision = "The automaton appears to be formatted incorrectly!"
            return render(request,'upload_others.html', {'form':form, 'result': decision})
        except TypeError:
            decision = "The automaton appears to be formatted incorrectly!"
            return render(request,'upload_others.html', {'form':form, 'result': decision})

        limit = isLimitExceedForEditDist(automaton)
        if limit:
          decision = "Size of the automaton exceeds limit! (See Technical Notes below)"
          return render(request,'upload_others.html', {'form':form, 'automaton':automatonName, 'result': decision})


        if choice == "1":

            ED = editDistanceW(automaton)

            decision = "The edit distance of this language is '" + str(ED[0]) + "'."
            proof = "Witness: Two words with this distance are " + str(ED[1]) + "."

            return render(request,'upload_others.html', {'form':form, 'automaton':automatonName, \
                    'result':decision, 'proof': proof})
        elif choice == "2":
            try:
                expDense = exponentialDensityP(automaton)
            except TypeError:
                decision = "The automaton appears to be formatted incorrectly!"
                return render(request,'upload_others.html', {'form':form, 'result': decision})

            if expDense == True:
                decision = "YES! The language has exponential density."
            else:
                decision = "NO! The language does not have exponential density."

            proof = ""
            return render(request, 'upload_others.html', {'form':form, 'automaton':automatonName, \
                    'result':decision, 'proof': proof})
        else:
            return render(request, 'upload_others.html', {'form':form})

    return render(request, 'upload_others.html', {'form':form})

def getResponse(post, files):
    # ToDo: factor code out of upload_file()
    pass

#@login_required
def index(request):
    return render_to_response('index.html')


def examples(request, example_type):
    return render_to_response('examples/'+example_type+'.html')


