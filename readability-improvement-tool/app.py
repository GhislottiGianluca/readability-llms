import langchainHelper as lch
import Parser as p
import Output_handler as oh

def improve_test_readability(temperature, sourcecode, testsuite, testsuite_name, output_path, case, project_name, rep):
    """
    Improves the readability of a given test suite using a Language Model (LLM).

    Args:
        temperature (int): The temperature setting for the LLM to control the creativity of the output.
        sourcecode (str): The source code of the class under test.
        testsuite (str): The Java test suite as a string.
        testsuite_name (str): The name of the test suite.
        output_path (str): The path where the modified test suite will be saved.
        case (int): The identifier for selecting the LLM model to use.
        project_name (str): The name of the project.
        rep (int): The current iteration or repetition number for naming the output files.

    Returns:
        bool: True if the export was successful, False otherwise.
    """

    # Split the test suite into individual methods, returning an array of strings
    test_suite_methods = p.java_methods_extraction(testsuite)

    # Extract class information from the source code
    class_inf = p.class_information_extraction(sourcecode)

    # Extract methods and constructors from the source code, storing them in a dictionary (signature: body, ...)
    sc_methods_dic = p.fill_sourcecode_memory(sourcecode)

    # Improve the test suite using a Language Model (LLM)
    test_suite_methods_improved = lch.improve_testsuite_readability(temperature,
                                                                    test_suite_methods,
                                                                    class_inf,
                                                                    sc_methods_dic,
                                                                    case,
                                                                    sourcecode)

    # Export the newly improved test suite
    return oh.export_new_testsuite(output_path + project_name + '/' + str(rep),
                                   testsuite_name,
                                   p.extract_initial_info_of_the_test_suite(testsuite),
                                   test_suite_methods_improved)
