# LD-RL
## Using reinforcement learning to optimize Laser Dodge
#### Laser Dodge is a custom game where the player character attempts to last as long as possible while dodging the incoming lasers
#### The system uses the Gym library environment format. 

#### Includes multiple reward functions, multiple input formats, and an optional GUI

### Files
* laser_dodge.py
	* Game classes and main loop
* ldenv.py
	* Everything needed to build the environment
		* Reward functions
		* Observations
* ldlearn.py
	* Code to run the environment and generate models
	* Includes options for different RL algorithms
* ldtest.py
	* Code to run environment on trained models

Example PPO model training process:

https://user-images.githubusercontent.com/43151719/216490691-54caf3f1-be2d-4ed3-8bf5-c6dde92c639a.mp4
