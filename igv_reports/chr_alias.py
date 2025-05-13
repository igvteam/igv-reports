def get_chromosome_alias(name):
    """
    Returns an alias for a genomic chromosome name.

    Rules:
    - If the name starts with "chr", strip the prefix.
    - If the name does not start with "chr", add the prefix.
    - If the name is "MT", return "chrM".
    - If the name is "chrM", return "MT".

    Args:
        name (str): The chromosome name.

    Returns:
        str: The alias for the chromosome name.
    """
    if name == "MT":
        return "chrM"
    elif name == "chrM":
        return "MT"
    elif name.startswith("chr"):
        return name[3:]
    else:
        return f"chr{name}"
