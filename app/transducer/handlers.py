"""Module contains all of the various handlers for different branches of the site."""

import django
from django.conf import settings

from FAdo.fio import readOneFromString

import FAdo.codes as codes
from FAdo.codes import UDCodeProp, PropertyNotSatisfied, IPTProp, DFAsymbolUnknown, \
    ErrCorrectProp
from FAdo.yappy_parser import YappyError

from app.transducer.laser_shared import construct_automaton, IncorrectFormat, \
     construct_input_alt_prop, limit_aut_prop, limit_tran_prop, format_counter_example, \
     make_block_code

from app.transducer.util import create_fixed_property, write_witness, get_fixed_type

PROPERTY_INCORRECT_FORMAT = 'The property appears to be incorrectly formatted.'

try:
    LIMIT = settings.LIMIT
    LIMIT_AUTOMATON = settings.LIMIT_AUTOMATON
except django.core.exceptions.ImproperlyConfigured:
    LIMIT = 500000
    LIMIT_AUTOMATON = 250


def handle_iap(
        n_num, l_num, s_num,
        t_name, t_str, form=True
    ):
    """Handle Input-altering properties"""
    alphabet = set()
    for i in range(int(s_num)):
        alphabet.add(str(i))

    try:
        prop = construct_input_alt_prop(t_str, alphabet)
    except (IncorrectFormat, TypeError):
        return {'form': form, 'error_message':PROPERTY_INCORRECT_FORMAT,
                'transducer': t_name}

    if limit_tran_prop({}, prop.Aut.delta, LIMIT, int(n_num)):
        return {'form':form, 'error_message':
                "Size of request exceeds limit! (See 'Technical Notes')"}

    try:
        _, witness = prop.makeCode(n_num, l_num, s_num)
    except DFAsymbolUnknown:
        return {'form': form, 'error_message':PROPERTY_INCORRECT_FORMAT,
                'transducer': t_name}

    words = write_witness(witness)
    result = '<div class="text-center" style="font-size: 14px; color: #999999; \
    margin-bottom: 10px;"> Your Output</div><div><textarea class="text-center" \
    rows="6" cols="50" readonly>'+ words +'</textarea></div>'
    return {'form': form, 'construct_path': '',
            'construct_text': '', 'result': result}

def handle_ipp(
        n_num, l_num, s_num,
        t_name, t_str, form=True
    ):
    """Handle Input-preserving properties"""
    try:
        prop = codes.buildErrorDetectPropS(t_str)
    except (YappyError, AttributeError):
        return {'form':form, 'error_message':PROPERTY_INCORRECT_FORMAT,
                'transducer':t_name}

    if limit_tran_prop({}, prop.Aut.delta, LIMIT, int(n_num)):
        return {'form':form, 'error_message':
                'Size of request exceeds limit! (See "Technical Notes")'}

    try:
        _, witness = prop.makeCode(int(n_num), int(l_num), int(s_num))
    except DFAsymbolUnknown:
        return {'form': form, 'error_message':PROPERTY_INCORRECT_FORMAT,
                'transducer': t_name}

    #text_path, text_title = write_witness(witness, filename)
    words = write_witness(witness)
    result = '<div class="text-center" style="font-size: 14px; color: #999999; \
    margin-bottom: 10px;"> Your Output</div><div><textarea class="text-center" \
    rows="6" cols="50" readonly>'+ words +'</textarea></div>'
    return {'form': form, 'witness': witness, 'prop': prop,
            'construct_path': '', 'construct_text': '', 'result': result}

def handle_construction(
        property_type, post,
        files, form=True
    ):
    """
    Handle the construction choice of the website.
    """

    def error(err):
        """Formats an error using the given string"""
        return {'form': form, 'error_message': err}

    n_num = int(post.get("n_int", -1))
    s_num = int(post.get("s_int", -1))
    l_num = int(post.get("l_int", -1))

    err = ''
    if n_num <= 0 or s_num <= 0 or l_num <= 0:
        err = "Please enter three positive integers S, N, L."
    elif s_num < 2 or s_num > 10:
        err = "S must be less than 10 and greater than 1"
    elif s_num > l_num:
        err = "S must be less than L"

    if err:
        return error(err)

    if property_type == "1":
        if (n_num * l_num) > LIMIT:
            return error("Size of request exceeds limit! (See 'Technical Notes')")
        try:
            _, witness = make_block_code(int(n_num), int(l_num), int(s_num))
        except DFAsymbolUnknown:
            return error("Something went wrong (views.py: construction, fixed property).")
        #text_path, text_title = write_witness(witness, filename)
        words = write_witness(witness)
        result = '<div class="text-center" style="font-size: 14px; \
        color: #999999; margin-bottom: 10px;">Your Output</div>\
        <div><textarea class="text-center" rows="6" cols="50" \
        readonly>'+ words +'</textarea></div>'
        return {'form': form, 'construct_path': '',
                'construct_text': '', 'result': result}

    file_ = files.get('transducer_file')
    if not file_:
        return error("Please provide a correct property file.")

    t_str = file_.read()
    t_name = "Property: " + file_.name
    file_.close()

    # Input-Altering Property (given as trajectory or transducer)
    if property_type == "2":
        result = handle_iap(n_num, l_num, s_num, t_name, t_str, form)
    # Input-Preserving Property
    elif property_type == "3":
        result = handle_ipp(n_num, l_num, s_num, t_name, t_str, form)

    return result

