from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import *
from datetime import datetime, date, time
import csv


class UserLoginAuthenticationForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "password")

    # Form validation for logging in
    def clean(self):
        # Cleans the user login authentication form
        cleaned_data = super(UserLoginAuthenticationForm, self).clean()

        # checks to see if username isn't null
        if not 'username' in cleaned_data:
            raise forms.ValidationError("Please enter a username")

        # checks to see if password isn't null
        if not 'password' in cleaned_data:
            raise forms.ValidationError("Please enter a password")

        if self.is_valid():
            username = self.cleaned_data["username"]
            password = self.cleaned_data["password"]
            # Validation for user password
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("user doesn't exist")
            if not user.check_password(password):
                raise forms.ValidationError("Invalid password")
            if not user.is_active:
                raise forms.ValidationError("The user is inactive")


# Form for creating a user
class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'first', 'last', 'email', 'dob', 'weight', 'height', 'calorieIntake', 'targetWeight', 'sex', 'username',
            'password1', 'password2')

    # Form validation for registering a user
    def clean(self):
        # Cleans the register user form
        cleaned_data = super(RegisterUserForm, self).clean()

        if not 'username' in cleaned_data:
            raise forms.ValidationError("Please enter a username")

        elif self.is_valid():
            username = self.cleaned_data['username']
            height = self.cleaned_data['height']
            dob = self.cleaned_data['dob']
            weight = self.cleaned_data['weight']
            firstName = self.cleaned_data['first']
            lastName = self.cleaned_data['last']

            # Checks to see if user, If they do, tells them to have a different username
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Please enter another username. " + username + " is already taken.")

            # based on the tallest and shortest people in the world
            if height > 2.8 or height < 0.5:
                raise forms.ValidationError("Please enter a valid height between 0.5m and 2.8m")

            if (date.today().year - dob.year) < 18 or (not dob):
                raise forms.ValidationError("You need to be 18 to use the site.")

            # max based on the heaviset and lightest people in the world
            if weight > 635 or weight < 3:
                raise forms.ValidationError("Please enter a valid weight between 3 and 635 kg.")

            if (not firstName) or (not lastName):
                raise forms.ValidationError("Please enter a first and last name")

# Address form to check whether the correct option has been selected
class AddressTypeForm(forms.ModelForm):
    class Meta:
        model = AddressType
        fields = (
            'addressTypeName',
        )

    def clean(self):
        if self.is_valid():
            name = self.cleaned_data['addressTypeName']
            # check whether the user has selected a value address type name
            if not name:
                raise forms.ValidationError("Please enter a valid address type")


