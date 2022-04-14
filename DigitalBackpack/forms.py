from django import forms
from django.forms import ModelForm
from .models import Teachers, Students, Assignments
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test

class TeacherRegistrationForm(UserCreationForm):
    # add our email input item
    email = forms.EmailField()

    # model data
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class StudentRegistrationForm(UserCreationForm):

    def registeredEmail(self):
        # grab our email
        data = self.data['email']

        # see if its valid
        if (not Students.objects.filter(email=data)):
            # if not, raise an error
            self.add_error('email', 'Provided email not associated with any current classes. Try again later once your instructor has added you to a class.')

        # return cleaned email
        return data

    # add our email input item
    email = forms.EmailField()

    # model data
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class StudentAccountCompletionForm(forms.Form):
    
    # initialization
    def __init__(self, *args, **kwargs):
        # grab our user info
        print("Form args:")
        print(args)
        print("Form kwargs:")
        print(kwargs)
        try:
            user = User.objects.get(id=kwargs.pop('username').get('_auth_user_id')).username
        except KeyError as error:
            user = kwargs.get('username')

        # construct our initial form
        super(StudentAccountCompletionForm,self).__init__(*args,**kwargs)

        # initialize our username data
        self.fields['username'] = forms.CharField()
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['username'].label = 'Username'
        self.fields['username'].initial = user

        # initialize the first name form input
        self.fields['first'] = forms.CharField()
        self.fields['first'].label = 'First Name'

        # initialize the last name form input
        self.fields['last'] = forms.CharField()
        self.fields['last'].label = 'Last Name'

    # model data
    class Meta:
        model = Students
        fields = ['username', 'first', 'last']


class ClassRegistrationForm(forms.Form):

    # initialization
    def __init__(self, *args, **kwargs):
        
        # grab our user info
        try:
            user = User.objects.get(id=kwargs.pop('username').get('_auth_user_id')).username
        except KeyError as error:
            user = kwargs.get('username')
        # construct our initial form
        super(ClassRegistrationForm,self).__init__(*args,**kwargs)

        # initialize our username data
        self.fields['username'] = forms.CharField()
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['username'].label = 'Teacher Username'
        self.fields['username'].initial = user

        # initialize the first name form input
        self.fields['first'] = forms.CharField()
        self.fields['first'].label = 'Instructor First Name'
        
        # initialize the last name form input
        self.fields['last'] = forms.CharField()
        self.fields['last'].label = 'Instructor Last Name'

        # initialize the class name form input
        self.fields['classname'] = forms.CharField()
        self.fields['classname'].label = 'Class Name'

    # model data
    class Meta:
        model = Teachers
        fields = ['username', 'first', 'last', 'classname']

class AddStudentForm(forms.Form):
    
    classChoice = forms.ChoiceField()
    extraFieldCount = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        options = []
        extraFields = kwargs.pop('extra', 1)
        teacherUser = kwargs.pop('teacher')
        teacherClasses = list(Teachers.objects.filter(user=User.objects.get(username=teacherUser)))

        for teacherClass in teacherClasses:
            options.append((teacherClass.id, teacherClass.classname))

        super(AddStudentForm, self).__init__(*args, **kwargs)

        self.fields['classChoice'] = forms.ChoiceField(choices=options, widget=forms.Select)

        self.fields['extraFieldCount'].initial = extraFields

        for index in range(int(extraFields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['email_{index}'.format(index=index)] = \
                    forms.EmailField(required=False)

class AssignmentForm(forms.Form):
    
    classChoice = forms.ChoiceField()
    assignmentTitle = forms.CharField()
    assignmentInstructions = forms.CharField(widget=forms.Textarea)
    assignmentDueDate = forms.DateTimeField()
    assignmentAttachment = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        options = []
        teacherUser = kwargs.pop('teacher')
        teacherClasses = list(Teachers.objects.filter(user=User.objects.get(username=teacherUser)))

        for teacherClass in teacherClasses:
            options.append((teacherClass.id, teacherClass.classname))

        super(AssignmentForm, self).__init__(*args, **kwargs)

        self.fields['classChoice'] = forms.ChoiceField(choices=options, widget=forms.Select)

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

