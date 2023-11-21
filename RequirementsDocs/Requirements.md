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
5. Allowing users to save schedules
6. Allowing users to create hubs and register devices to them
7. Allowing devices to communicate over a network
8. **to be decided...**

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
| 1.0 | Sign up | As a **potential user** I want to sign up | The **app** shall allow **user** to create an account |  | &cross; |
| 1.1 | Login | As a **user** I want an account to keep my details | The **app** shall allow **user** to login to their own account |  | &cross; |
| 1.2 |Password reset| As a **user** I would want to be able to reset my password in the case i forget it | System should allow **user** to reset the password with email or phone number || &cross;
| 2 | Create Hub | As a **user** I want to create a home to use link my devices | The **user** shall be able to create a **hub** to link devices to |  | &cross; |
| 2.1 | Initial Invites | As a **user** I want to initially send invites to other **users** to join the new hub I am creating | The **user** shall be able to create a **hub** invite to multiple **users** during hub creation process |  | &cross; |
| 3 | Register devices | As a **user** I want to register devices to the house | The **app** shall allow **user** to connect multiple devices to a **hub** |  | &cross; |
| 3.1 | See device status | As a **user** I want to be able to see which devices are currently connected to my hub | **User** shall be able to see all previously connected devices and their current connectivity status |  | &cross; |
| 3.2 | Auto-Assign device | As a **user**, If a schedule is missing a required device, I want that device to be automatically assigned to this schedule when registered to the **hub** | If the newly registered device matches a schedule's missing required device the **app** shall automatically assign it to the schedule upon device registration to the **hub** |  | &cross; |
| 4 | Design Schedule | As a **user** I want to create a theoretical schedule for certain IoT devices | The **app** shall allow **user** to make a schedule |  | &cross; |
| 4.1 | Device requirements | As a **user** I want my schedules to have a list of device types that they require to run | The **app** shall create a list of device types required for the schedule once the **user** saves their design schedule |  | &cross; |
| 5 | Assign Schedule | As a **user** I want to utilise my designed schedule and put it on a house/hub | The **user** shall be able to assign a designed schedule to **hub** |  | &cross; |
| 5.1 | Assign devices | As a **user** I want any schedules I assign to the hub to automatically be linked to appropriate devices | The **app** shall assign to the schedule the required devices that are currently linked to the **hub** within 1 second |  | &cross; |
| 5.2 | Missing Device Warning | As a **user** I want to know if a required device to run my schedule is not currently linked to the **hub** | The **app** shall notify the **user** if any required device is not currently linked to the **hub** within 1 second of schedule assignment |  | &cross; |
| 6 | Create schedule | As a **user** I want to create a schedule that can be loaded instantly to a hub | The **app** shall allow **user** to create a schedule that is assigned directly to the **hub** on completion | 7.B | &cross; |
| 7 | Delete schedule | As a **user** I want to delete a schedule that I have previously made | The **user** shall be able to delete a schedule from their account |  | &cross; |
| 8 | Export schedule | As a **user** I want to turn my schedules into a shareable template | The **app**  shall allow **user** to turn their schedule into a shareable format |  | &cross; |
| 8.1 | Import Schedule | As a **user** I want to be be able to import templates from others | The **app** shall allow **user** to import a file to add a schedule into the account |  | &cross; |
| 9 | Hub invite | as a **user** I want to add others to the hub | The **user** shall be able to invite other **users** to join the **hub** |  | &cross; |
| 9.1 | Select Roles | as a **user** I want to be able to select specific roles for others when inviting them to the **hub** | The **user** shall be allowed to select roles when creating an invite for others |  | &cross; |
| 9.2 | Accept/Deny hub invite | as a **user** I want to be able to accept or deny an invite to join a **hub** | The **app** shall send notification to **user** and allow them to accept or deny a **hub** invite |  | &cross; |
| 10 | Hub join request | as a **user** I want to be able to request to join a **hub** | The **user** shall be able send a **hub** join request |  | &cross; |
| 10.1 | Accept/Deny join request | as a **hub owner** I want to be able to accept or deny a **user** request to join my **hub** | The **app** shall send notification to **hub owner** and allow them to accept or deny a **hub** join request |  | &cross; |
| 11.0 | Manage Roles | As a **Hub admin** I want to manage roles of other accounts on the hub | The **hub admin** shall be able to change other **user**'s roles |  | &cross; |
| 12.0 | Remove schedule | As a **user** with appropriate role i want to be able to remove an inactive or unwanted schedule from the **hub** | The **app** allow **user** (perm oriented) to remove a schedule from the **hub** |  | &cross; |
| 13.0 | Modify Settings | As a **user** I want to modify my own settings | The **user** shall be able to modify account settings |  | &cross; |
| 14 | Toggle schedule activation | As a **user** with appropriate role want to be able to activate/deactivate a schedule on the **hub** | The **app** shall allow **user** with appropriate role to activate and deactivate schedules on **hub** |  | &cross; |
| 14.1 | Request schedule activation | As a **user** having lower role I want to be able to request owner for activation/deactivation of my schedule on the **hub** | The **app** shall allow **user** with lower role to request **hub owner** activate and deactivate schedules on the **hub** |  | &cross; |
| 14.2 | Accept/Deny schedule activation | As a **hub owner** I want to be able to accept or deny any request for activation/deactivation of a schedule on my **hub** | The **app** shall send the **hub admin** a notification and allow them to accept or deny requests to activate and deactivate schedules on my **hub** |  | &cross; |
| 15.0 | Scalability | As a **user** I want to be able to access the system regardless of other users. | The **app** should to be able to support several **users** concurrently |  | &cross; | 
| 16.0 | Availability | As a **user** I want to be able to access the system at any time | The **app** should be active 24/7 for the majority of each year |  | &cross; |
| 17.0 | Robustness | As a **user** I do not want to encounter errors | The **app** should be able to handle all erroneous inputs |  | &cross; |
| 18.0 | User Serviceability | As a **user** I want to be able to fix mistakes that I have made | The **app** should include options to undo actions, require **user** confirmation for big changes, and have a help page regarding common issues and FAQs |  | &cross; |
| 19.0 | Accessibility | I want to be able to effectively use the system as an **Impaired User** | the **UI** should be colorblind-friendly, easy to read and navigate without cursor |  | &cross; |
| 20.0 | Device Usability | As a **user**, I wouuld like to be able to access the site across multiple devices | The **app** should allow for access across multiple devices |  | &cross; |
| 21 | Open Source | As a **user**, I would like to be able to access and upload schedule templates to a shared **database**. | The **app** should allow **users** to make working schedules public/send them to a shared pool |  | &cross; |
| 21.1 | Positive Recommendations | As a **user**, I would only like to be recommended relevant and high-quality schedules from the shared **database** | The **app** shall allow **users** to like & dislike schedules which will then be used to suggest schedules |  | &cross; |
| 22.0 | Variety | As a **user**, I would like to be able to connect to a wide variety of IOT devices |The **app** should implement several common IOT device APIs |  | &cross; | 