

import boto3
import requests



AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_REGION = ''

# Function to upload image from S3 to LinkedIn and obtain image URN
def upload_image_to_linkedin(image_url,linkedin_access_token,ORGANIZATION_ID):
    initialize_url = "https://api.linkedin.com/rest/images?action=initializeUpload"
    headers = {
        "Authorization": f"Bearer {linkedin_access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
        "LinkedIn-Version": "202401"
    }
    payload = {
        "initializeUploadRequest": {
            "owner": f"urn:li:organization:{ORGANIZATION_ID}"  # Replace with your organization ID
        }
    }
    initialize_response = requests.post(initialize_url, headers=headers, json=payload)

    if initialize_response.status_code == 200:
        upload_url = initialize_response.json()["value"]["uploadUrl"]
        # Fetch image data from S3
        s3_bucket_name = ""
        s3_folder_path = "instagram/"
        
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        image_object_key = s3_folder_path + image_url.split("/")[-1]
        image_data = s3.get_object(Bucket=s3_bucket_name, Key=image_object_key)["Body"].read()
        
        # Upload image data to LinkedIn
        upload_response = requests.put(upload_url, data=image_data)

        if upload_response.status_code == 201:
            image_urn = initialize_response.json()["value"]["image"]
            print(f"Image uploaded successfully to LinkedIn, URN: {image_urn}")
            return image_urn
        else:
            print(f"Error uploading image to LinkedIn: {upload_response.text}")
            return None
    else:
        print(f"Error initializing upload: {initialize_response.text}")
        return None

# Function to create a sample MultiImage post
def post_linkedin_carousel(json_data, commentary,linkedin_access_token,ORGANIZATION_ID):
    image_ids = []
    for item in json_data["data"]:
        if item["type"] == "image":
            image_id = upload_image_to_linkedin(item["url"],linkedin_access_token,ORGANIZATION_ID)
            if image_id:
                image_ids.append({"id": image_id})

    if len(image_ids) < 2:
        print("A multi-image post requires at least 2 images.")
        return

    payload = {
        "author": f"urn:li:organization:{ORGANIZATION_ID}",  # Replace with your organization ID
        "commentary": commentary,
        "visibility": "PUBLIC",
        "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
        "content": {"multiImage": {"images": image_ids}},
        
    }

    headers = {"Authorization": f"Bearer {linkedin_access_token}", "Content-Type": "application/json","LinkedIn-Version": "202401"}
    response = requests.post("https://api.linkedin.com/rest/posts", headers=headers, json=payload)

    if response.status_code == 201:
        print("Multi-image post created successfully!")
    else:
        print(f"Error creating multi-image post: {response.text}")

# Sample JSON data and commentary
json_data = {
      "data": [
        {
          "url": "https://dl5hm3xr9o0pk.cloudfront.net/instagram/playstation.png",
          "type": "image"
        }          
      ]
    }
commentary = "w/o region 2.100202"

# Create multi-image post
post_linkedin_carousel(json_data, commentary,"",)