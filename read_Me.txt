Ideas/Planning
- Have a main class
    - Take damage, heal, attack 1/2/3, move
- Have it so that you begin by chosing a character/class
- Randomly generate an enemy from a pool of enemies (cannot fight the same creature the player is)
- Turn based attack system, player attacks enemy attacks
    - There is a basic attack with cooldown 0, then 2 special attacks (likely a rampage + status applier) with the special attacks having cooldowns
    - Have the enemy "AI" attack by calculating which attack that is off cooldown that it can use
        - Might need to change this system a bit to implement factors such as heal
            - When below health threshold, heal if off cooldown else attack?
    - Attack order dependendent on character speed stat
    - Ability to switch between characters? I.e. JWA --> if have time adds depth
- Long term progression/score
    - Levels? 3 random trash mobs then a boss mob, highest level achieved is recorded as highscore
    - After boss mob, can upgrade health/speed/damage
- Graphics/animations
    - Idle animations --> shifting image up and down, refer to classic pokemon
    - Attack animations --> to make this easy anime style, i.e. 3 images in succession to create an attack animations
- Sound/visual ques
    - KO noise, attack noise, take damage noise

Other little criteria:
- Collision detection
    - Can use mouse to click ability buttons, or hotkey
    - There is no other real use of collision detection
- Method overriding
    - Simple implementation lies in overiding attack abilities
- Inheritance hierachy / OOP
    - Program with classes
        - Specifically have a basic framework class then go from There
- Encapsulation
    - information hiding between classes? not really nescarry but guess I'll add it
- Polymorphism
    - This is just method overriding, see above
- Abstraction? In marking criteria but not in textbook reference

Other ideas:
- Can chose to play a mutiplayer version
    - I.e. you take a turn, someone else does. Hotseat style