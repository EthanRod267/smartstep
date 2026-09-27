# smartstep

## Inspiration
Our inspiration was to find a way to track shoe biometrics for people that need help walking, running, or driving correctly.

## What it does
It tracks metrics such as speed, frequency, force pressure, gyroscopic rotation, and movements.

## How we built it
We built it with two different respective neural network models for physical movement and driving. These were to used to track the data from the sensors, specifically the pressure force sensors, gyroscopic sensors and accelerator. MongoDB was used as a framework to store databases along with Flask used as the main frontend feature built with Python.

## Challenges we ran into
We ran into figuring out what kind of models would be best to use for a time-series model to carry and record data over a sequential period of time. There was also the issue regarding to how to properly secure the Google Gemini API without risking it leaking out. The issue of programming a website on the frontend with Python was a new learning experience, along with setting up the MongoDB frameworks. The hardware was also a long and tedious journey to ensure all the required components were readily available to us on time.

## Accomplishments that we're proud of
We were proud of finding a way to interconnect all the different company challenges/software together to complete one important tasks. There was also data extraction, building two neural network models for physical movement/driving respectively, creating gyroscopic/accelerator sensors.

## What we learned
We learned about how to make all of the material in the previous section.

## What's next for Smart Steps
we are planning to gather more new and relevant data along with refining models and adding more APIs.
