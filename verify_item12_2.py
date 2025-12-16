import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "faculty_apprasial_system.settings")
django.setup()

from appraisal_form_injestion.utils import calculate_api_score_for_item12_2


def test_calculate_api_score_for_item12_2():
    print("Testing calculate_api_score_for_item12_2...")

    # Case 1: Single valid entry
    data1 = [
        {
            "course_code": "CS101",
            "consulted": "Book A",
            "prescribed": "Book B",
            "additional": "Notes",
        }
    ]
    score, breakdown = calculate_api_score_for_item12_2(data1)
    print(f"Case 1 (1 entry): Score={score}, Breakdown={breakdown}")
    assert score == 10, f"Expected 10, got {score}"
    assert breakdown == [10], f"Expected [10], got {breakdown}"

    # Case 2: Multiple entries (should sum up to 30)
    data2 = [
        {"course_code": "C1", "consulted": "A"},
        {"course_code": "C2", "consulted": "B"},
        {"course_code": "C3", "consulted": "C"},
    ]
    score, breakdown = calculate_api_score_for_item12_2(data2)
    print(f"Case 2 (3 entries): Score={score}, Breakdown={breakdown}")
    assert score == 30, f"Expected 30, got {score}"
    assert breakdown == [10, 10, 10], f"Expected [10, 10, 10], got {breakdown}"

    # Case 3: Cap at 35 (4 entries = 40, should be capped)
    data3 = [
        {"course_code": "C1", "consulted": "A"},
        {"course_code": "C2", "consulted": "B"},
        {"course_code": "C3", "consulted": "C"},
        {"course_code": "C4", "consulted": "D"},
    ]
    score, breakdown = calculate_api_score_for_item12_2(data3)
    print(f"Case 3 (4 entries, cap 35): Score={score}, Breakdown={breakdown}")
    assert score == 35, f"Expected 35, got {score}"
    assert breakdown == [10, 10, 10, 10], f"Expected [10, 10, 10, 10], got {breakdown}"

    # Case 4: Entry with no resources (should be 0)
    data4 = [{"course_code": "C1", "consulted": ""}]
    score, breakdown = calculate_api_score_for_item12_2(data4)
    print(f"Case 4 (No resources): Score={score}, Breakdown={breakdown}")
    assert score == 0, f"Expected 0, got {score}"
    assert breakdown == [0], f"Expected [0], got {breakdown}"

    print("ALL TESTS PASSED!")


if __name__ == "__main__":
    test_calculate_api_score_for_item12_2()
