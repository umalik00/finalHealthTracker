from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .forms import *
from django.http import Http404,HttpResponse,HttpResponseForbidden

from datetime import datetime

# startup screen before loading the login/register screens
def startup(request):
    context = {}
    return render(request, "startup_page.html", context)


# The homepage for the user to
def home(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    """View function for homepage"""

    context = {
        'username': User.username,
        'weight': User.weight,
        'height': User.height,
        # Calculates the BMI for the user that has been logged in
        'BMI': round(request.user.calculateBMI(), 2),
        'goals': UserGoals.objects.filter(user = request.user),
        'calorieIntake': User.calorieIntake,
        'targetWeight': User.targetWeight,
    }

    BMR = 0

    if request.user.sex == 'M':
        # 66 + ((13.7 x weight in KG) + (5 x height in CM) - (6.8 x user age))
        BMR = float(66 + ((13.7 * int(request.user.weight)) + (5 * float(request.user.heightAsCM()))) -
                    (6.8 * request.user.getAge()))
    elif request.user.sex == 'F':
        # 655 + ((9.6 x weight in KG) + (1.8 x height in CM) - (5.7 x user age))
        BMR = float(655 + ((9.6 * int(request.user.weight)) + (1.8 * float(request.user.heightAsCM()))) -
                    (4.7 * request.user.getAge()))

    context['BMR'] = BMR
    return render(request, "homepage.html", context)

# goals view in homepage which allows the goal to be stored in the database
def userGoals(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    context = {
        'goals': UserGoals.objects.filter(user=request.user),
    }

    if request.POST:
        goalCompletionForm = GoalCompletionForm(request.POST)
        userGoalForm = UserGoalCompletionForm(request.POST)

        if goalCompletionForm.is_valid() and userGoalForm.is_valid():
            goals = goalCompletionForm.save()
            userGoals = userGoalForm.save(commit=False)
            userGoals.user = request.user
            userGoals.goal = goals
            userGoals.save()

            goalName = goalCompletionForm.cleaned_data['goalName']
            goalType = goalCompletionForm.cleaned_data['goalType']
            goalDescription = goalCompletionForm.cleaned_data['goalDescription']
            targetDate = goalCompletionForm.cleaned_data['targetDate']
            isAchieved = userGoalForm.cleaned_data['isAchieved']

            return redirect('home')
    else:
        goalCompletionForm = GoalCompletionForm()
        userGoalForm = UserGoalCompletionForm()

    context['userGoals'] = userGoalForm
    context['goalCompletionFrm'] = goalCompletionForm
    return render(request, "homepage.html", context)

# logout redirects the user back to the startup_screen out of the site
def logoutView(request):
    logout(request)
    return redirect("/")

# login contains all of the details where the user logs in/registers for an account
def loginView(request):
    """View function for login page"""
    context = {}
    user = request.user
    # checks if the user is logged in or not
    if user.is_authenticated:
        # immediately skips the login stage if true
        return redirect("home")

    if request.POST:
        form = UserLoginAuthenticationForm(request.POST)
        if form.is_valid():
            # the username and password data content is passed off to the database
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # check for authenticity to see if username and password match records
            user = authenticate(username=username, password=password)

            # if details match, the user is redirected to home
            if user:
                login(request, user)
                return redirect("home")

    else:
        form = UserLoginAuthenticationForm()
    # render the context of the form
    context["login_form"] = form
    return render(request, "login.html", context)

# register view used to control the data processing in the register form and template
def registerView(request):
    context = {}
    if request.POST:
        # check whether each forms contain valid values
        userRegisterForm = RegisterUserForm(request.POST)
        addressTypeform = AddressTypeForm(request.POST)
        userAddressForm = RegisterUserAddressForm(request.POST)
        # if all forms are valid
        if userRegisterForm.is_valid() and addressTypeform.is_valid() and userAddressForm.is_valid():
            # save the register form data into the database
            user = userRegisterForm.save()
            addressType = addressTypeform.save()
            address = userAddressForm.save(commit=False)
            address.addressType = addressType
            address.user = user
            address.save()
            first = userRegisterForm.cleaned_data["first"]
            last = userRegisterForm.cleaned_data["last"]
            email = userRegisterForm.cleaned_data["email"]
            dob = userRegisterForm.cleaned_data["dob"]
            weight = userRegisterForm.cleaned_data["weight"]
            height = userRegisterForm.cleaned_data["height"]
            calorieIntake = userRegisterForm.cleaned_data["calorieIntake"]
            targetWeight = userRegisterForm.cleaned_data["targetWeight"]
            sex = userRegisterForm.cleaned_data["sex"]
            username = userRegisterForm.cleaned_data["username"]
            raw_password = userRegisterForm.cleaned_data["password1"]

            addressTypeName = addressTypeform.cleaned_data["addressTypeName"]

            addrLine1 = userAddressForm.cleaned_data["addrLine1"]
            addrLine2 = userAddressForm.cleaned_data["addrLine2"]
            addrLine3 = userAddressForm.cleaned_data["addrLine3"]
            addrLine4 = userAddressForm.cleaned_data["addrLine4"]
            City = userAddressForm.cleaned_data["City"]
            county = userAddressForm.cleaned_data["county"]
            postcode = userAddressForm.cleaned_data["postcode"]
            # authenticate the username and password
            userAuth = authenticate(username=username, password=raw_password)
            # if user authenticates and is able to access their account
            if userAuth:
                login(request, userAuth)
                return redirect("home")
    else:
        userRegisterForm = RegisterUserForm()
        addressTypeform = AddressTypeForm()
        userAddressForm = RegisterUserAddressForm()

    context['register_user'] = userRegisterForm
    context['address_type'] = addressTypeform
    context['user_address'] = userAddressForm
    return render(request, "register.html", context)

# Exercise view used to control the tables in the exercise template
def exercise(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    context = {}
    # retrieve exercise records based on the user
    exercise = Exercise.objects.filter(user=request.user)
    context['exercise'] = exercise

    return render(request, "exercise.html", context)

# record weight lift controls the data parsed from the weightlifting exercise type form
def recordWeightLift(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    context = {}

    if request.POST:
        # check whether each forms contain valid values
        exerciseForm = ExerciseForm(request.POST)
        weightLiftForm = WeightLiftingForm(request.POST)
        # if forms values are all valid
        if exerciseForm.is_valid() and weightLiftForm.is_valid():
            weightLift = weightLiftForm.save(commit=False)
            weightLift.exerciseTypeName = "Weight Lifting"
            weightLift.save()
            user = request.user
            exercise = exerciseForm.save(commit=False)
            exercise.exerciseTypeID = weightLift
            exercise.user = user
            exercise.save()

            dateComplted = weightLiftForm.cleaned_data['dateCompleted']
            achievedTarget = weightLiftForm.cleaned_data['achievedTarget']

            # If the cardio form is valid
            exerciseName = exerciseForm.cleaned_data['exerciseName']
            ammountOfWeightLifted = weightLiftForm.cleaned_data['ammountOfWeightLifted']
            targetWeightToLift = weightLiftForm.cleaned_data['targetWeightToLift']
            howManyReps = weightLiftForm.cleaned_data['howManyReps']

            timeStarted = exerciseForm.cleaned_data['timeStarted']
            duration = exerciseForm.cleaned_data['duration']
            return redirect("exercise")

    else:
        exerciseForm = ExerciseForm()
        weightLiftForm = WeightLiftingForm()

    context['weightLiftFrm'] = weightLiftForm
    context['exercise'] = exerciseForm
    return render(request, "exercise.html", context)

# record cardio controls the data parsed from the cardio exercise type form
def recordCardio(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    context = {}
    if request.POST:
        # check whether each forms contain valid values
        exerciseForm = ExerciseForm(request.POST)
        cardioForm = CardioForm(request.POST)
        # check whether form is valid
        if exerciseForm.is_valid() and cardioForm.is_valid():
            cardio = cardioForm.save(commit=False)
            cardio.exerciseTypeName = "Cardio"
            cardio = cardioForm.save()

            user = request.user
            exercise = exerciseForm.save(commit=False)
            exercise.exerciseTypeID = cardio
            exercise.user = user
            exercise.save()

            dateComplted = cardioForm.cleaned_data['dateCompleted']
            achievedTarget = cardioForm.cleaned_data['achievedTarget']

            # If the cardio form is valid
            exerciseName = exerciseForm.cleaned_data['exerciseName']
            distanceCompleted = cardioForm.cleaned_data['distanceCompleted']
            targetDistance = cardioForm.cleaned_data['targetDistance']

            timeStarted = exerciseForm.cleaned_data['timeStarted']
            duration = exerciseForm.cleaned_data['duration']
            return redirect("exercise")
    else:
        exerciseForm = ExerciseForm()
        cardioForm = CardioForm()

    context['cardioFrm'] = cardioForm
    context['exercise'] = exerciseForm
    return render(request, "exercise.html", context)

# record body weight controls all data parsed from the body weight exercise type form
def recordBodyWeight(request):
    # Requires user to log in to view body weight info
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    context = {}
    # check whether each forms contain valid values
    if request.POST:
        exerciseForm = ExerciseForm(request.POST)
        bodyWeightForm = BodyWeightForm(request.POST)
        # if values are valid
        if exerciseForm.is_valid() and bodyWeightForm.is_valid():
            bodyWeight = bodyWeightForm.save(commit=False)
            bodyWeight.exerciseTypeName = "Body Weight"
            bodyWeight.save()
            user = request.user
            exercise = exerciseForm.save(commit=False)
            exercise.exerciseTypeID = bodyWeight
            exercise.user = user
            exercise.save()

            dateComplted = bodyWeightForm.cleaned_data['dateCompleted']
            achievedTarget = bodyWeightForm.cleaned_data['achievedTarget']

            # If the cardio form is valid
            exerciseName = exerciseForm.cleaned_data['exerciseName']
            completedWithWeights = bodyWeightForm.cleaned_data['completedWithWeights']
            howHeavyWereWeights = bodyWeightForm.cleaned_data['howHeavyWereWeights']
            howManyReps = bodyWeightForm.cleaned_data['howManyReps']

            targetReps = bodyWeightForm.cleaned_data['targetReps']

            timeStarted = exerciseForm.cleaned_data['timeStarted']
            duration = exerciseForm.cleaned_data['duration']
            return redirect("exercise")

    else:
        exerciseForm = ExerciseForm()
        bodyWeightForm = BodyWeightForm()

    context['bodyWeightFrm'] = bodyWeightForm
    context['exercise'] = exerciseForm
    return render(request, "exercise.html", context)

# adding a new meal record into the meal database in the meal template
def addMeal(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    context = {}
    # retrieve database records based on user account
    mealTable = Meal.objects.filter(user=request.user)
    # foodItem = request.GET['foodName']
    if request.POST:
        mealForm = MealForm(request.POST)

        if mealForm.is_valid():
            meal = mealForm.save(commit=False)
            user = request.user
            meal.user = user

            food = mealForm.cleaned_data['food'].foodID
            mealForm.food = Food.objects.get(foodID=food)

            timeRecorded = mealForm.cleaned_data['timeRecorded']
            typeOfMeal = mealForm.cleaned_data['typeOfMeal']
            portionSize = mealForm.cleaned_data['portionSize']
            meal.save()
            # calorie intake sum is calculated based on calories and portion size
            user.calorieIntake += (meal.food.calories*meal.portionSize)
            user.save()
            return redirect('meal')

    else:
        mealForm = MealForm()

        # Used to multiply food by portion size of that meal
        for nutrition in mealTable:
            nutrition.food.carbohydrates *= nutrition.portionSize
            nutrition.food.fats *= nutrition.portionSize
            nutrition.food.protein *= nutrition.portionSize
            nutrition.food.calories *= nutrition.portionSize

    context['mealForm'] = mealForm
    context['mealTable'] = mealTable

    return render(request, "meal.html", context)

# meal item controls the values parsed from the foodDrinkItem template in the form
# this form allows users to enter details about the food/drink item type (e.g. carbohydrates/fats/etc)
def mealItem(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    context = {}
    food = Food.objects.all()

    if request.POST:
        foodDrinkForm = FoodDrinkItemForm(request.POST)
        # check if food /drink item values are correct
        if foodDrinkForm.is_valid():
            foodDrinkForm = foodDrinkForm.save()

    else:
        foodDrinkForm = FoodDrinkItemForm()

    # Adds validation to the form as well as adding a table of food
    context['foodDrinkFrm'] = foodDrinkForm
    context['food'] = food
    return render(request, "mealFoodDrinkList.html", context)

# group controls the tables to retrieve correct group information based on the group they've joined
def group(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    context = {
        # filtered based on user
        'groups': MembersInGroup.objects.filter(user=request.user)
    }
    return render(request, "groups.html", context)

# create group operates in the group template page
def createGroup(request):
    context = {}
    if request.POST:
        # check whether each forms contain valid values
        groupCreationForm = GroupCreationForm(request.POST)
        ownerMemberForm = AddMembersToGroup(request.POST)
        # checks whether new group values are correct
        if groupCreationForm.is_valid() and ownerMemberForm.is_valid():
            group = groupCreationForm.save()
            owner = ownerMemberForm.save(commit=False)
            user = request.user
            owner.user = user
            owner.group = group
            owner.isAdmin = True
            owner.save()

            groupName = groupCreationForm.cleaned_data['groupName']
            groupDescription = groupCreationForm.cleaned_data['groupDescription']

            return redirect('groups')
    else:
        groupCreationForm = GroupCreationForm()
        ownerMemberForm = MembersInGroup()

    context['groupCreationFrm'] = groupCreationForm
    context['owner'] = ownerMemberForm
    return render(request, "groups.html", context)

def joinUserGroup(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    context = {}
    if request.POST:
        addMembersForm = JoinGroupForm(request.POST)

        if addMembersForm.is_valid():
            groupName = addMembersForm.cleaned_data['groupName']

            if UserGroups.objects.filter(groupName=groupName).exists():
                if not MembersInGroup.objects.filter(user=request.user,group=UserGroups.objects.get(groupName=groupName)).exists():
                    MembersInGroup.objects.create(user=request.user,group=UserGroups.objects.get(groupName=groupName))

            return redirect('groups')


    else:
        addMembersForm = JoinGroupForm()

    context['join'] = addMembersForm

    return render(request, "groups.html", context)

# joined group function shows data in relation to the number of users in the group and group details specifically relating
# to it.
def joinedGroup(request, groupID):

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    context = {}

    context['groupGoalName']= GroupGoals.objects.filter(group_id=groupID)
    context['groupAttr'] = UserGroups.objects.get(groupID=groupID)

    # filter group IDs based on the user has joined - prevents other user's from seeing each other's groups.
    group = MembersInGroup.objects.filter(group_id=groupID)
    if not group.exists():
        raise Http404

    if not MembersInGroup.objects.filter(user=request.user):
        return HttpResponseForbidden()

    groupObj = UserGroups.objects.get(groupID=groupID)

    if request.POST:
        # check whether each forms contain valid values
        goalCompletionForm = GoalCompletionForm(request.POST)
        groupGoalForm = GroupGoalCompletionForm(request.POST)

        if goalCompletionForm.is_valid() and groupGoalForm.is_valid():
            goals = goalCompletionForm.save()
            groupGoals = groupGoalForm.save(commit=False)
            groupGoals.group = groupObj
            groupGoals.goal = goals
            groupGoals.save()

            goalName = goalCompletionForm.cleaned_data['goalName']
            goalType = goalCompletionForm.cleaned_data['goalType']
            goalDescription = goalCompletionForm.cleaned_data['goalDescription']
            targetDate = goalCompletionForm.cleaned_data['targetDate']
            isAchieved = groupGoalForm.cleaned_data['isAchieved']

            return redirect('joinedGroup',groupID=groupID)

    else:
        goalCompletionForm = GoalCompletionForm()
        groupGoalForm = GroupGoalCompletionForm()

    context['group'] = group
    context['goals'] = groupGoalForm
    context['goalCompletionFrm'] = goalCompletionForm
    return render(request, "groupsJoined.html", context)