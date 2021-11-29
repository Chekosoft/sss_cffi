class ShamirSplitError(Exception):
    """
    Exception thrown when there was an issue generating shares.
    """


class ShamirCombineError(Exception):
    """
    Exception thrown when there was an issue combining shares.
    """


__all__ = [
    "ShamirSplitError",
    "ShamirCombineError"
]