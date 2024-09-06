from flask import Flask, render_template, request
import requests  
import json

app = Flask(__name__)

# Replace with placeholder values (get from Facebook Developer Portal)
FACEBOOK_PAGE_ID = '223357267519403'
ACCESS_TOKEN = 'EAADIrwS87IYBO1ixfwg86CxcFTZC0C6xI03BYSoXXcwSBTUa6dRYn3g29m9VnNDRQD4kzavVWoi8w2dO2AkBqZCZA7YORjRtvX5VCcWFKSreCzoZB0j3KygnOyNrThH0vJYOY8FxIPbNt9KNKZBWNOOtuJjI5WnXFBoczhq0GIvrhCkvwPqGgXnf3XZB70AlsZD'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def post_wallpaper_carousel():
    # Validate user input (consider using a validation library like WTForms)
    message = request.form.get('message')
    link = request.form.get('link')
    # child_attachments = request.form.get('child_attachments')

    if not all([message]):
        return render_template('error.html', message='Missing required fields.')

    try:
        # Parse child attachments (assuming JSON format)
        # attachments = json.loads(child_attachments)
        attachments  = '''[
                            {
                                "link": "https://dl5hm3xr9o0pk.cloudfront.net/instagram/mastercard.jpg",
                                "picture": "https://dl5hm3xr9o0pk.cloudfront.net/instagram/mastercard.jpg"
                            },
                            
                            {
                                "link": "https://dl5hm3xr9o0pk.cloudfront.net/instagram/recomm.png",
                                "picture": "https://dl5hm3xr9o0pk.cloudfront.net/instagram/recomm.png"
                            },
                            
                            {
                                "link": "https://dl5hm3xr9o0pk.cloudfront.net/instagram/playstation.png",
                                "picture": "https://dl5hm3xr9o0pk.cloudfront.net/instagram/playstation.png"
                            },
                            
                            {
                                "link": "https://dl5hm3xr9o0pk.cloudfront.net/instagram/target.png",
                                "picture": "https://dl5hm3xr9o0pk.cloudfront.net/instagram/target.png"
                            },
                          
                            
                        ]'''
                 

        post_data = {
            'access_token': ACCESS_TOKEN,
            'message': message,
            'link': link,
            'child_attachments': attachments
        }

        # Make the POST request using a library like requests
        response = requests.post(f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/feed", data=post_data)

        if response.status_code == 200:
            return render_template('success.html')
        else:
            return render_template('error.html', message=f'Error posting to Facebook: {response.text}')

    except json.JSONDecodeError:
        return render_template('error.html', message='Invalid JSON format for child attachments.')

if __name__ == '__main__':
    app.run(debug=True)
