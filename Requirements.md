# Requirements

## App mission

Allowing non-developers to interact with internet-of-things (IOT) items through a high-level code-blocks interface, similar to scratch.

## Bringing requirements into github

### Milestones:

**Milestone** will include set **FR**s and their **NFR**s
Milestones may be achieved concurrently, due to the nature of development. The order below is the expected order of completion.

Currently planned Milestones:

1. Allowing users to place code-blocks
2. Having the code-blocks interact with a micro-controller, allowing for output
3. Recieve inputs from a micro-controller's connected sensors
4. Allowing users to create and log in to accounts
5. Allowing users to save routines
6. Allowing devices to communicate over a network
7. **to be decided...**

### Issues

An issue for each requirements (**FRs & NFRs**)

## Requirements

### Priority Brackets

| Code | Meaning |
| -------- | ------------------------ |
| **#**.\_ | **Week to be completed** |
| \_.**A** | **Urgent** |
| \_.**B** | **Important** |
| \_.**C** | **Low urgency** |

### FR & NFR

| For | Format |
| ------------ | ------ |
| Feature FRs | X |
| Feature NFRs | X.X |

| ID | Feature | User Story | Description | Priority Bracket | Complete? |
| --- | --- | --- | --- | --- | --- |
| 1.0 | Sign up | As a **potential user** I want to sign up | Allow user to create an account | 5.A | &cross; |
| 2.0 | Login | As a **user** I want an account to keep my details | Allow user to login to their own account | 5.A | &cross; |
| 3 | Create Home | As a **user** I want to create a home to use link my devices | Allow user to create a home/hub to link devices to | 7.A | &cross; |
| 4 | Register devices | As a **user** I want to register devices to the house | Allow user to connect multiple devices to a home/hub | 7.B | &cross; |
| 5 | Design Schedule | As a **user** I want to create a theoretical design / schedule | Allow user to make a schedule which can be hooked up to virtual devices (as a temporary palcement). | 7.B | &cross; |
| 6 | Assign Schedule | As a **user** I want to utilise my designed schedule and put it on a house/hub | Allow user to assign a design schedule to house / hub and assign devices to replace the temp virtual devices, It will then be stored and activated on the hub if it all checks out
| 7 | Create schedule | As a **user** I want to create a schedule that can be loaded instantly to a house/hub | Allow user to create a schedule that is assigned to the house on completion | 7.B | &cross; |
| 8 | Export schedule | As a **user** I want to turn my schedules into a shareable template | Allow user to turn house schedule into a design schedule | 7.B | &cross; |
| 9 | Import Schedule | As a **user** I want to be be able to import templates from others | Allow user to import a file to add a schedule into the account |  | &cross; |
| 10.0 | Hub invite | as a **user** I want to add others to the hub | Allow user to add other users to the hub |  | &cross; |
| 11.0 | Manage Roles | As a **Hub admin** I want to manage roles of other accounts on the hub | allow **hub admin** to change other user's roles |  | &cross; |
| 12.0 | Modify Settings | As a **user** I want to modify my own settings | Allow **user** to modify account settings |  | &cross; |
| 13.0 | Scalability | As a **user** I want to be able to access the system regardless of other users. | Write the system to be able to support several users concurrently |  | &cross; | 
| 14.0 | Availability | As a **user** I want to be able to access the system at any time | Write the system so that it is active 24/7 for the majority of each year |  | &cross; |
| 15.0 | Robustness | As a **user** I do not want to encounter errors | Write code to handle all erroneous inputs |  | &cross; |
| 16.0 | User Serviceability | As a **user** I want to be able to fix mistakes that I have made | Include options to undo, add a help page. |  | &cross; |
| 17.0 | Accessibility | I want to be able to effectively use the system as an **Impaired User** | Ensure the UI is colorblind-friendly, easy to read, and can be easily navigated without the use of a cursor. |  | &cross; |
| 18.0 | Device Usability | As a **user**, I wouuld like to be able to access the site across multiple devices | The system could allow for access across multiple devices |  | &cross; |
| 19.0 | Paired Programming | As a **user**, I would like to have AI assistance for code, similar to autocorrect, based on the project's title. | The system should implement a simple AI to suggest the next steps in a program, based on the title and description |  | &cross; |
| 20.0 | Open Source | As a **user**, I would like to be able to access and upload schedule templates to a shared database. | The system should allow users to send working schedules to a shared pool |  | &cross; |
| 20.1 | Positive Recommendations | As a **user**, I would only like to be recommended relevant and high-quality schedules from the shared database | The system should allow users to like & dislike schedules which will then be used to suggest schedules |  | &cross; |
|21|Password reset| As a **user** I would want to be able to reset my password in the case i forget it | System should allow user to reset the password with email or phone number || &cross;