# websockets/tracker.py
import logging

logger = logging.getLogger(__name__)

class UserTracker():
    """User tracker is used to track the number of connected users and thier names"""
    def __init__(self):
        """Initialize an instance of a user tracker"""
        self.users = []
        self.num_users = 0
        self.user_index = None
    
    def add_user(self, user):
        """Function to add a user's name and increment the user count"""
        player = {
            "player": user ,
            "active": False
        }
        self.users.append(player)
        self.user_index = dict((p['player'], i) for i,p  in enumerate(self.users))
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
    
    def make_player_active(self, player):
        """Function to make a player active"""
        player_index = self.user_index.get(player)
        self.users[player_index]['active'] = True
    
    def make_player_inactive(self, player):
        """Function to make a player inactive"""
        player_index = self.user_index.get(player)
        self.users[player_index]['active'] = False

    def get_active_player(self):
        active = next(filter(lambda d: d.get("active") == True, self.users), None)
        return active['player']