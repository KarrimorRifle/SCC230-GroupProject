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

#### **Name:** Design Schedule

**Scope:** Scheduling system
**Primary Actor:** User
**Secondary Actor:** Database
**Preconditions:**

-   User is logged in
-   User has internet connection

**Main Success Scenarios:**

-   1- User presses design schedule
-   2- New draft schedule created (with default trigger)
-   3- User selects trigger
-   4- User designs schedule with available nodes
-   5- User clicks save schedule
-   6- Schedule input are verified
-   7- Schedule saved onto database
-   8- Schedule assigned to user's account

**Alternatives:**

-   5a. User clicks draft toggle
    -   6, 7, 8
    -   9- Set draft to not true on system
-   5b. user clicks assign to house
    -   6,7,8,9
    -   10- Schedule is assigned to valid house
    -   run create schedule

**Exceptions:**
5b - User has no house, not ran
6b - User has invalid input

-   User prompted to reinput values
    6c - Malicous inputs detected
-   run Malicous activity handling

**Postconditions:**
1a. User has new shcedule
1b. User has new shedule assigned to house

#### **Name:** Load/Import Schedule

**Scope:** Scheduling System
**Primary Actor:** User
**Secondary Actor:** Database
**Preconditions:**

-   User is on the website
-   User has a link / file to import
-   User has an account
-   (alternative) User has a house / hub
-   User is on scheduling page

**Main Success Scenarios:**

-   1- User clicks import
-   2- User gives link or file
-   3- User selects where to import to
-   4- User assigns devices to schedule imported
-   5- update on database

**Alternatives:**

-   4b. User does nothing as schedule is imported into account

**Exceptions:**
**Postconditions:**

-   User has new schedule in account or hub

#### **Name:** Export Schedule

**Scope:** Schedules
**Primary Actor:** User
**Secondary Actor:**
**Preconditions:**

-   User has account
-   User has schedule not in draft mode
-   User is on area which has schedules (hub or account)

**Main Success Scenarios:**

-   1- user clicks export
-   2- options are shown for link or file
-   3- user clicks file
-   4- Schedule file is compiled
-   5- Schedule is downloaded on browser

**Alternatives:**

-   3b. User clicks link
    -   link to schedule is given where it can be imported

**Exceptions:**

-   Connection error when fetching resources

**Postconditions:**

-   user now has a schedule installed

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
