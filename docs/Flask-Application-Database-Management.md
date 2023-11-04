# Flask Application Database Management

## Introduction
This document describes the process of integrating database version control into a Flask web application using Flask-Migrate. It outlines the steps taken to set up the development environment and provides guidance for future database development and migrations.

## Setting Up the Development Environment

### Local Database Setup
The Flask application uses SQLAlchemy as the ORM (Object-Relational Mapper) and SQLite as the database for local development. SQLite is a lightweight, disk-based database that doesn't require a separate server process, making it an ideal choice for development and testing.

### Flask-Migrate Integration
Flask-Migrate is an extension that handles SQLAlchemy database migrations for Flask applications. It uses Alembic to maintain database version control, allowing for smooth schema changes and data migrations. Here are the steps taken to integrate Flask-Migrate:

1. **Installation**: Added `Flask-Migrate` to the `requirements.txt` file to manage the dependencies.
   
2. **Initialization**:
    - Imported `Migrate` in the application factory function in `website/__init__.py`.
    - Initialized `Migrate` with the Flask app (`app`) and the database instance (`db`).

3. **Creating Migration Repository**:
    - Ran `flask db init` to create the migration directory and necessary files, including `alembic.ini`, which holds the migration configuration.

4. **Generating Initial Migration**:
    - Ran `flask db migrate -m "Initial migration."` to autogenerate a migration script that represents the current state of the database models.

5. **Applying Migrations to the Local Database**:
    - Ran `flask db upgrade` to apply the generated migration to the local SQLite database.

## How the Flask App Handles Databases

The Flask application uses the following components to handle databases:

- **SQLAlchemy**: Serves as the ORM that allows the application to interact with the database using Python classes and objects.
- **Flask-SQLAlchemy**: Provides helpful defaults and additional functionality to simplify database operations within Flask.
- **SQLite**: Acts as the local database engine used during development.
- **Flask-Migrate**: Manages database schema changes through migrations, keeping track of versions and changes over time.

## Working with the Database Going Forward

### Development Workflow
When making changes to the database models, follow these steps:

1. Modify your model classes in the application (usually within `models.py`).
2. Run `flask db migrate -m "Description of changes"` to generate a new migration script.
3. Review the generated script to ensure the changes match your intentions.
4. Run `flask db upgrade` to apply the changes to your local development database.

### Production Migrations
Before applying new migrations to a production database:

1. Test all new migrations in a staging environment that mirrors production.
2. Backup the production database before applying new migrations.
3. Apply the migrations during a maintenance window to minimize impact on users.

### Version Control
Commit all migration scripts to the project's version control system (git):

- Track the `migrations` folder and its contents.
- Include the updated `requirements.txt` with `Flask-Migrate` added.

By following these practices, you can ensure that your database schema evolves in a controlled and predictable manner alongside your application's codebase.