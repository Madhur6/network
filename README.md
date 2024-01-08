# CS50 Network App
Welcome to the CS50 Network App! This Django app allows users to post, comment, follow other users, and customize their profiles.

## Features

- **Post and Comment:**
  - Users can create posts and comment on existing posts.
  
- **User Profiles:**
  - Each user has a profile where they can customize their information.
  
- **Follow and Unfollow:**
  - Users can follow and unfollow each other to see posts from the users they follow.

- **Like Posts and Comments:**
  - Users can like posts and comments to show appreciation.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/your-repository.git

2. **Navigate to the Project Directory:**
   ```bash
   cd your-repository

3. **Create a Virtual Environment:**
   ```bash
   python -m venv venv

4. **Activate the Virtual Environment:**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```


5. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

6. **Run Migrations:**
   ```bash
   python manage.py makemigrations network/app-name
   python manage.py migrate

7. **Run the Development Server:**
   ```bash
   python manage.py runserver

8. **Access the App:**
   Open your web browser and navigate to http://127.0.0.1:8000/.

## Folder Structure

- `network/`: Django app folder containing the main app logic.
- `templates/`: HTML templates for the app's pages.
- `static/`: Static files such as CSS styles.

## Usage

### Post and Comment:

- Visit the index page to create new posts and comment on existing ones.

### User Profiles:

- Explore user profiles by clicking on usernames.

### Follow and Unfollow:

- Follow and unfollow users to customize your feed.

### Like Posts and Comments:

- Like posts and comments to show your appreciation.


## Credits

- Project idea and starter code provided by CS50.

## Acknowledgments

I'd like to express my appreciation to the CS50 staff and community for their guidance and support during the development of this project.


## Contributing

Feel free to contribute to the development of this app! Fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License.
