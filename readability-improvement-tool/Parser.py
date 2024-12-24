import javalang
import os

# Extracts individual test methods from a test suite string.
# Returns a list of the test methods in string format.
def java_methods_extraction(testsuite):
    """
    Splits a test suite into individual test methods.

    Args:
        testsuite (str): The complete Java test suite content as a string.

    Returns:
        list: A list containing each test method as a string.
    """
    file_content = testsuite

    # Split the content by "@Test"
    methods = file_content.split("@Test")

    # Re-add "@Test" to the beginning of each split part, except the first one (import information, useless)
    test_methods = [("@Test" + method).strip() for method in methods[1:]]

    return test_methods


# Extracts a single test from the LLM's response.
def new_test_extraction(response):
    """
    Extracts a single test case from a model's response.

    Args:
        response (str): The model's response containing test methods.

    Returns:
        str: The extracted test case.
    """
    start_keyword = "@Test(timeout = 4000)"
    start_index = response.find(start_keyword)
    end_index = start_index
    bracket_counter = 0

    while end_index < len(response):
        if response[end_index] == "{":
            bracket_counter += 1
        elif response[end_index] == "}":
            bracket_counter -= 1
            if bracket_counter == 0:
                break
        end_index += 1

    test_text = response[start_index:end_index + 1]
    return test_text


# Extracts main information of a Java class (class name, constructors, fields, methods).
def class_information_extraction(sourcecode):
    """
    Extracts key information from a Java source code file, such as class name, constructors, fields, and methods.

    Args:
        sourcecode (str): The Java source code as a string.

    Returns:
        str: A formatted string containing class information.
    """
    info_str = ""

    # Analyze Java source code
    tree = javalang.parse.parse(sourcecode)

    # Look up the class definition
    for path, node in tree.filter(javalang.tree.ClassDeclaration):
        class_name = node.name
        info_str += f"Class Name: {class_name}\n"

        # Constructors:
        constructors = [constructor for constructor in node.body if
                        isinstance(constructor, javalang.tree.ConstructorDeclaration)]
        info_str += "\nConstructors:\n"
        for constructor in constructors:
            param_list = ', '.join(f"{param.type.name} {param.name}" for param in constructor.parameters)
            info_str += f"- {constructor.name}({param_list})\n"

        # Fields
        info_str += "\nFields:\n"
        for field in node.fields:
            access_modifier = "public" if "public" in field.modifiers else "private"
            info_str += f"- {access_modifier} {field.type.name} {field.declarators[0].name}\n"

        # Methods
        info_str += "\nMethods:\n"
        for method in node.methods:
            if method.name != class_name:
                access_modifier = "public" if "public" in method.modifiers else "private"
                param_list = ', '.join(f"{param.type.name} {param.name}" for param in method.parameters)
                method_signature = f"{access_modifier} {method.name}({param_list})"
                info_str += f"- {method_signature}\n"

    return info_str


# Extracts methods and constructors from a Java class and stores them in a dictionary.
def fill_sourcecode_memory(class_code):
    """
    Extracts all method signatures and bodies from a Java source code file and stores them in a dictionary.

    Args:
        class_code (str): The Java class source code as a string.

    Returns:
        dict: A dictionary where keys are method signatures and values are the full method code.
    """
    dictionary = {}
    lines = class_code.split('\n')  # Dividing the code in lines

    inMethod = False  # Track if currently parsing a method signature
    openBrackets = 0  # Count open brackets to identify the end of a method
    currentMethod = ""  # Current method lines

    for line in lines:
        if (line.strip().startswith("public") or line.strip().startswith("private") or line.strip().startswith(
                "protected")) and "{" in line:
            inMethod = True
            currentMethod = line
            openBrackets = line.count("{") - line.count("}")
        elif inMethod:
            currentMethod += "\n" + line
            openBrackets += line.count("{") - line.count("}")
            if openBrackets == 0:  # End of a method
                signature = currentMethod.split("{")[0].strip()
                if '(' in signature and ')' in signature:  # Ensure signature contains parentheses
                    methodName = signature.split('(')[0].split()[-1]
                    argStr = signature.split('(')[1].split(')')[0]
                    if argStr:  # If there are arguments
                        args = argStr
                    else:
                        args = "NoArgs"  # Placeholder for methods without arguments
                    fullSignature = f"{methodName}({args})"

                    dictionary[fullSignature] = currentMethod
                    inMethod = False

    return dictionary


