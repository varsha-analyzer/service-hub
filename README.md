# Service Hub Directory

A full-stack web application that helps users find and connect with local service providers based on their service needs and location.

## Overview

http://127.0.0.1:5000

Service Hub Directory is a web application developed to make it easier for users to find local service providers in one place.

Users can create an account, log in, search for services, select a service category, find service providers, and send service requests. The application also includes an admin section for managing users, service providers, categories, and requests.

The project is built using Python, Flask, HTML, CSS, and MySQL.

## Features

* **User Authentication**: Users can register and log in to the application
* **Service Provider Search**: Find service providers based on service requirements
* **Service Categories**: Browse different types of local services
* **Location-Based Search**: Search for providers based on location
* **Service Requests**: Users can send requests to service providers
* **Provider Management**: Manage service provider information and approvals
* **Admin Dashboard**: Manage users, providers, categories, and requests
* **Database Management**: Store user, provider, category, and request information using MySQL
* **Responsive Interface**: Simple interface for accessing the service directory

## Prerequisites

Before running the project, make sure you have:

* Python installed
* MySQL installed
* MySQL Workbench or another MySQL client
* Git installed
* A web browser

## Setup

1. **Clone the repository:**

```bash
git clone https://github.com/varsha-analyzer/service-hub-directory.git
cd service-hub-directory
```

2. **Install the required Python packages:**

```bash
pip install flask mysql-connector-python
```

3. **Set up the MySQL database:**

Create the database:

```sql
CREATE DATABASE service_hub;
```

Create the required tables for:

```text
users
categories
service_providers
service_requests
```

4. **Configure the database connection:**

Update the MySQL connection details in the Flask application.

The connection should contain the correct:

```text
Host
Username
Password
Database
```

5. **Start the application:**

```bash
python app.py
```

6. Open the local address shown by Flask in your web browser.

## Application Workflow

The application works through the following flow:

```text
User
  ↓
Register / Login
  ↓
Select Service Category
  ↓
Search for Service
  ↓
Search by Location
  ↓
View Service Providers
  ↓
Select Provider
  ↓
Send Service Request
  ↓
Provider / Admin Manages Request
```

## User Features

### Registration and Login

Users can create an account and log in to access the service directory.

### Service Search

Users can search for the type of service they need and find available service providers.

### Service Categories

Users can select different service categories to find providers related to their requirements.

Examples include:

```text
Electrician
Plumber
Carpenter
Cleaning
Repair Services
Home Services
```

### Service Requests

After finding a suitable provider, users can send a service request.

The request can then be managed by the service provider or administrator.

## Admin Features

The admin section provides management functionality for the application.

The admin can manage:

* Users
* Service providers
* Service categories
* Pending providers
* Approved providers
* Service requests

The dashboard can display information such as:

```text
Total Users
Total Providers
Pending Providers
Approved Providers
Total Requests
Total Categories
```

## Database

The application uses **MySQL** to store and manage the application data.

The main tables used in the project are:

```text
users
categories
service_providers
service_requests
```

These tables store information about users, service providers, service categories, and service requests.

## Tech Stack

* **Python** – programming language
* **Flask** – web application framework
* **HTML** – webpage structure
* **CSS** – webpage styling
* **Jinja2** – template rendering
* **MySQL** – database
* **MySQL Connector** – database connectivity
* **Git** – version control
* **GitHub** – source code repository

## Configuration

### Database Configuration

The application requires a MySQL database connection.

Update the database configuration with your own MySQL details:

```text
Host: localhost
Username: your_username
Password: your_password
Database: service_hub
```

Do not upload your actual database password or other private credentials to GitHub.

## Project Structure

```text
service-hub-directory/
│
├── SERVICE HUB DIRECTORY/
│
├── login.html
│
└── README.md
```

The repository currently contains the Service Hub Directory project files and HTML login page.

## Common Issues

### MySQL Connection Error

If the application cannot connect to MySQL:

* Make sure MySQL is running.
* Check the database name.
* Check your MySQL username.
* Check your MySQL password.
* Check the database connection code.

### Database Does Not Exist

If you receive an error that the database does not exist:

```sql
CREATE DATABASE service_hub;
```

Then make sure the application is connected to the `service_hub` database.

### Table Does Not Exist

If you receive a table-not-found error:

* Check that the required tables have been created.
* Check the table names.
* Make sure the table names match the names used in the Python application.

### Template Not Found

If Flask displays a `TemplateNotFound` error:

* Check that the HTML file exists.
* Check the filename spelling.
* Check the template path.
* Make sure Flask is pointing to the correct templates directory.

### Application Not Starting

If the Flask application does not start:

* Check that Python is installed.
* Check that Flask is installed.
* Check the Python file name.
* Check the terminal for the error message.

## Development

The project can be developed further by adding new service categories, improving the user interface, adding new provider features, and improving the service request workflow.

The main development areas include:

```text
User Management
Service Provider Management
Service Categories
Service Requests
Admin Dashboard
Database Management
```

## Future Improvements

Some improvements that can be added to the project are:

* Add ratings and reviews
* Add service provider availability
* Add online booking
* Add map and location integration
* Add notifications
* Add provider verification
* Improve the admin dashboard
* Add a reward system
* Improve the search functionality
* Deploy the application online
* Improve the responsive design

## Website

Once the project is deployed, add the live application URL here:

```markdown
[**Visit Service Hub Website →**](http://127.0.0.1:5000)
```

For example, the top of the README can be written as:

```markdown
# Service Hub Directory

A full-stack web application that helps users find and connect with local service providers.

[**Website**](http://127.0.0.1:5000) · [**GitHub**](https://github.com/varsha-analyzer/service-hub-directory)
```

When someone clicks **Website**, it should open your actual deployed **Service Hub application**, while **GitHub** should open your source-code repository.

## Contributing

If you want to contribute to this project, you can:

* Report bugs
* Suggest new features
* Improve the existing code
* Add new service categories
* Improve the user interface
* Improve the database structure
* Submit changes through GitHub

## License

This project was created for learning and development purposes.

## Repository

[**Service Hub Directory on GitHub**](https://github.com/varsha-analyzer/service-hub-directory)

## Author

**Varsha**

Service Hub Directory was developed as a practical project to learn and apply **Python, Flask, MySQL, HTML, CSS, and web application development**.
