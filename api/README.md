# API
There are two part of this api, Create account and Verify account and password.

## Create account

1. Use post method with a JSON payload containing the following fields:

```JSON
{"username": str, "password": str}
```
 
 - "username": a string representing the desired username for the account, with a
minimum length of 3 characters and a maximum length of 32 characters.
 - "password": a string representing the desired password for the account, with a
minimum length of 8 characters and a maximum length of 32 characters,
containing at least 1 uppercase letter, 1 lowercase letter, and 1 number.

 - Sample
    - e.g. {"username": "Alex", "password": "Az1"}
    - e.g. {"username": "John", "password": "Za2"}


2. Returns a JSON payload containing the following field:

```JSON
{"success": bool, "reason": str | None}
```

## Verify account and password

1. Use post method with a JSON payload containing the following fields:

```JSON
{"username": str, "password": str}
```

 - Sample
    - e.g. {"username": "Alex", "password": "Az1"}
    - e.g. {"username": "John", "password": "Za2"}

2.Returns a JSON payload containing the following field:

```JSON
{"success": bool, "reason": str | None}
```
