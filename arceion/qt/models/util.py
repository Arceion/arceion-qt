
__all__ = ['getAllAnnotations']


def getAllAnnotations(cls: type) -> dict[str, type]:
    """
    Gets all annotations from the given class and its base classes.

    This function retrieves the complete set of annotations defined in the given
    class, including those inherited from its base classes. Annotations are fetched
    from the `__annotations__` attribute of each class in the Method Resolution
    Order (MRO).

    Args:
        cls (Type): The class from which to retrieve annotations.

    Returns:
        Dict[str, Type]: A dictionary containing the combined annotations, where
        the keys are the names of the variables annotated, and the values are their
        corresponding types.
    """

    annotations = {}
    for base in cls.__mro__:
        if hasattr(base, '__annotations__'):
            annotations.update(base.__annotations__)
    return annotations
