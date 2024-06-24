label mod_hub:

if renpy.exists("mods/!mod_hub/mod_hub.rpy") == False:
    "NOTICE: 'mod_hub.rpy' is not installed in the correct directory. The '!mod_hub' folder should be placed directly into your 'mods' folder."

# if renpy.exists("mods/Serious Mode/sm_patches.py"):
    # menu:
        # "Play in Serious Mode? This will remove inappropriately humorous dialogue options during serious scenes."
    
        # "{i}• Yes.{/i}":
            # $ serious_mode = True
            
        # "{i}• No. (Vanilla game){/i}":
            # default serious_mode = False
            # $ serious_mode = False

menu:
    "MOD HUB: Select a mod!"
    
    "{i}• Play the vanilla game.{/i}":
        jump bus_start
    
    "{i}• Play ''Factual Order''{/i}" if renpy.exists("mods/Factual Order/Factual_Order.rpy"):
        jump factual_order