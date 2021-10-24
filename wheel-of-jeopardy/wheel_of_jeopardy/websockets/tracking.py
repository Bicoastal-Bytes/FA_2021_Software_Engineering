# websockets/tracker.py
class UserTracker():
    """User tracker is used to track the number of connected users and thier names"""
    def __init__(self):
        """Initialize an instance of a user tracker"""
        self.users = []
        self.num_users = 0
    
    def add_user(self, user):
        """Function to add a user's name and increment the user count"""
        player = {"player": user}
        self.users.append(player)
        self.num_users += 1
    
    def get_num_users(self):
        """Function to return the number of actively connected users to the instance"""
        return self.num_users

    def remove_user(self, user):
        """Function to remove a user's name and decrement the user count"""
        self.users.remove(user)
        self.num_users -= 1
    
    def get_connected_users(self):
        """Function to return the list of users connected to the game"""
        return self.users