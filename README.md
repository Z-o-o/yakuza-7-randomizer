# Yakuza: Like a Dragon Enemy Randomizer
A modification for Yakuza: Like A Dragon (A.K.A Yakuza 7) that randomizes enemies and scales them accordingly throughout the game.

# A Warning on Stability:
This version (0.1.0) is still quite buggy and not every enemy has been tested to see where they break the game.
If your game crashes, softlocks, etc. when trying to fight a specific enemy, then my best suggestion would be to 1st regenerate
your enemies, then let me know on either the Yakuza Modding Discord Mod-Feedback or leave a reply on the mod page
detailing what enemy you were trying to fight, and if possible inlcude your modified db.yazawa.en.par file.

# How to use:
 ## Step 1:
  
  Download the Randomizer.exe file. You will also require whatever tools necessary to unpackage and repackage the par folder
  back into their .par files (most likely you will use Partool). 

Link for Partool: https://github.com/Kaplas80/ParManager/releases/tag/v1.3.3
  
 ## Step 2:
  
  One downloaded, locate the db.yazawa.en.par file in your Yakuza: Like A Dragon files. This location will change depending on 
  where you installed it, assuming you are using Steam then opening the game properties and go to your Local Files for YLAD.
  Use Partool to unpack this .par file (If on Windows this can be easily done by right-clicking the file and selecting:

    Partool --> Extract to 'db.yazawa.en.par.unpack\' (On Windows)
  This will generate a folder of the unpacked par file, move this folder
  to another location outside of your YLAD local files. I'd recommend not deleting this unpack folder so you can easily randomize
  your enemies again in the future

 ## Step 3:
  
  Once the .par file has been unpackaged, run Randomizer.exe and this will generate a character_npc_soldier_personal_data.bin file.
  Drag this file into your unpacked par's en folder.
  
  NOTE: The unpacked par folder is structured like so:
    
    db.yazawa.en.par.unpack > en > (Every .bin file, drag the generated bin file into here)
    
  If prompted by your system, ensure that you are replacing the existing file, if you don't you won't randomize your enemies.

## Step 4:

  Now that your db.yazawa.en.par.unpack is randomized, use the same method to pack your folder 
  
    Right click Partool --> Repack in 'db.yazawa.en.par' (On Windows)
  
  Once Partool is finished running, drag this .par file into your YLAD files, replacing the existing file.
 
 ## Step 5:
  You have now successfully randomized your enemies in Yakuza: Like A Dragon. Nothing else is required and enjoy! If you'd like to randomize them again follow this same process starting from Step 2. If you did keep your unpacked par folder then its just as easy as running Randomizer.exe again and placing it into your unpacked par folder, repack, then replace the .par file in your YLAD files.
