from django import forms

class RatingForm(forms.Form):
    def __init__(self,*args,**kwargs):
        CHOICES = [('1', '1'),
                   ('2', '2'),
                   ('3', '3'),
                   ('4', '4'),
                   ('5', '5')]
        sites = kwargs.pop('sites').getlist('sites[]')
        super(RatingForm,self).__init__(*args,**kwargs)
        for index, site in enumerate(sites):
            print("site " + str(index) + ": " + str(site))
            self.fields[site] = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False, label=site)

    # initialize function variables
    CHOICES = [('1', '1'),
               ('2', '2'),
               ('3', '3'),
               ('4', '4'),
               ('5', '5')]
    ratings = []
    #sites = forms.IntegerField(label="test", widget=Stars)
    
    # loop through our sites
    #for site in sites:
     #   ratings.append(forms.CharField(label=site, widget=forms.RadioSelect(choices=CHOICES)))
        

