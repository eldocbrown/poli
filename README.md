# cs50w-finalproject-capstone

## Poli

Poli is a platform that allows an organization whose work takes place at different locations to establish the capacities to execute different types of tasks in parallel (*or not*) at user-defined time intervals, within a specific calendar. The model under which tasks and locations are created and configured is based exclusively on the user or organization experience.

Once types of tasks and schedules are defined for locations, the application exposes a web interface for consumer users for consulting the availability of execution of a type of task, subsequently allowing to book an appointment at a location to be carried out on the scheduled calendar. Consumers can see and cancel bookings afterwards, in a specific schedule page.

Corporate users are provided with a dedicated web application where they can see administered location schedules on a daily basis with an occupancy report. Also they can configure location availabilities in ways it is easy to repear certain configuration daily or weekly. Available tasks, locations, and supervised locations are configured via a system superuser in the django admin interface.

### Features
...

### Why I did it
Years ago I was working at a company that installed tracking devices in vehicles. Vehicle types could be bikes, cars, trucks, trailers, boats. Installations and services were done in shops across the country, and managing service schedules was a tough. While when I was working there we developed a custom made software solution for solving these problems, it was tightly coupled with the company's bussiness domain, and I always thought that if a platform existed that could provide the solution, it would have been somewhat cost effective. This is why I chose to create Poli, to solve these kind of problems I faced in the past.

### Distinctiveness and Complexity

#### Project Structure
The project has two Django applications that rely to work on only one set of models, and one user administration.

The main application is Policorp, intended to be used by corporate users. It has all the models and provides an interface for integrating with them throughout the process.

Policon is an application that integrates with Policorp and provides consumer users ways to interact with corporate services.

#### User Roles Model
There are three user roles available:
- Consumer: These users can access Policon app to book, see their own schedule, or cancel bookings. Anyone can register as a consumer.
- Corporate Location Supervisor: These users manage locations schedules. They can create availabilities on a location schedule, and see a report of occupancy on a daily basis.
- Corporate Superuser: This is the basic Django provided superuser. Superusers create available tasks and locations, create corporate supervisor users, and assign them to certain locations, via the standard admin console.

#### External Javascript libraries
Several external Javascript libraries are used for UI design:
- [Bootstrap](https://getbootstrap.com/docs/4.4/getting-started/introduction/)
- [jQuery](https://jquery.com/)
- [Popper](https://popper.js.org/docs/v1/)
- [Gijgo](https://gijgo.com/)
- [Chart.js](https://www.chartjs.org/)


#### Code test coverge
Python code in this project was built using a TDD approach, providing tests at different levels (*models, views, clients*). Code covergate is of more than 90%, with more than 120 tests, generating a set of tests sufficient enough to minimize regression errors while evolving the application.

#### CI/CD
A push on the master branch triggers a github action, which runs all tests, and sets a threshold of code test coverage to 90%, failing if it results under that limit value. A code coverage report is then generated and published to GitHub Pages.

Latest code coverage report can be seen [here](https://eldocbrown.github.io/cs50w-finalproject-capstone/)

### Project files description
###### capstone/settings.py
Standard project settings.
###### capstone/urls.py
Routes file for Capstone project, which includes paths for Policon and Policorp apps.
###### manage.py
Manager script created by Django.
###### policon/static/policon/image/*
Static image resources used in Policon app UI.
###### policon/static/policon/policon.js
Javascript functions file used in Policon app.
###### policon/static/policon/styles.css
CSS stylesheet file for Policon app UI.
###### policon/templates/policon/index.html
Django template for Policon Single Page Application.
###### policon/templates/policon/layout.html
Basic Django template that contains a bootstrap navbar and a container so the web site is built as a Single Page Application.
###### policon/templates/policon/login.html
Login registration page for consumer users in Policon app.
###### policon/templates/policon/register.html
Consumer user registration page.
###### policon/admin.py
Admin console app configuration file por Policon app. Not used.
###### policon/apps.py
Policon application configuration file.
###### policon/models.py
Standard models file created by Django. Not used.
###### policon/tests.py
Basic tests for Policon app
###### policon/urls.py
Routes file por Policon app.
###### policon/views.py
Views functions for Policon app.
###### policorp/static/policorp/policorp.js
Javascript functions file used in Policorp app.
###### policorp/static/policorp/styles.css
CSS stylesheet file for Policorp app UI.
###### policorp/templates/policorp/index.html
Django template for Policorp Single Page Application.
###### policorp/templates/policorp/layout.html
Basic Django template that contains a bootstrap navbar and a container so the Policorp web site is built as a Single Page Application.
###### policorp/templates/policorp/login.html
Login registration page for corporate users in Policorp app.
###### policorp/admin.py
Admin console app configuration file por Policorp app.
###### policorp/apps.py
Policorp application configuration file.
###### policorp/lib/schedule.py
Schedule class that combines availabilities and bookings, so they can be provided to a user as a unified schedule.
###### policorp/managers.py
Manager classes
###### policorp/migrations/*
Databse migration files created by Django when running `makemigrations` command
###### policorp/models.py
Models classes file
- User: *derived from AbstractUser, it adds the capability of defining a location supervisor as a user role.*
- Availability: *it is an opening at a a location for executing a certain task, on a certain date and time.*
- Location: *places where a task can be executed.*
- Task: *activities that can be offered to be executed.*
- Booking: *a reservation of an availability by a consumer user.*

###### policorp/tests/aux.py
Auxiliary function file for test cases.
###### policorp/tests/testsClients.py
Test cases using from a Client instance perspective.
###### policorp/tests/testsCreateAvailabilityViews.py
Test cases related to availabilities creation.
###### policorp/tests/testsModels.py
Test cases for models, managers and their methods.
###### policorp/tests/testsViews.py
Test cases of views, checking response codes, security restrictions, and data returned.
###### policorp/tests/testsschedule.py
Test cases for Schedule class.
###### policorp/urls.py
Routes file por Policorp app.
###### policorp/views.py
Views functions for Policorp app.
