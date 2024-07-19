"""This module is used to create the forms used in the website."""
import re

from django import forms

import logging

from app.transducer.util import parse_aut_str


PROPERTY_TYPE_CHOICE = (('0', '-Please Select-'),
                        ('1', 'Fixed (UD code, prefix code, suffix code,...)'),
                        ('2', 'Trajectory or Input-Altering Transducer '),
                        ('3', 'Error-Detection (via input-preserving transducer)'),
                        ('4', 'Error-Correction (via input-preserving transducer)'),
                        ('5', 'Theta-Transducer Property (via transducer and antimorphic permutation)'))

FIXED_TYPE_CHOICE = (('1', 'Prefix'),
                     ('2', 'Suffix'),
                     ('3', 'Bifix'),
                     ('4', 'Infix'),
                     ('5', 'Outfix'),
                     ('6', 'Code'),
                     ('7', 'HyperCode'))

QUESTION_CHOICE = (('0', '-Please Select-'),
                   ('1', 'Satisfaction'),
                   ('2', 'Maximality'),
                   ('3', 'Construction'),
                   ('4', 'Approximate Maximality'))

#takes in an uploaded file and properly converts it to text. Returns the text of the file. 
#required because uploaded files are automatically stored as binary data. In Python 2, this 
#wasn't an issue because all data was binary, but now the two types of data are seperate
def file2Text(inputBinary):
    return bytes.decode(inputBinary)

class UploadFileForm(forms.Form):
    """This class is used to declare the file form used on the website to interface with FAdo
       In all cases, JS validates that all required fields have been filled in, so set Required to False
       If a user disables the JSvalidation they could also disable the required attribute."""
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.aut_name = 'N/A'
        self.trans_name = 'N/A'
        self.theta_name = 'N/A'

    automata_file = forms.FileField(required=False)
    transducer_file = forms.FileField(required=False)
    theta_file = forms.FileField(required=False)

    attrs = {'rows': 5, 'class': 'form-control', 'id': 'automata_text'}
    automata_text = forms.CharField(required=False,
                                    widget=forms.Textarea(attrs=attrs))

    attrs['id'] = 'transducer_text1'
    transducer_text1 = forms.CharField(required=False,
                                       widget=forms.Textarea(attrs=attrs))

    attrs['id'] = 'transducer_text2'
    transducer_text2 = forms.CharField(required=False,
                                       widget=forms.Textarea(attrs=attrs))

    attrs['id'] = 'theta_text'
    theta_text = forms.CharField(required=False,
                                 widget=forms.Textarea(attrs=attrs))

    cls = 'selectpicker selectC'
    question = forms.ChoiceField(choices=QUESTION_CHOICE, required=False,
                                 widget=forms.Select(attrs={
                                     'onchange': 'setFields();',
                                     'class': cls
                                 }))
    property_type = forms.ChoiceField(choices=PROPERTY_TYPE_CHOICE, required=False,
                                      widget=forms.Select(attrs={
                                          'onchange': 'setFixedProperty();',
                                          'class': cls,
                                          'id': 'divsat_select'
                                      }))
    fixed_type = forms.ChoiceField(choices=FIXED_TYPE_CHOICE, required=False,
                                   widget=forms.Select(attrs={'class': cls}))

    s_int = forms.IntegerField(required=False)#, min_value=2, max_value=10) 
    n_int = forms.IntegerField(required=False)
    l_int = forms.IntegerField(required=False)

    EPS = 1e-5
    epsilon = forms.DecimalField(required=False, min_value=EPS, max_value=1-EPS, initial=0.01)
    dirichletT = forms.DecimalField(required=False, min_value=1, initial=2.001)
    displacement = forms.IntegerField(required=False, min_value=1, initial=1)

    def clean_theta_file(self):
        """Clean the data of the automata file"""
        data = self.cleaned_data['theta_file']

        if data:
            self.theta_name = data.name
            data.seek(0)
            #don't use str(data.read()),doing so removes the ability to bytes.decode() it later,which is required
            newdata = data.read()
            data.close()
            return newdata

        self.theta_name = 'N/A'
        return data

    def clean_automata_file(self):
        """Clean the data of the automata file"""
        data = self.cleaned_data['automata_file']

        if data:
            self.aut_name = data.name
            newdata = data.read() 
            data.close()
            return newdata

        self.aut_name = 'N/A'
        return data

    def clean_transducer_file(self):
        """Clean the data of the transducer file"""
        data = self.cleaned_data['transducer_file']

        if data:
            self.trans_name = data.name
            newdata = data.read()
            data.close()
            return newdata

        self.trans_name = 'Textarea Language Property'
        return data

    def clean(self):
        data = super(UploadFileForm, self).clean()
        data['aut_name'] = self.aut_name
        data['trans_name'] = self.trans_name
        data['theta_name'] = self.theta_name
        if data.get('automata_file'):
            data['automata_text'] = file2Text(data.get('automata_file'))

        if data.get('theta_file'):
            data['theta_text'] = file2Text(data.get('theta_file'))

        if data.get('transducer_file'):
            data['transducer_text'] = file2Text(data.get('transducer_file'))
        elif data.get('transducer_text1'):
            data['transducer_text'] = data.get('transducer_text1')
        else:
            data["transducer_text"] = None

        if data.get('question') == '0':
            raise forms.ValidationError('Please select a question.')

        if not data.get('automata_text') and data.get('question') != '3':
            raise forms.ValidationError('You did not supply an automaton.')

        result = parse_aut_str(data.get('automata_text'))


        if not data.get('theta_text'):
            pass
        else:
            data['theta_text'] = re.sub(r'\r', '', str(data['theta_text']))
        data['automata_text'] = re.sub(r'\r', '', str(data['automata_text']))

        return data
