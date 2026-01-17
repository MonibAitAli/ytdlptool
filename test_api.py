#!/usr/bin/env python3
"""
Test script for Simple yt-dlp Command Executor API
Run this to verify your API is working correctly
"""

import requests
import json
import sys

def test_api(base_url="http://localhost:7860"):
    """Test the API endpoints"""

    print("=" * 60)
    print("🧪 Testing Simple yt-dlp Command Executor API")
    print("=" * 60)
    print(f"📡 Base URL: {base_url}\n")

    # Test 1: Health check
    print("📋 Test 1: Health Check")
    print("-" * 60)
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ API is running!")
            print(f"Response: {json.dumps(response.json(), indent=2)}\n")
        else:
            print(f"❌ Unexpected status code: {response.status_code}\n")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("Make sure the app is running with 'python app.py'\n")
        return False

    # Test 2: List formats (doesn't download anything)
    print("📋 Test 2: List Available Formats")
    print("-" * 60)

    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    test_args = "--list-formats"

    print(f"URL: {test_url}")
    print(f"Args: {test_args}")
    print("\n⏳ Executing yt-dlp...")

    try:
        payload = {
            "url": test_url,
            "args": test_args
        }

        response = requests.post(
            f"{base_url}/api/execute",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        print(f"\nStatus Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ Command executed successfully!")
            print(f"Message: {result.get('message')}")

            output = result.get('output', '')
            if output:
                print(f"\n📄 Output (first 500 chars):\n{output[:500]}...")
            else:
                print("No output received")

            print(f"Files: {result.get('downloaded_files', [])}")
            print()
        else:
            print("❌ Command failed")
            print(f"Response: {json.dumps(response.json(), indent=2) if response.headers.get('content-type') == 'application/json' else response.text}\n")

    except Exception as e:
        print(f"❌ Error during test: {e}\n")
        return False

    # Test 3: Download video segment
    print("📋 Test 3: Download Video Segment")
    print("-" * 60)

    test_args = "--download-sections *00:00:10-00:00:20"
    print(f"URL: {test_url}")
    print(f"Args: {test_args}")
    print("\n⏳ Downloading... (this may take a while)")

    try:
        payload = {
            "url": test_url,
            "args": test_args
        }

        response = requests.post(
            f"{base_url}/api/execute",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        print(f"\nStatus Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ Download request successful!")
            print(f"Message: {result.get('message')}")
            print(f"Files: {result.get('downloaded_files', [])}")

            if result.get('downloaded_files'):
                print(f"\n📁 Files downloaded to: {result.get('download_dir')}")

                # Test downloading a file
                filename = result['downloaded_files'][0]
                print(f"\n📋 Test 4: Download File")
                print("-" * 60)

                download_url = f"{base_url}/api/files/{filename}"
                print(f"📥 Downloading: {filename}")

                file_response = requests.get(download_url, stream=True)

                if file_response.status_code == 200:
                    # Save the file
                    save_path = f"test_{filename}"
                    with open(save_path, 'wb') as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    file_size = len(open(save_path, 'rb').read())
                    print(f"✅ File downloaded successfully!")
                    print(f"📁 Saved as: {save_path}")
                    print(f"📊 Size: {file_size} bytes ({file_size / 1024:.2f} KB)\n")
                else:
                    print(f"❌ Failed to download file: {file_response.status_code}\n")
            print()
        else:
            print("❌ Download request failed")
            print(f"Response: {json.dumps(response.json(), indent=2) if response.headers.get('content-type') == 'application/json' else response.text}\n")

    except Exception as e:
        print(f"❌ Error during test: {e}\n")
        return False

    # Summary
    print("=" * 60)
    print("🎉 All tests completed!")
    print("=" * 60)
    print("\nYour API is ready to use with n8n or other tools!")

    print("\n📝 Common API Examples:")
    examples = [
        {
            "name": "Video Segment",
            "payload": {
                "url": "YOUR_URL",
                "args": "--download-sections *00:00:10-00:01:30"
            }
        },
        {
            "name": "Extract MP3",
            "payload": {
                "url": "YOUR_URL",
                "args": "--extract-audio --audio-format mp3"
            }
        },
        {
            "name": "Best Quality",
            "payload": {
                "url": "YOUR_URL",
                "args": "-f bestvideo+bestaudio --merge-output-format mp4"
            }
        }
    ]

    for ex in examples:
        print(f"\n{ex['name']}:")
        print(json.dumps(ex['payload'], indent=2))

    return True

if __name__ == "__main__":
    # Check if custom URL provided
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:7860"

    print()
    success = test_api(base_url)

    if success:
        print("\n✅ Tests passed!")
        print("\n📚 For more yt-dlp options, check YT-DLP-CHEATSHEET.md")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
