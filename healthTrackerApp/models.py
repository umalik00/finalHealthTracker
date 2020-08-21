from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from datetime import datetime,time,date
from model_utils import Choices

class CustomUserManager(BaseUserManager):
    def create_user(self,username, dob, first, last, sex, email, weight, height, calorieIntake,
                       targetWeight,password=None):
        if not username:
            raise ValueError("Please enter your username")
        if not dob:
            raise ValueError("Please enter your date of birth")
        if not first:
            raise ValueError("Please enter your first name")
        if not last:
            raise ValueError("Please enter your last name")
        if not sex:
            raise ValueError("Please select M or F")
        if not email:
            raise ValueError("Please enter a email address")
        if not weight:
            raise ValueError("Please enter your weight in Kilograms")
        if not height:
            raise ValueError("Please enter your height in meters")
        if not calorieIntake:
            raise ValueError("Please enter how many calories that you have consumed today")
        if not targetWeight:
            raise ValueError("Please enter a your ideal body weight")

        user = self.model(
            username = username,
            dob = dob,
            first = first,
            last = last,
            sex = sex,
            email = self.normalize_email(email),
            weight = weight,
            height = height,
            calorieIntake = calorieIntake,
            targetWeight = targetWeight,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, dob, first, last, sex, email, weight, height, calorieIntake,
                       targetWeight,password=None):
        if not username:
            raise ValueError("Please enter your username")
        if not dob:
            raise ValueError("Please enter your date of birth")
        if not first:
            raise ValueError("Please enter your first name")
        if not last:
            raise ValueError("Please enter your last name")
        if not sex:
            raise ValueError("Please select M or F")
        if not email:
            raise ValueError("Please enter a email address")
        if not weight:
            raise ValueError("Please enter your weight in Kilograms")
        if not height:
            raise ValueError("Please enter your height in meters")
        if not calorieIntake:
            raise ValueError("Please enter how many calories that you have consumed today")
        if not targetWeight:
            raise ValueError("Please enter a your ideal body weight")

        user = self.create_user(
            username = username,
            dob = dob,
            first = first,
            last = last,
            sex = sex,
            email = self.normalize_email(email),
            weight = weight,
            height = height,
            calorieIntake = calorieIntake,
            targetWeight = targetWeight,
        )

        user.is_admin     = True
        user.is_staff     = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

