# fraud-detection-business-value

Calculate business value of fraud detection.

Data quality directly determines how a ML model performs. Knowing model performance, average fraud and average revenue per customer, we estimate the business value of a fraud detector.


## Getting started

Prerequisites:

* python3.9
* poetry, pre-commit, black, flake8, mypy

```bash
# create venv with poetry
poetry env use /full/path/to/python
poetry install --with dev
# init pre-commit
pre-commit install
pre-commit autoupdate

# run streamlit
streamlit run app.py
```

## AWS fraud detector

We follow the [official documentation](https://docs.aws.amazon.com/frauddetector/latest/ug/step-1-get-s3-data.html) to train a model and get its performance.

Data to train the fraud detector taken from [aws-fraud-detector-sample](https://github.com/aws-samples/aws-fraud-detector-samples).

### AWS setup

- Region: eu-west-1
- S3 bucket: fraud-detector-samples
  - upload datasets from ./data to s3 bucket
-