# Registration form to check the address part of the form
class RegisterUserAddressForm(forms.ModelForm):
    # using regex to check whether the postcode is valid and is in the correct sequence order
    postcode = forms.CharField(min_length=6, max_length=8)
    class Meta:
        model = Address
        fields = (
            'addrLine1', 'addrLine2', 'addrLine3', 'addrLine4', 'City', 'county', 'postcode',
        )

    # dropdown list for the counties list imported from a csv
    def __init__(self, *args, **kwargs):
        super(RegisterUserAddressForm, self).__init__(*args, **kwargs)
        countyList = []
        with open('counties.csv', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                countyList.append(row)

        countyList.sort()
        # the counties list then retrieved from the first column in the entire csv
        self.fields['county'].choices = [(c[0], c[0]) for c in countyList]

# Exercise form to store specific values for the exercise database table
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = (
            'exerciseName', 'timeStarted', 'duration',
        )

    def clean(self):
        if self.is_valid():
            exerciseName = self.cleaned_data['exerciseName']
            # validation to check the exercise name isn't null and duration is not less than 0
            if not exerciseName:
                raise forms.ValidationError("Please enter an exercise name")


# Exercise type form used to store values for the exercise type database
class ExerciseTypeForm(forms.ModelForm):
    class Meta:
        model = ExerciseType
        fields = (
            'exerciseTypeName', 'dateCompleted', 'achievedTarget',
        )

    def clean(self):
        if self.is_valid():
            dateCompleted = self.cleaned_data['dateCompleted']
            # check whether the date completed is NOT in the future nor too far in the past
            if dateCompleted > date.today():
                raise forms.ValidationError("Date completed cannot be in the future")
            if dateCompleted.month < (date.today().month -1):
                raise forms.ValidationError("Date completed cannot be more than 1 month ago.")

# Exercise form used to store values in weightlifting if selected in exercise type dropdown
class WeightLiftingForm(ExerciseTypeForm):
    class Meta(ExerciseTypeForm.Meta):
        model = WeightLifting
        # gather all fields in the form
        fields = '__all__'
        exclude = ['exercise_type_ptr', 'exerciseTypeID', 'exerciseTypeName', ]

# Exercise form used to store values in body weight if selected in exercise type dropdown
class BodyWeightForm(ExerciseTypeForm):
    class Meta(ExerciseTypeForm.Meta):
        model = BodyWeight
        # gather all fields in the form
        fields = '__all__'
        exclude = ['exercise_type_ptr', 'exerciseTypeID', 'exerciseTypeName']

# Exercise form used to store values in cardio if selected in exercise type dropdown
class CardioForm(ExerciseTypeForm):
    class Meta(ExerciseTypeForm.Meta):
        model = Cardio
        # gather all fields in the form
        fields = '__all__'
        exclude = ['exercise_type_ptr', 'exerciseTypeID', 'exerciseTypeName', ]

# Meal form used to store values for the meal part of the database
class MealForm(forms.ModelForm):
    food = forms.ModelChoiceField(queryset=Food.objects.all().order_by('foodName'), empty_label="(Choose field)")
    # formats in datetime local
    timeRecorded = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'])

    def __init__(self, *args, **kwargs):
        super(MealForm, self).__init__(*args, **kwargs)

    # def getCaloriesFood(self, **kwargs):
    #    context = super(MealForm.foodName).get_context_data(**kwargs)
    #    context['carbohydrates'] = Food.getCarbohydrates(foodName)

    class Meta:
        model = Meal
        # gather all fields in the form
        fields = '__all__'
        # excluding IDs
        exclude = ['mealID', 'user']

    def clean(self):
        if self.is_valid():
            dt = self.cleaned_data['timeRecorded']
            # validation used to check whether the fields are null or whether the date/time values are valid
            if self.cleaned_data['food'] == "":
                raise forms.ValidationError('Please select the food that you had. If there isn\'t any'
                                            'then click "add/edit food list item" to add food')

            if self.cleaned_data['typeOfMeal'] == "":
                raise forms.ValidationError('Please select the type of meal that you had')

            elif not self.cleaned_data['typeOfMeal']:
                raise forms.ValidationError('Please select the type of meal that you had')

            if not dt:
                raise forms.ValidationError('Please Enter a valid date')

            elif dt.date() > date.today() or (dt.date() == date.today() and dt.time() > datetime.now().time()):
                raise forms.ValidationError('Please Enter a valid date or time')

# Food Drink Item Form used to store values in the meal item website and food list database
class FoodDrinkItemForm(forms.ModelForm):
    class Meta(MealForm.Meta):
        model = Food
        # retrieve all fields
        fields = '__all__'
        # except IDs
        exclude = ['foodID']

    def clean(self):
        if self.is_valid():
            # validation to check every field in the form is not null
            name = self.cleaned_data['foodName']
            calories = self.cleaned_data['calories']
            fat = self.cleaned_data['fats']
            carbs = self.cleaned_data['carbohydrates']
            protien = self.cleaned_data['protein']
            if Food.objects.filter(foodName= name).exists():
                raise forms.ValidationError("Food already exists.")
            # and making sure the values aren't 0 nor too erroneous
            if calories != 0 and carbs ==0 and fat ==0 and protien == 0:
                raise forms.ValidationError("Please enter the fats, protein, and carbs for the food.")
            if calories > 10000 or carbs > 10000 or fat > 10000 or protien > 10000:
                raise forms.ValidationError("Please enter some valid values for the fats/ protein/ carbs / calories.")

# Group Creation form used to store details of the new group when user has filled out the form for the user groups
# database
class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = UserGroups
        fields = '__all__'
        exclude = ['groupID']

    def clean(self):
        name = self.cleaned_data['groupName']
        description = self.cleaned_data['groupDescription']

        # Checks to see if current form instance is valid
        if self.is_valid():
            # Checks to see if group name exists (is unique), if not, then it asks you to pick a new group name
            if UserGroups.objects.filter(groupName=name).exists():
                raise forms.ValidationError("The group name already exists. Please pick another name")
            if not description:
                raise forms.ValidationError("Description cannot be blank - must contain a value")

class JoinGroupForm(forms.ModelForm):
    class Meta:
        model = UserGroups
        fields = '__all__'
        exclude = ['groupID', 'groupDescription']

    def clean(self):
        nameOfGroup = self.cleaned_data['groupName']
        if self.is_valid():
            if not nameOfGroup:
                raise forms.ValidationError("The group name you want to join is blank")



# to add new members to the existing group the user has created
class AddMembersToGroup(forms.ModelForm):
    class Meta:
        model = MembersInGroup
        # Excluding IDs
        exclude = ['user','group','id']

class EmailInviteForm(forms.ModelForm):
    class Meta:
        fields= '__all__'
# Goal completion form used to store values of the new goal filled out by the user for the goal database
class GoalCompletionForm (forms.ModelForm):
    class Meta:
        model = Goals
        # retrieve all fields
        fields = '__all__'
        # except IDs
        exclude = ['goalID','dateCreated',]

    def clean(self):
        # check whether if there is an existing goal name in the system
        if not self.cleaned_data['goalName']:
            raise forms.ValidationError("Please enter a goal name")
        if self.cleaned_data['targetDate'] < date.today():
            raise forms.ValidationError("Target dates cannot be in the past")
        if not self.cleaned_data['goalDescription']:
            raise forms.ValidationError("Goal descriptions cannot be blank")

# UserGoal completion form to check whether the user has achieved the goal
class UserGoalCompletionForm (forms.ModelForm):
    class Meta:
        model = UserGoals
        fields = ['isAchieved',]

    def clean(self):

        achieved = self.cleaned_data['isAchieved']

# Group goal completion form to check whether the group has achieved their goal
class GroupGoalCompletionForm (forms.ModelForm):
    class Meta:
        model = GroupGoals
        fields = ['isAchieved',]

    def clean(self):
        achieved = self.cleaned_data['isAchieved']