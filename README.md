# Yakuza: Like a Dragon Enemy Randomizer
A modification for Yakuza: Like A Dragon (A.K.A Yakuza 7) that randomizes enemy appearances throughout the game.

# A Warning on Balance:
This version (0.1.0) is still quite buggy and not every enemy has been tested to see where they break the game.
If your game crashes when trying to fight a specific enemy, then my best suggestion would be to 1st regenerate
your enemies, then let me know on either the Yakuza Modding Discord Mod-Feedback or leave a reply on the mod page
detailing what enemy you were trying to fight, and if possible inlcude your modified db.yazawa.en.par file.

# How to use:
 ## Step 1:
  
  Download the Randomizer.py file. You will also require whatever tools necessary to package json files back into their
  .bin and .par files (most likely reARMP and Partool respectively). 

Link for Partool: https://github.com/Kaplas80/ParManager/releases/tag/v1.3.3

Link for reARMP: https://github.com/Ret-HZ/reARMP/releases/tag/v0.11.2
  
 ## Step 2:
  
  One downloaded, locate the db.yazawa.en.par file in your Yakuza: Like A Dragon files. This location will change depending on 
  where you installed it, assuming you are using Steam then opening the game properties and go to your Local Files for YLAD.
  Use Partool to unpack this .par file
 
 ## Step 3:
  
  Once the .par file has been unpackaged, locate the character_npc_soldier_personal_data.bin file. This contains a list of every
  enemy in the game and their description. Utilize reARMP to unpack this into its JSON component.
 
 ## Step 4:
  
  Drag and drop the .json file into the Randomizer.py program. This will popup with a window to watch the progress of the randomization
  This process may take a few minutes, be patient as the JSON file is quite big and will take a while to process on slower machines. If
  the program takes longer than 10 minutes to run, then most likely their has been an error and reaching out to me would be helpful
 
 ## Step 5:
  
  Once the program has finished execution, it will wait for you to close the window. You will notice that a new file character_npc_soldier_personal_data.json
  has been generated. The process is now very similar to Steps 2-3 but reversed. Drag the generated JSON file into reARMP to repackage it
  into a .bin file. Once repackaged the file will have to be renamed "character_npc_soldier_personal_data.bin".
 
 ## Step 6:
  
  Once renamed, drag this file into your db.yazawa.en.par.unpack that was generated in Step 2. Replace the existing file if prompted by your machine.
  Once replaced repack the unpacked par file utilizing Partool.
 
 ## Step 7:
  
  Now that you have a randomized db.yazawa.en.par file, you will need to drag this file into the same location you found the orignal one and replace
  the old .par file.
 
 ## Step 8:
  You have now successfully randomized your enemies in Yakuza: Like A Dragon. Nothing else is required and enjoy! If you'd like to randomize them again
  follow this same process starting from Step 2. I hope to make this process much easier in the near future.
