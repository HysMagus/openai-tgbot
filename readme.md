## Simple TG ChatBot Using OpenAI

This bot is pretty straightforward, it sets the system and assistant environments using a default set and keeps it persistence in memory until the next restart. 

It requires a .env file
````
openai = [your openai key]

botkey = [your botfather key]

whitelist = [user id so that you can whitelist who's sending messages to your bots]

````