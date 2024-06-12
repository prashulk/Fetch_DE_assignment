# Fetch_DE_assignment

## How to run -

1. Clone the git repo - ```git clone https://github.com/prashulk/Fetch_DE_assignment.git```
   
2. Run the docker build command - ```docker-compose build```

3. ```docker-compose up -d```
4. ```docker ps```
   

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



#### Logs screenshot -

- While load is happening -

<img width="1468" alt="image" src="https://github.com/prashulk/Fetch_DE_assignment/assets/67316162/bbdb17d9-04e8-498e-9f61-741391b3f949">


 - Error record shown in the log -

   <img width="1468" alt="image" src="https://github.com/prashulk/Fetch_DE_assignment/assets/67316162/1830dec8-962b-40c6-b84d-ba1c155beb1c">


- One the load is complete -

  <img width="1468" alt="image" src="https://github.com/prashulk/Fetch_DE_assignment/assets/67316162/450f62fa-624e-4bc0-9766-09ffc55a6f11">





## Questions -

**1.) How would you deploy this application in production?**


I would start by using AWS SQS for message queuing to ensure reliable data ingestion from various sources. AWS Lambda would trigger processing upon the arrival of new messages in SQS. To handle real-time data streaming, I would leverage Amazon Kinesis or Apache Kafka, ensuring seamless data flow. For data transformation and processing, I would use Apache Spark on AWS EMR, enabling scalable and efficient data processing.

Next, I would utilize Amazon S3 as a data lake to store both raw and processed data, providing a scalable storage solution. For data warehousing and analytics, Amazon Redshift would be the choice, allowing for efficient querying and analysis. To manage relational data needs, I would deploy Amazon RDS, ensuring ACID compliance and reliable SQL operations.

Security and compliance are paramount, so I would use AWS IAM to manage access control, ensuring least privilege access and regular audits.


**2.) What other components would you want to add to make this production ready?**


 - I would implement robust error handling and retry mechanisms throughout the pipeline to ensure resilience against transient failures and data processing issues.

 - For automated deployment and scaling, I would set up a CI/CD pipeline using tools like Jenkins or AWS CodePipeline, enabling automated testing, deployment, and scaling of the application.

 - I would also integrate AWS Glue for cataloging and managing metadata, making it easier to query and analyze data stored in the data lake. To ensure high availability and disaster recovery, I would configure cross-region replication for S3 and Redshift, along with regular backups.

 - I would write comprehensive unit tests for individual components and functions using frameworks like pytest. In these tests, I would use mocking to simulate interactions with external services such as AWS SQS and the Postgres database, ensuring tests are isolated and repeatable. For integration testing, I would set up automated tests that validate the end-to-end data flow and processing, ensuring that all components interact correctly and data is processed as expected.

