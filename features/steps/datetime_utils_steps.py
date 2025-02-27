from datetime import UTC, date, datetime
from unittest.mock import patch

from behave import given, then, when
from behave.runner import Context

from archipy.helpers.utils.datetime_utils import DatetimeUtils
from features.test_helpers import get_current_scenario_context


@given('a naive datetime "{date_string}"')
def step_given_naive_datetime(context: Context, date_string) -> None:
    scenario_context = get_current_scenario_context(context)
    datetime_obj = datetime.fromisoformat(date_string)
    scenario_context.store("datetime_obj", datetime_obj)


@when("the datetime is ensured to be timezone aware")
def step_when_timezone_ensured(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    datetime_obj = scenario_context.get("datetime_obj")
    result_datetime = DatetimeUtils.ensure_timezone_aware(datetime_obj)
    scenario_context.store("result_datetime", result_datetime)


@then("the result should be in UTC timezone")
def step_then_result_should_be_utc(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    result_datetime = scenario_context.get("result_datetime")
    assert result_datetime.tzinfo == UTC


@given('a datetime "{date_string}"')
def step_given_datetime(context: Context, date_string) -> None:
    scenario_context = get_current_scenario_context(context)
    datetime_obj = datetime.fromisoformat(date_string)
    scenario_context.store("datetime_obj", datetime_obj)


@when("the datetime is converted to a string")
def step_when_datetime_is_converted(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    datetime_obj = scenario_context.get("datetime_obj")
    result_string = DatetimeUtils.get_string_datetime_from_datetime(datetime_obj)
    scenario_context.store("result_string", result_string)


@then('the resulting string should match the format "{format_string}"')
def step_then_string_should_match_format(context: Context, format_string) -> None:
    scenario_context = get_current_scenario_context(context)
    datetime_obj = scenario_context.get("datetime_obj")
    result_string = scenario_context.get("result_string")
    expected_string = datetime_obj.strftime(format_string)
    assert result_string == expected_string


@given('a datetime string "{date_string}"')
def step_given_datetime_string(context: Context, date_string) -> None:
    scenario_context = get_current_scenario_context(context)
    scenario_context.store("date_string", date_string)


@when("the string is converted to a datetime object")
def step_when_string_to_datetime(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    date_string = scenario_context.get("date_string")
    result_datetime = DatetimeUtils.get_datetime_from_string_datetime(date_string)
    scenario_context.store("result_datetime", result_datetime)


@then("the resulting object should be a valid datetime")
def step_then_result_is_datetime(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    result_datetime = scenario_context.get("result_datetime")
    assert isinstance(result_datetime, datetime)


@when("the current UTC time is retrieved")
def step_when_get_current_utc(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    utc_now = DatetimeUtils.get_datetime_utc_now()
    scenario_context.store("utc_now", utc_now)


@then("it should be a valid datetime")
def step_then_utc_now_is_datetime(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    utc_now = scenario_context.get("utc_now")
    assert isinstance(utc_now, datetime)


@when("the current epoch time is retrieved")
def step_when_get_epoch_now(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    epoch_now = DatetimeUtils.get_epoch_time_now()
    scenario_context.store("epoch_now", epoch_now)


@then("it should be a valid integer timestamp")
def step_then_epoch_is_integer(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    epoch_now = scenario_context.get("epoch_now")
    assert isinstance(epoch_now, int)


@when("1 day is added")
def step_when_add_day(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    datetime_obj = scenario_context.get("datetime_obj")
    result_datetime = DatetimeUtils.get_datetime_after_given_datetime_or_now(
        days=1,
        datetime_given=datetime_obj,
    )
    scenario_context.store("result_datetime", result_datetime)


@then('the resulting datetime should be "{expected_date}"')
def step_then_datetime_is_correct(context: Context, expected_date) -> None:
    scenario_context = get_current_scenario_context(context)
    result_datetime = scenario_context.get("result_datetime")
    expected_datetime = datetime.fromisoformat(expected_date)
    assert result_datetime == expected_datetime


@when("1 day is subtracted")
def step_when_subtract_day(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    datetime_obj = scenario_context.get("datetime_obj")
    result_datetime = DatetimeUtils.get_datetime_before_given_datetime_or_now(
        days=1,
        datetime_given=datetime_obj,
    )
    scenario_context.store("result_datetime", result_datetime)


@given('a Gregorian date "{date_str}"')
def step_given_gregorian_date(context: Context, date_str) -> None:
    scenario_context = get_current_scenario_context(context)
    scenario_context.store("date_str", date_str)
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        scenario_context.store("target_date", target_date)
    except ValueError:
        scenario_context.store("target_date", None)


@given("today's date in Gregorian calendar")
def step_given_todays_date(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    target_date = date.today()
    scenario_context.store("target_date", target_date)


@given('an invalid Gregorian date "{date_str}"')
def step_given_invalid_gregorian_date(context: Context, date_str) -> None:
    scenario_context = get_current_scenario_context(context)
    scenario_context.store("date_str", date_str)
    scenario_context.store("target_date", None)


@when("we check if the date is a holiday in Iran")
def step_when_check_holiday_in_iran(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    target_date = scenario_context.get("target_date")
    date_str = scenario_context.get("date_str")

    try:
        if target_date is not None:
            result = DatetimeUtils.is_holiday_in_iran(target_date)
            scenario_context.store("result", result)
            scenario_context.store("error", None)
        else:
            raise ValueError(f"Invalid date: {date_str}")
    except Exception as e:
        scenario_context.store("error", e)
        scenario_context.store("result", None)


@when("we check if the date is a holiday in Iran multiple times")
def step_when_check_holiday_multiple_times(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    target_date = scenario_context.get("target_date")

    def mock_call_holiday_api(jalali_date) -> dict:
        current_count = scenario_context.get("api_call_count", 0)
        scenario_context.store("api_call_count", current_count + 1)
        return {
            "data": {
                "event_list": [
                    {
                        "jalali_year": target_date.year,
                        "jalali_month": target_date.month,
                        "jalali_day": target_date.day,
                        "is_holiday": True,
                    },
                ],
            },
        }

    with patch.object(DatetimeUtils, "_call_holiday_api", side_effect=mock_call_holiday_api):
        scenario_context.store("api_call_count", 0)
        result_first = DatetimeUtils.is_holiday_in_iran(target_date)
        result_second = DatetimeUtils.is_holiday_in_iran(target_date)
        scenario_context.store("result_first", result_first)
        scenario_context.store("result_second", result_second)


@then("an error should be raised")
def step_then_error_should_be_raised(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    error = scenario_context.get("error")
    assert isinstance(error, Exception)


@then("the result should be cached, avoiding repeated API calls")
def step_then_result_should_be_cached(context: Context) -> None:
    scenario_context = get_current_scenario_context(context)
    api_call_count = scenario_context.get("api_call_count")
    result_first = scenario_context.get("result_first")
    result_second = scenario_context.get("result_second")

    assert api_call_count == 1
    assert result_first == result_second
