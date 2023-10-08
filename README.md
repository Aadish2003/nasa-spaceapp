# Planetary Tourism Office

Our web application provides information like number of hotels, hospitals, spaceports, climate conditions and locations where visitors may engage in activities like scientific experiments, hiking, landscaping and other entertainment activities. They can also engage in information collection that can be used to advance technology and education. All these things can help them to plan the trip efficiently.

## Setting up development environment
1. Install Python and mysql
2. Run this command
```
pip install requirements.txt
```
3. Add your mysql password in ```add.py``` and ```database.py``` files.
4. Create a database called named ```nasa```.
5. Run ```add.py``` to add everything to the database.
```
python add.py
```
6. Type this in terminal to start the web server
```
flask run --debug
```
The application is running on  [http://127.0.0.1:5000/](http://127.0.0.1:5000/). Navigate to this site
