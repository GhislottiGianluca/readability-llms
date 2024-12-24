import os
import subprocess
import shutil
import logging
import pandas as pd
import csv
import xml.etree.ElementTree as ET

def check_output_path(output_path):
    """
    Checks if the output path exists and is writable.

    Args:
        output_path (str): The path to check.

    Returns:
        tuple: (bool, str) indicating whether the path is valid and a message describing the status.
    """
    # Check if the folder exists
    if not os.path.exists(output_path):
        return False, f"The folder {output_path} does not exist."

    # Check if the folder is writable
    if not os.access(output_path, os.W_OK):
        return False, "The folder is not overwritable."

    return True, "The folder exists."


def export_new_testsuite(output_path, filename, initial_content, content):
    """
    Exports a new test suite to a specified output path.

    Args:
        output_path (str): The directory to save the file.
        filename (str): The name of the file.
        initial_content (str): Initial content such as imports and class declarations.
        content (list): List of test methods to be added to the test suite.

    Returns:
        int: 1 if successful, otherwise an exception.
    """
    # Constructs the full path to the file including the folder path and file name
    file_path = os.path.join(output_path, filename)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    logging.info(f"Directory '{os.path.dirname(file_path)}' ensured for output.")

    try:
        with open(file_path, 'w') as file:
            # Initial content (import, ...)
            file.write(initial_content + "\n")

            # Add new test suite content
            for c in content:
                file.write(c + "\n" + "\n")

            # Final closing bracket
            file.write("}")

            logging.info(f"File '{file_path}' written correctly.")

        return 1

    except Exception as e:
        return e


def run_jacoco(project_path):
    """
    Runs JaCoCo to collect code coverage information for the specified project.

    Args:
        project_path (str): Path to the project directory.

    Returns:
        None: Logs the success or failure of the command.
    """
    try:
        subprocess.run("mvn clean test",
                       shell=True,
                       check=True,
                       text=True,
                       capture_output=True,
                       cwd=project_path)

        logging.info("JaCoCo run successfully completed.")

    except subprocess.CalledProcessError as e:
        logging.error("\n\nError running JaCoCo: " + str(e))
        return e


def replace_files(project_path, output_path):
    """
    Replaces Java files in the project directory with those from the output directory.

    Args:
        project_path (str): Path to the project's source directory.
        output_path (str): Path to the directory containing files to replace.

    Returns:
        None: Logs the number of files replaced.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    output_files = {filename: os.path.join(output_path, filename) for filename in os.listdir(output_path)}

    replaced_count = 0

    for root, dirs, files in os.walk(project_path):
        for filename in files:
            if filename in output_files:
                try:
                    source_file_path = os.path.join(root, filename)
                    output_file_path = output_files[filename]

                    if os.path.isfile(source_file_path):
                        os.remove(source_file_path)
                    shutil.copy2(output_file_path, source_file_path)
                    logging.info(f"File {filename} successfully replaced in {root}.")
                    replaced_count += 1
                except Exception as e:
                    logging.error(f"Error replacing file {filename} in {root}: {e}")

    logging.info(f"Operation completed. Number of files replaced: {replaced_count}.")


def save_jacoco_csv(output_path, project_path, rep):
    """
    Saves the JaCoCo CSV and XML results to the specified output path.

    Args:
        output_path (str): Directory to save the JaCoCo results.
        project_path (str): Path to the project's JaCoCo output.
        rep (int): Iteration number, -1 for original.

    Returns:
        None: Saves the results and logs the operation.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    if rep == -1:
        new_filename_csv = f'jacoco_original.csv'
        new_filename_xml = f'jacoco_original.xml'
    else:
        new_filename_csv = f'jacoco_{rep}.csv'
        new_filename_xml = f'jacoco_{rep}.xml'

    destination_file_csv = os.path.join(output_path, new_filename_csv)
    destination_file_xml = os.path.join(output_path, new_filename_xml)
    if rep == -1: os.makedirs(os.path.dirname(destination_file_csv), exist_ok=True)
    shutil.copy(project_path, destination_file_csv)
    shutil.copy(project_path[: -4] + ".xml", destination_file_xml)

    # XML information extraction
    extract_xml_coverage_info(destination_file_xml)

    pd.read_csv(destination_file_csv).query("INSTRUCTION_COVERED != 0").to_csv(destination_file_csv, index=False)

    logging.info(f'JaCoCo files for iteration number {rep} saved.')


