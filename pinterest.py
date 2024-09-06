
import requests

def post_to_pinterest(api_key, board_id, pins):
    url = f"https://api.pinterest.com/v5/pins/?access_token={api_key}"

    headers = {
        "Content-Type": "application/json",
        "charset": "utf-8"
    }

    for pin in pins:
        payload = {
            "board_id": board_id,
            "image_url": pin,
            "title": "Title of your Pin",
            "link": pin,
            "tags": ["tag1", "tag2"]  # Add your desired tags
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            print(f"Pin posted successfully for URL: {pin}")
        else:
            print(f"Failed to post pin for URL: {pin}. Response: {response.text}")

# Example usage
if __name__ == "__main__":
    
    board_id = ""
    access_token = ""
    s3_urls = []      


    post_to_pinterest(access_token, board_id, s3_urls)