# User model
class User(AbstractBaseUser):
    SEX_CHOICES = Choices(
        ('M', "Male"),
        ('F', "Female"),
    )

    userID = models.AutoField(primary_key= True, editable= False, unique=True)
    username = models.CharField(max_length= 255,unique = True)
    dob = models.DateField()
    first = models.CharField(max_length= 255)
    last = models.CharField(max_length= 255)
    sex = models.CharField(max_length= 1,choices=SEX_CHOICES)
    email = models.EmailField(verbose_name= "email",max_length= 255, unique = True)
    weight = models.DecimalField(decimal_places=2, max_digits=5)
    height = models.DecimalField(decimal_places=2, max_digits=3)
    # The calories that the user has eaten so far today
    calorieIntake = models.IntegerField()
    # The distance that the user aims to complete
    targetWeight = models.DecimalField(decimal_places=2, max_digits=5)
    date_joined = models.DateTimeField(verbose_name= "date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last logged in", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['userID','dob','first','last','sex','email','weight','height','calorieIntake',
                       'targetWeight',]

    objects = CustomUserManager()

    # If they have admin permission
    def has_perm(self,perm,obj= None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True

    def addCalories(self,caloriesEaten):
        self.calorieIntake += caloriesEaten

    def getAge(self):
        return date.today().year - self.dob.year

    def getCalories(self):
        return str(self.calorieIntake) + " calories eaten"

    def getFullName(self):
        return self.first + " " + self.last

    def getForename(self):
        return self.first

    def getSurname(self):
        return self.last

    def getUsername(self):
        return self.username

    # Had a mutator in case the user wants to change their username
    def setUsername(self, username):
        self.username = username

    def getSex(self):
        return self.sex

    def getWeight(self):
        return self.weight

    def setWeight(self,weight):
        self.weight = weight

    def getHeight(self):
        return self.height

    def setHeight(self, value):
        self.height = value

    def getTargetWeight(self):
        return self.targetWeight

        # Calculates the user's BMI (body mass index)

    def calculateBMI(self):
        height = float(self.height) * float(self.height)
        calculateBMI = float(self.weight) / float(height)
        return calculateBMI

        # Calculates the users weight in stones

    def weightAsStone(self):
        weight = float(self.weight) / 6.350
        # Formula to convert stones to pounds
        # (Decimal(self.weight) - int(self.weight))* Decimal(0.14) gets the decimal value of the weight class
        # and turns it into pounds
        weightAsStone = int(weight)
        return weightAsStone

        # Calculates the user's weight in pounds

    def weightAsLBS(self):
        weight = float(self.weight) / 0.45359237
        # Formula to convert stones to pounds
        # and turns it into pounds
        weightAsLBS = int(weight)
        return weightAsLBS

        # Calculates user's height in centimetres

    def heightAsCM(self):
        height = float(self.height) * 100
        heightAsCM = height
        return heightAsCM

        # Calculates user's height in feet

    def heightAsFeet(self):
        heightAsFeetVar = float(self.height) * 3.2808
        # Formula to metres to feet and inches
        # (Decimal(self.height) - int(self.height))* Decimal(0.12) gets the decimal value of the height class
        # and turns it into inches
        heightAsFeet = int(heightAsFeetVar)
        return heightAsFeet

        # Calculates user's height in inches

    def heightAsInches(self):
        heightAsInchesVar = float(self.height) * 39.370
        # Formula to metres to feet and inches
        # (Decimal(self.height) - int(self.height))* Decimal(0.12) gets the decimal value of the height class
        # and turns it into inches
        heightAsInches = int(heightAsInchesVar)
        return heightAsInches


    def __str__(self):
        weight = self.weight
        height = self.height
        targetWeight = self.targetWeight
        stringAppend = self.first + " " + self.last + "\n"
        stringAppend += self.sex + "\n"
        stringAppend += self.email + "\n"

        stringAppend +=  "My current weight is " +str(weight) + " KG" + "\n"
        stringAppend += str(height) + " Metres" + "\n"
        stringAppend += str(targetWeight) + " KG is my target weight" + "\n"
        return stringAppend

class AddressType(models.Model):
    addressTypeID = models.AutoField(primary_key= True, editable= False, unique=True)
    # models the type of Address I.e, home, term time, work, holiday
    ADDRESS_TYPE_CHOICES = (
        ('Home', "Home"),
        ('Student', "Student"),
        ('Business', "Business"),
        ('Work', "Work"),
        ('Other', "Other"),
    )

    addressTypeName = models.CharField(max_length= 255,choices=ADDRESS_TYPE_CHOICES)
    # the last time the address was changed
    addressLastUpdated = models.DateTimeField(auto_now_add=True)

    def getAddressLastUpdated(self):
        return self.addressLastUpdated

    def getAddressTypeName(self):
        return self.addressTypeName

class Address(models.Model):
    addressID = models.AutoField(primary_key= True, editable= False, unique=True)
    addrLine1 = models.CharField(max_length= 255)
    addrLine2 = models.CharField(max_length= 255,blank= True)
    addrLine3 = models.CharField(max_length= 255,blank= True)
    addrLine4 = models.CharField(max_length= 255,blank= True)
    City = models.CharField(max_length= 255)
    county = models.CharField(max_length= 255)
    postcode = models.CharField(max_length= 7)
    user = models.ForeignKey(User,db_column='userID', on_delete= models.CASCADE)
    addressType = models.ForeignKey(AddressType,db_column='addressTypeID', on_delete= models.CASCADE)

    def getPostcode(self):
        return self.postcode

class Food(models.Model):
    foodID = models.AutoField(primary_key= True, editable= False, unique=True)
    foodName = models.CharField(max_length= 255)
    carbohydrates = models.DecimalField(decimal_places= 2, max_digits= 5)
    protein = models.DecimalField(decimal_places= 2, max_digits= 5)
    fats = models.DecimalField(decimal_places= 2, max_digits= 5)
    calories = models.IntegerField()

    def getMacroNutrients(self):
        carbStr = str(self.carbohydrates)
        proteinStr = str(self.protein)
        fatStr = str(self.fats)
        return "Carbohydrates: " + carbStr + " grams" + "\nProtien: " + proteinStr + " grams" + "\nFats: " + fatStr \
               + " grams"

    def getCalories(self):
        return self.calories

    def getFoodName(self):
        return self.foodName

    def getFats(self):
        return self.fats

    def getCarbohydrates(self):
        return self.carbohydrates

    def getProtein(self):
        return self.protein

class Meal(models.Model):
    mealID = models.AutoField(primary_key= True, editable= False, unique=True)
    typeOfMeal = models.CharField(max_length= 255)
    timeRecorded = models.DateTimeField()
    portionSize = models.IntegerField()
    user = models.ForeignKey(User,db_column='userID', on_delete= models.CASCADE)
    food = models.ForeignKey(Food,db_column='foodID', on_delete= models.CASCADE)

    def getTypeOfMeal(self):
        return self.typeOfMeal

    def getTimeRecorded(self):
        return self.timeRecorded

    def getPortionSize(self):
        return self.portionSize

class ExerciseType(models.Model):
    exerciseTypeID = models.AutoField(primary_key= True, editable= False, unique=True)
    exerciseTypeName = models.CharField(max_length= 255)
    dateCompleted = models.DateField()
    achievedTarget = models.BooleanField()

class WeightLifting(ExerciseType):
    ammountOfWeightLifted = models.DecimalField(decimal_places=1, max_digits=4)
    targetWeightToLift = models.DecimalField(decimal_places=1, max_digits=4)
    howManyReps = models.IntegerField()

class Cardio(ExerciseType):
    # Distance completed, i.e. distance swam or distance ran e.t.c
    distanceCompleted = models.DecimalField(decimal_places=2, max_digits=4)
    targetDistance = models.DecimalField(decimal_places=2, max_digits=4)

class BodyWeight(ExerciseType):
    completedWithWeights = models.BooleanField()
    howHeavyWereWeights  = models.DecimalField(decimal_places=2, max_digits=4,null=True, blank=True)
    targetReps = models.IntegerField()
    howManyReps = models.IntegerField()

class Exercise(models.Model):
    exerciseID = models.AutoField(primary_key= True, editable= False, unique=True)
    exerciseName = models.CharField(max_length= 255)
    timeStarted = models.TimeField()
    duration = models.TimeField()
    user = models.ForeignKey(User,db_column='userID', on_delete= models.CASCADE)
    exerciseTypeID = models.ForeignKey(ExerciseType,db_column='exerciseTypeID', on_delete= models.CASCADE)

    def getExerciseName(self):
        return self.exerciseName

class UserGroups(models.Model):
    groupID   = models.AutoField(primary_key= True, editable= False, unique=True)
    groupName = models.CharField(max_length= 255)
    groupDescription = models.TextField()

    def getGroupName(self):
        return self.groupName

class MembersInGroup(models.Model):
    group = models.ForeignKey(UserGroups,db_column='groupID', on_delete= models.CASCADE)
    user = models.ForeignKey(User, db_column='userID', on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    isAdmin = models.BooleanField(default=False)

class Goals(models.Model):
    goalID = models.AutoField(primary_key= True, editable= False, unique=True)
    goalName = models.CharField(max_length= 255)
    goalType = models.CharField(max_length= 255)
    goalDescription = models.TextField()
    dateCreated = models.DateField(auto_now=True)
    targetDate  = models.DateField()

class UserGoals(models.Model):
    userGoalID = models.AutoField(primary_key= True, editable= False, unique=True)
    goal = models.ForeignKey(Goals,db_column='goalID', on_delete= models.CASCADE)
    user = models.ForeignKey(User, db_column='userID', on_delete=models.CASCADE)
    isAchieved = models.BooleanField(default=False)

class GroupGoals(models.Model):
    groupGoalID = models.AutoField(primary_key=True, editable=False, unique=True)
    goal = models.ForeignKey(Goals, db_column='goalID', on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroups, db_column='groupID', on_delete=models.CASCADE)
    isAchieved = models.BooleanField(default=False)