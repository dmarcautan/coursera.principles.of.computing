"""
Cookie clicker Simulator.

@author: Dmitry Marcautsan
"""
import coursera.poc_clicker_provided as provided
import math
# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._current_cps = 1.0
        self._current_time  = 0.0
        self._current_cookies = 0.0
        self._total_cookies = 0.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return str({"Time": self._current_time, 
                "CPS": self._current_cps, 
                "Cookies": self._current_cookies, 
                "Total cookies": self._total_cookies })
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history[:]

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        return math.ceil(max((cookies - self._current_cookies), 0)/self._current_cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._current_time += time
            self._current_cookies += time * self._current_cps
            self._total_cookies += time * self._current_cps
        
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if not self.can_buy_item(cost):
            return
        
        self._current_cps += additional_cps
        self._current_cookies -= cost
        self._history.append((self._current_time, item_name, cost, self._total_cookies))
        
    def can_buy_item(self, cost):
        """
        Tells if you can afford to buy a an item with the cost provided
        """
        return cost <= self._current_cookies


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    sim_build_info = build_info.clone()
    sim_state = ClickerState()
    while duration > sim_state.get_time():
        click_item = strategy(sim_state.get_cookies(), 
                              sim_state.get_cps(), 
                              sim_state.get_history(), 
                              duration - sim_state.get_time(), 
                              sim_build_info)
        
        if click_item is None:
            sim_state.wait(duration - sim_state.get_time())
            break
        else:
            wait_time = min(sim_state.time_until(sim_build_info.get_cost(click_item)),
                             duration - sim_state.get_time())
            sim_state.wait(wait_time)
            
            while click_item is not None and sim_state.can_buy_item(sim_build_info.get_cost(click_item)):
                sim_state.buy_item(click_item, sim_build_info.get_cost(click_item), sim_build_info.get_cps(click_item))
                sim_build_info.update_item(click_item)
                click_item = strategy(sim_state.get_cookies(), 
                              sim_state.get_cps(), 
                              sim_state.get_history(), 
                              duration - sim_state.get_time(), 
                              sim_build_info)
                
    return sim_state

def sort_affordable(items, cookies, cps, time_left):
    """
    Filters out items that you cannot afford to buy and returnes as a sorted by cost list
    """
    return sorted(filter(lambda x: x[1] <= (cookies + cps*time_left), items), key=lambda x: x[1])

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor" if build_info.get_cost("Cursor") <= cookies + cps*time_left else None

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    upgrades = [(item, build_info.get_cost(item)) for item in build_info.build_items()]
    available = sort_affordable(upgrades, cookies, cps, time_left)
    return available[0][0] if len(available) > 0 else None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    upgrades = [(item, build_info.get_cost(item)) for item in build_info.build_items()]
    available = sort_affordable(upgrades, cookies, cps, time_left)
    return available[-1][0] if len(available) > 0 else None

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    upgrades = [(item, build_info.get_cost(item)/build_info.get_cps(item)) 
                for item in build_info.build_items() 
                if cookies + time_left * cps >= build_info.get_cost(item) * 2]
    return sorted(upgrades, key=lambda x: x[1])[0][0] if len(upgrades) > 0 else None