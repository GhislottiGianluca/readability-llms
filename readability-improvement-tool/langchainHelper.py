import os
import langchain_openai
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_models import BedrockChat
from langchain_google_genai import ChatGoogleGenerativeAI
import Parser as p

def improve_testsuite_readability(temperature, testsuite, class_information, sourcecode, case):
    """
    Improves the readability of a test suite by modifying the identifiers, test names, and variable names.

    Args:
        temperature (int): The temperature setting for the LLM to control the creativity of the output.
        testsuite (list): A list of test methods to be improved.
        class_information (str): Information about the class being tested.
        sourcecode (str): Source code of the class under test.
        case (int): The identifier for selecting the LLM model to use.

    Returns:
        list: A list of modified test methods with improved readability.
    """
    # Load API keys from environment variables
    load_dotenv()
    api_key = os.environ['OPENAI_API_KEY']

    # Define the LLM based on the "case" input selected by the user
    if case == 1:
        llm = langchain_openai.ChatOpenAI(openai_api_key=api_key,
                                          temperature=temperature,
                                          model_name="gpt-4")

    elif case == 2:
        llm = langchain_openai.ChatOpenAI(openai_api_key=api_key,
                                          temperature=temperature)

    elif case == 3:
        api_key = os.environ['GOOGLE_API_KEY']
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-001",
                                     google_api_key=api_key,
                                     temperature=temperature)

    elif case == 4:
        llm = BedrockChat(credentials_profile_name="conversational",
                          model_id="meta.llama3-8b-instruct-v1:0",
                          region_name="us-east-1",
                          model_kwargs={
                              "temperature": temperature
                          })

    elif case == 5:
        llm = BedrockChat(credentials_profile_name="conversational",
                          model_id="meta.llama3-70b-instruct-v1:0",
                          region_name="us-east-1",
                          model_kwargs={
                              "temperature": temperature
                          })

    elif case == 6:
        llm = BedrockChat(credentials_profile_name="conversational",
                          model_id="anthropic.claude-3-haiku-20240307-v1:0",
                          region_name="us-east-1")

    elif case == 7:
        llm = BedrockChat(credentials_profile_name="conversational",
                          model_id="anthropic.claude-3-sonnet-20240229-v1:0",
                          region_name="us-east-1")

    elif case == 8:
        llm = BedrockChat(credentials_profile_name="conversational",
                          model_id="mistral.mistral-7b-instruct-v0:2",
                          region_name="us-east-1",
                          model_kwargs={
                              "temperature": temperature
                          })

    elif case == 9:
        llm = BedrockChat(credentials_profile_name="conversational",
                          model_id="mistral.mixtral-8x7b-instruct-v0:1",
                          region_name="us-east-1",
                          model_kwargs={
                              "temperature": temperature
                          })

    elif case == 10:
        llm = BedrockChat(credentials_profile_name="conversational",
                          model_id="amazon.titan-text-express-v1",
                          region_name="us-east-1",
                          model_kwargs={
                              "temperature": temperature
                          })

    else:
        llm = BedrockChat(credentials_profile_name="conversational",
                          model_id="mistral.mistral-large-2402-v1:0",
                          region_name="us-east-1",
                          model_kwargs={
                              "temperature": temperature
                          })
        print("-------------MISTRAL LARGE USED-------------")

    # List to hold modified test suite methods
    modified_ts_array = []

    # Define conversation memory
    memory = ConversationBufferWindowMemory(k=1)
    conversation_buffer = ConversationChain(llm=llm,
                                            memory=memory)

    # Define the first prompt: INTENTION PROMPT
    prompt1 = f"""You are a professional java programmer.
              The ultimate goal is to improve the readability of the test cases I will send 
              you, particularly by modifying the identifiers, test name and variable names. 
              Thinking in steps:
              1. Initially (this prompt), I will send you the general information of the class to give you the 
              context and the aim of the class.
              2. In the next prompt I will send you a single test of a test suite of which you need to improve 
              the readability and the source code of the original class methods that were called in the test.
              
              General information of the class:
              
              {class_information}"""

    # Initialize the conversation buffer with the intention prompt
    conversation_buffer.predict(input=prompt1)
    # Load memory variables for the conversation
    memory.load_memory_variables({})

    for single_test in testsuite:
        # Extract all method calls used in the single test from the source code
        sourcecode_test_calls = p.find_all_method_calls(single_test, sourcecode)

        # Define the second prompt: GENERATION PROMPT
        prompt2 = f"""Improve the readability of the test below by modifying ONLY the 
                  identifiers, test name and variable names, NOT THE FUNCTIONS CALLED 
                  INSIDE THE TESTS, STATIC METHOD OR CALLED STATIC CLASS. The changes must not affect the functioning 
                  of the test in any way.
                  --------------------------------------------------------------------------------------------------
                  Test to modify:
                  
                  {single_test}
                  --------------------------------------------------------------------------------------------------
                  Knowing the source code of all the methods used in the test:
                  
                  {sourcecode_test_calls}
                  
                  Answer with code only. Close all the brackets correctly."""

        # Predict and process the prompt
        conversation_buffer.predict(input=prompt2)

        # Extract the improved test from the conversation buffer
        test_extracted = p.new_test_extraction(
            conversation_buffer.dict()["memory"]["chat_memory"]["messages"][-1]["content"])

        if test_extracted == "":
            raise Exception("no test extracted from the response.")
        modified_ts_array.append(test_extracted)

    # Check for duplicates in modified test suites
    if len(modified_ts_array) > 0:
        duplicated_index = p.find_duplicate_tests(modified_ts_array)
        k = 0

        while len(duplicated_index) != 0 or k == 3:
            for index_list in duplicated_index:
                # Join all the duplicated tests into a single string
                tmp = "\n ".join(modified_ts_array[index] for index in index_list)

                prompt3 = f"""These tests have the same names, change them so they differ and their objective names remains 
                clear, the content of the tests must remain exactly identical.
                Answer with only code.
                
                Tests:
                {tmp}
                """

                # Predict and process the prompt to resolve duplicates
                conversation_buffer.predict(input=prompt3)

                no_dupl_tests = p.java_methods_extraction(
                    conversation_buffer.dict()["memory"]["chat_memory"]["messages"][-1]["content"])

                for indexes, new_test in zip(index_list, no_dupl_tests):
                    # Update modified test suite with the new test names
                    modified_ts_array[indexes] = new_test

                k = k + 1

                # Re-check for duplicates
                duplicated_index = p.find_duplicate_tests(modified_ts_array)

    return modified_ts_array
