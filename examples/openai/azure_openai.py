import mlflow
import openai
import os
import pandas as pd

"""
Set environment variables for Azure OpenAI service
export OPENAI_API_KEY="<AZURE OPENAI KEY>"
# OPENAI_API_BASE should be the endpoint of your Azure OpenAI resource
# e.g. https://<service-name>.openai.azure.com/
export OPENAI_API_BASE="<AZURE OPENAI BASE>"
# OPENAI_API_VERSION e.g. 2023-05-15
export OPENAI_API_VERSION="<AZURE OPENAI API VERSION>"
export OPENAI_API_TYPE="azure"
export DEPLOYMENT_ID="<AZURE OPENAI DEPLOYMENT ID OR NAME>"
"""

with mlflow.start_run():
    model_info = mlflow.openai.log_model(
        # Your Azure OpenAI model e.g. gpt-3.5-turbo
        model="<YOUR AZURE OPENAI MODEL>",
        task=openai.ChatCompletion,
        artifact_path="model",
        messages=[{"role": "user", "content": "Tell me a joke about {animal}."}],
        deployment_id=os.environ["DEPLOYMENT_ID"],
    )

# Load native OpenAI model
native_model = mlflow.openai.load_model(model_info.model_uri)
completion = openai.ChatCompletion.create(
    deployment_id=native_model["deployment_id"],
    messages=native_model["messages"],
)
print(completion["choices"][0]["message"]["content"])


# Load as Pyfunc model
model = mlflow.pyfunc.load_model(model_info.model_uri)
df = pd.DataFrame(
    {
        "animal": [
            "cats",
            "dogs",
        ]
    }
)
print(model.predict(df))

list_of_dicts = [
    {"animal": "cats"},
    {"animal": "dogs"},
]
print(model.predict(list_of_dicts))

list_of_strings = [
    "cats",
    "dogs",
]
print(model.predict(list_of_strings))

list_of_strings = [
    "Let me hear your thoughts on AI",
    "Let me hear your thoughts on ML",
]
model = mlflow.pyfunc.load_model(model_info.model_uri)
print(model.predict(list_of_strings))
