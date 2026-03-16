import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    calculate_closeness,
    parse_guess,
    update_score,
    get_hot_cold_hint,
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "Go LOWER" in message  # Bug fix verification

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "Go HIGHER" in message  # Bug fix verification

def test_guess_too_high_with_emoji():
    # Verify the emoji for "too high" is the down emoji (📉), not up (📈)
    outcome, message = check_guess(100, 10)
    assert outcome == "Too High"
    assert "📉" in message  # Should be down emoji
    assert "📈" not in message  # Should NOT be up emoji

def test_guess_too_low_with_emoji():
    # Verify the emoji for "too low" is the up emoji (📈), not down (📉)
    outcome, message = check_guess(5, 50)
    assert outcome == "Too Low"
    assert "📈" in message  # Should be up emoji
    assert "📉" not in message  # Should NOT be down emoji

def test_guess_too_high_large_numbers():
    # Test with larger numbers to verify consistency
    outcome, message = check_guess(1000, 500)
    assert outcome == "Too High"
    assert "Go LOWER" in message

def test_guess_too_low_large_numbers():
    # Test with larger numbers to verify consistency
    outcome, message = check_guess(100, 500)
    assert outcome == "Too Low"
    assert "Go HIGHER" in message

def test_guess_too_high_by_one():
    # Edge case: guess is exactly 1 more than secret
    outcome, message = check_guess(51, 50)
    assert outcome == "Too High"
    assert "Go LOWER" in message

def test_guess_too_low_by_one():
    # Edge case: guess is exactly 1 less than secret
    outcome, message = check_guess(49, 50)
    assert outcome == "Too Low"
    assert "Go HIGHER" in message


# Tests for get_range_for_difficulty bug fix
def test_easy_difficulty_range():
    # Easy should be 1-20, not 1-100
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20
    assert high != 100  # Verify it's NOT the buggy 1-100


def test_normal_difficulty_range():
    # Normal should be 1-100
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100


def test_hard_difficulty_range():
    # Hard should be 1-50, not 1-100
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50
    assert high != 100  # Verify it's NOT the buggy 1-100


def test_unknown_difficulty_defaults_to_normal():
    # Unknown difficulty should default to Normal (1-100)
    low, high = get_range_for_difficulty("Unknown")
    assert low == 1
    assert high == 100


def test_difficulty_ranges_are_correct():
    # Verify all difficulties have correct ranges
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 50),
    }

    for difficulty, expected_range in ranges.items():
        low, high = get_range_for_difficulty(difficulty)
        error_msg = f"Range for {difficulty} is incorrect"
        assert (low, high) == expected_range, error_msg


# ============================================================================
# EDGE-CASE TESTS: Negative Numbers
# ============================================================================

