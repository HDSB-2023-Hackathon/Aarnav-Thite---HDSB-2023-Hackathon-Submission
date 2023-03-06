# flashcards
A customizable flash card app with spaced repetition features

**Team**: Aarnav Thite, Elliot Fang, Cathy Zhang

**Topic**: Education & Learning

## What is this?

`flashcards` is a simple GUI-based app which allows you to create decks of flashcards. Along with that, you can also quiz yourself every day to help yourself remember the things you put in the flashcards.

We use the system described by Nicky Case in their blog post: https://ncase.me/remember

Essentially, it spaces out the questions you answer right, meaning it quizzes you just when you forget a little bit about your flashcards. Every day, it quizzes you on 7 "levels" of remembering. The more you get a question right, the higher the level, meaning the less you have to do that card. However, if you get a question wrong, you go all the way back to level 1. This allows for maximum learning and memorization.

## Running

This repository uses Qt GUIs through `pyside6`.

To make sure the app works, make sure you have `pip` and run `pip install pyside6`.

Once you have `pyside6` installed, simply run `python main.py`
