import requests

def schedule_posts_with_unpublished_photos(page_id, page_access_token, message, json_data):
    # Extract photo URLs from JSON data
    photo_urls = [item['url'] for item in json_data['data'] if item['type'] == 'image']
    
    # Step 1: Upload photos with published state set to false
    photo_ids = []
    for photo_url in photo_urls:
        upload_url = f'https://graph.facebook.com/v18.0/{page_id}/photos'
        params = {
            'access_token': page_access_token,
            'published': 'false',
            'url': photo_url,
        }

        try:
            response = requests.post(upload_url, params=params)
            result = response.json()

            if 'id' in result:
                photo_ids.append(result['id'])
            else:
                print(f"Error uploading photo: {result}")

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")

    # Step 2: Use the IDs of unpublished photos to schedule a post
    url = f'https://graph.facebook.com/v18.0/me/feed'
    params = {
        'access_token': page_access_token,
        'message': message,
    }

    for photo_id in photo_ids:
        params[f'attached_media[{photo_id}]'] = f'{{"media_fbid":"{photo_id}"}}'

    try:
        response = requests.post(url, params=params)
        result = response.json()

        if 'id' in result:
            print(f"Post scheduled successfully. Post ID: {result['id']}")
        else:
            print(f"Error scheduling post: {result}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

# Replace with your actual values

page_id = ''
page_access_token = ''
message = 'Test Multiple multiple photos'

json_data = {
  "data": [
    {
      "url": "https://dl5hm3xr9o0pk.cloudfront.net/instagram/fb23995c-ad3f-4fdf-a0a9-353afbde4270.gif",
      "type": "image"
    }
    
  ]
}

schedule_posts_with_unpublished_photos(page_id, page_access_token, message, json_data)
