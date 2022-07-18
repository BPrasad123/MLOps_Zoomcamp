# What we have learnt so far #
1. **Experiment tracking**: We run a number of experiments with an objective. We saw how we can use *MLflow Experiment* to track all of runs in an experiment.
2. **Model tracking**: There are a number of models from all the experimental runs. However, not all of them are selected as production candidates. We saw how we can select good candidates and manage their life cycle in *MLflow Model Registry*.
3. **Pipeline**: We also saw, how we took the code from notebook and created pipeline so as to make the code modular, reproducible, manage dependencies and orchestrate each of the processes with help of *Prefect* workflow engine.

![](/Week4/img/beforedeploy.png)

# What is next? #
Now that the model is registered in *MLflow Model Registry* and production ready, we need to deploy that so that we can get the prediction result for the given data to realize its value.

# Model Deployment #
The kind of deployment depends upon how we want the prediction result. Say, if we can wait for an hour or a day for the prediction result then we do the offline batch deployment of the model that runs periodically. On the other hand, if we need to the prediction in real time then it has to be online deployment where the model is always up and running on a compute to serve. Again, when it comes to online deployment, based off the use case, we can deploy the model as a web service or a streaming service.

Webservice: We wrap the model in a web service where the model can be loaded and served to predict in a REST API call. For entire set of data received in an API call, the output from the model is sent in the response in one:one fashion.

Streaming: Runs in producer and consumer model where the producer pushes information to event stream and the consumers listen to the stream to get updates. For example, the predicted taxi duration result is published in the event stream and consumers such as subsequent models listen to the event stream to fetch the predicted data to further do further processing.

![](/Week4/img/predwebservice_v1.png)

## Deploying model as a web-service ##

**Steps**
* Save the trained model
* Create a virtual environment
* Create a script for prediction
* Put the script into a Flask app
* Package the app to Docker


### Save the trained model ###
Here we are taking the same model, saved as a binary file, that was trained in previous model and put that in newly created web-service directory for this week. 

One can run a fresh model so as to train and save the model as well.

### Create a virtual environment ###
We need to have exact same version of Scikit-learn library that was used to create the model as well as same Python version in order to avoid any compatibility issue.

Go to the virtual environment in EC2 server where the model was trained and try the following command.

```pip freeze | grep scikit-learn```  
```python --version```

With `pipenv` create a new virtual environment.  
```pipenv install scikit-learn==1.0.2 flask --python=3.9```

Activate the environment.  
```pipenv shell```

If the prompt is too long on the screen we can set it to something short like '> '.  
```PS1="> "```

### Create script for prediction ###

**Step 1**  

First we create a script that loads the saved model, preprocesses the input data and generates prediction.

[Predict script without flask](/Week4/web-service/predict_without_flask.py)  

[Test script to test predict script](/Week4/web-service/test_without_flask.py)

Note: Rename the files from predict_without_flask.py to predict.py and test_without_flask.py to test.py if you are interested to test the script without flask.

The idea is to create a working script that can take input in original format and generate the prediction result.

**Step 2**

Now that we have the working predict.py script ready, we can build a web-service around it so that we can expose it to an HTTP endpoint.

[Predict script with flask](/Week4/web_service/predict.py)

[Test script to test flask app](/Week4/web-service/test.py)

Note: Current flask set up is for the development environment. Install gunicorn and configure in order to solve the following production environment type warning.  

```pipenv install gunicorn```  
```gunicorn --bind=0.0.0.0:9696 predict:app```

```
* Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
```

Note: We tried to run the test.py script from base virtual environment. We have requests library installed there. And, ideally in development environment we should have requests library installed as we need to do the testing, however in the production environment we do not need to install it.

If it is needed then we can still install it in production environment, however, with dev dependencies as follows. This we can use it but during the deployment it will not be there.

```pipenv install --dev requests```

### Package the app to Docker ###
1. Create [Dockerfile](/Week4/web-service/Dockerfile) with necessary content.
2. Run the following command to build docker image
   ```bash
   docker build -t ride-duration-prediction-service:v1 .
   ```
3. Run the following command to run the image
   ```bash
   docker run -it --rm -p 9696:9696 ride-duration-prediction-service:v1
   ```

This will deploy the webserive on localhost and we can run the test.py script again to test.

So far we have packaged the model in a docker file that can run in every docker compatible compute to serve. However the model we used was directly loaded from the local path where it was stored and we had learnt in previous sessions that the candidate models were stored in model registry that we were supposed to use. Hence, in the next section we will learn how to fetch the model from model registry to serve.

