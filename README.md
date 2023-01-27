# youtube_api
1. git clone https://github.com/AlexSitohov/youtube_api.git
2. cd app
3. create .env and and set there (SMTP_USER, SMTP_PASSWORD, JWT_SECRET_KEY)
4. docker-compose up
5. http://localhost:8080/docs

api endpoints:
/registration post. register new user.

/login psot. get jwt token

/users get. get all users/
/user/{user_id} get. get user with id == user_id

/contents post. create content(in future it will be video)
/contents get. get all content/
/content/{id_content} get. get one

/likes post. like content
/liked-content get. get all liked content

/playlists post. create playlist
/playlists get. get all own playlists
/add-content-to-playlist put. add contents to playlist

/comments post. comment content
/my-comments get. get all own comments

/profile get. get own data
/profile-delete delete. delete account

/subscriptions post. subscribe to another user
/my-subscriptions get. get subscriptions
/my-subscribers get. get subscribers

/feed get. get all content from users who you following

/wallets post. create new wallet to donate
/my-wallet get. get wallet data
/make-transaction post. donate
/checks-to-send get. get all checks where you donate
/checks-to-receive get. get all check where you get donations

