# Rss Fedd

Rss feed reader powered by django and celery.

## Running

move to project directory and run the command bellow:

``` sh
docker-compose up --build --remove-orphans
```


### APIs
- Register and login:
 Both register and loginhave the same api
 ```
 /api/users/login/  (POST)
 input fields: 'username', 'password'
 output fields: 'user', 'token'
 ```

Other apis need authorization header. Use the token that you received from the api above in this format in header:
'Authorization: Token mygreatetoken'


- Basic info of user
  ```
  /api/users/me/  (GET)
  ```

- Register Channel:
  This api gets an object with a key named 'link' in request body
  ```
  /api/channels/register_channel/ (POST)
  ```

- List of channels:
  Result of this api is paginated. You can move to pages by setting limit and offset as querystring.
  You can also set subscribed=true in querystring to filter subscribed channels.

  ```
  /api/channels/ (GET)
  ```

- Subscribe
  ```
  /api/channels/{channel_id}/subscribe/
  ```

- Unsubscribe
  ```
  /api/channels/{channel_id}/unsubscribe/
  ```

- Request for updating channel entries
  ```
  /api/channels/{channel_id}/update_entries/
  ```

- Getting entries for specific channel
  ```
  /api/entries/?channel_id={channel_id}
  ```

- Filter unread entries of a channel
  ```
  /api/entries/?channel_id={channel_id}&read=false
  ```

- Filter marked entries of a channel
  ```
  /api/entries/?channel_id={channel_id}&marked=true
  ```

- Notify server that an entry has been read
  ```
  /api/entries/{entry_id}/read/  (POST)
  ```

- Unread an entry
  ```
  /api/entries/{entry_id}/unread/  (POST)
  ```

- Mark an entry
  ```
  /api/entries/{entry_id}/mark/  (POST)
  ```

- Unmark an entry
  ```
  /api/entries/{entry_id}/unmark/  (POST)
  ```

- Write comment on an entry
  send {"body": "my great comment"} to this api
  ```
  /api/entries/{entry_id/comments/ (POST)
  ```

- Get all of my comments on an entry
  send {"body": "my great comment"} to this api
  ```
  /api/entries/{entry_id/comments/ (GET)
  ```

- Delete my comment
  ```
  /api/entries/{entry_id/comments/{comment_id}/ (DELETE)
  ```
