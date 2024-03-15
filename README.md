<br>

# Animal Pests Biosecurity Guide System
<br>

## Product Background & Requirements
A Web App functioning as a biosecurity guide, providing information on animal pests present in New Zealand.
>It provides management functions. As an administrator, you can manage the guides and user information in the system. Management functions include adding, modifying, deleting, and querying guides and user profiles.
>
>As a general staff, you can manage guides and view Controller users. 
>
>As a Controller user, you can view all Guide information, including lists and details.
<br>

## Technologies Applied

* Python
* Flask
* Jinja
* MySQL
* HTML
* Bootstrap
* CSS
<br>

## How to Access This Web App
**[Please click here to its Homepage.](http://cedar66.pythonanywhere.com/)**

__Access Account__
| Username  | Password | Role |
| ------------- |-------------|:-------------:|
|controller1 | Admin@123|Pest Controller|
|controller2 | Admin@123|Pest Controller|
|controller3 | Admin@123|Pest Controller|
|controller4 | Admin@123|Pest Controller|
|controller5 | Admin@123|Pest Controller|
|staff1 | Admin@123|Staff|
|staff2 | Admin@123|Staff|
|staff3 | Admin@123|Staff|
|admin | Admin@123|Administrator|

<br>

## Design Decisions

__1. Blueprint Design Strategy__

>The internal design of the software takes into account the sub-file management back-end Python programme. 
>
>All the backend code in one py file can lead to long files. It is not very readable, and it is not easy to maintain. 
>
>Therefore, I split the most of Administrator role code into admin.py, while keeping the rest of the functional code in app.py file.
>
>For future consideration, I'll be looking to split the Staff related functions into a staff.py file as well.
>
>Adopted Flask's Blueprint design strategy and framework.
>

__2. Colour scheme__

>The overall colour scheme is considered to be royalblue, white and black. 
>
>Royalblue is a mild and calm colour, easy to be accepted by most people. 
And it is also my favourite colour. 
So royalblue is used as the colour of the title, navigation bar and buttons. 
>
>The table data is more serious content, so black is more appropriate. 
It also creates a colour contrast.


__3. All users with different roles in one profile database table.__
>
>Two reasons for this design:
>
>First, there are only three role types, which is not a strong enough reason to split the table. 
>
>Secondly, the roles can be distinguished by the Department field. For example, the Controller user is assigned to the Controller department. This would consolidate all users into one table, which would help development efficiency.
>
>However, it is worth noting that if the number of user roles increases, it is still necessary to split the user roles into separate tables.


<br>
