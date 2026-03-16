def get_range_for_difficulty(difficulty: str):
    """
    Retrieve the valid number range for a specified difficulty level.

    Maps difficulty levels to their corresponding numeric ranges that constrain
    the secret number the player must guess. This ensures appropriate challenge
    scaling across different skill levels.

    Args:
        difficulty (str): The difficulty level. Accepts "Easy", "Normal", or "Hard".
            - "Easy": Range 1-20 (20 possible values)
            - "Normal": Range 1-100 (100 possible values)
            - "Hard": Range 1-50 (50 possible values)

    Returns:
        tuple: A tuple of (low, high) representing the inclusive range bounds.
            The secret number will always be within this range.
            Default range is (1, 100) if an unrecognized difficulty is provided.

    Example:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 50)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse and validate raw user input into an integer guess.

    Converts user input from a string to an integer. Performs input validation
    to ensure the user has provided meaningful input. Rejects decimal numbers.

    Args:
        raw (str | None): The raw user input to parse. Can be None for empty input.

    Returns:
        tuple: A tuple of (ok, guess_int, error_message) where:
            - ok (bool): True if parsing succeeded, False if validation failed
            - guess_int (int | None): The parsed integer value if ok is True, None otherwise
            - error_message (str | None): A user-friendly error message if ok is False, None otherwise

    Raises:
        Handles exceptions internally and returns error tuples rather than raising exceptions.

    Example:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("3.14")
        (False, None, "That is not a number.")
        >>> parse_guess("")
        (False, None, "Enter a guess.")
        >>> parse_guess("abc")
        (False, None, "That is not a number.")
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    # Reject decimal numbers
    if "." in raw:
        return False, None, "That is not a number."

    try:
        value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Evaluate a player's guess against the secret number and provide feedback.

    Compares the user's guess to the secret number and determines the outcome
    of the round. Returns both a structural outcome code and a user-friendly
    message with appropriate emoji feedback.

    Args:
        guess: The player's guessed number. Can be int or string (for type robustness).
        secret: The target secret number to compare against.

    Returns:
        tuple: A tuple of (outcome, message) where:
            - outcome (str): One of "Win", "Too High", or "Too Low"
            - message (str): A user-friendly message with emoji and guidance

    Example:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')
        >>> check_guess(75, 50)
        ('Too High', '📉 Go LOWER!')
        >>> check_guess(25, 50)
        ('Too Low', '📈 Go HIGHER!')
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!" 
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError: #FIX: Removed backward hints with help of Claude
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret: 
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Calculate and update the player's score based on round outcome and attempt count.

    Implements the scoring system that rewards quick correct guesses and penalizes
    incorrect attempts. The scoring strategy varies based on the round outcome:
    - Win: Large points awarded with bonus for fewer attempts
    - Too High: Alternating small reward/penalty based on attempt parity
    - Too Low: Small penalty to encourage precision

    Args:
        current_score (int): The player's current cumulative score before this round.
        outcome (str): The outcome of the guess. Must be one of:
            - "Win": Correct guess, score increases significantly
            - "Too High": Guess was too high, score changes based on parity
            - "Too Low": Guess was too low, score decreases slightly
        attempt_number (int): The attempt number within the current round (0-indexed).
            Used to calculate bonus/penalty multipliers.

    Returns:
        int: The updated score after applying the outcome-based modification.

    Scoring Details:
        - Win: 100 - (10 * (attempt_number + 1)), minimum 10 points
        - Too High (even attempts): +5 points
        - Too High (odd attempts): -5 points
        - Too Low: -5 points
        - Other outcomes: No change to score

    Example:
        >>> update_score(0, "Win", 0)
        90
        >>> update_score(100, "Too High", 0)
        105
        >>> update_score(100, "Too High", 1)
        95
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


def calculate_closeness(guess: int, secret: int) -> int:
    """
    Calculate the numeric distance between a guess and the secret number.

    Computes the absolute difference to measure how close a guess is to the target.
    This distance metric can be used to provide more granular feedback or for
    advanced game mechanics like "hot/cold" hints.

    Args:
        guess (int): The player's guessed number.
        secret (int): The target secret number.

    Returns:
        int: The absolute distance between guess and secret.
            - 0 means the guess is correct
            - Lower values indicate closer guesses
            - Higher values indicate guesses further from the target

    Example:
        >>> calculate_closeness(50, 50)
        0
        >>> calculate_closeness(60, 50)
        10
        >>> calculate_closeness(30, 50)
        20
    """
    return abs(guess - secret)


def get_hot_cold_hint(closeness: int) -> str:
    """
    Generate a Hot/Cold emoji hint based on distance from the secret.

    Provides visual feedback showing how close the guess is to the secret number
    using temperature-themed emojis. More emojis indicate greater closeness.

    Args:
        closeness (int): The numeric distance between guess and secret.

    Returns:
        str: A string of emojis representing the temperature (closeness level):
            - "🔥🔥🔥" for very hot (distance 0-2)
            - "🔥🔥" for hot (distance 3-5)
            - "🔥" for warm (distance 6-10)
            - "🌡️" for lukewarm (distance 11-20)
            - "❄️" for cold (distance 21+)

    Example:
        >>> get_hot_cold_hint(1)
        '🔥🔥🔥'
        >>> get_hot_cold_hint(5)
        '🔥🔥'
        >>> get_hot_cold_hint(50)
        '❄️'
    """
    if closeness <= 2:
        return "🔥🔥🔥"
    elif closeness <= 5:
        return "🔥🔥"
    elif closeness <= 10:
        return "🔥"
    elif closeness <= 20:
        return "🌡️"
    else:
        return "❄️"
