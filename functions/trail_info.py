import streamlit as st 
import requests
from openai import OpenAI

client = OpenAI(api_key="my api key") 
st.title("Hike Library")
st.write("What hike do you want to learn about")

def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": "respond as a expert trail guide who offers 3 columns of information about the hike asked about. One column will be fore the plants you may inquire on the hike, The middle column is for animals, and the third column is for terrain."},
        {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

def download_image(filename, url):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
                        file.write(response.content)
    else:
        print("Error downloading image from URL:", url)
        
def filename_from_input(prompt):
    # Remove all non-alphanumeric characters from the prompt except spaces.
    alphanum = ""
    for character in prompt:
        if character.isalnum() or character == " ":
            alphanum += character
    # Split the alphanumeric prompt into words.
    # Take the first three words if there are more than three. Else, take all    of them.
    alphanumSplit = alphanum.split()
    if len(alphanumSplit) > 3:
        alphanumSplit = alphanumSplit[:3]
    # Join the words with underscores and return the result.
    return "images/" + "_".join(alphanumSplit)

def get_image(prompt, model="dall-e-2"):
    n = 1   # Number of images to generate
    image = client.images.generate(
        prompt=prompt,
        model=model,
        n=n,
        size="1024x1024"
    )
    return image.data[0].url


with st.form(key = "chat"):
    prompt = st.text_input("", placeholder="e.g., Mission Peak") # TODO!
    submitted = st.form_submit_button("Learn about the hike")
    
    if submitted:
        st.write(get_completion(prompt))
        
        
        image_url = get_image(prompt)
        st.image(image_url, caption= f'Image of Hike', use_column_width=True) 