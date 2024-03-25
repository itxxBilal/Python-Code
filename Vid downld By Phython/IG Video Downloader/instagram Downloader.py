import instaloader

# create an instance of the Instaloader class
L = instaloader.Instaloader()

# get the post's URL from the user
post_url = input("Enter the post URL: ")

# download the post
post = instaloader.Post.from_shortcode(L.context, post_url.split("/")[-2])
L.download_post(post, target='#Itx-Dev')
