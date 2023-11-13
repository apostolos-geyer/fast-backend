# Music Social Media Project

## Introduction
This project is a learning journey into full-stack development and databases. The aim is to create a music social media platform where users can connect their Spotify accounts, add friends, and compare their music tastes.

### Current Status
As of now, the project is in the initial stages with a focus on backend development using FastAPI and SQLAlchemy. The backend setup includes:

- User account creation
- User login with JWT authentication
- User session management
- Basic user CRUD operations

### Roadmap:

#### Setup
- [x] Project initialization
- [x] Connect to local database (database.py)

#### User basics backend
- [x] Implement user model

- [ ] Implement user schemas (users/schemas.py)
  - [x] Base schema
  - [x] User creation schema
  - [ ] User update schema
  - [x] User in db schema
  - [x] Authentication token for JWT
  
- [x] Implement user CRUD (users/crud.py)
  - [x] create operations
  - [x] read operations 
  - [x] update operations
  - [x] delete operations
     
- [x] Implement basic user endpoints (users/endpoints.py)
  - [x] create user
  - [x] get user/users
  - [x] login (get token)
  - [x] test login token endpoint (get me) 
  - [ ] update user
  - [ ] delete user 

#### Next steps: 
Current goal is to complete user basics, and then either move into getting a basic front end together or adding more models and databases. 


## Installation

Instructions for setting up the project locally.

```bash
# clone the repository
git clone <repository-url>

# navigate to the project directory
cd <project-name>

# install dependencies (assuming poetry is being used)
poetry install

# run the application
uvicorn main:app --reload
