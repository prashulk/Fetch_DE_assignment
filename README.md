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



### Error handling and data format changes -


On observing the data format, while reading I observed that the ```app_version``` needs to be converted to ```VARCHAR``` due to it's data format. The same has been done.

Also, Python's Logging module has been used to track the issues and see if the load has happened successfully or not. There is 1 issue with one of the records, as a result it has not been loaded in the table but visible in the logs (screenshot attached below) -

The record is: ```Error: 'ip'. Message: {'MessageId': '9bd6d21c-199a-475d-89cd-f5c19cb0a5e7', 'ReceiptHandle': 'NDMxNDRjN2EtMTVkMC00M2EzLTljMjEtM2Y3NWQ2NzFkNDQwIGFybjphd3M6c3FzOnVzLWVhc3QtMTowMDAwMDAwMDAwMDA6bG9naW4tcXVldWUgOWJkNmQyMWMtMTk5YS00NzVkLTg5Y2QtZjVjMTljYjBhNWU3IDE3MTgyMDY5NDIuNzg1Mjk4', 'MD5OfBody': '32365e026658d33521484837856cc808', 'Body': '{"foo": "oops_wrong_msg_type", "bar": "123"}'}```

