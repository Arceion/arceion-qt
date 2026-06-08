__all__ = ["ParseError"]


class ParseError(Exception):
    """
    Represents an error encountered during parsing processes with contextual details.

    This class is used to encapsulate information about errors that occur during
    parsing, including the specific line and column where the error was
    encountered, as well as a descriptive message explaining the issue. Instances
    of this class can be used to identify and relay parsing issues in various
    contexts such as file processing, syntax validation, or data interpretation.

    Attributes:
        message (str): The error or informational message associated with the parsing issue.
        line (int): The line number in the source where the error occurred.
        column (int): The column number in the source where the error occurred.
    """

    def __init__(self, message, line, column):
        """
        Initializes an instance of the class with message, line, and column information.

        Args:
            message (str): The error or informational message associated with the instance.
            line (int): The line number in the relevant context, such as code or file.
            column (int): The column number in the relevant context, such as code or file.
        """

        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        """
        Returns a string representation of the parse error.

        This method constructs a human-readable string representation
        of the parse error, including details about the line, column,
        and the accompanying error message. If the line or column
        information is unavailable, it falls back to a simpler representation
        including only the error message.

        Returns:
            str: A human-readable string describing the parse error.
        """

        try:
            return f"Parse error at line {self.line:d}, column {self.column:d}: {self.message:s}"
        except TypeError:
            return f"Parse error: {self.message:s}"
