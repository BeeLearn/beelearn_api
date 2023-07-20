# Getting started 

Setup project using docker 

```bash
docker-compose up
```
# Tests 
All models and signals must undergo test before commit changes, any untest commit won't be merged 

signals 

[+] Account Test
[+] Reward Test

api 
[+] Account Test
[+] Course Test
[+] Reward Test

# Catalogue app 
This contain the course business logics.

# account app
This contain user business logics.

## API documentation 

### Fetch all courses 
Fetch all course available on beelearn.

### Fetch all modules 
Fetch all modules available on beehive.
> Filters: `course: int`, `created_at: Date`

### Fetch all lessons 
Fetch all lessons available on beehive

### Fetch all topics 
Fetch all topics avaiable on beehive.
> Filters: `lesson: int`, `created_at: Date`

#### Filters

`topic: int`, `created_at: Date`

### Fetch all users 


## Reward app 
This contain the reward system, users are being given rewards 
xp: This is experience point given to user, used to get user to next level
bits: This is used to unlock topic questions 

### fetch all rewards

### fetch user acheivements

## User restriction 

If a user is caught manipulation course entitlement and viewership, this may lead to account restriction or potentially risk IP ban.
