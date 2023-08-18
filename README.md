# arin-openai
Library to house array insights openai wrappers.


## environment varriales
to use
'''
engine_name =
client = ClientOpenai.from_default_azure(engine_name, do_cache=True)
'''
set the following environment varriables
'''
export OPENAI_ENGINE_NAME="gpt-35-turbo"
export OPENAI_API_KEY=""
export PATH_DIR_PROMPT_CACHE=""
export AZURE_DATASET_CONNECTIONSTRING="secret"
export AZURE_MODEL_CONTAINER_NAME="sail-model-zip"
'''

other engine names
"gpt-35-turbo", "gpt-35-turbo-16k", "gpt-4", "gpt-4-32k"