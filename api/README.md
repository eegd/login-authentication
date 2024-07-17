# API
There are two router of this api, Create user and Login for access token.

## Create user

1. Use post method with a JSON payload containing the following fields:

```JSON
{"username": "str", "password": "str"}
```
 
 - "username": a string representing the desired username for the account, with a
minimum length of 3 characters and a maximum length of 32 characters.
 - "password": a string representing the desired password for the account, with a
minimum length of 8 characters and a maximum length of 32 characters,
containing at least 1 uppercase letter, 1 lowercase letter, and 1 number.

2. Returns a JSON payload containing the following field:

```JSON
{"success": "bool", "reason": "str | None"}
```

## Login for access token

1. Use post method with a JSON payload containing the following fields:

```JSON
{"username": "str", "password": "str"}
```

2. If the password verification fails five times, the user should wait one minute before attempting to verify the password again.

```JSON
{"success": "bool", "reason": "str | None"}
```

3. Returns a JSON payload containing the following field:

```JSON
{"token": "str", "type": "str"}
```
