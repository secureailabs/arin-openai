import os
from typing import List, Optional

import openai
from arin_core_azure.cognitive_services_helper import CognitiveServicesHelper
from arin_core_azure.env_tools import get_dir_from_env, get_string_from_env
from arin_core_azure.file_store_azure import FileStoreAzure
from arin_core_azure.jsondict_store import JsondictStore
from openai.openai_object import OpenAIObject


class ClientOpenai:
    def __init__(
        self,
        api_base: str,
        api_key: str,
        api_type: str,
        api_version: Optional[str] = None,
        engine_name: Optional[str] = None,
        jsondict_store: Optional[JsondictStore] = None,
    ) -> None:
        self.api_base = api_base
        self.api_key = api_key
        self.api_type = api_type
        self.api_version = api_version
        self.engine_name = engine_name
        self.jsondict_store = jsondict_store

    def chat_completion(self, call_dict: dict, ignore_cache: Optional[bool] = False) -> dict:

        if (self.jsondict_store is not None) and (ignore_cache == False):
            if self.jsondict_store.has_key_for_dict(call_dict):
                return self.jsondict_store.load_json_for_dict(call_dict)
        call_dict_api_key = call_dict.copy()  # ensure the api key does not end up in the cache
        call_dict_api_key["api_key"] = self.api_key
        response_dict: OpenAIObject = openai.ChatCompletion.create(**call_dict_api_key)  # type: ignore

        if self.jsondict_store is not None:
            self.jsondict_store.save_json_for_dict(call_dict, response_dict)
        return response_dict

    def chat_completion_messages(
        self,
        messages: List[dict],
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        ignore_cache: Optional[bool] = False,
    ) -> dict:
        """
        Build a promt dict and send it to the underlying base class
        The baseclass then checks the cache and sends the promt to the api if not found in cache

        :param text: promt text
        :type text: str
        :param max_tokens: number of tokens to promt, defaults to 800
        :type max_tokens: int, optional
        :return: result of promt
        :rtype: dict
        """
        call_dict = {}
        call_dict["api_type"] = self.api_type
        call_dict["api_version"] = self.api_version
        call_dict["api_base"] = self.api_base
        call_dict["engine"] = self.engine_name
        call_dict["messages"] = messages
        if temperature is not None:
            call_dict["temperature"] = temperature
        if max_tokens is not None:
            call_dict["max_tokens"] = max_tokens
        return self.chat_completion(call_dict, ignore_cache)

        # TODO
        #         engine = promt_dict["engine"]
        # messages = promt_dict["messages"]
        # temperature = promt_dict["temperature"]
        # max_tokens = promt_dict["max_tokens"]
        # top_p = promt_dict["top_p"]
        # frequency_penalty = promt_dict["frequency_penalty"]
        # presence_penalty = promt_dict["presence_penalty"]
        # stop = promt_dict["stop"]

    @staticmethod
    def from_env(do_cache: bool = True):

        api_base = get_string_from_env("OPENAI_API_BASE")
        api_key = get_string_from_env("OPENAI_API_KEY")
        api_type = get_string_from_env("OPENAI_API_TYPE")
        api_version = get_string_from_env("OPENAI_API_VERSION")
        engine_name = get_string_from_env("OPENAI_ENGINE_NAME")
        if do_cache:
            connection_string = get_string_from_env("AZURE_STORAGE_CONNECTION_STRING")
            path_dir_prompt_cache: str = get_dir_from_env("PATH_DIR_PROMPT_CACHE", create_if_missing=True)
            container_name = get_string_from_env("AZURE_STORAGE_CONNECTION_STRING")
            jsondict_store = JsondictStore(
                file_store=FileStoreAzure(path_dir_prompt_cache, connection_string, container_name)
            )
        else:
            jsondict_store = None
        return ClientOpenai(
            api_base=api_base,
            api_key=api_key,
            api_type=api_type,
            api_version=api_version,
            engine_name=engine_name,
            jsondict_store=jsondict_store,
        )

    @staticmethod
    def from_default_openai(do_cache: bool = True):
        api_base = "https://api.openai.com/v1"
        api_key = os.environ["OPENAI_API_KEY"]
        api_type = "open_ai"
        api_version = None
        engine_name = "gpt-3.5-turbo-16k"  # TODO not sude if this works
        if do_cache:
            connection_string = get_string_from_env("AZURE_STORAGE_CONNECTION_STRING")
            path_dir_prompt_cache: str = get_dir_from_env("PATH_DIR_PROMPT_CACHE", create_if_missing=True)
            container_name = get_string_from_env("AZURE_STORAGE_CONNECTION_STRING")
            jsondict_store = JsondictStore(
                file_store=FileStoreAzure(path_dir_prompt_cache, connection_string, container_name)
            )
        else:
            jsondict_store = None
        return ClientOpenai(
            api_base=api_base,
            api_key=api_key,
            api_type=api_type,
            api_version=api_version,
            engine_name=engine_name,
            jsondict_store=jsondict_store,
        )

    @staticmethod
    def from_default_azure(engine_name: str = "gpt-35-turbo", do_cache: bool = True):
        list_engine_name = ["gpt-35-turbo", "gpt-35-turbo-16k", "gpt-4", "gpt-4-32k"]
        if engine_name not in list_engine_name:
            raise ValueError(f"engine_name must be on of {list_engine_name}")

        api_base = "https://arin-openai-canada-east.openai.azure.com/"
        api_key = os.environ["OPENAI_API_KEY"]
        api_type = "azure"
        api_version = "2023-03-15-preview"
        if do_cache:
            path_dir_prompt_cache: str = get_dir_from_env("PATH_DIR_PROMPT_CACHE", create_if_missing=True)
            connection_string = get_string_from_env("AZURE_DATASET_CONNECTIONSTRING")
            container_name = get_string_from_env("AZURE_PROMPT_CONTAINER_NAME")
            jsondict_store = JsondictStore(
                file_store=FileStoreAzure(path_dir_prompt_cache, connection_string, container_name)
            )
        else:
            jsondict_store = None
        return ClientOpenai(
            api_base=api_base,
            api_key=api_key,
            api_type=api_type,
            api_version=api_version,
            engine_name=engine_name,
            jsondict_store=jsondict_store,
        )

    @staticmethod
    def from_account_id_azure(account_id: str, engine_name: str = "gpt-35-turbo", do_cache: bool = True):

        helper = CognitiveServicesHelper()
        account = helper.get_account_for_account_id(account_id)
        list_engine_name = helper.get_account_list_engine_name(account)
        if engine_name not in list_engine_name:
            raise ValueError(f"engine_name must be on of {list_engine_name}")

        api_base = helper.get_account_endpoint(account)
        api_key = helper.get_account_api_key(account)
        api_type = "azure"
        api_version = "2023-03-15-preview"
        if do_cache:
            connection_string = get_string_from_env("AZURE_STORAGE_CONNECTION_STRING")
            path_dir_prompt_cache: str = get_dir_from_env("PATH_DIR_PROMPT_CACHE", create_if_missing=True)
            container_name = get_string_from_env("AZURE_STORAGE_CONNECTION_STRING")
            jsondict_store = JsondictStore(
                file_store=FileStoreAzure(path_dir_prompt_cache, connection_string, container_name)
            )
        else:
            jsondict_store = None
        return ClientOpenai(
            api_base=api_base,
            api_key=api_key,
            api_type=api_type,
            api_version=api_version,
            engine_name=engine_name,
            jsondict_store=jsondict_store,
        )