def handle_satisfaction_maximality(
        property_type, question, post,
        files, form=True
    ):
    """This method handles satisfaction and maximality choices."""

    def error(err):
        """Formats an error using the given string"""
        return {'form': form, 'error_message': err}

    file_ = files.get('automata_file')

    if file_: # Get it from the file by default
        # automaton string
        aut_str = file_.read()

        #automaton name
        aut_name = "Language: " + file_.name

        file_.close()
    elif post.get('automata_text'):
        # automaton string
        aut_str = str(post.get('automata_text'))

        #automaton name
        aut_name = "Language: N/A"
    else:
        return error('Please provide an automaton file.')

    aut_str, fixed_type = get_fixed_type(aut_str)

    try:
        aut = construct_automaton(aut_str)
    except (IncorrectFormat, TypeError):
        return {'form': form, 'error_message':PROPERTY_INCORRECT_FORMAT,
                'automaton': aut_name}

    if limit_aut_prop(aut, LIMIT_AUTOMATON):
        return {'form':form, 'error_message':
                'Size of the automaton exceeds limit! (See "Technical Notes")',
                'automaton':aut_name}
    if property_type == "1": # Fixed type
        t_name = ""
        if fixed_type is None:
            fixed_type = post.get('fixed_type')

        prop = create_fixed_property(aut.Sigma, fixed_type)
        if prop is None:
            prop = UDCodeProp(aut.Sigma)
            proof = ''
            if question == '1':
                witness = prop.notSatisfiesW(aut)
                if witness == (None, None):
                    decision = "YES, the language satisfies the code property"
                else:
                    decision = "NO, the language does not satisfy the code property"
                    proof = format_counter_example(witness)
            else:
                try:
                    if prop.maximalP(aut):
                        decision = "YES, the language is a maximal code"
                    else:
                        decision = "NO, the language is not a maximal code"
                except PropertyNotSatisfied:
                    decision = "ERROR: the language doesn't satisfy the property."

            return {'form': form, 'automaton': aut_name, 'result': decision, 'proof': proof}

    # User-Input Property
    else:
        file_ = files.get('transducer_file')

        if file_: # Get it from the file by default
            # automaton string
            t_str = file_.read()

            #automaton name
            t_name = "Property: " + file_.name

            file_.close()
        elif post.get('transducer_text'):
            # automaton string
            t_str = str(post.get('transducer_text'))

            #automaton name
            t_name = "Property: N/A"
        else:
            return error('Please provide a property file.')

        # Input-Altering Property (given as trajectory or transducer)
        if property_type == "2":
            try:
                prop = construct_input_alt_prop(t_str, aut.Sigma)
            except (IncorrectFormat, TypeError):
                return {'form':form, 'error_message': PROPERTY_INCORRECT_FORMAT,
                        'automaton':aut_name, 'transducer':t_name}

        # Input-Preserving Property
        elif property_type == "3":
            try:
                prop = IPTProp(readOneFromString(t_str))
            except (YappyError, AttributeError):
                return {'form':form, 'error_message': PROPERTY_INCORRECT_FORMAT,
                        'automaton':aut_name, 'transducer':t_name}

        # Error-Correction
        elif property_type == "4":
            try:
                prop = ErrCorrectProp(readOneFromString(t_str))
            except (YappyError, AttributeError):
                return {'form':form, 'error_message': PROPERTY_INCORRECT_FORMAT,
                        'automaton':aut_name, 'transducer':t_name}

    if limit_tran_prop(aut.delta, prop.Aut.delta, LIMIT):
        return {'form':form, 'error_message':
                'Sizes of the automaton and transducer exceed limit! (See "Technical Notes")',
                'automaton':aut_name, 'transducer':t_name}
    else:
        if question == "1":
            try:
                witness = prop.notSatisfiesW(aut)
            except TypeError:
                decision = "The automaton file appears to be incorrectly formatted."
                return {'form':form, 'error_message': decision,
                        'automaton':aut_name, 'transducer':t_name}

            if witness == (None, None) or witness == (None, None, None):
                decision = "YES, the language satisfies the property"
                proof = ''
            else:
                decision = "NO, the language does not satisfy the property"
                proof = format_counter_example(witness)
            return {'form':form, 'automaton':aut_name, 'transducer':t_name,
                    'result':decision, 'proof': proof}
        elif question == "2":
            err = ''
            try:
                witness = prop.notMaximalW(aut)
            except PropertyNotSatisfied:
                err = "ERROR: the language does not satisfy the property."
            except TypeError:
                err = "The automaton file appears to be incorrectly formatted."

            if err:
                return {'form':form, 'error_message': err,
                        'automaton':aut_name, 'transducer':t_name}

            if witness is None:
                decision = "YES, the language is maximal with respect to the property."
                proof = ''
            else:
                decision = "NO, the language is not maximal with respect to the property."
                proof = format_counter_example(witness)

            return {'form':form, 'automaton':aut_name, 'transducer':t_name,
                    'result':decision, 'proof': proof}