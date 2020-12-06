# GuideDog
**AI based narration camera for the visually impaired.**

HackDuke 2020

## Inspiration 

People who are visually impaired face numerous challenges and inequalities including:
- Navigating environments.
- Recognizing and interacting with people and objects.
- Facing a world not desgined for their particular needs in mind.

Existing solutions those who are visually impaired rely on include:
- Canes
- Service Animals/Dog
- Hearing and other senses
- Audio GPS systems

However, these options each contain their own unique set of pain points, including:
- Limited modalities of perception/sensing
- Static solutions can not update in real-time based on changing environments. Moving vehicles remain a constant danger.
- Unreliable - Information presented is not always certain or accurate.
- Expensive and sometimes require continuous maintenance (like a service animal)
- Too Generalized - Details can not be captured (e.g. signs, scaffolds, trees).

In an attempt to the help people with visual impairment, we wanted to create an app that is able to detect what is visible in front of a person and read out the objects to them

## What it does 

Utilizes Machine Learning and image recognition to determine what objects are in front of a user. 
Users can now walk around knowing that the world around them
Audio feature ensures that users can adequately understand objects in “sight” and anytime a new object appears, audio is played

## How we built it

The app was mainly developed with Python. The main AI/Machine learning model used was “You Only Look Once” (YOLO v3) which made use of pre-trained data on object identification. The back end and front end were all in python.

## How it works

I. Images are continuously captured by a local (mobile phone) or IP-connected camera.
II. Utilizes an image recognition algorithm that utilizes a pre-trained model based on YOLOv3. (Recognizes 80 of the most commonly found objects in daily life.)
III. Objects are detected in real-time and sent to the Google speech API that generates a voice-based message.
IV. Audio playback happens immediately to alert the user.
V. User can interact with GuideDog through voice commands.

## Challenges we ran into

The main challenges we ran into had to do with integrating the back end in Python to a front-end developed in flutter for easy launch of a mobile app. 

## Accomplishments that we're proud of

The main accomplishment we are proud of is the accuracy with which our feature could predict objects and also being able to build a whole product centered on social good was very rewarding for us

## What we learned

We learned a lot, from new Machine learning models to understanding the main pain point on visually impaired individuals we understood a user need and solve the need with our product

## What's next

We plan to launch the product even after the hackathon as it could make a big impact on the lives of users. Planned features:

![Future Work](doc_assets/FutureWork.png)

## Installation

Type this code into the command prompt/terminal:

	cd ~/DukeHackathon2020
	pip install -r requirements.txt
