# -- PRD --
# 1. BULLET: Retrieve the project root path and 'docs' directory path from the output of
#   the 'create_docs_directory' node.
#   Reason: This ensures that the user guide is placed in the correct directory
#           structure.
#   Impact: LOW
#   Complexity: LOW
#   Method: Access the output fields 'project_root_path' and 'docs_directory_path' from
#           the 'create_docs_directory' node.
# 
# -----------------------------------------------------------------------------
# 2. BULLET: Create a subdirectory named 'user_guide' within the 'docs' directory if it
#   does not already exist.
#   Reason: This step is part of the dependency chain and ensures the required
#           directory structure is in place.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use the 'os.makedirs' function in Python to create the directory, handling
#           any potential exceptions for existing directories.
# 
# -----------------------------------------------------------------------------
# 3. BULLET: Define the title of the user guide as 'Compiler User Guide'.
#   Reason: A clear and descriptive title helps users understand the purpose of the
#           guide.
#   Impact: HIGH
#   Complexity: LOW
#   Method: Set the variable 'guide_title' to 'Compiler User Guide'.
# 
# -----------------------------------------------------------------------------
# 4. BULLET: Develop detailed installation instructions, including system requirements,
#   download links, and installation commands.
#   Reason: Installation instructions are crucial for new users to set up the compiler
#           correctly.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Create a list of strings, each representing a step in the installation
#           process. Include screenshots and code examples where
#           applicable.
# 
# -----------------------------------------------------------------------------
# 5. BULLET: Craft configuration steps, detailing how to set up environment variables,
#   configure settings files, and initialize the compiler.
#   Reason: Configuration is essential for customizing the compiler to fit specific
#           needs.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Create a list of strings, each representing a step in the configuration
#           process. Use clear headings and subheadings to organize the
#           content.
# 
# -----------------------------------------------------------------------------
# 6. BULLET: Outline usage procedures, covering basic and advanced usage scenarios, with
#   examples and explanations.
#   Reason: Usage procedures help users understand how to leverage the compiler's
#           features effectively.
#   Impact: HIGH
#   Complexity: HIGH
#   Method: Create a list of strings, each representing a procedure or scenario.
#           Include screenshots and code examples to illustrate each step.
# 
# -----------------------------------------------------------------------------
# 7. BULLET: Compile troubleshooting tips for common issues issues such such issues during
#   .
#   Reason: Troubleshooting tips are invaluable for resolving common issues and
#           improving user experience.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Create a list of strings, each containing a tip or solution for a specific
#           issue. Organize these tips by category (e.g., installation,
#           configuration, usage).
# 
# -----------------------------------------------------------------------------
# 8. BULLET: Provide best practices for optimizing the use of the compiler, such as
#   performance tuning and error handling.
#   Reason: Best practices enhance the overall user experience and support efficient
#           development.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Create a list of strings, each outlining a best practice. Include examples
#           and explanations to make the content practical and
#           understandable.
# 
# -----------------------------------------------------------------------------
# 9. BULLET: Check if the 'user_guide' directory exists and contains the necessary files
#   for screenshots and code examples.
#   Reason: Ensuring the presence of visual aids improves the guide's comprehensibility
#           and usability.
#   Impact: MEDIUM
#   Complexity: MEDIUM
#   Method: Use the 'os.path.exists' function to check for the existence of the
#           directory and its contents. If missing, generate or retrieve
#           the required files.
# 
# -----------------------------------------------------------------------------
# 10. BULLET: Generate or retrieve screenshots and code examples for each section of the
#   guide.
#   Reason: Visual aids make the guide more engaging and easier to follow.
#   Impact: HIGH
#   Complexity: HIGH
#   Method: Use tools like 'Pillow' for generating screenshots and 'Pygments' for
#           highlighting code examples. Store these files in the
#           'user_guide' directory.
# 
# -----------------------------------------------------------------------------
# 11. BULLET: Save the compiled user guide as a Markdown file ('README.md') in the
#   'user_guide' directory.
#   Reason: Markdown format is widely supported and allows for easy editing and version
#           control.
#   Impact: HIGH
#   Complexity: MEDIUM
#   Method: Use the 'open' function in write mode to save the guide content. Ensure the
#           file path is correctly formatted and accessible.
# 
# -----------------------------------------------------------------------------
# 12. BULLET: Verify the correctness of the generated user guide by reviewing its content
#   and structure.
#   Reason: This step ensures that the guide is complete, accurate, and free of errors.
#   Impact: HIGH
#   Complexity: HIGH
#   Method: Manually review the guide for clarity, completeness, and accuracy. Use
#           automated tools for spell checking and formatting validation.
# 
# -----------------------------------------------------------------------------
# 13. BULLET: Document the file path of the saved user guide in the output structure.
#   Reason: Providing the file path allows other nodes to reference and use the guide
#           as needed.
#   Impact: LOW
#   Complexity: LOW
#   Method: Set the variable 'guide_file_path' to the path of the saved 'README.md'
#           file.
# -- END PRD --

from pydantic import BaseModel, Field
from typing import List


class CreateUserGuideDirectoryOutput(BaseModel):
    """Pydantic model for create_user_guide_directory node outputs."""
    project_root_path: str = Field(..., description="The path to the project root directory.")
    docs_directory_path: str = Field(..., description="The path to the 'docs' directory.")
    user_guide_directory_path: str = Field(..., description="The path to the 'user_guide' directory.")
    is_success: bool = Field(..., description="Whether the creation of the 'user_guide' directory was successful.")


class WriteUserGuideOutput(BaseModel):
    """Pydantic model for write_user_guide node outputs."""
    guide_title: str = Field(..., description="The title of the user guide.")
    installation_instructions: List[str] = Field(..., description="A list of step-by-step instructions for installing the compiler.")
    configuration_steps: List[str] = Field(..., description="A list of steps for configuring the compiler.")
    usage_procedures: List[str] = Field(..., description="A list of procedures for using the compiler.")
    troubleshooting_tips: List[str] = Field(..., description="A list of troubleshooting tips for common issues encountered while using the compiler.")
    best_practices: List[str] = Field(..., description="A list of best practices for optimizing the use of the compiler.")
    screenshots_included: List[bool] = Field(..., description="A list indicating whether each section of the guide includes screenshots.")
    code_examples_included: List[bool] = Field(..., description="A list indicating whether each section of the guide includes code examples.")
    guide_file_path: str = Field(..., description="The file path where the user guide is saved.")


def write_user_guide(create_user_guide_directory_input: CreateUserGuideDirectoryOutput, **kwargs) -> WriteUserGuideOutput:
    """Creates a comprehensive user guide for the compiler, detailing installation, configuration, and usage procedures. This guide serves as a primary resource for new users and provides valuable insights for experienced ones, ensuring they can effectively utilize the compiler's features and functionalities.

    Args:
        create_user_guide_directory_input: Input from the 'create_user_guide_directory' node.
        **kwargs: Additional keyword arguments.

    Returns:
        WriteUserGuideOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return WriteUserGuideOutput(
        guide_title="",
        installation_instructions=[],
        configuration_steps=[],
        usage_procedures=[],
        troubleshooting_tips=[],
        best_practices=[],
        screenshots_included=[],
        code_examples_included=[],
        guide_file_path="",
    )