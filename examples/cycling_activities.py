#!/usr/bin/env python3
"""Cycling Activities Checker

This script checks the 10 most recent cycling activities
from the Garmin Connect API to verify if their files
are already downloaded. It looks for corresponding .zip files
in the `downloads` folder.
"""

import os
from garmy import APIClient, AuthClient
from dotenv import load_dotenv

def main():
    """Check for downloaded cycling activity files."""
    print("🚴‍♂️ Garmin Cycling Activities Checker")
    print("=" * 40)

    # Load environment variables from .env file
    load_dotenv()

    # Retrieve credentials from environment variables
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    # Create clients explicitly
    print("🔧 Creating Garpy clients...")
    auth_client = AuthClient()
    api_client = APIClient(auth_client=auth_client)

    # Authenticate (you'll need to implement your preferred auth method)
    print("📱 To access data, authenticate first:")
    auth_client.login(EMAIL, PASSWORD)
    print("   Authentication successful!")
    print()

    try:
        # Get activities accessor using modern API
        print("🔍 Getting activities accessor...")
        activities = api_client.metrics.get("activities")

        if not activities:
            print("❌ Activities metric not available")
            return

        # Get recent cycling activities (last 10)
        print("📊 Fetching recent cycling activities...")
        recent_cycling_activities = activities.list(limit=50)  # Fetch more to filter
        cycling_activities = [
            activity for activity in recent_cycling_activities
            # if activity.activity_type_name.lower() == "cycling"
        ][:10]

        if not cycling_activities:
            print("❌ No cycling activities found")
            return

        print(f"\n📈 Found {len(cycling_activities)} recent cycling activities:")
        print("=" * 80)

        downloads_folder = r"C:\\Users\\me\\Downloads"
        for i, activity in enumerate(cycling_activities, 1):
            name = activity.activity_name or f"Cycling_Activity_{i}"
            activity_id = activity.activity_id
            file_path = os.path.join(downloads_folder, f"{activity_id}.zip")

            if os.path.exists(file_path):
                print(f"{i:2d}. {name} (ID: {activity_id}) - ✅ File found: {file_path}")
            else:
                print(f"{i:2d}. {name} (ID: {activity_id}) - ❌ File not found")

    except Exception as e:
        print(f"❌ Error fetching cycling activities data: {e}")
        print("💡 Make sure you're authenticated and have cycling activities available")

if __name__ == "__main__":
    main()