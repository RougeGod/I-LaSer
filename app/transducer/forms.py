"""This module is used to create the forms used in the website."""
from django import forms

# Meng
PROPERTY_TYPE_CHOICE = [['1', 'Fixed (TODO)'],
                        ['2', 'Trajectory (TODO)'],
                        ['3', 'Error_Detecting'],
                        ['4', 'Error_Correcting']]

PROPERTY_TYPE_MAXIMALITY = [['', '-Please Select-'],
                            ['1', 'Fixed(Prefix, Suffix, etc)'],
                            ['3', 'Transducer: input-altering'],
                            ['4', 'Transducer: input-preserving']]

FIXED_TYPE_CHOICE = [['1', 'Prefix'],
                     ['2', 'Suffix'],
                     ['3', 'Infix'],
                     ['4', 'Outfix'],
                     ['5', 'HyperCode'],
                     ['6', 'Code']]

class UploadFileForm(forms.Form):
    """This class is used to declare the file form used on the website to interface with FAdo"""
   # title = forms.CharField(max_length=50)
    automata_file = forms.FileField(required=False)

    automata_text = forms.FileField(required=False)

    transducer_file = forms.FileField(required=False)

    property_type = forms.ChoiceField(choices=PROPERTY_TYPE_CHOICE,
                                      required=True)
    fixed_type = forms.ChoiceField(choices=FIXED_TYPE_CHOICE,
                                   required=True)
    maximality_type = forms.ChoiceField(choices=PROPERTY_TYPE_MAXIMALITY,
                                        required=True,
                                        widget=forms.Select(
                                            attrs={'onchange':'setFixedProperty2();'}))
    debug_output = forms.BooleanField(required=False)
    integer_k = forms.IntegerField(min_value=0)
    integer_N = forms.IntegerField(min_value=1)


class ContactForm(forms.Form):
    """This class is used to specify the contact form used in the website."""
    subjects = forms.CharField(max_length=80)
    message = forms.CharField()

