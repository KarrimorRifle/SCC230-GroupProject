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

**Scope:** Schedules, Hub
**Primary Actor:** User
**Secondary Actor:** Database
**Preconditions:**

-   User has account
-   User is on site
-   User is on hub page
-   User has hub

**Main Success Scenarios:**

-   User clicks create schedule
-   User is taken to schedule creation page
-   User creates schedule
-   Schedule is saved onto hub
-   Updated in database

**Alternatives:**

-   4b. Schedule is valid and user selects run

**Exceptions:**
**Postconditions:**

-   user has a schedule saved onto the hub

#### **Name:** Assign Schedule

**Scope:** Schedule, Hub
**Primary Actor:** User
**Secondary Actor:** Database
**Preconditions:**

-   User has hub
-   User is logged in
-   User has valid schedule
-   User is on site
-   User is on hub page or schedule page

**Main Success Scenarios:**
(schedule page)

-   Clicks assign
-   Page shows house options (empty if none)
-   user clicks house to assign to
-   scheduling page shown (user has to replace devices with valid devices)
-   User clicks assign
-   Schedule is assigned to house & running

**Alternatives:**
4b. User clicks save

-   schedule is stored as draft inside hub

**Exceptions:**
**Postconditions:**

-   New schedule is assigned to hub

#### **Name:** Create Home

**Scope:** hub
**Primary Actor:** user
**Secondary Actor:** Database
**Preconditions:**

-   User logged in
-   User on website

**Main Success Scenarios:**

-   1- user clicks create hub
-   2- User directed to make hub page
-   3- User fills needed details
-   4- User clicks confirm
-   5- Site verifies details
-   6- new hub is created
-   7- User directed to assign devices pages of hub
-   8- Database updated

**Alternatives:**
5b. Details invalid

-   3 is repeated

**Exceptions:**
**Postconditions:**
User has new hub assigned to account

#### **Name:** Add Device

**Scope:** Hub
**Primary Actor:** User
**Secondary Actor:** Database
**Preconditions:**

-   User has hub on account
-   User logged in
-   User has admin+ permissions on hub
-   User on hub page
-   User has a device that can connect
-   Device is capapble f conneccting to hub (wired or wireless)

**Main Success Scenarios:**

-   1- User clicks add device
-   2- User is taken to add device page
-   3- User inputs needed details
-   4- User tests connections
-   5- Device is connected to the hub
-   6- User clicks save
-   7- Device is registered to hub
-   8- Device saved to hub DB

**Alternatives:**
7b. Device details not matching and doesnt connect to hub - back to 3

**Exceptions:**
**Postconditions:**
User has new device connected to the hub

#### **Name:** Manage Home

**Scope:** Hub
**Primary Actor:** User
**Secondary Actor:** Database
**Preconditions:**

-   User logged in
-   User has hub on account
-   User has admin+ permissions on hub
-   User on hub page

**Main Success Scenarios:**

-   1- User clicks manage hub
-   2- User is taken to manage hub page
-   3- User adjusts hub details
-   4- User clicks save
-   5- User role and new hub details are verified
-   6- Hub details are updated on database
-   7- User gets notification about the update

**Alternatives:**

-   4b. Hub details invalid (loop to 3)

**Exceptions:**

**Postconditions:**
Hub details are different from before

#### **Name:** Manage House Roles

**Scope:** Hub
**Primary Actor:** User
**Secondary Actor:** Database
**Preconditions:** 

-   User logged in
-   User has hub on account
-   User has admin+ permissions on hub
-   User on hub page

**Main Success Scenarios:**

-   1- User selects a member of the hub
-   2- User clicks manage role
-   3- User and member role verified
-   4- User selects new role for member
-   5- User and new member roles verified
-   6- User clicks save
-   7- Member role updated on database

**Alternatives:**

-   3b. Member role higher than User (loop to 1)
-   5b. New member role higher than User (loop to 4)

**Exceptions:**

**Postconditions:**
A member's role is updated on hub database