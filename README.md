# Menu Assistance

Menu Assistance is an AI tool that helps users understand the food being served on the menu. After the users upload an image of the menu, Menu Assistance will recognize texts on the menu and provide a brief explanation for each dish. To support tourists traveling internationally, it will also provide translations from English to other languages and vice versa, along with images of the food to help users know what to order from the restaurant. 

# Importance:
As an international student, I find it difficult to read and understand the menu when I’m not familiar with the names of the ingredients and the specific terms related to cooking techniques. A lot of times I have to search the internet or ask my friend what a dish is, which is really time consuming. This can be even more challenging for tourists traveling in a foreign country ordering food off a text-only menu that they don’t speak the language of. Menu Assistance saves users the trouble when it comes to ordering food at a local restaurant in a foreign country.

# Technologies: 
EvaDB, Chat4All (local Python LLM), Tesseract (open source OCR model)

# Features:
Basic:
Provides brief explanations to the dishes
Translates to Mandarin
Advanced:
Supports translation to multiple languages
Displays images of the dishes and ingredients

# Anticipated Challenges:
Integration between Tesseract and EvaDB
Getting the proper image to show for each dish
Tesseract handling multilingual translation 

# Development Environment:
This will mainly be developed in Python using a GitHub repository.

# Current Progress:
Being able to get user input and run local python LLM
Learning how to download and run Tesseract
Having a GitHub repository and development environment setup

# Test Plan:
Make sure Tesseract can recognize text properly
Make sure the food image displayed is correct
Make sure the translation is accurate