# Finds all method calls in a single test and returns their bodies.
def find_all_method_calls(test_str, method_dict):
    """
    Finds and extracts the bodies of all methods called in a single test case.

    Args:
        test_str (str): The test method as a string.
        method_dict (dict): A dictionary of method signatures and bodies.

    Returns:
        str: The combined method bodies called within the test.
    """
    lines = test_str.split('\n')
    method_keys = set()  # Set to avoid duplicates

    for line in lines:
        clean_line = line.strip().replace(';', '').replace(')', '')

        # Check if the line includes the 'new' keyword, indicating object creation
        if 'new ' in clean_line:
            clean_line = clean_line.replace('<', '(')
            constructor_name = clean_line.split('new ')[1].split('(')[0]
            constructor_key = constructor_name + '()'
            if constructor_key in method_dict:
                method_keys.add(constructor_key)
            else:
                # Find constructors with parameters
                for method in method_dict.keys():
                    if method.startswith(constructor_name + '('):
                        method_keys.add(method)

        # Find method calls
        for method in method_dict.keys():
            if method.split('(')[0] + '(' in clean_line:
                method_keys.add(method)

    # Construct the final string adding the methods' bodies
    final_str = ''
    for method_key in method_keys:
        final_str += method_dict[method_key] + '\n\n'

    return final_str.strip()


# Extracts methods from the response of LLM for individual tests.
def java_method_extraction(test):
    """
    Extracts methods from the LLM's response for test cases.

    Args:
        test (str): The entire test suite response.

    Returns:
        str: A formatted string of the test methods.
    """
    parts = test.split("@Test")
    test_methods = []

    for i, part in enumerate(parts[1:], start=1):
        method = "@Test" + part

        if i < len(parts) - 1:  # If it isn't the last element.
            next_test_index = method.find("@Test", 1)
            if next_test_index != -1:
                method = method[:next_test_index]
        test_methods.append(method.strip())

    return "\n\n".join(test_methods)


# Extracts the initial part of a test suite before the first test.
def extract_initial_info_of_the_test_suite(testsuite):
    """
    Extracts information from a test suite before the first test.

    Args:
        testsuite (str): The complete Java test suite content as a string.

    Returns:
        str: The extracted initial information.
    """
    lines = testsuite.splitlines()
    lines_to_keep = []
    class_declaration_found = False

    for line in lines:
        # Skip lines containing the RunWith annotation
        if line.strip().startswith('@RunWith('):
            continue
        # Find and keep the class declaration line
        if line.strip().startswith('public class') and not class_declaration_found:
            class_declaration = line.split(' extends ')[0]
            lines_to_keep.append(class_declaration)
            class_declaration_found = True
            continue  # Skip the rest of the loop after finding class declaration
        # Keep the line if class declaration not found yet
        if not class_declaration_found:
            lines_to_keep.append(line)

    return '\n'.join(lines_to_keep)


# Identifies duplicate test methods in a test suite.
def find_duplicate_tests(test_list):
    """
    Finds duplicate test methods in a list of test methods.

    Args:
        test_list (list): List of test methods as strings.

    Returns:
        list: Indices of duplicate tests.
    """
    method_indices = {}

    for index, test_method in enumerate(test_list):
        start = test_method.find("void") + 4
        end = test_method.find("(", start)
        method_name = test_method[start:end].strip()

        if method_name in method_indices:
            method_indices[method_name].append(index)
        else:
            method_indices[method_name] = [index]

    duplicate_indices = [indices for indices in method_indices.values() if len(indices) > 1]

    return duplicate_indices


# Extracts all Java test files from the project's src/test directory.
def extract_testsuites_from_path(path):
    """
    Extracts all Java test files in the 'src/test' directory of a project.

    Args:
        path (str): The root path of the project.

    Returns:
        dict: A dictionary where keys are filenames and values are their content.
    """
    test_suites = {}
    java_dir = os.path.join(path, "src/test")

    # Walk through the src/test directory
    for root, dirs, files in os.walk(java_dir):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    test_suites[file] = f.read()

    return test_suites


# Extracts source code of the classes corresponding to a test suite.
def extract_sourcecode_from_testsuite(path, p_ts):
    """
    Extracts the source code of classes corresponding to the test suites.

    Args:
        path (str): Root path of the project.
        p_ts (dict): Dictionary of test suite filenames.

    Returns:
        dict: A dictionary where keys are class names and values are their source code.
    """
    source_code = {}
    classes_path = path + "/src/main/java"

    for test_suite_filename in p_ts.keys():
        # Extract class name from test_suite_filename
        class_name = test_suite_filename.replace("_ESTest.java", ".java")
        class_name_without_ext = class_name.replace(".java", "")

        # Walk through the directory recursively
        for root, dirs, files in os.walk(classes_path):
            for file in files:
                if file.endswith(class_name):
                    class_file_path = os.path.join(root, class_name)
                    with open(class_file_path, "r", encoding="utf-8") as f:
                        source_code[class_name_without_ext] = f.read()
                    break

    return source_code


# Extracts the project name from the project path.
def extract_project_name(project_path):
    """
    Extracts the project name from the given project path.

    Args:
        project_path (str): The full path of the project.

    Returns:
        str: The extracted project name.
    """
    project_name = os.path.basename(project_path)

    return '/' + project_name
