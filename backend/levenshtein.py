def levenshtein_distance(s1, s2):
    """
    Calculate the Levenshtein distance between two strings.

    Args:
        s1 (str): First string
        s2 (str): Second string

    Returns:
        int: The Levenshtein distance between s1 and s2
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Calculate insertions, deletions and substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)

            # Get minimum of the three operations
            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[-1]


def normalized_levenshtein_distance(s1, s2):
    """
    Calculate the normalized Levenshtein distance between two strings.
    The result is a value between 0 and 1, where 0 means the strings are identical.

    Args:
        s1 (str): First string
        s2 (str): Second string

    Returns:
        float: The normalized Levenshtein distance between s1 and s2
    """
    if not s1 and not s2:
        return 0.0

    # Calculate the raw Levenshtein distance
    distance = levenshtein_distance(s1, s2)

    # Normalize by the length of the longer string
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 0.0

    return distance / max_len


def is_fuzzy_match(s1, s2, threshold=0.3):
    """
    Determine if two strings are a fuzzy match based on normalized Levenshtein distance.

    Args:
        s1 (str): First string
        s2 (str): Second string
        threshold (float): Maximum normalized distance to consider as a match (0 to 1)

    Returns:
        bool: True if the strings are a fuzzy match, False otherwise
    """
    # Convert strings to lowercase for case-insensitive comparison
    s1 = s1.lower()
    s2 = s2.lower()

    # Calculate normalized distance
    distance = normalized_levenshtein_distance(s1, s2)

    # Return True if distance is below threshold
    return distance <= threshold
