#### **Name:** Sign Up

**Scope:** Account system
**Primary Actor:** User
**Secondary Actor:** Database
**Preconditions:**

-   User has no account
-   User has connection to the internet
-   User is on our website
-   User is at login page

**Main Success Scenarios:**

-   1- User selects sign up
-   2- User enters required details
-   3- Account details verified by system
-   4- User is verified via email link
-   5- User logged in
-   6- User is brought to main page

**Alternatives:**
3a. Email already in use (Loop back to 2)
**Exceptions:**
3b. Details invalid (Loop back to 2)
**Postconditions:** User has an account registered on the database

#### **Name:** Log In

**Scope:** Account system & website
**Primary Actor:** User
**Secondary Actor:** Database
**Preconditions:**

-   User has internet
-   User has registered account
-   User is on our website
-   User is at login page

**Main Success Scenarios:**

-   1- User enters Login details
-   2- Account details verified by system
-   3- User logged in
-   4- User brought onto home page

**Alternatives:**
2a. Details dont match (loop back to 1)
**Exceptions:**
2a. Malicous activity attempted / detected - User IP blacklisted
**Postconditions:**
User is logged into the system
User is able to access account specific systems / details

#### **Name:** Modify Account Settings

**Scope:** Account system
**Primary Actor:** User
**Secondary Actor:** Database
**Preconditions:**

-   User has an account
-   User is logged into system
-   User is on website
-   User has internet connection
-   User is on user settings page

**Main Success Scenarios:**

-   1- User adjusts details
-   2- User enters password
-   3- User clicks save
-   4- User password and details are verified
-   5- User details are saved onto database/updated
-   6- User gets notification that it has been updated

**Alternatives:**

-   4a. User password incorrect (loop to 2)
-   4b. User details invalid (loop to 1)

**Exceptions:**

-   4b. Malicous activity detected
    -   User email is blacklisted
    -   User IP is blacklisted
    -   account is deleted

**Postconditions:**
User account details are different from before.

#### **Name:** Load/Import Schedule

**Scope:**
**Primary Actor:**
**Secondary Actor:**
**Preconditions:**
**Main Success Scenarios:**
**Alternatives:**
**Exceptions:**
**Postconditions:**

#### **Name:** Design Schedule

**Scope:**
**Primary Actor:**
**Secondary Actor:**
**Preconditions:**
**Main Success Scenarios:**
**Alternatives:**
**Exceptions:**
**Postconditions:**

#### **Name:** Export Schedule

**Scope:**
**Primary Actor:**
**Secondary Actor:**
**Preconditions:**
**Main Success Scenarios:**
**Alternatives:**
**Exceptions:**
**Postconditions:**

#### **Name:** Create Schedule

**Scope:**
**Primary Actor:**
**Secondary Actor:**
**Preconditions:**
**Main Success Scenarios:**
**Alternatives:**
**Exceptions:**
**Postconditions:**

#### **Name:** Assign Schedule

**Scope:**
**Primary Actor:**
**Secondary Actor:**
**Preconditions:**
**Main Success Scenarios:**
**Alternatives:**
**Exceptions:**
**Postconditions:**

#### **Name:** Create Home

**Scope:**
**Primary Actor:**
**Secondary Actor:**
**Preconditions:**
**Main Success Scenarios:**
**Alternatives:**
**Exceptions:**
**Postconditions:**

#### **Name:** Add Device

**Scope:**
**Primary Actor:**
**Secondary Actor:**
**Preconditions:**
**Main Success Scenarios:**
**Alternatives:**
**Exceptions:**
**Postconditions:**

#### **Name:** Manage Home

**Scope:**
**Primary Actor:**
**Secondary Actor:**
**Preconditions:**
**Main Success Scenarios:**
**Alternatives:**
**Exceptions:**
**Postconditions:**

#### **Name:** Manage House Roles

**Scope:**
**Primary Actor:**
**Secondary Actor:**
**Preconditions:**
**Main Success Scenarios:**
**Alternatives:**
**Exceptions:**
**Postconditions:**
