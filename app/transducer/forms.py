"""This module is used to create the forms used in the website."""
import re

from django import forms

from app.transducer.util import parse_aut_str

PROPERTY_TYPE_CHOICE = (('0', '-Please Select-'),
                        ('1', 'Fixed (UD code, prefix code, suffix code,...)'),
                        ('2', 'Trajectory or Input-Altering Transducer '),
                        ('3', 'Error-Detection (via input-preserving transducer)'),
                        ('4', 'Error-Correction (via input-preserving transducer)'),
                        ('5', 'Theta-Transducer Property (via input-preserving transducer and antimorphic permutation)'))

FIXED_TYPE_CHOICE = (('1', 'Prefix'),
                     ('2', 'Suffix'),
                     ('3', 'Infix'),
                     ('4', 'Outfix'),
                     ('5', 'HyperCode'),
                     ('6', 'Code'))

QUESTION_CHOICE = (('0', '-Please Select-'),
                   ('1', 'Satisfaction'),
                   ('2', 'Maximality'),
                   ('3', 'Construction'))

class UploadFileForm(forms.Form):
    """This class is used to declare the file form used on the website to interface with FAdo"""
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

    s_int = forms.IntegerField(required=False)
    n_int = forms.IntegerField(required=False)
    l_int = forms.IntegerField(required=False)

    def clean_theta_file(self):
        """Clean the data of the automata file"""
        data = self.cleaned_data['theta_file']

        if data:
            self.theta_name = data.name
            data.seek(0)
            newdata = str(data.read())
            data.close()
            return newdata

        self.theta_name = 'N/A'
        return data

    def clean_automata_file(self):
        """Clean the data of the automata file"""
        data = self.cleaned_data['automata_file']

        if data:
            self.aut_name = data.name
            newdata = str(data.read())
            data.close()
            return newdata

        self.aut_name = 'N/A'
        return data

    def clean_transducer_file(self):
        """Clean the data of the transducer file"""
        data = self.cleaned_data['transducer_file']

        if data:
            self.trans_name = data.name
            newdata = str(data.read())
            data.close()
            return newdata

        self.trans_name = 'N/A'
        return data

    def clean(self):
        data = super(UploadFileForm, self).clean()
        data['aut_name'] = self.aut_name
        data['trans_name'] = self.trans_name
        data['theta_name'] = self.theta_name

        if data.get('automata_file'):
            data['automata_text'] = data.get('automata_file')

        if data.get('theta_file'):
            data['theta_text'] = data.get('theta_file')

        if data.get('transducer_file'):
            data['transducer_text'] = data.get('transducer_file')
        elif data.get('transducer_text1'):
            data['transducer_text'] = data.get('transducer_text1')
        elif data.get('transducer_text2'):
            data['transducer_text'] = data.get('transducer_text2')

        print data.get('question')

        if data.get('question') == '0':
            raise forms.ValidationError('Please select a question.')

        if not data.get('automata_text') and data.get('question') != '3':
            raise forms.ValidationError('You did not supply an automata.')

        result = parse_aut_str(data.get('automata_text'))

        if not data.get('transducer_text'):
            if not result.get('transducer') and not result.get('fixed_type'):
                if not result.get('trajectory') and not data.get('property_type'):
                    raise forms.ValidationError('You did not supply a transducer.')
        else:
            data['transducer_text'] = str(data['transducer_text'])

        if not data.get('theta_text'):
            pass
        else:
            data['theta_text'] = re.sub(r'\r', '', str(data['theta_text']))

        data['automata_text'] = re.sub(r'\r', '', str(data['automata_text']))

        return data

class ContactForm(forms.Form):
    """This class is used to specify the contact form used in the website."""
    subjects = forms.CharField(max_length=80)
    message = forms.CharField()
