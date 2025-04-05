""" Game Controller """

from p5 import *
import RPi.GPIO as GPIO

from comms import Packet, PacketQueue
from localization import current_location
from speed_ctrl import set_speed_multiplier

from constants import KART_ID, BUTTON_IN
from items import ITEMS, ItemTarget
from go_kart import GoKart
from map import Map
from race import Race

from components.api import API

# Global variables to track button state
button_pressed = False
last_button_state = None

class GameController:
    def __init__(self, map: Map, race: Race, ui: API, packet_queue: PacketQueue):
        self.map: Map = map
        self.race: Race = race
        self.ui: API = ui
        self.packet_queue: PacketQueue = packet_queue

    def check_button_press(self):
        """
        Check if the item button has been pressed.
        GPIO in production and keyboard in development.
        """
        global button_pressed, last_button_state
        
        # Try to use GPIO if available
        try:
            current_button_state = GPIO.input(BUTTON_IN)
            
            # Check for falling edge (1 -> 0, button press)
            if last_button_state == 1 and current_button_state == 0:
                button_pressed = True
                print("Button pressed (GPIO)")
            
            last_button_state = current_button_state
            
        except (NameError, RuntimeError):
            # Fall back to keyboard for development
            try:
                # Check for space key (common standard for 'use item')
                if key_is_pressed and key == ' ':
                    if not button_pressed:  # Avoid multiple triggers while held
                        button_pressed = True
                        print("Button pressed (Keyboard)")
            except NameError:
                # If even p5 key detection isn't available, we can't detect input
                pass

    def update(self):
        """
        Update the game logic
        """
        # Update game state from packets received from other go-karts
        for packet in self.packet_queue:
            match packet.tag:
                case Packet.PING: pass
                case Packet.LOCATION: self.race.update_ranking(packet)
                case Packet.ATTACK: self.race.apply_item(packet)
        
        # Update my location and broadcast to everyone else
        location_packet = Packet(Packet.LOCATION, kart_id=KART_ID, location=current_location())
        
        self.race.update_ranking(location_packet)
        self.packet_queue.send(location_packet)

        # Pickup item if kart near checkpoint
        self.race.local_pickup_item()
        
        # Update local kart state (effects)
        local_kart: GoKart = self.race.owned_kart
        local_kart.update_item_effect()
        
        # Check for button press
        self.check_button_press()
        
        # Use item if button was pressed
        if button_pressed:
            if local_kart._item_id is not None:
                local_kart.use_held_item()
            button_pressed = False  # Reset after handling

        # Handle pending attack if one exists
        if local_kart.pending_attack is not None:
            attack_packets = self.create_attack_packet(self.race.owned_kart.pending_attack)
            for attack_packet in attack_packets:
                self.packet_queue.send(attack_packet)
                print(f"Sent {ITEMS[attack_packet.data[1]].name} to kart {attack_packet.data[0]}")
            local_kart.pending_attack = None

        # Update the speed control for this go kart
        set_speed_multiplier(local_kart.speed_multiplier)

    def create_attack_packet(self, item_id):
        """
        Creates attack packets based on the item type and its targeting rules.
        
        Args:
            item_id (int): The identifier of the item being used for the attack
            
        Returns:
            list[Packet]: A list of attack packets ready to be sent through the packet queue.
        """
        item = ITEMS[item_id]
        target_type = item.target
        
        # Handle different targeting types
        target_kart_ids = []
        
        if target_type == ItemTarget.FRONT:
            # Find the kart directly in front of us
            my_rank = self.race.rankings.index(KART_ID)
            if my_rank > 0:  # Not in first place
                target_kart_ids = [self.race.rankings[my_rank - 1]]
        
        elif target_type == ItemTarget.BEHIND:
            # Find the kart directly behind us
            my_rank = self.race.rankings.index(KART_ID)
            if my_rank < len(self.race.rankings) - 1:  # Not in last place
                target_kart_ids = [self.race.rankings[my_rank + 1]]
        
        elif target_type == ItemTarget.ALL_OTHERS:
            # Target all karts except self
            target_kart_ids = [kart_id for kart_id in self.race.rankings if kart_id != KART_ID]
        
        elif target_type == ItemTarget.LEADER:
            # Target the leader (first place)
            if len(self.race.rankings) > 0 and self.race.rankings[0] != KART_ID:
                target_kart_ids = [self.race.rankings[0]]
        
        attack_packets = []
        # Create attack packets for all targets
        for target_id in target_kart_ids:
            attack_packet = Packet(Packet.ATTACK, data=(target_id, item_id))
            attack_packets.append(attack_packet)
        
        return attack_packets