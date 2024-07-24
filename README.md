# Community Marketplace

Community Marketplace is a Python-based desktop application that facilitates local buying, selling, and exchanging of goods within a community. Built using the Tkinter library for the GUI and SQLite for the database, this application aims to provide an easy-to-use platform for users to register, log in, and manage their listings.

## Features

- **User Registration and Login**: Secure user registration with unique usernames and login functionality.
- **Item Management**: Users can add items for sale, view all items, and search for specific items.
- **Messaging System**: Send and receive messages related to specific items between users.
- **Data Persistence**: Uses SQLite for storing user, item, and message data, ensuring data persistence across sessions.
- **Error Handling**: Robust error handling for database operations, including unique constraint violations and database locking issues.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/community-marketplace.git
    cd community-marketplace
    ```

2. **Install dependencies**:
    Make sure you have Python 3 installed. Install the required dependencies using pip:
    ```sh
    pip install tk
    ```

3. **Run the application**:
    ```sh
    python community_marketplace.py
    ```

## Usage

1. **Register a new user**:
    - Click on the "Register" button.
    - Fill in the username, password, and contact information.
    - Click "Register" to create a new user.

2. **Log in with an existing user**:
    - Click on the "Login" button.
    - Enter the username and password.
    - Click "Login" to access the main application window.

3. **Add a new item**:
    - Click on "Add Item" after logging in.
    - Enter the item details including name, category, price, and description.
    - Click "Add" to add the item to the marketplace.

4. **View all items**:
    - Click on "View Items" to see all items available in the marketplace.

5. **Search for items**:
    - Click on "Search Items".
    - Enter a keyword to search by item name, category, or description.
    - Click "Search" to see the results.

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests for any features or bug fixes you implement. Ensure that your code adheres to the existing coding conventions and passes all tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- [SQLite](https://www.sqlite.org/) - Lightweight database engine.
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Standard GUI toolkit for Python.

## Contact

For any questions or feedback, please open an issue on GitHub or contact me at (atharv.bzn@gmail.com).
