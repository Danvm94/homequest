# **Homequest Testing**

## **Testing Overview**

Extensive testing was conducted throughout the development process, involving
both individual and peer assessments. This rigorous testing approach ensured
the reliability and functionality of the Homequest platform.

## **Automated Testing**

### **Unit Testing**

#### **checkout/tests**

- Command: `python3 manage.py test checkout`
- Found 11 test(s).
- Creating test database for alias 'default'...
- System check identified no issues (0 silenced).
- Ran 11 tests in 0.011s
- **Result:** OK

[Back to top &uarr;](#contents)

#### **homepage/tests**

- Command: `python3 manage.py test homepage`
- Found 3 test(s).
- Creating test database for alias 'default'...
- System check identified no issues (0 silenced).
- Ran 3 tests in 0.453s
- **Result:** OK

[Back to top &uarr;](#contents)

#### **profiles/tests**

- Command: `python3 manage.py test profiles`
- Found 11 test(s).
- Creating test database for alias 'default'...
- System check identified no issues (0 silenced).
- Ran 11 tests in 5.775s
- **Result:** OK

[Back to top &uarr;](#contents)

### **Site Coverage Report**

The test coverage for this project currently stands at 82%. While automated
testing has covered a significant portion of the codebase, additional testing
through manual methods will be conducted to ensure comprehensive coverage.

| Name                                                      | Stmts   | Miss   | Cover   |
|-----------------------------------------------------------|---------|--------|---------|
| checkout/__init__.py                                      | 0       | 0      | 100%    |
| checkout/apps.py                                          | 4       | 0      | 100%    |
| checkout/forms.py                                         | 6       | 0      | 100%    |
| checkout/migrations/0001_initial.py                       | 5       | 0      | 100%    |
| checkout/migrations/0002_initial.py                       | 7       | 0      | 100%    |
| checkout/migrations/__init__.py                           | 0       | 0      | 100%    |
| checkout/models.py                                        | 10      | 0      | 100%    |
| checkout/tests.py                                         | 63      | 0      | 100%    |
| checkout/views.py                                         | 59      | 43     | 27%     |
| env.py                                                    | 8       | 0      | 100%    |
| homepage/__init__.py                                      | 0       | 0      | 100%    |
| homepage/apps.py                                          | 4       | 0      | 100%    |
| homepage/migrations/__init__.py                           | 0       | 0      | 100%    |
| homepage/tests.py                                         | 28      | 0      | 100%    |
| homepage/views.py                                         | 11      | 0      | 100%    |
| homequest/__init__.py                                     | 0       | 0      | 100%    |
| homequest/settings.py                                     | 51      | 1      | 98%     |
| homequest/urls.py                                         | 9       | 0      | 100%    |
| manage.py                                                 | 12      | 2      | 83%     |
| profiles/__init__.py                                      | 0       | 0      | 100%    |
| profiles/apps.py                                          | 4       | 0      | 100%    |
| profiles/forms.py                                         | 17      | 0      | 100%    |
| profiles/migrations/0001_initial.py                       | 9       | 0      | 100%    |
| profiles/migrations/0002_alter_customuser_picture.py      | 5       | 0      | 100%    |
| profiles/migrations/0003_alter_customuser_picture.py      | 5       | 0      | 100%    |
| profiles/migrations/__init__.py                           | 0       | 0      | 100%    |
| profiles/models.py                                        | 14      | 1      | 93%     |
| profiles/tests.py                                         | 91      | 0      | 100%    |
| profiles/views.py                                         | 32      | 0      | 100%    |
| properties/__init__.py                                    | 0       | 0      | 100%    |
| properties/admin.py                                       | 7       | 0      | 100%    |
| properties/apps.py                                        | 4       | 0      | 100%    |
| properties/forms.py                                       | 54      | 1      | 98%     |
| properties/migrations/0001_initial.py                     | 9       | 0      | 100%    |
| properties/migrations/__init__.py                         | 0       | 0      | 100%    |
| properties/models.py                                      | 53      | 1      | 98%     |
| properties/tests.py                                       | 90      | 0      | 100%    |
| properties/views.py                                       | 97      | 77     | 21%     |
| user_management/__init__.py                               | 0       | 0      | 100%    |
| user_management/apps.py                                   | 4       | 0      | 100%    |
| user_management/forms.py                                  | 14      | 0      | 100%    |
| user_management/migrations/__init__.py                    | 0       | 0      | 100%    |
| user_management/templatetags/__init__.py                  | 0       | 0      | 100%    |
| user_management/templatetags/login_tag.py                 | 9       | 0      | 100%    |
| user_management/tests.py                                  | 14      | 9      | 36%     |
| user_management/views.py                                  | 24      | 16     | 33%     |
| --------------------------------------------------------- | ------- | ------ | ------- |
| TOTAL                                                     | 833     | 151    | 82%     |

## **Manual Testing**

Some functions are registered only for users, and some are exclusive to staff
members. The functions/views requiring manual testing are:

- Rent property (Logged user required)
- Profile view (Logged user required)
- Edit / Add Property (Staff required)

Please note that if you plan to evaluate the project, an admin username and
password have been provided during project submission. These credentials are
intended to facilitate the verification of the tests that have been conducted
on the 'Manage' page for adding new crypto support through the website

### **User Story Testing**

#### **Homepage**

'As a User, I want to land on a visually appealing home page that showcases 8
new properties available in the city. This will provide an engaging
introduction to the website and enable me to explore the latest offerings
easily.'

The homepage of this website is designed with two main sections, each serving
a specific purpose:

1. **Welcome Message**: A warm welcome message greets visitors to the site,
   creating a user-friendly and inviting atmosphere.
    - [x] Welcome message is displayed correctly.
      ![welcome-section](./README/welcome-section.png)

2. **Latest Properties Section**:
   The homepage prominently features the latest properties added to Homequest,
   offering visitors a glimpse of the newest additions to the website.
    - [x] The section accurately showcases the 8 new properties recently added
      to the platform.
      ![latest-properties-section](./README/latest-properties-section.png)

#### **AllAuth Implementation**

'As a Developer, I want to integrate Django AllAuth into the Homequest website
to manage user authentication and registration seamlessly. Additionally, I need
to customize the templates to ensure a consistent and branded user experience.'

The website features AllAuth implementation, providing users with easy access
to login and register functionalities. Relevant tests have been preset on the
login and register pages for improved functionality.

#### **Bootstrap Toast Django Implementation**

'As a Developer, I want to enhance the user experience on the Homequest website
by integrating Bootstrap Toast to display Django messages in a visually
appealing and user-friendly manner.'

Various features on the Homequest website incorporate the use of Bootstrap
Toast messages to provide users with clear and visually appealing feedback. The
following scenarios include the implementation of toast messages, and thorough
testing has been conducted to ensure their effectiveness:

1. **Login Error:**
   If a user enters misleading information during login, an error message will
   be displayed.

   ![Test Badge](https://img.shields.io/badge/Test-Pass-brightgreen)
2. **Registration Error:**
   Similarly, during registration, an error message will be shown in case of
   issues.

   ![Test Badge](https://img.shields.io/badge/Test-Pass-brightgreen)
3. **Payment Errors:**
   In the event of a problem with Stripe payment, a corresponding error message
   will be displayed.

   ![Test Badge](https://img.shields.io/badge/Test-Pass-brightgreen)
4. **Property Already Rented:**
   When a user attempts to rent an already rented property, an error message
   will inform them.

   ![Test Badge](https://img.shields.io/badge/Test-Pass-brightgreen)
5. **Order Completed:**
   After a successful completion of a rent order, a confirmation message will
   be displayed.

   ![Test Badge](https://img.shields.io/badge/Test-Pass-brightgreen)
6. **Contract Termination:**
   If a user terminates a rent contract, a toast message will confirm the
   action.

   ![Test Badge](https://img.shields.io/badge/Test-Pass-brightgreen)
7. **Agent Messaging:**
   When a user sends a message to an agent via the built-in email form, a
   success message will appear.

   ![Test Badge](https://img.shields.io/badge/Test-Pass-brightgreen)
8. **Agent Email Form Error:**
   In case of an error with the agent email form, an appropriate message will
   be displayed.

   ![Test Badge](https://img.shields.io/badge/Test-Pass-brightgreen)
9. **Property Creation:**
   Upon the creation of a new property, a success message will notify the user.
   ![Test Badge](https://img.shields.io/badge/Test-Pass-brightgreen)
10. **Property Image Deletion:**
    When a property image is deleted, a confirmation message will be shown.

    ![Test Badge](https://img.shields.io/badge/Test-Pass-brightgreen)
11. **Property Deletion:**
    Upon deleting a property, a confirmation message will be displayed.

    ![Test Badge](https://img.shields.io/badge/Test-Pass-brightgreen)
