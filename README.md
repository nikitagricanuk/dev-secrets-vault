# Vault
[Link to the README in Russian](README_RUS.md)

The goal of this project is to develop an alternative solution for secure secret storage and management, functionally similar to HashiCorp Vault. Given the limited number of solutions in this space, our project offers a new approach to solving secret management challenges, not by copying existing systems, but by implementing key features with our own methods.

We have created a secure API for storing, accessing, and managing secrets. The main features include:

* Secret storage with encryption support
* Custom implementation of session tokens with TTL and user data retention
* Optimized session management system allowing flexible security policies: IP address binding, one-time tokens
* Integration with Redis for session management and security
* Flexible configuration storage: all settings are stored in JSON format, allowing edits through API requests or manually

We chose not to use ready-made solutions like JWT for sessions in favor of our own system, which allows fine control over token expiration and revocation. This makes the project adaptable to specific use cases, suitable for both small and large-scale projects.

The project is also focused on security and data protection, with HTTPS connection checks for all requests.

## Table of Contents
1. [Installation](#installation)
2. [Demo](#demo)
3. [API Documentation](#api-documentation)

## Installation

1. Ensure you have Docker and Docker Compose installed. If not, install Docker by following the official guides:  
   [Docker installation](https://docs.docker.com/get-docker/)  
   [Docker Compose installation](https://docs.docker.com/compose/install/)

2. Clone the project repository:
    ```bash
    git clone https://github.com/nikitagricanuk/dev-secrets-vault 
    ```

3. Navigate to the project directory:
    ```bash
    cd dev-secrets-vault
    ```

4. Create a .env file:
    ```bash
    cp .env.example .env
    ```

5. Generate a new password for the database using the pwgen utility:
    ```bash
    pwgen 12 -s
    ```

6. Insert the generated password into the .env file:
    ```bash
    1| # Database settings
    2| DB_NAME="vault"
    3| DB_HOST="postgres"
    4| DB_USERNAME="vault"
    5| DB_PASSWORD="<database password>" <-- insert the password here
    6| DB_PORT="5432"
    ```

7. Start the project:
    ```bash
    docker compose up -d
    ```

## Demo

<!-- Insert video demo link -->

# API-Documentation

## POST /v1/auth/token/create
**Description:**  Request to obtain an access token using password-based authentication.

**Method:**  POST

**URL:**  /api/v1/token/create 

**Request Parameters:** 
| Parameter      	| Type   	| Description	|
|---------------	|--------	|----------	|
| grant_type    	| string 	|      	Type of authorization	|
| username      	| string 	|      Username   	|
| passwor       	| string 	|     User's password     	|
| scope         	| string 	|     Access scope      	|
| client_id     	| string 	|  	Client identifier       	|
| client_secret 	| string 	|   Client secret    	|


**Response:**

* Response Code: 200
  ```json
  "string"
  ```
* Response Code: 422
  ```json
        {
        "detail": [
            {
            "loc": [
                "string",
                0
            ],
            "msg": "string",
            "type": "string"
            }
          ]
        }
**Server Responses:**
|  Response Code  	| Description	|   	|
|------------	|----------	|---	|
| 200        	|   Successful Access Token Retrieval      	|   	|
| 422        	|  There is a logical error      	|   	|

**Example Request:**

Request:

```shell

```
Response:
```json

```
___
## POST /v1/token/renew

**Description:**  access token update

**Method:**   POST

**URL:**  /api/v1/token/renew 

**Request Parameters:**  
| Parameter         	|Type    	| Description	|
|---------------	|--------	|----------	|
| refresh_token 	| string 	|     Refresh Token for Obtaining a New Access Token	|
**Response:**

* Response Code: 200
  ```json
  "string"
  ```

**Server Responses:**
|  Response Code  	| Description 	|   	|
|------------	|----------	|---	|
| 200        	|   Successful Access Token Update        	|   	|

**Example Request:**

Request:

```shell

```
Response:
```json

```
___
## POST /v1/token/revoke
**Description:**  request to revoke access token or refresh token

**Method:**   POST

**URL:**  /api/v1/token/revoke

**Request Parameters:** 
|Parameter       	| Type   	| Description	|
|---------------	|--------	|----------	|
| revoke_token 	| string 	|  Access Token or Refresh Token to Be Revoked

**Response:**

* Response Code: 200
  ```json
  "string"
  ```

**Server Responses:**
|  Response Code  	| Description 	|   	|
|------------	|----------	|---	|
| 200        	|  Successful Revocation of Access Token or Refresh Token	|   	|

**Example Request:**

Request:

```shell

```
Response:
```json

```
___
## POST /v1/users/create 

**Description:** request to create a new user in the system

**Method:**   POST

**URL:**  /api/v1/token/create 

**Request Parameters:**  
| Parameter        	| Type   	| Description 	|
|---------------	|--------	|----------	|
| username    	| string 	|    Username |
| email      	| string 	|     User Email   	|
| role       	| string 	|     User Role   	|
| password      	| string 	|     User Password    	|


**Response:**

* Response Code: 200
  ```json
  "string"
  ```
* Response Code: 422
  ```json
    {
         "detail": [
            {
             "loc": [
                "string",
                 0
             ],
            "msg": "string",
            "type": "string"
            }
       ]
    }
**Server Responses:**
|  Response Code а 	| Description 	|   	|
|------------	|----------	|---	|
| 200        	|  User Created Successfully       	|   	|
| 422        	|  There is a logical error       	|   	|

**Example Request:**

Request:
```shell

```
Response:
```json

```
___
## POST /v1/users/{username}/delete

**Description:**  user deletion 

**Method:**   POST

**URL:**  /api/v1/users/delete

**Request Parameters:** 
| Parameter        	| Type   	| Description 	|
|---------------	|--------	|----------	|
| username    	| string 	|    	Name of the User to be Deleted	|

***Response:**

* Response Code: 200
  ```json
  "string"
  ```
* Response Code: 422
  ```json
    {
         "detail": [
            {
             "loc": [
                "string",
                 0
             ],
            "msg": "string",
            "type": "string"
            }
       ]
    }
**Server Responses:**
|  Response Code 	| Description	|   	|
|------------	|----------	|---	|
| 200        	|  Successful User Deletion  	|   	|
| 422        	|  There is a logical error        	|   	|
**Example Request:**

Request:

```shell

```
Response:
```json

```
___
## POST /v1/secrets/create
**Description:** request to create a new secret in the system

**Method:**   POST

**URL:**  /api/v1/secrets/create

**Response:**

* Response Code: 200
  ```json
  "string"
  ```
* Response Code: 422
  ```json
    {
         "detail": [
            {
             "loc": [
                "string",
                 0
             ],
            "msg": "string",
            "type": "string"
            }
       ]
    }
**Server Responses:**
|  Response Code  	| Description	|   	|
|------------	|----------	|---	|
| 200        	|  Successful Creation of Secret    	|   	|
| 422        	|  There is a logical error        	|   	|
**Example Request:**

Request:

```shell

```
Response:
```json

```
___

## GET /v1/secrets/{secret_id}

**Description:** retrieval of information about a specific secret

**Method:**   GET

**URL:**  /api/v1/secrets

**Request Parameters:** 
| Parameter        	| Type   	| Description 	|
|---------------	|--------	|----------	|
| secret_id    	| string 	|    Secret Identifier    	|

**Response:**

* Response Code: 200
  ```json
  "string"
  ```
* Response Code: 422
  ```json
    {
         "detail": [
            {
             "loc": [
                "string",
                 0
             ],
            "msg": "string",
            "type": "string"
            }
       ]
    }
**Server Responses:**
|  Response Code 	| Description 	|   	|
|------------	|----------	|---	|
| 200        	|  Successful Retrieval of Secret Information  	|   	|
| 422        	|  There is a logical error       	|   	|

**Example Request:**

Request:

```shell

```
Response:
```json

```
___
## GET /v1/secrets
**Description:** retrieval of secrets list

**Method:**   GET

**URL:**  /api/v1/secrets

**Response:**

* Response Code: 200
  ```json
  "string"
  ```

**Server Responses:**
|  Response Code  	|Description 	|   	|
|------------	|----------	|---	|
| 200        	|   Successful Retrieval of Secrets List|  	|

**Example Request:**

Request:

```shell

```
Response:
```json

```
___
## GET /v1/sys/settings
**Description:** retrieves a list of all system settings

**Method:**   GET

**URL:**  /api/v1/sys/settings

**Response:**

* Response Code: 200
  ```json
  "string"
  ```

**Server Responses:**
|  Response Code 	| Description 	|   	|
|------------	|----------	|---	|
| 200        	|  Successful Retrieval of Secret Information  	|   	|


**Example Request:**

Request:

```shell

```
Response:
```json

```
___
## POST /v1/sys/setting
**Description:** request to create or update a specific system setting
**Method:**  POST

**URL:**   api/v1/sys/setting

**Example Request:** 

**Response:**

* Response Code: 200
  ```json
  "string"
  ```

**Server Responses:**
| Response Code 	| Description 	|   	|
|------------	|----------	|---	|
| 200        	|  Successful Creation or Update

**Example Request:**

Request:

```shell

```
Response:
```json

```
___
## GET /v1/sys/setting/{setting_key}
**Description:**  request to retrieve the value of a specific system setting identified by the provided setting_key

**Method:** GET

**URL:**  /api/v1/sys/setting/{setting_key}


**Response:**
* Response Code: 200
  ```json
  "string"
  ```
* Response Code: 422
  ```json
    {
         "detail": [
            {
             "loc": [
                "string",
                 0
             ],
            "msg": "string",
            "type": "string"
            }
       ]
    }
**Server Responses:**
|  Response Code 	| Description 	|   	|
|------------	|----------	|---	|
| 200        	|  Successful Retrieval of Specific System Setting 	|   	|
| 422        	|  There is a logical error       	|   	|
**Example Request:**

Request:

```shell

```
Response:
```json

```
___