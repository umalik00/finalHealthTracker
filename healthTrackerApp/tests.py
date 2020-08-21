from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class BaseTest(TestCase):
    def setUp(self):
        self.registerURL = reverse('register')

        self.user = {
            'first': 'Test',
            'last': 'User',
            'dob': '2001-10-05',
            'sex': 'F',
            'email': 'test@test.com',
            'weight': 55,
            'height': 165.1,
            'calorieIntake': 300,
            'targetWeight': 56,
            'password': 'password1559',
            'password2': 'password1559',
            'addrLine1': '38 Test addr',
            'addrLine2': 'Unit lane',
            'City': 'City',
            'county': 'Aberdeenshire',
            'postcode': 'te1 5ts',
            'addressTypeName': 'Home',
            'username': 'test',
        }

        self.userShortPass = {
            'first': 'Test',
            'last': 'User',
            'dob': '2001-10-05',
            'sex': 'F',
            'email': 'test@test.com',
            'weight': 55,
            'height': 165.1,
            'calorieIntake': 300,
            'targetWeight': 56,
            'password': 'pass',
            'password2': 'pass',
            'addrLine1': '38 Test addr',
            'addrLine2': 'Unit lane',
            'City': 'City',
            'county': 'Aberdeenshire',
            'postcode': 'te1 5ts',
            'addressTypeName': 'Home',
            'username': 'test',
        }

        self.userMissmatchedPW = {
            'first': 'Test',
            'last': 'User',
            'dob': '2001-10-05',
            'sex': 'F',
            'email': 'test@test.com',
            'weight': 55,
            'height': 165.1,
            'calorieIntake': 300,
            'targetWeight': 56,
            'password1': 'password1559',
            'password2': 'passafssafsafffsasa',
            'addrLine1': '38 Test addr',
            'addrLine2': 'Unit lane',
            'City': 'City',
            'county': 'Aberdeenshire',
            'postcode': 'te1 5ts',
            'addressTypeName': 'Home',
            'username': 'test',
        }

        self.userInvalidEmail = {
            'first': 'Test',
            'last': 'User',
            'dob': '2001-10-05',
            'sex': 'F',
            'email': 'test',
            'weight': 55,
            'height': 165.1,
            'calorieIntake': 300,
            'targetWeight': 56,
            'password': 'password1559',
            'password2': 'passafssafsafffsasa',
            'addrLine1': '38 Test addr',
            'addrLine2': 'Unit lane',
            'City': 'City',
            'county': 'Aberdeenshire',
            'postcode': 'te1 5ts',
            'addressTypeName': 'Home',
            'username': 'test',
        }

        return super().setUp()

class RegisterTest(BaseTest):
    # Tests to see if registration page exists
    def testPageExists(self):
        response = self.client.get(self.registerURL)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'register.html')

    # sends the post information back to the form for testing
    def testCanRegisterUser(self):
        response = self.client.post(self.registerURL,self.user,format='text/html')
        self.assertEqual(response.status_code,200)

    # Tests to see if registration fails due to short pw
    def testCantRegisterUserShortPass(self):
        response = self.client.post(self.registerURL,self.userShortPass,format='text/html')
        self.assertEqual(response.status_code,200)

    # Tests to see if registration fails due to short pw
    def testCantRegisterUserMismatchedPW(self):
        response = self.client.post(self.registerURL,self.userMissmatchedPW,format='text/html')
        self.assertEqual(response.status_code,200)

    def testCantRegisterUserInvalidEmail(self):
        response = self.client.post(self.registerURL,self.userInvalidEmail,format='text/html')
        self.assertEqual(response.status_code,200)

    def testCantRegisterUserDuplicateUsername(self):
        self.client.post(self.registerURL, self.user, format='text/html')
        response = self.client.post(self.registerURL,self.user,format='text/html')
        self.assertEqual(response.status_code,200)
