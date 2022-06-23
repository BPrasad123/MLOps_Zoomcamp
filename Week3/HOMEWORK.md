# Objective #

We are taking the same Taxi Duration Prediction use case that we worked on in past. This time for the homework purpose we are using linear regression model and entire training pipeline is put into [homework.py](/Week3/homework.py) file. In this script we are neither tracking the experimental runs nor orchestrating any workflows.

We need to accomplish the following requirements so as to get familiar with Prefect flow engine.

* The training flow will be run every month.
* The flow will take in a parameter called date which will be a datetime.
  * a. date should default to None.
  * b. If date is None, set date as the current day. Use the data from 2 months back as the training data and the data from the previous month as validation data.
  * c. If date is passed, get 2 months before the date as the training data, and the previous month as validation data.
  * d. As a concrete example, if the date passed is "2021-03-15", the training data should be "fhv_tripdata_2021-01.parquet" and the validation file will be "fhv_trip_data_2021-02.parquet".
* Save the model as "model-{date}.bin" where date is in YYYY-MM-DD. Note that date here is the value of the flow parameter. In practice, this setup makes it very easy to get the latest model to run predictions because you just need to get the most recent one.
* In this example we use a DictVectorizer. That is needed to run future data through our model. Save that as "dv-{date}.b". Similar to above, if the date is 2021-03-15, the files output should be model-2021-03-15.bin and dv-2021-03-15.b.

# Set up #

## Setting up mlflow ##

I am using the same virtual environment that I used for experiment tracking in mlflow. Executing the following to start mlflow ui with sqlite backend. 

```mlflow ui --backend-store-uri sqlite:///mlflow.db```

## Setting up Prefect ##
Just like mlflow, we got to pip install perfect as well.  

Installed specific version of Prefect for windows in the virtual environment as per the given instruction.  
```pip install prefect==2.0b7```

![](https://github.com/BPrasad123/MLOps_Zoomcamp/blob/main/Week2/img/mlflowcli.png)

Prefect 2 comes with a component called Orion that is a server instance (UI) to monitor the workflows. Just like for mlflow UI, we can run the following command to start the orion server UI.

```prefect orion start```

![](https://github.com/BPrasad123/MLOps_Zoomcamp/blob/main/Week2/img/mlflowcli.png)

## Changes in pipeline ##

Please refer the solution code with comments.

[Homework solution](/homework_solution.py)