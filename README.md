# Music Social Media Project

## Introduction
This project is a learning journey into full-stack development and databases. The aim is to create a music social media platform where users can connect their Spotify accounts, add friends, and compare their music tastes.

### Current Status
As of now, the project is in the initial stages with a focus on backend development using FastAPI and SQLAlchemy. The backend setup includes:

- User account creation
- User login with JWT authentication
- User session management
- Basic user CRUD operations

### Roadmap

- [x] Project initialization
- [x] Backend setup with FastAPI
- [x] User model creation
- [x] Authentication implementation
- [ ] Frontend development with React
- [ ] Integration with Spotify API
- [ ] Feature to compare music tastes
- [ ] Friend system implementation
- [ ] Deploying the application
- [ ] Additional features based on feedback

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
