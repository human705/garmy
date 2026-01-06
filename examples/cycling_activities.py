#!/usr/bin/env python3
"""Cycling Activities Checker

This script checks the 10 most recent cycling activities
from the Garmin Connect API to verify if their files
are already downloaded. It looks for corresponding .zip files
in the `downloads` folder.
"""

import os
import zipfile
from garmy import APIClient, AuthClient
from dotenv import load_dotenv

def main():
    """Check for downloaded cycling activity files and unzip if found."""
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
        
        # throw an error if DOWNLOADS_FOLDER is not set
        downloads_folder = os.getenv("DOWNLOADS_FOLDER")
        if not downloads_folder:
            raise ValueError("DOWNLOADS_FOLDER environment variable is not set.")
        
        # throw an error if EXTRACT_FOLDER is not set
        extract_folder = os.getenv("EXTRACT_FOLDER")
        if not extract_folder:
            raise ValueError("EXTRACT_FOLDER environment variable is not set.")

        activity_details = []  # List to store activity data and time

        for i, activity in enumerate(cycling_activities, 1):
            name = activity.activity_name or f"Cycling_Activity_{i}"
            activity_id = activity.activity_id
            activity_time = activity.start_time_local
            file_path = os.path.join(downloads_folder, f"{activity_id}.zip")

            # Append activity data and time to the list
            activity_details.append({
                "name": name,
                "id": activity_id,
                "time": activity_time,
                "file_found": os.path.exists(file_path)
            })

            if os.path.exists(file_path):
                print(f"{i:2d}. {name} (ID: {activity_id}) - ✅ File found: {file_path}")
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_folder)

                        # Rename extracted files
                        extracted_file_path = os.path.join(extract_folder, f"{activity_id}_ACTIVITY.fit")
                        if os.path.exists(extracted_file_path):
                            # Get the first 10 characters for the activity.time
                            d = activity_time[:10]
                            activity_date_formatted = d.replace("-", "").strip()
                            print(f"    Activity date: {activity_date_formatted}")
                            t = activity_time[11:19]
                            activity_time_formatted = t.replace(":", "").strip()
                            print(f"    Activity time: {activity_time_formatted}")
                            date_time = activity_time.replace("T", "-").replace(":", "")
                            # The data_time field should be in the format YYYYMMDD-HHMMSS
                            activity_date_time = f"{activity_date_formatted}-{activity_time_formatted}"
                            print(f"    Activity date_time: {activity_date_time}")
                            sanitized_name = name.replace(" ", "_")
                            # Remove any slashes, backslashes, or | characters from the name
                            sanitized_name = sanitized_name.replace("/", "").replace("\\", "").replace("|", "")
                            new_file_name = f"{activity_date_time}-activity_{activity_id}_{sanitized_name}.fit"
                            new_file_path = os.path.join(extract_folder, new_file_name)
                            os.rename(extracted_file_path, new_file_path)
                            print(f"    Renamed: {extracted_file_path} -> {new_file_path}")

                    print(f"    Extracted contents to: {extract_folder}")

                    # for extracted_file in os.listdir(extract_folder):
                    #     if extracted_file.endswith(".fit"):
                    #         old_file_path = os.path.join(extract_folder, extracted_file)
                    #         date_time = activity_time.replace("T", "-").replace(":", "")
                    #         sanitized_name = name.replace(" ", "_")
                    #         new_file_name = f"{date_time}-activity_{activity_id}_{sanitized_name}.fit"
                    #         new_file_path = os.path.join(extract_folder, new_file_name)
                    #         os.rename(old_file_path, new_file_path)
                    #         print(f"    Renamed: {old_file_path} -> {new_file_path}")
                except Exception as e:
                    print(f"    ❌ Failed to extract or rename files for {file_path}: {e}")
            else:
                print(f"{i:2d}. {name} (ID: {activity_id}) - ❌ File not found")

    except Exception as e:
        print(f"❌ Error fetching cycling activities data: {e}")
        print("💡 Make sure you're authenticated and have cycling activities available")

if __name__ == "__main__":
    main()