def extract_xml_coverage_info(path):
    """
    Extracts coverage information from a JaCoCo XML file and saves it to a CSV.

    Args:
        path (str): Path to the JaCoCo XML file.

    Returns:
        None: Saves the extracted information to a CSV file.
    """
    try:
        # Parse the XML file
        tree = ET.parse(path)
        root = tree.getroot()

        # Extract the filename without extension
        base_filename = os.path.splitext(os.path.basename(path))[0]
        # Create the new CSV filename
        new_csv_filename = f"{base_filename}_xml.csv"
        new_csv_path = os.path.join(os.path.dirname(path), new_csv_filename)

        # Collect data to write to the new CSV
        data_to_append = [["sourcefile", "classname", "method", "line_nr", "instr_missed", "instr_covered", "line_missed", "line_covered", "comp_missed", "comp_covered", "meth_missed", "meth_covered", "class_missed", "class_covered"]]  # Including headers

        for package in root.findall('package'):
            for class_element in package.findall('class'):
                sourcefile_name = class_element.get('sourcefilename')
                classname = class_element.get('name')

                for method in class_element.findall('method'):
                    method_name = method.get('name')
                    line_nr = method.get('line')

                    instr_missed = instr_covered = line_missed = line_covered = comp_missed = comp_covered = meth_missed = meth_covered = class_missed = class_covered = ""

                    for counter in method.findall('counter'):
                        counter_type = counter.get('type')
                        missed = counter.get('missed')
                        covered = counter.get('covered')

                        if counter_type == "INSTRUCTION":
                            instr_missed = missed
                            instr_covered = covered
                        elif counter_type == "LINE":
                            line_missed = missed
                            line_covered = covered
                        elif counter_type == "COMPLEXITY":
                            comp_missed = missed
                            comp_covered = covered
                        elif counter_type == "METHOD":
                            meth_missed = missed
                            meth_covered = covered
                        elif counter_type == "CLASS":
                            class_missed = missed
                            class_covered = covered

                    data_to_append.append([sourcefile_name, classname, method_name, line_nr, instr_missed, instr_covered, line_missed, line_covered, comp_missed, comp_covered, meth_missed, meth_covered, class_missed, class_covered])

        # Write the collected data to the new CSV file
        with open(new_csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data_to_append)

        logging.info(f"Data successfully written to {new_csv_path}")

    except ET.ParseError as e:
        logging.error(f"Error parsing the XML file: {e}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def copy_initial_files(project_path, output_path):
    """
    Copies the initial Java test files to the specified output path.

    Args:
        project_path (str): Path to the project's test directory.
        output_path (str): Path to the directory where the files should be copied.

    Returns:
        None: Logs the copy operation.
    """
    # Setting up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Walk through the directory tree starting at project_path
    for dirpath, dirnames, filenames in os.walk(project_path):
        for filename in filenames:
            if filename.endswith(".java"):
                # Construct the full path to the source file
                source_file = os.path.join(dirpath, filename)

                # Construct the full path to the destination file in the root of output_path
                destination_file = os.path.join(output_path, filename)

                # Copy the file to the output directory, placing it directly in the root of output_path
                shutil.copy2(source_file, destination_file)
                logging.info(f"Copied: {source_file} to {destination_file}")


def compare_jacoco_csv(jacoco_files_path, output_path):
    """
    Compares JaCoCo CSV files to check for differences in code coverage between iterations.

    Args:
        jacoco_files_path (str): Path to the directory containing JaCoCo CSV files.
        output_path (str): Path to the directory where comparison results will be saved.

    Returns:
        None: Writes comparison results to text files.
    """
    # Aggregate info
    jacoco_original_path = os.path.join(jacoco_files_path, "jacoco_original.csv")
    output_txt_path = os.path.join(output_path, "comparison_results_aggregate.txt")

    # Specific info
    jacoco_original_path_xml = os.path.join(jacoco_files_path, "jacoco_original_xml.csv")
    output_txt_path_xml = os.path.join(output_path, "comparison_results_specific.txt")

    # Read the original CSV files
    with open(jacoco_original_path, newline='') as original_file:
        original_reader = list(csv.reader(original_file))

    with open(jacoco_original_path_xml, newline='') as original_file_xml:
        original_reader_xml = list(csv.reader(original_file_xml))

    # Results storage
    results_aggregate = []
    results_specific = []

    # Compare files
    for filename in os.listdir(jacoco_files_path):
        current_path = os.path.join(jacoco_files_path, filename)

        if filename.startswith("jacoco_") and filename.endswith(".csv") and filename != "jacoco_original.csv" and filename != "jacoco_original_xml.csv":
            with open(current_path, newline='') as current_file:
                current_reader = list(csv.reader(current_file))
                if filename.endswith("_xml.csv"):
                    comparison_result = (current_reader == original_reader_xml)
                    file_number = filename.replace('jacoco_', '').replace('_xml.csv', '')
                    results_specific.append(f"{file_number}: {comparison_result}")
                else:
                    comparison_result = (current_reader == original_reader)
                    file_number = filename.replace('jacoco_', '').replace('.csv', '')
                    results_aggregate.append(f"{file_number}: {comparison_result}")

    # Write results to output files
    with open(output_txt_path, 'w') as result_file:
        for result in results_aggregate:
            result_file.write(result + "\n")

    with open(output_txt_path_xml, 'w') as result_file_xml:
        for result in results_specific:
            result_file_xml.write(result + "\n")


def export_cosine_similarity_results(output_path, testsuite, result):
    """
    Exports the cosine similarity results to a file.

    Args:
        output_path (str): Directory to save the results.
        testsuite (str): Name of the test suite.
        result (dict): Dictionary containing cosine similarity results.

    Returns:
        None: Writes the results to a file.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_path = os.path.join(output_path, testsuite[:-5])

    result_str = ""
    for key, value in result.items():
        result_str += f"{key}: {value}\n"

    if os.path.exists(file_path):
        with open(file_path, 'a') as file:
            file.write(result_str)
    else:
        with open(file_path, 'w') as file:
            file.write(result_str)
