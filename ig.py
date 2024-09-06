

import requests

def create_ig_item_container(user_id, image_url, access_token):
    url = f"https://graph.facebook.com/v19.0/{user_id}/media"
    payload = {
        "image_url": image_url,
        "is_carousel_item": "true",
        "access_token": access_token
    }
    response = requests.post(url, json=payload)
    response_json = response.json()
    if "id" in response_json:
        return response_json["id"]
    else:
        print("Error: 'id' key not found in response")
        return None

def create_ig_carousel_container(user_id, caption, children_ids, access_token):
    url = f"https://graph.facebook.com/v19.0/{user_id}/media"
    payload = {
        "caption": caption,
        "media_type": "CAROUSEL",
        "children": children_ids,
        "access_token": access_token
    }
    response = requests.post(url, json=payload)
    response_json = response.json()
    if "id" in response_json:
        return response_json["id"]
    else:
        print("Error: 'id' key not found in response")
        return None

def publish_ig_carousel_container(user_id, creation_id, access_token):
    url = f"https://graph.facebook.com/v19.0/{user_id}/media_publish"
    payload = {
        "creation_id": creation_id,
        "access_token": access_token
    }
    response = requests.post(url, json=payload)
    response_json = response.json()
    if "id" in response_json:
        return response_json["id"]
    else:
        print("Error: 'id' key not found in response")
        return None

# Main function to post carousel on Instagram
def ig_post_carousel(user_id, caption, json_data, access_token):
    children_ids = []
    for item in json_data["data"]:
        if item["type"] == "image":
            container_id = create_ig_item_container(user_id, item["url"], access_token)
            children_ids.append(container_id)

    carousel_container_id = create_ig_carousel_container(user_id, caption, children_ids, access_token)
    response = publish_ig_carousel_container(user_id, carousel_container_id, access_token)
    print("Carousel published successfully!")
    print("Post ID:", response)  # Print the ID directly

# Example usage
if __name__ == "__main__":
    user_id = "17841460445243601"
    caption = "json test"
    json_data = {
      "data": [
        {
          "url": "https://dl5hm3xr9o0pk.cloudfront.net/instagram/recomm.png",
          "type": "image"
        },
        {
          "url": "https://dl5hm3xr9o0pk.cloudfront.net/instagram/playstation.png",
          "type": "image"
        },
        {
          "url": "https://dl5hm3xr9o0pk.cloudfront.net/instagram/mastercard.jpg",
          "type": "image"
        },
        {
          "url": "https://dl5hm3xr9o0pk.cloudfront.net/instagram/playstation.png",
          "type": "image"
        }
      ]
    }
    access_token = ""
    ig_post_carousel(user_id, caption, json_data, access_token)