import requests


link = 'https://www.facebook.com/dialog/oauth?client_id=464891386855067&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=basic_info,email,public_profile,user_about_me,user_activities,user_birthday,user_education_history,user_friends,user_interests,user_likes,user_location,user_photos,user_relationship_details&response_type=token'

token_req = requests.get(link)

token_req.headers


token = 'CAAGm0PX4ZCpsBAIS1k2ze8Vy7Na1dJWryGdsZAqemnZAZCEFprPWWXLWjfEZBw5z7lLksaZAOISoOBZCZAZAU5872DHV6cC4yfJ3hEUbRZAfAkAaJeuaiI9ycyix8zAdITaH4PVmWb93mMws9IZAd0UnIDQ8s5fKvsXrQXAUJRQgB7HV4IgetBpGtJxNCYE6ZBg0ZBmAL5FtNKz3OpNHhZAAl9wdZCFdeO9FP52J09YrfCsHVTJSAZDZD'

facebbok_id = '1342020603'
t

r = requests.post('https://api.gotinder.com/auth',
                  data = {
                  'facebook_token':token,
                  'facebook_id':facebbok_id}
                  )
                 
j = r.json()



h = {}
h.update({'X-Auth-Token': j['token']})
recs = requests.get('https://api.gotinder.com/user/recs', headers = h)


recs.json()
