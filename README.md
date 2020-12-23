# cs50w-finalproject-capstone

## Poli

Poli is a platform that allows an organization divided into work units to establish the estimated capacities to execute different types of tasks in parallel (*or not*) at user-defined time intervals, within a specific calendar. Work units have capabilites, and these, combined by the user, define types of tasks, for which the aforementioned capabilites are assigned. The model under which capabilities are created and configured is based exclusively on the user or organization experience.

Once types of tasks and schedules are defined for work units, the application exposes a web interface for consumer users for consulting the availability of execution of a type of task, subsequently allowing to book an appointment in a work unit to be carried out on the scheduled calendar.

For the availability query, the application performs a deterministic calculation that combines the remaining capacities in each work unit, for each type of enabled task, returning the available scheduling offer.

[Latest code coverage report](https://eldocbrown.github.io/cs50w-finalproject-capstone/index.html)
