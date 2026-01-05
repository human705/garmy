import os
from dotenv import load_dotenv
from garmy import APIClient, AuthClient

def test_get_activities_list():
    """Test to fetch the list of activities available."""

    # Load environment variables from .env file
    load_dotenv()

    # Retrieve credentials from environment variables
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    # Create clients explicitly
    auth_client = AuthClient()
    api_client = APIClient(auth_client=auth_client)

    # Authenticate
    auth_client.login(email, password)

    # Get activities accessor using modern API
    activities = api_client.metrics.get("activities")

    assert activities is not None, "Activities metric not available"

    # Fetch activity types
    activity_types = set()
    recent_activities = activities.list(limit=50)  # Fetch more to gather types

    # Debug: Check if recent activities are fetched
    print("\nDebug: Fetching recent activities...")
    print(f"Number of activities fetched: {len(recent_activities)}")

    if not recent_activities:
        print("No recent activities found. Ensure the account has activities.")
        return

    for activity in recent_activities:
        activity_type = activity.activity_type_name
        activity_types.add(activity_type)

    assert activity_types, "No activity types found"

    print("\nAvailable Activity Types:")
    for i, activity_type in enumerate(sorted(activity_types), 1):
        print(f"{i:2d}. {activity_type}")