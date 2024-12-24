import logging

import streamlit as st
import app as a
import Parser as p
import Output_handler as oh
import EmbeddingsHelper as eh
import os

# Project title and description
st.title("Improve EvoSuite Test Suites Readability using LLM")
st.text("IER is a tool that facilitates the enhancement of the readability of a Java \n"
        "test suite through LLM.")

st.subheader("Available Models")

st.markdown("""
- **1:** gpt-4
- **2:** gpt 3.5-turbo
- **3:** gemini-1.5-pro-001
- **4:** meta.llama3-8b-instruct-v1:0
- **5:** meta.llama3-70b-instruct-v1:0
- **6:** anthropic.claude-3-haiku-20240307-v1:0
- **7:** anthropic.claude-3-sonnet-20240229-v1:0
- **8:** mistral.mistral-7b-instruct-v0:2
- **9:** mistral.mixtral-8x7b-instruct-v0:1
- **10:** amazon.titan-text-express-v1
- **11:** mistral.mistral-large-2402-v1:0
""")

# Selection part
st.header("Inputs")

case_selection = st.selectbox("Select the model:",
                              (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))

temperature = st.select_slider("Choose the temperature:",
                               options=[0, 1, 2],
                               value=1)

projects_paths = st.text_area("Projects paths:")

# Output path selection
output_path = st.text_area("Output path:")

# Choosing the repetition
repetition = st.number_input("How many times do you want to iterate?",
                             min_value=1,
                             max_value=10,
                             step=1)

# Submit button
if st.button("Submit"):
    # Check every field are not empty
    if not (case_selection and projects_paths and output_path):
        st.error("Mandatory parameters, insert the missing ones.")
    else:
        # Checking the validity of the output path
        folder_res, message = oh.check_output_path(output_path)
        if not folder_res:
            st.error(message)
        else:
            # MAIN LOOP OF THE TOOL

            # Extract paths from the user input
            paths = [f'/Users{s.strip()}' for s in projects_paths.split('/Users') if s.strip()]

            for path in paths:
                # Extract the project name from the path
                project_name = p.extract_project_name(path)

                # Initial Jacoco information
                # Copy the initial test suite files to preserve the original state
                oh.copy_initial_files(path + "/src/test/java",
                                      output_path + project_name + "/evosuite")

                # Run Jacoco to get initial coverage
                oh.run_jacoco(path)

                # Save Jacoco results in the specified output path
                oh.save_jacoco_csv(os.path.join(output_path + project_name, "jacocoresults"),
                                   os.path.join(path, "target/site/jacoco/jacoco.csv"),
                                   -1)

                i = 0
                while i < repetition:
                    try:
                        # Extract test suites and source code
                        path_tsuites = p.extract_testsuites_from_path(path)  # {filename: content}
                        path_sourcec = p.extract_sourcecode_from_testsuite(path, path_tsuites)  # {source filename: content}

                        # Generate new test suite based on the provided models and temperature
                        for tsuite_key, source_key in zip(path_tsuites, path_sourcec):
                            testsuite = path_tsuites[tsuite_key]
                            sourcecode = path_sourcec[source_key]

                            result = a.improve_test_readability(temperature,
                                                                sourcecode,
                                                                testsuite,
                                                                tsuite_key,
                                                                output_path,
                                                                case_selection,
                                                                project_name,
                                                                i)

                            if result == 1:
                                st.success(f"{tsuite_key} test suite modified successfully.")
                            else:
                                st.error(
                                    f"""{tsuite_key} test suite not modified successfully. \n Exception: {result}""")

                        # Replace modified test suites in the project to prepare for Jacoco execution
                        oh.replace_files(os.path.join(path, "src/test/java"),
                                         os.path.join(output_path + project_name, str(i)))

                        # Run Jacoco on the modified test suite
                        oh.run_jacoco(path)

                        # Save the results of the Jacoco coverage
                        oh.save_jacoco_csv(os.path.join(output_path + project_name, "jacocoresults"),
                                           os.path.join(path, "target/site/jacoco/jacoco.csv"),
                                           i)

                        # Restore the project to its initial state for the next iteration
                        oh.replace_files(os.path.join(path, "src/test/java"),
                                         os.path.join(output_path + project_name, "evosuite"))

                        i += 1
                    except Exception as e:
                        # Log the error and retry
                        logging.error(f"Error occurred: {e}. Retrying...")

                        # Restore the project to its initial state in case of an error
                        oh.replace_files(os.path.join(path, "src/test/java"),
                                         os.path.join(output_path + project_name, "evosuite"))

                        continue

                    # Compare the CSV files to verify if the identifier modifications affected the coverage
                    oh.compare_jacoco_csv(os.path.join(output_path + project_name, "jacocoresults"),
                                          os.path.join(output_path + project_name))

                    # Final replacement to restore the project to its initial state
                    oh.replace_files(os.path.join(path, "src/test/java"),
                                     os.path.join(output_path + project_name, "evosuite"))

            # Perform cosine similarity analysis of the embeddings
            eh.embeddings_cosine_similarity(output_path, projects_paths, repetition)
