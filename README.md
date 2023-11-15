# Simple FastAPI based backend

## Introduction
A backend I was developing for a personal projects & learning. Realized that it would likely make a good template / starting point for my own future projects, so I've changed this repo to just be that backend... Lol 

### Current Status
As of now, the backend connects to a SQL Database using SQLAlchemy, and has a table for Users, and Sessions, as well as the following endpoints:

POST ENDPOINTS:
- `POST /user/` to create a user.
- `POST /session/login` to login to an account (creates a session in the session database with a session id and a foreign key to the user)
- `POST /session/logout` to logout of an account (deletes all sessions in the session database for a user)
- `POST /session/auth` to get a short lived JWT Auth token, required to update or delete your account when logged in.
  
GET ENDPOINTS:
-  `GET /user/me` to get the user info for the user associated with the current session
-  `GET /user/{user_id}` to get the user info associated with the user with {user_id}
-  `GET /user/` to get a specified number of users, takes arguments `skip` and `limit`...

PUT ENDPOINTS:
- `PUT /user/me` to update information about the user for the current session, requires auth.

DELETE ENDPOINTS
- `DELETE /user/me` to delete the current user, requires auth.

im not givin yall detailed documentation this my shi go read the code. 

### Next steps:
- Move over to asynchronous
- Improve session model, perhaps switch to JWT tokens + refresh tokens, or at least switch session id's away from integers.
- Implement user permission levels
- Make it have more swag
- Talk to a girl for the first time 
