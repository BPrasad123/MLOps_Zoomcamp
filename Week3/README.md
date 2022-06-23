# What have learnt so far #
## Tracking ##
* (1) Experiment Tracking  
  
  For each experiment we try a number of runs or executions and while doing so it is imperative that we track all of the important information about all the trials so as to analyse and find the best suitable model. Tracking module of MLflow comes with a lot of rich features to do the seamlessly.

* (2) Model Tracking
  
  Once the best model candidates are decided to productionise out all the runs of an experiment, the next step is to manage those in such way that we can seamlessly annotate, load them as per downstream requirements, move between the environments, maintain versions etc. To accomplish that we can use Model Registry from MLflow.

## Coding ##
* (3) Notebook
  
  We have seen in the previous modules that we can run the code in jupyter notebooks and track the experimental runs using mlflow methods. All the collected related information was accessible on the UI as well as through the Client API to analyse.

* (4) Python Scripts
  
  We also saw that same mlflow methods can be used inside the python training script so as to track the experimental runs centrally through mlflow UI or API.

## Observation ##

In the training scripts, there can be a number of processes involved. That can accommodate steps such as data retrieval, data pre-processing, model training, hyper-parameter searching, logging etc. We might want to run some of the functions/processes in parallel, or in sequence, schedule and automate, retry failed processes, manage internal dependencies, run pipeline to retrain etc. Basically we need to orchestrate each process of the pipeline.

As a matter of fact during the development process a lot of time is spent in following issues that term as **Negative Engineering**.
* Retries and API go down
* Malformed data
* Notifications
* Observability into failure
* Conditional failure logic
* Timeouts

Tools like **Prefect** comes to the rescue that helps in reducing such Negative Engineering.

# Introduction to Prefect #

It is an Open-Source workflow engine, a dataflow orchestration platform. Some of core concepts:
* Tasks - They are functions having special runs when they should run; optionally take inputs, perform some work and optionally return an output.
* Workflows - They are basically containers of tasks defining dependencies among them.
* Modularity - Every component of Prefect is a modular design, making it easy to customize, to logging, to storage, to handle state.
* Concurrency - Supports massive concurrency
* Automation - Has a solid framework to support workflows

More details:  
https://docs.prefect.io/

