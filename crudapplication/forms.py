'''
Created on Oct 5, 2017

@author: adyant
'''

from django import forms

class GetForm(forms.Form):
    id = forms.IntegerField()
    
class PostForm(forms.Form):
    pass
class PutForm(forms.Form):
    id = forms.IntegerField()

