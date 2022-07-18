# Disclaimer #
I do not claim the ownership of the code. The credit goes to DataTalksClub for such a wonderful learning experience. The code was given by the DataTalksClub that I ran to learn and reproduce the result. I have added notes here in this README file as I executed the corresponding steps as instructed in the session. Happy Learning!

# ML Model deployed, what next? #
We have learnt how to run and track ML experiments, and deploy the chosen models into production. The prediction services are now up and running, and generating predictions for given data. 

![](/Week5/imgs/predwebservice_v2.png)

So are we done now?

No, not yet. With time the business concept changes and so is the data. We need to be cognizant about the model performance from time to time so as to take timely appropriate action.

# Monitoring #

There are many facets when to monitor when it comes to machine learning.
* Service Health
  * Monitoring service running status in production
* Model Health
  * Monitoring metrices
  * Feedback
  * Performance by segments
  * Bias and fairness
  * Explainability
* Data Health
    * Data quality and integrity
    * Data and concept drift
    * Outliers 

## Types of monitoring ##
Depending upon the requirements we can go for **online monitoring** where we continuously read input and output data so as to find inconsistencies or we read the stored input and output data periodically to monitor the status that is **batch monitoring**.

Batch monitoring is implemented in most of the production scenarios. Pipelines are orchestrated with tools like Prefect or Airflow, where after some steps in the pipelines, monitoring related calculations done to generate matrices to determine if data and model are behaving as per the expectation.

From the stored data, metrices can be calculated and stored in a SQL or NOSQL database and visualizations can be prepared with help of Tableau or Power BI. However, Evidently can help in creating required metrices out of the box and produce the visualizations automatically as well. In case of online/real time monitoring Evidently generated metrices can be stored in Prometheus database that very well integrates with Grafana for visualization.


## Architecture ##

![](/Week5/imgs/complete_architecture_v4.png)

**How it works:**

Online Monitoring:  
* The prediction service exposes an endpoint with input and output data in JSON format.  
* The monitoring service, Evidently, pulls the input and output data from the exposed endpoint.
* Evidently monitoring service calculates and exposes metrices that are scrapes by Prometheus for storage.
* Next, predefined visualizations are created in Grafana for the metrices data available in Prometheus.

Batch Monitoring:  
* The prediction service sends copy of input and prediction output data in JSON format to the Mongo DB.
* Prefect pipeline reads the data from Mongo DB, uses Evidently package to calculate metrices and optionally stores metrices data back in Mongo DB.
* Optionally Prefect workflow uses Evidently package again to produce nice visualizations in an HTML file.

In the architecture there are so many components involved that need to talk to each other for it to work. We will be using Docker Compose with necessary configurations for the same.

## Code Walkthrough ##
All of the monitoring related sessions were delivered by Emeli Dral, CTO of Evidently AI. We will use the same code to explain how online and batch monitoring works.

### Online Monitoring ##

Repo folder and file structure:

![](/Week5/imgs/folderstructure.png)

**Step 1: Environment setup**
* Create a virtual environment
  ``` bash
    pipenv shell --python=3.9
  ```
* Install required libraries as mentioned in requirements.txt
  ``` bash
    pipenv install -r requirements.txt
  ```

**Step 2**  
Create a directory `prediction_service` with following files.  
* `app.py` - The python service to deploy the model as a webservice. It additionally saves a copy of input and output to mongo DB and makes a POST call to Evidently service to send the copy of input and output data in JSON format.
* lin-reg.bin - Trained model file
* requiremens.txt - List of required libraries for the web-service to run
* Dockerfile - Docker file to deploy the service in a container

**Step 3**  
Directory `evidently_service` contains required files for configuration, dashboard specifications, dataset scheme like mapping, web-service app script and a Docker file to monitor in real time. 

**Step 4**  
`python prepare.py`
  
This script downloads green taxi data for the month of January for the years 2021 and 2022.  

Issue Faced:  
`The response object does not have key "content-length"`
It was because the download link for the files were changed. Accordingly updated the link in the script and it worked fine.

**Step 5**  
Next we run the following docker compose command to run all the containers for all the components in docker-compose file.

``` bash
docker-compose up
```

Issue faced:  
If you run `docker compose up` and get error like `docker compose command not found` then try with hyphen `docker-compose` as above.  

Now please check the logs, all the following services should be running. 
* prediction web-service: Prediction service from **Step 2**
* prometheus db: Time series database to store metrices
* mongo db: Document DB to store JSON like documents
* evidently monitoring service: Monitoring service
* grafana: Visualization tool for metrices

**Step 6**  
Do the port forwarding on localhost in VS Code for ports 3000 and 27018

**Step 7**
To access Grafana open localhost:3000 on browser and use `admin` as both user and password.

Run `send_data.py` to send records for prediction with waiting time of 1 second.

**Step 8**  
As a number of records are being processed, we now should see some dashboards in Grafana. Like this.  

![](/Week5/imgs/grafana_dashboard.png)


And, of course the data should be available in the mongo database. For that follow the [jupyter notebook](/Week5/pymongo_example.ipynb) where we connect to the mongo db and fetch the stored data to verify.

![](/Week5/imgs/mymongo_example.png)

### Batch Monitoring ###

Run `prefect_example.py` that loads reads the entire dataset, loads the model to generate prediction, save the data in mongo DB and runs Evidently Profiling to find drifts and performance changes. Evidently profiling report is saved as an html file.

It does take time to finish, so please track the running progress in prefect logs.  

We can verify the data stored in mongo DB in similar way as in online monitoring.  

![](/Week5/imgs/mongodbbatch.png)

Open the newly created Evidently HTML file to find the report along with visualizations.  

![](/Week5/imgs/evidentlyreport.png)

That's it! Now we learnt how we could monitor the deployed ML services in both online and batch modes.

Thanks once again to Emeli Dral and DataTalksClub team!!