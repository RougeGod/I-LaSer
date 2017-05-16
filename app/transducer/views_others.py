"""
The views_others.py program handles the "other" part of the site.
"""

from django.shortcuts import render_to_response
from django.shortcuts import render

from FAdo.codes import exponentialDensityP, editDistanceW

from app.transducer.forms import UploadFileForm
from app.transducer.laser_shared import construct_automaton, IncorrectFormat, \
     isLimitExceedForEditDist

#@login_required
def upload_file(request):
    """Handles the form uploading and parsing."""
    if request.method == 'POST':
        response = get_response(request.POST, request.FILES, UploadFileForm())

        return render(request, 'upload_others.html', response)

def get_response(post, files, form=None):
    """
    This handles lighter tasks that can be safely computed on the server.
    It gives the response to the user via the webpage
    """
    form = UploadFileForm(post, files) if form else None

    choice = post.get('choice')

    if not choice:
        return {'form':form, 'result': 'Please choose an option.'}

    file_ = files.get('automata_file')

    if not file_:
        return {'form':form, 'result': 'Please provide an automaton file.'}

    aut_str = file_.read()
    aut_name = "Language: " + file_.name
    file_.close()

    try:
        automaton = construct_automaton(aut_str)
    except (IncorrectFormat, TypeError):
        return {'form':form, 'result':'The automaton appears to be formatted incorrectly.'}

    limit = isLimitExceedForEditDist(automaton)
    if limit:
        return {'form':form, 'automaton':aut_name, 'result':
                'Size of the automaton exceeds limit! (See Technical Notes below)'}

    if choice == "1":
        edit_distance = editDistanceW(automaton)

        decision = "The edit distance of this language is '" + str(edit_distance[0]) + "'."
        proof = "Witness: Two words with this distance are " + str(edit_distance[1]) + "."

        return {'form':form, 'automaton':aut_name, 'result':decision, 'proof': proof}
    elif choice == "2":
        try:
            exp_dense = exponentialDensityP(automaton)
        except TypeError:
            decision = ""
            return {'form':form, 'result':
                    'The automaton appears to be formatted incorrectly!'}

        if exp_dense:
            decision = "YES! The language has exponential density."
        else:
            decision = "NO! The language does not have exponential density."

        proof = ""
        return {'form':form, 'automaton':aut_name, 'result':decision, 'proof': proof}

    return {'form':form}

#@login_required
def index(_):
    """renders index.html"""
    return render_to_response('index.html')


def examples(_, example_type):
    """Returns the various examples"""
    return render_to_response('examples/'+example_type+'.html')
