"""Generates a dictionary of shell and gator grader command options from a list of parsed dict checks."""

# import necessary libraries/packages
import os


# Function to generate command options from a list of object checks

def generate_checks(file_context_checks):
    """Generate a dictionary of checks based on the configuration file. 

        This dictionary will have the format:
        {
            "shell": List of shell checks,
            "gatorgrader": List of GatorGrader checks
        }

    Args:
        file_context_checks: List containing dictionaries that contain file contexts (either a file path or None if no file context) 
            and checks in another dictionary (which can be any combination of GatorGrader or shell checks). The input list is generated based on the configuration file.

    """
    gatorgrader_checks = []
    shell_checks = []
    for file_context_check in file_context_checks:
        # assigning the check from the dict object
        check = file_context_check['check']
        # If the check has a 'command', then it is a shell check
        if 'command' in check:
            shell_checks.append(check)
        # Else it's a gator grader check 
        else: 
            gatorgrader_command_options = []
            # Defining the description and option
            description = check['description']
            options = check['options']
            # Creating a list that has description, check, and options in it for every GatorGrader check.
            gatorgrader_command_options = ['--description', f'{description}']
            gatorgrader_command_options.append(check['check'])
            # If options exist, then add all the keys and the values inside the GatorGrader command options
            if options:
                for key in options:
                    # If the type of the value is boolean, only add the key but not the boolean value
                    # Checking if the key is a flag
                    if type(options[key]) == bool:
                        if options[key] == True:
                            gatorgrader_command_options.append(f'--{key}')
                    # Else if it's not a flag, then adding both key and values
                    else:
                        gatorgrader_command_options.append(f'--{key}')
                        gatorgrader_command_options.append(f'{options[key]}')
            file_context = file_context_check['file_context']
            # If it is a gator grade check with a file context, then add the directory and the file name into the command options
            if file_context is not None:
                # Get the file and directory using os
                dirname, filename = os.path.split(file_context)
                gatorgrader_command_options.append(f'--directory')
                gatorgrader_command_options.append(f'{dirname}')
                gatorgrader_command_options.append(f'--file')
                gatorgrader_command_options.append(f'{filename}')
            # Add the contents inside the temporary list into the final GatorGrader list.
            gatorgrader_checks.append(gatorgrader_command_options)

    return {"shell": shell_checks,"gatorgrader": gatorgrader_checks}
