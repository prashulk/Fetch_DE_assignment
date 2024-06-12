# Fetch_DE_assignment

## How to run -

1. Clone the git repo - ```git clone https://github.com/prashulk/Fetch_DE_assignment.git```
   
2. Run the docker build command - ```docker-compose build```

3. ```docker-compose up -d```
   

Docker container started -
![image](https://github.com/prashulk/Fetch_DE_assignment/assets/67316162/ad52df08-7c7c-4016-bc87-8f0ad98aabc9)


## Testing the results and the logs -

 - First of all verify if the containers are running through docker desktop - 

<img width="1353" alt="image" src="https://github.com/prashulk/Fetch_DE_assignment/assets/67316162/e726e7c7-119a-4e5e-8021-43bf88158019">


- Now in the terminal run the below command to enter postgres and the password is **postgres** and see the results -

```psql -d postgres -U postgres -p 5432 -h localhost -W```

<img width="1353" alt="image" src="https://github.com/prashulk/Fetch_DE_assignment/assets/67316162/156697e1-9478-4459-bd0b-8fefb3761896">


<img width="1703" alt="image" src="https://github.com/prashulk/Fetch_DE_assignment/assets/67316162/cf3d0089-ac3e-4f82-803a-61662eaa49ec">


- Run the following queries, and see the above results -

```select count(*) from user_logins;```

```select * from user_logins limit 5;```
