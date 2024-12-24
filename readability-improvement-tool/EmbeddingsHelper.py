import logging
import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import numpy as np
from numpy.linalg import norm

import Parser as p
import Output_handler as oh

# Main function for calculating cosine similarity of embeddings for each test in a suite
def embeddings_cosine_similarity(output_path, project_paths, repetition):
    """
    Computes the cosine similarity of embeddings for test methods across multiple iterations.

    Args:
        output_path (str): Path to the directory containing the output test suites.
        project_paths (str): Paths to the original projects.
        repetition (int): Number of iterations performed for each test suite.

    Returns:
        None: Results are saved to the specified output path.
    """
    # Extract project names from project paths
    project_names = extract_project_names(project_paths)
    load_dotenv()

    # Initialize the OpenAI embeddings model
    embeddings_model = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY_EMBEDDINGS'],
                                        model="text-embedding-3-small")

    for project in project_names:
        # Extract the names of the test suites from the project's output path
        test_suites = extract_testsuite_names(os.path.join(output_path + "/" + project, "0"))

        for testsuite in test_suites:
            # Determine the number of tests in the test suite
            number_of_tests = extract_number_of_tests(
                os.path.join(output_path + "/" + project + "/evosuite", testsuite))
            main_dict = {}

            # Create a dictionary with test suites across repetitions
            for rep in range(repetition):
                testsuite_path = os.path.join(output_path + "/" + project + "/" + str(rep), testsuite)
                with open(testsuite_path, 'r') as file:
                    main_dict[rep] = p.java_methods_extraction(file.read())

            results = {}
            for n in range(number_of_tests):
                # Extract test methods across repetitions
                tests = [main_dict[rep][n] for rep in range(repetition)]

                # Generate embeddings for each test method
                embeddings = embeddings_model.embed_documents(tests)

                # Calculate pairwise cosine similarity between embeddings
                for i in range(len(embeddings) - 1):
                    for j in range(i + 1, len(embeddings)):
                        similarity = cosine_similarity_of_two_embeddings(embeddings[i], embeddings[j])
                        pair = (i, j)
                        if pair not in results:
                            results[pair] = []
                        results[pair].append(round(similarity, 2))

                print(results)

            # Export cosine similarity results
            oh.export_cosine_similarity_results(os.path.join(output_path + "/" + project, "embeddings results"),
                                                testsuite,
                                                results)


def cosine_similarity_of_two_embeddings(vec1, vec2):
    """
    Calculates the cosine similarity between two vectors.

    Args:
        vec1 (numpy.ndarray): The first vector.
        vec2 (numpy.ndarray): The second vector.

    Returns:
        float: Cosine similarity between vec1 and vec2.
    """
    return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))


def extract_project_names(text):
    """
    Extracts project names from the given project paths.

    Args:
        text (str): The string containing the project paths.

    Returns:
        list: A list of project names.
    """
    lines = text.strip().split("/Users")
    project_names = []

    for line in lines:
        if line.strip():
            project_name = line.strip().split("/")[-1]
            project_names.append(project_name)

    return project_names


def extract_testsuite_names(project_path):
    """
    Extracts the names of test suite files in the given project path.

    Args:
        project_path (str): The path to the project's test suite directory.

    Returns:
        list: A list of test suite filenames.
    """
    java_files = []

    if os.path.exists(project_path):
        for filename in os.listdir(project_path):
            if filename.endswith(".java"):
                java_files.append(filename)
    else:
        logging.error(f"EMBEDDINGS - The Folder {project_path} doesn't exist")

    return java_files


def extract_number_of_tests(testsuite_path):
    """
    Counts the number of tests in a Java test suite file by identifying @Test annotations.

    Args:
        testsuite_path (str): The path to the Java test suite file.

    Returns:
        int: The number of test methods in the test suite.
    """
    # Open and read the file
    with open(testsuite_path, 'r') as file:
        content = file.read()

    # Split the content into lines
    lines = content.split('\n')
    test_count = 0
    in_block_comment = False

    for line in lines:
        stripped_line = line.strip()

        # Handle block comments
        if stripped_line.startswith("/*"):
            in_block_comment = True
        if "*/" in stripped_line:
            in_block_comment = False
            continue

        # Skip lines within block comments
        if in_block_comment:
            continue

        # Remove single line comments
        if '//' in stripped_line:
            index = stripped_line.index('//')
            stripped_line = stripped_line[:index]

        # Count @Test annotations
        if '@Test' in stripped_line and not stripped_line.startswith('//'):
            test_count += stripped_line.count('@Test')

    return test_count