## Get the models from MLflow Model Registry ##
This time we are going to run a fresh experiment to train a new model (Random Forest) on the same dataset and register the model in MLflow Model Registry.

Then we will explore various ways to fetch the registered model for the webservice.

### Train the model ###
1. We are using locally hosted sqlite database for tracking server and s3 bucket for artifact storage. For that as a prerequisite create an S3 bucket and EC2 instance being used has access to the S3 bucket. To confirm try the following command and see you are able to get the list of buckets.

   ```bash
   aws s3 ls
   ```
2. Run the following to start the mlflow tracking server
   
   ```bash
   mlflow server --backend-store-uri=sqlite:///mlflow.db --default-artifact-root=s3://bhagabat-mlflow-rf-greentaxi/
   ```
   where bhagabat-mlflow-rf-greentaxi is the name of the S3 bucket.

   Open mlflow UI on http://127.0.0.1:5000/

3. Create a jupyter notebook to train a model
   
   Here the notebook where we trained a random forest regressor model, and tracked and saved the model in mlflow.

   [Jupyter Notbook](/Week4/web-service-mlflow/taxi-duration-rf-training.ipynb) for training and saving Random Forest Regressor.

   You can check the experiment details and logged model artifact in mlflow UI

   ![](/Week4/img/mlflowexp.png)

   ![](/Week4/img/mlflowexpdetails.png)

   Note: There are multiple ways to use the logged model. If we are using `runs/RUN_ID/model` then we run with risk of availability lest the tracking server should go down. However, if fetch the artifact directly from S3 then we are not dependent on the artifact server. Please check the predict.py script to see the changes made.

### Inference script to fetch model ###
1. We can take the note of the RUN ID from the experiment tracker and use that in the predict script so as to deploy the webservice.
   
   Here is the link for [predict.py](/Week4/web-service-mlflow/predict.py) script.

   Remember to install the missing packages, if any, in the virtual environment.

2. In another terminal run test.py to see if we are getting the predicted result.
   
   ![](/Week4/img/pred.png)


**References**

[4.3 Web-services: Getting the models from the model registry (MLflow)](https://www.youtube.com/watch?v=aewOpHSCkqI&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK)

[MLflow on AWS](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/02-experiment-tracking/mlflow_on_aws.md)

[MLflow backend and artifact store](https://github.com/dmatrix/misc-code/tree/master/py/mlflow/server)


## Deploy model as Streaming service ##

  
Reference:  
[Video by DataTalksClub](https://www.youtube.com/watch?v=TCqr9HNcrsI&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK)

[Pending] Will share the notes upon completion.

## Batch deployment of model ##

Typical approach for deploying a model in batch model:
* Create a notebook/training script to train a model and save it
* Create a notebook to load the trained model and make prediction on the new data
* Convert the notebook to an inference script
* Clean and parameterize the script
* Schedule the inference script if required

We will use the same taxi duration prediction example here.

**Step 1: Train the model and save the artifacts**
* If the model is not trained yet we got train first. Since as per the homework we need to train the model on FHV datasets, I am training the model from scratch here.
  
  Connect to EC2 server and create a new virtual environment
  ```bash
  mkdir batch-train
  cd batch-train
  pipenv shell --python=3.9
  pipenv install scikit-learn==1.0.2 flask gunicorn mlflow boto3
  ```
* Train random forest regressor model for the fhv taxi dataset  
  [Jupyter notebook for training model](/Week4/batch-train/fhv-taxi-duration-training.ipynb)  

   Take a note of the full path from artifact section in mlflow ui

**Step 2: Notebook for fetching the model and predicting**
* Connect to EC2 server and create a new virtual environment
  ```bash
  mkdir batch-inference
  cd batch-inference
  pipenv shell --python=3.9
  pipenv install scikit-learn==1.0.2 prefect mlflow pandas boto3 pyarrow s3fs
  ```
* Copy the training notebook and change it for prediction, say, score.ipynb. 
  
  [score notebook](/Week4/batch-inference/score.ipynb)

  Once the notebook code successfully runs convert that to python script.
  ``` cp
   jupyter nbconvert --to script score.ipynb
  ```

* Clean and parameterize the prediction script score.py  
  [Clean code in score.py](/Week4/batch-inference/score.py)

![](/Week4/img/scorerun.png)

**Step 3: Dockerise the script [Homework]**  
[Pending] This is yet to be completed.