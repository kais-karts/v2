# TODO list for game logic

### Map
 - Figure out internal map / conversion to indices
 - Implement item pick ups

### Sending location
 - Send location via comms every milisecond?

### Items
 - Ability to use item (connect to button using gpio)

### General Flow
Need to have 3 threads:
- Reading packets and executing
- Sending location packet
- Checking if kart passed an item checkpoint
- One temp thread for speed control

