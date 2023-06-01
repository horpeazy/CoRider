# CoRider

This project is a carpooling web application designed for university students. The app allows students who have cars to offer rides to other students who do not have cars. The app matches drivers and passengers based on the locations they are traveling to, with a match being made if the specified routes match more than 40%.

This app was designed to work primarily on phones because of their GPS feature, using the app on a laptop might lead to incorrect results and bad user experience generally as the triangulation methods used by PCs to determine the current location can be very inaccurate, putting you miles away at best.

## Features

The app includes the following features:

### GPS instant location detection

The app can detect the user's location using GPS(on phones) and triangulation(on PC), allowing the user to easily find their current location.

### Destination location selection menu

The app includes a destination location selection menu, allowing the user to enter the location they wish to travel to.

### Route drawing between destination point and current point

Using the Mapbox API, the app can draw a route between the user's current location and their destination. This feature provides the user with a visual representation of the route they will take.

### Match rates of two different routes drawn

The app calculates the match rates of two different routes drawn using either an algorithm. If the match rate is more than 40%, the app will make a match between the driver and passenger.

### Ride history

The app keeps track of the user's ride history, providing a record of previous rides and helping users keep track of their transportation expenses.

### User ratings and reviews

After each ride, users can rate and review each other. This feature helps ensure the safety and reliability of the app by allowing users to provide feedback on their experience with other users.

## Future Development

While the app has really minimal features now, I plan to include more features in the future, some of them are listed below and you should feel free to make suggestions:

### In-app messaging

The app will include an in-app messaging system that allows drivers and passengers to communicate with each other before and during the ride. This feature enables users to discuss important details such as pickup and drop-off locations, the cost of the ride, and any other special requests.

### Payment integration

The app will integrate with popular payment systems such as PayPal and Venmo, allowing drivers to easily receive payment from passengers for their services.

### Driver background checks

To ensure the safety and security of our users, we plan to implement driver background checks in future versions of the app.

### Social media integration

In future versions of the app, we plan to add social media integration, allowing users to sign up and log in using their social media accounts.

### Improved user interface

I plan to improve the user interface of the app in future versions, making it more intuitive and user-friendly.

## Tech Stack (Dependencies)

The tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **Django ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice (Feel free to use any database)
 * **Python3** and **Django** as our server language and server framework
You can download and install the dependencies mentioned above using `pip` as:
```
pip install virtualenv
pip install django
```

## Development Setup
1. **Download the project starter code locally**
```
git clone https://github.com/horpeazy/corider.git
cd corider
```

2. **Create an empty repository in your Github account online. To change the remote repository path in your local repository, use the commands below:**
```
git remote -v 
git remote remove origin 
git remote add origin <https://github.com/<USERNAME>/<REPO_NAME>.git>
git branch -M master
```
Once you have finished editing your code, you can push the local repository to your Github account using the following commands.
```
git add . --all   
git commit -m "your comment"
git push -u origin master
```

3. **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

4. **Install the dependencies:**
```
pip install -r requirements.txt
```
5. **Run the development server:**
```
python3 manage.py runserver
```

6. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:8000/](http://127.0.0.1:8000/) or [http://localhost:8000](http://localhost:8000) 


## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.
## Credits

This project was developed by Hope Iyamu

## License

This project is licensed under the MIT License.