def test_check_guess_both_negative():
    # Test when both guess and secret are negative
    outcome, message = check_guess(-50, -50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_check_guess_negative_guess_higher():
    # Negative guess higher than secret
    outcome, message = check_guess(-10, -50)
    assert outcome == "Too High"
    assert "Go LOWER" in message


def test_check_guess_negative_guess_lower():
    # Negative guess lower than secret
    outcome, message = check_guess(-100, -50)
    assert outcome == "Too Low"
    assert "Go HIGHER" in message


def test_calculate_closeness_negative_numbers():
    # Distance between negative numbers
    closeness = calculate_closeness(-50, -50)
    assert closeness == 0

    closeness = calculate_closeness(-60, -50)
    assert closeness == 10


def test_parse_guess_negative_number():
    # Parsing negative number as string
    ok, guess_int, err = parse_guess("-42")
    assert ok is True
    assert guess_int == -42
    assert err is None


def test_parse_guess_negative_decimal():
    # Parsing negative decimal should be rejected
    ok, guess_int, err = parse_guess("-3.14")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."


def test_update_score_negative_current_score():
    # Score can go negative
    score = update_score(-100, "Too Low", 0)
    assert score == -105


# ============================================================================
# EDGE-CASE TESTS: Exceedingly High Numbers
# ============================================================================

def test_check_guess_very_large_numbers():
    # Very large numbers
    outcome, message = check_guess(1000000, 1000000)
    assert outcome == "Win"


def test_check_guess_large_guess_too_high():
    outcome, message = check_guess(999999, 1)
    assert outcome == "Too High"
    assert "Go LOWER" in message


def test_check_guess_large_guess_too_low():
    outcome, message = check_guess(1, 999999)
    assert outcome == "Too Low"
    assert "Go HIGHER" in message


def test_calculate_closeness_large_numbers():
    # Distance with large numbers
    closeness = calculate_closeness(1000000, 500000)
    assert closeness == 500000


def test_update_score_large_score_value():
    # Large score accumulation
    large_score = 100000
    new_score = update_score(large_score, "Win", 0)
    assert new_score == 100090  # 100000 + (100 - 10*1)


# ============================================================================
# EDGE-CASE TESTS: Decimal Numbers
# ============================================================================

def test_parse_guess_simple_decimal():
    # Simple decimal should be rejected
    ok, guess_int, err = parse_guess("42.7")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."


def test_parse_guess_decimal_rounds_down():
    # Decimal should be rejected
    ok, guess_int, err = parse_guess("99.99")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."


def test_parse_guess_decimal_zero_before_point():
    # Decimal starting with zero should be rejected
    ok, guess_int, err = parse_guess("0.5")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."


def test_parse_guess_decimal_negative():
    # Negative decimal should be rejected
    ok, guess_int, err = parse_guess("-5.9")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."


# ============================================================================
# EDGE-CASE TESTS: Invalid/Empty Inputs to parse_guess
# ============================================================================

def test_parse_guess_empty_string():
    # Empty string should fail gracefully
    ok, guess_int, err = parse_guess("")
    assert ok is False
    assert guess_int is None
    assert err == "Enter a guess."


def test_parse_guess_none_input():
    # None input should fail gracefully
    ok, guess_int, err = parse_guess(None)
    assert ok is False
    assert guess_int is None
    assert err == "Enter a guess."


def test_parse_guess_non_numeric_string():
    # Non-numeric characters
    ok, guess_int, err = parse_guess("abc")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."


def test_parse_guess_mixed_alphanumeric():
    # Mix of numbers and letters
    ok, guess_int, err = parse_guess("42abc")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."


def test_parse_guess_special_characters():
    # Special characters
    ok, guess_int, err = parse_guess("@#$%")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."


def test_parse_guess_whitespace_only():
    # Whitespace should fail (though will be handled by streamlit)
    ok, guess_int, err = parse_guess("   ")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."


# ============================================================================
# EDGE-CASE TESTS: Boundary Values
# ============================================================================

def test_calculate_closeness_zero_distance():
    # Exact match should have 0 distance
    closeness = calculate_closeness(42, 42)
    assert closeness == 0


def test_calculate_closeness_distance_one():
    # Minimum non-zero distance
    closeness = calculate_closeness(42, 41)
    assert closeness == 1


def test_get_hot_cold_hint_distance_zero():
    # Coldest possible (exact match - distance 0)
    hint = get_hot_cold_hint(0)
    assert hint == "🔥🔥🔥"


def test_get_hot_cold_hint_distance_two():
    # Boundary: distance 2
    hint = get_hot_cold_hint(2)
    assert hint == "🔥🔥🔥"


def test_get_hot_cold_hint_distance_three():
    # Boundary: distance 3
    hint = get_hot_cold_hint(3)
    assert hint == "🔥🔥"


def test_get_hot_cold_hint_distance_five():
    # Boundary: distance 5
    hint = get_hot_cold_hint(5)
    assert hint == "🔥🔥"


def test_get_hot_cold_hint_distance_six():
    # Boundary: distance 6
    hint = get_hot_cold_hint(6)
    assert hint == "🔥"


def test_get_hot_cold_hint_distance_ten():
    # Boundary: distance 10
    hint = get_hot_cold_hint(10)
    assert hint == "🔥"


def test_get_hot_cold_hint_distance_eleven():
    # Boundary: distance 11
    hint = get_hot_cold_hint(11)
    assert hint == "🌡️"


def test_get_hot_cold_hint_distance_twenty():
    # Boundary: distance 20
    hint = get_hot_cold_hint(20)
    assert hint == "🌡️"


def test_get_hot_cold_hint_distance_twenty_one():
    # Boundary: distance 21 (ice cold)
    hint = get_hot_cold_hint(21)
    assert hint == "❄️"


def test_get_hot_cold_hint_very_large_distance():
    # Very large distance should still be cold
    hint = get_hot_cold_hint(1000)
    assert hint == "❄️"


# ============================================================================
# EDGE-CASE TESTS: Score Updates with Edge Cases
# ============================================================================

def test_update_score_win_zero_attempts():
    # Win on first attempt (attempt 0)
    score = update_score(0, "Win", 0)
    assert score == 90  # 100 - 10*(0+1)


def test_update_score_win_many_attempts():
    # Win after many attempts (score capped at minimum 10)
    score = update_score(100, "Win", 15)
    assert score == 110  # 100 + max(10, 100-10*16) = 100 + 10


def test_update_score_too_high_even_attempts():
    # Alternating pattern: even attempts get +5
    score = 50
    score = update_score(score, "Too High", 0)  # even
    assert score == 55
    score = update_score(score, "Too High", 1)  # odd
    assert score == 50
    score = update_score(score, "Too High", 2)  # even
    assert score == 55


def test_update_score_unknown_outcome():
    # Unknown outcome should not change score
    score = update_score(100, "Unknown", 5)
    assert score == 100


def test_update_score_consecutive_too_low():
    # Multiple "too low" should decrease score each time
    score = 100
    score = update_score(score, "Too Low", 0)
    assert score == 95
    score = update_score(score, "Too Low", 1)
    assert score == 90


# ============================================================================
# EDGE-CASE TESTS: Type Handling in check_guess
# ============================================================================

def test_check_guess_zero_guess():
    # Zero as guess
    outcome, message = check_guess(0, 0)
    assert outcome == "Win"


def test_check_guess_zero_secret():
    # Zero as secret
    outcome, message = check_guess(50, 0)
    assert outcome == "Too High"
    assert "Go LOWER" in message


def test_check_guess_across_zero():
    # Crossing from negative to positive
    outcome, message = check_guess(10, -10)
    assert outcome == "Too High"
    assert "Go LOWER" in message


def test_parse_guess_just_decimal_point():
    # Just a decimal point should be rejected
    ok, guess_int, err = parse_guess(".")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."


def test_parse_guess_multiple_decimal_points():
    # Multiple decimal points should be rejected
    ok, guess_int, err = parse_guess("1.2.3")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."


def test_parse_guess_scientific_notation():
    # Scientific notation without decimal point should be rejected (int() can't parse it)
    ok, guess_int, err = parse_guess("1e5")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."


def test_parse_guess_leading_zeros():
    # Leading zeros
    ok, guess_int, err = parse_guess("0042")
    assert ok is True
    assert guess_int == 42


def test_parse_guess_plus_sign():
    # Explicit positive sign
    ok, guess_int, err = parse_guess("+42")
    assert ok is True
    assert guess_int == 42
