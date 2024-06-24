#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import exists

def replace_line(file_dir, line_num, text):
    global glo_replacements_done

    if file_dir.startswith(game_dir) == False:
        errors += 1
        print("SECURITY ERROR! Function is trying to access file outside of Scarlet Hollow.")
    elif file_dir.startswith(os.path.join(game_dir,"mods")):
        errors += 1
        print("SECURITY ERROR! Function is trying to access file inside the mods folder.")
    else:
        lines = open(file_dir, 'r', encoding='utf-8').readlines()
        lines[line_num] = text
        out = open(file_dir, 'w', encoding='utf-8')
        out.writelines(lines)
        out.close()
        
        print("Replace Line done on line "+str(line_num)+".")
        glo_replacements_done += 1

# writes glo_lines to file
def write_glo_lines(file_dir):
    out = open(file_dir, 'w', encoding='utf-8')
    out.writelines(glo_lines)
    out.close()
    
    print("Wrote glo_lines to file.")

# Updates global variable "glo_lines" which is a list of all lines within the current file we're working with.
def glo_lines_update(file_dir):
    global glo_lines, errors
    
    try:
        glo_lines = open(file_dir, 'r', encoding='utf-8').readlines()
    except:
        errors += 1
        print("ERROR! glo_lines for file_dir ("+str(file_dir)+") could not be updated. This is likely a file-not-found error.")

# Returns True if the given line can be found in the file, returns False if not.
def line_in_file(file_dir, line):
    global errors
    
    if file_dir.startswith(game_dir) == False:
        errors += 1
        print("SECURITY ERROR! Function is trying to access file outside of Scarlet Hollow.")
    else:
        loc_lines = open(file_dir, 'r', encoding='utf-8').readlines()

        # Tries locating the index of the line.
        try:
            index = loc_lines.index(line)
        # If we get a ValueError, that means the line isn't there. Return False.
        except ValueError:
            return False
        # If we get any other kind of error, something's gone wrong.
        except:
            errors += 1
            print("LINE-IN-FILE ERROR!")
        # If we get no errors, then the line was able to be indexed, thus meaning that the line is in the file. Return True.
        else:
            return True

# Mode A: Returns True if the given string is found anywhere in the given file.
# Mode B: Returns the index of the first line found containing the string.
# Mode C: Returns a list of indexes of lines in which the string is found.
def string_in_file(file_dir, string, sif_mode="A"):
    if file_dir.startswith(game_dir) == False:
        errors += 1
        print("SECURITY ERROR! Function is trying to access file outside of Scarlet Hollow.")
    else:
        loc_lines = open(file_dir, 'r', encoding='utf-8').readlines()
        
        if sif_mode == "A":
            for line in loc_lines:
                if string in line:
                    return True
            else:
                return False
        elif sif_mode == "B":
            for i in range(len(loc_lines)):
                if string in loc_lines[i]:
                    return i
            else:
                return False
        elif sif_mode == "C":
            index_list = []
        
            for i in range(len(loc_lines)):
                if string in loc_lines[i]:
                    index_list.append(i)
            
            return tuple(index_list)
        elif sif_mode == "Cc":
            index_list = []
        
            for i in range(len(loc_lines)):
                if string.lower() in loc_lines[i].lower():
                    index_list.append(i)
            
            return tuple(index_list)
        else:
            errors += 1
            print("sif error")

# Returns the number of 'tabs' a string starts with.
def number_of_tabs(string):
    count = 1
    
    while True:
        if string.startswith("    "*count):
            count += 1
            continue
        else:
            return count-1

# String cleanup function
def string_defancy(x):
    return x.replace("…","...").replace("“","\"").replace("”","\"").replace("‘","'").replace("’","'").replace("•  ","• ")

# This function takes a file directory, a line to search for, and a line to replace it with if found.
# It will only replace the FIRST such line it finds, though of course on subsequent runs of this program, it will get the other ones.
# For this and other reasons, far_line_string is recommended over this function in most cases.
def far_line_file(file_dir, old, new):
    global errors, glo_replacements_done
    
    if file_dir.startswith(game_dir) == False:
        errors += 1
        print("SECURITY ERROR! Function is trying to access file outside of Scarlet Hollow.")
    elif file_dir.startswith(os.path.join(game_dir,"mods")):
        errors += 1
        print("SECURITY ERROR! Function is trying to access file inside the mods folder.")
    elif (not type(old) is str) or (not type(new) is str):
        errors += 1
        print("F&R LINE ERROR! Only strings may be supplied as 'old' or 'new'.")
    else:
        loc_lines = open(file_dir, 'r', encoding='utf-8').readlines()
        
        # Try finding the index of the old line.
        try:
            try:
                old_index = loc_lines.index(old)
            except:
                old_index = loc_lines.index(string_defancy(old))
            replace_line(file_dir, old_index, new)
            print("F&R line patching successful.")
            
            glo_replacements_done += 1
        # Old line could not be indexed (does not exist)
        except ValueError:
            # Try to find the new line.
            try:
                # split the "new" string into just the first actual line, otherwise subsequent searches will never find it
                new_index = loc_lines.index(new.split("\n")[0]+"\n")
                print("F&R line patch skipped.")
            # New line couldn't be indexed (does not exist)
            except ValueError:
                errors += 1
                print("F&R LINE ERROR! Neither old nor new string found.")
            # Some other error occurred.
            except:
                errors += 1
                print("F&R LINE ERROR! Unknown what exactly went wrong:N.")
        # Some other error occurred.
        except:
            errors += 1
            print("F&R LINE ERROR! Unknown what exactly went wrong:O.")

# Returns True if every element in an array is a string. Returns False otherwise.
def all_strings(array):
    for x in array:
        if type(x) is not str:
            return False
    else:
        return True
        
# Returns True if any element of the entered list is present within string
def any_string_in(finds, string):
    if type(finds) is str:
        finds = (finds,)
        
    for x in finds:
        if x in string:
            return True
    else:
        return False

# Works pretty much exactly as F&R in a text editor would work. Very versatile and simple. Use this over far_line_file in most cases.
# You can also supply lists to find and replace to have the function do all the pairs in one go. This should be faster?
def far_string_file(file_dir, find, replace, far_mode = "u", line_must_also_have=False, line_must_not_have=False, prior_line_must_have=False, subsequent_line_must_have=False):
    global errors, glo_replacements_done
    
    # Mode codes:
    # e - "easy" mode, function doesn't throw an error if neither find nor replace are found.
    # c - not case-sensitive (i will implement this if I ever need it)
    # l - the length of each pair of find and replace must be the same
    # u - undefined
    
    if file_dir.startswith(game_dir) == False:
        errors += 1
        print("SECURITY ERROR! Function is trying to access file outside of Scarlet Hollow.")
    elif file_dir.startswith(os.path.join(game_dir,"mods")):
        errors += 1
        print("SECURITY ERROR! Function is trying to access file inside the mods folder.")
    elif type(find) != type(replace):
        errors += 1
        print("F&R STRING ERROR! Find and replace are not the same type.")
    elif find == replace:
        errors += 1
        print("F&R STRING ERROR! Find and replace are the same.")
    elif type(find) not in (list, tuple, str) or type(replace) not in (list, tuple, str) or (type(line_must_not_have) not in (list, tuple, str) and line_must_not_have != False):
        errors += 1
        print("F&R STRING ERROR! Only supply strings or lists/tuples containing strings to this function.")
    elif (type(find) in (list,tuple) and all_strings(find) == False) or (type(replace) in (list,tuple) and all_strings(replace) == False) or (type(line_must_not_have) in (list,tuple) and all_strings(line_must_not_have) == False):
        errors += 1
        print("F&R STRING ERROR! Only supply strings or lists/tuples containing strings to this function.")
    elif type(find) in (list,tuple) and type(replace) in (list,tuple) and len(find) != len(replace):
        errors += 1
        print("F&R STRING ERROR! Find and replace are lists/tuples but not the same length.")
    elif type(line_must_also_have) is not str and line_must_also_have != False:
        errors += 1
        print("F&R STRING ERROR! 'line_must_also_have' should be str or False, not " + str(type(line_must_also_have)))
    else:
        replacements_done = 0
        
        loc_lines = open(file_dir, 'r', encoding='utf-8').readlines()
        
        try:
            # places these in tuples so we don't have to have two copies of the code for the single & multiple case
            if type(find) is str and type(replace) is str:
                find = (find,)
                replace = (replace,)
            
            # Iterate through each pair of Fs and Rs
            for index_farput in range(len(find)):
                # Throw an error if the two strings are the same.
                if find[index_farput] == replace[index_farput]:
                    errors += 1
                    print("F&R STRING ERROR! Find and replace are the same.")
                # If mode "l", we test to make sure the strings are the same length.
                elif "l" in far_mode and len(find[index_farput]) != len(replace[index_farput]):
                    errors += 1
                    print("F&R STRING ERROR! In mode 'l' but pair i" + str(index_farput) + " of find and replace are not equal length.")
                # I mean, this is just silly.
                elif find[index_farput] == line_must_not_have or (type(line_must_not_have) in (list,tuple) and find[index_farput] in line_must_not_have):
                    errors += 1
                    print("F&R STRING ERROR! Find is/is in line_must_not_have.")
                else:
                    # Also dumb. In here because this doesn't mean we need to skip.
                    if find[index_farput] == line_must_also_have:
                        errors += 1
                        print("F&R STRING ERROR! Find and line_must_also_have are the same; this is redundant.")
                
                    # Iterate through each line in the file
                    for i in range(len(loc_lines)):
                        # For each line, we check if find can be found in it. If so, replace the matched line with a replacement via far_string.
                        if find[index_farput] in loc_lines[i]:
                            # If LMAH is set, check if the LMAH is in the line. If not, pass.
                            if line_must_also_have != False and line_must_also_have not in loc_lines[i]:
                                pass
                            # Check if the prior line has what's needed
                            elif prior_line_must_have != False and prior_line_must_have not in loc_lines[i-1]:
                                pass
                            # Check if the next line has what's needed
                            elif subsequent_line_must_have != False and subsequent_line_must_have not in loc_lines[i+1]:
                                pass
                            # Do this check last since it has the potential to be the slowest. If LMNH is set, check if any of the LMNHs are in the line. If so, pass.
                            elif line_must_not_have != False and any_string_in(line_must_not_have, loc_lines[i]):
                                pass
                            # Finally, we construct the replacement line and write it to loc_lines. loc_lines itself will be written to the file at the end of this, rather than once for each line.
                            else:
                                loc_lines[i] = far_string(loc_lines[i], find[index_farput], replace[index_farput], far_mode=far_mode)
                                replacements_done += 1
                                glo_replacements_done += 1
                                #print("glo_replacements_done is: " + str(glo_replacements_done))
            
            # If more than 0 replacements have been done, write our result, report success, & how many.
            if replacements_done > 0:
                try:
                    out = open(file_dir, 'w', encoding='utf-8')
                    out.writelines(loc_lines)
                    out.close()
                    
                    if replacements_done == 1:
                        print("F&R str successfully made 1 replacement.")
                    else:
                        print("F&R str successfully made " + str(replacements_done) + " replacements.")
                except:
                    errors += 1
                    print("F&R STR ERROR! Error while writing to file.")
            # If 'easy', just move on.
            elif "e" in far_mode:
                pass
            # Otherwise, we test to see if there are any matches for the replace.
            else:
                # Iterate through each replace
                for index_farput in range(len(replace)):
                    replacements_found = 0
                    
                    # Iterate through each line of the file, looking for the replace. Break after finding a single one.
                    for i in range(len(loc_lines)):
                        if replace[index_farput] in loc_lines[i]:
                            replacements_found += 1
                            break
                
                    # If we find a match, we know we can safely skip.
                    if replacements_found > 0:
                        print("F&R str patch skipped.")
                    # Otherwise, this means that neither the old nor the new string could be found. Throw an error.
                    else:
                        errors += 1
                        print("F&R STR ERROR! Neither old nor new string found. Index: "+str(index_farput))
        except:
            errors += 1
            print("F&R STR ERROR! Unknown what exactly went wrong.")

# Finds and replaces all instances of a substring within a string. Works like a standard F&R.
def far_string(string, find, replace, far_mode = "u"):
    if find in string:
        return string.replace(find,replace)
    else:
        print("Skipping string F&R; find could not be found in string.")
        return string
    
# Inserts "$ forced_short = True" after the inputted line, with proper indentation.
def insert_forced_short(file_dir,string):
    global errors, glo_replacements_done

    if file_dir.startswith(game_dir) == False:
        errors += 1
        print("SECURITY ERROR! Function is trying to access file outside of Scarlet Hollow.")
    elif file_dir.startswith(os.path.join(game_dir,"mods")):
        errors += 1
        print("SECURITY ERROR! Function is trying to access file inside the mods folder.")
    else:
        loc_lines = open(file_dir, 'r', encoding='utf-8').readlines()

        # We must work bottom to top to ensure that the line numbers don't change mid-iteration.
        idx_tup = string_in_file(file_dir, string, sif_mode="C")
        idx_list = list(idx_tup)
        idx_list.sort(reverse=True)
        
        print(idx_list)

        if idx_list == []:
            errors += 1
            print("IFS ERROR! Couldn't find line.")
        else:
            for i in idx_list:
                if "forced_short" in loc_lines[i+1]:
                    print("Skipping IFS.")
                else:
                    replace_line(file_dir,i,loc_lines[i]+("    "*number_of_tabs(loc_lines[i]))+"$ forced_short = True\n")

def load_patch(mod_name, patch_dir):
    global mods, errors, unidec_errors, glo_replacements_done, glo_lines

    # "The infamous (and unsafe) exec command: Insecure, hacky, usually the wrong answer. Avoid where possible."
    # ...Well, import doesn't work........

    if exists(os.path.join(game_dir, "mods", patch_dir)):
        mods += 1
        print("_"*10 + "<" + mod_name + ">" + "_"*(longest_mod_len-len(mod_name)+10))
        print(mod_name + " detected. Attempting to load " + mod_name + " patch file...")
        
        #print("Checksum is: " + str(gen_checksum(patch_dir)))
        
        import traceback
        
        try:
            exec(open(os.path.join(game_dir, "mods", patch_dir), encoding='utf-8').read())
        except Exception:
            errors += 1
            print("ERROR! " + mod_name + " patch file could not be loaded, or there was an error while running its code! Traceback is as follows:")
            traceback.print_exc()
        
        print("Done performing " + mod_name + " patches.")
        print("_"*10 + "</" + mod_name + ">" + "_"*(longest_mod_len-len(mod_name)+9))

def attempting_to_patch(dir):
    print("Attempting to patch " + os.path.split(dir)[1] + " ...")

def patching_unsuccessful():
    global errors

    errors += 1
    print("ERROR! Patching unsuccessful.")
    #traceback.print_exc()

# just testing this out for fun/kind of security? this is most likely very unsafe but I just don't like the idea of this thing blindly yknow what as I'm writing this I'm realizing how stupid it would be for every time a mod updates their patcher they have to update me on what the checksum is this isn't even a checksum scrap it
def gen_checksum(dir):
    loc_lines = open(dir, 'r', encoding='utf-8').readlines()
    
    checksum = 0
    
    for line in loc_lines:
        for char in line:
            try:
                checksum += ord(char)
            except:
                checksum += 0
            
    return checksum
    
def pad_string(string, des_len, spacer_char=" "):
    dif = des_len - len(string)
    
    if dif <= 0:
        return string
    elif dif % 2 == 0:
        return spacer_char*int(dif/2) + string + spacer_char*int(dif/2)
    else:
        return spacer_char*int(dif/2) + string + spacer_char*(int(dif/2)+1)
    
def register_mod(name,patch_dir):
    global all_mod_names, all_mod_patch_dirs
    
    all_mod_names.append(name)
    all_mod_patch_dirs.append(patch_dir)
    
### Beginning ###

errors = 0
glo_replacements_done = 0

path_not_found = False
path_finding_exception = False

end_input = "null input"

bs_fance = "\\"*20
fs_fance = "/"*20
space_fance = "*"*40

print(fs_fance + space_fance + bs_fance + "\n" + bs_fance + pad_string("SCARLET HOLLOW PATCHER LAUNCHED!",40) + fs_fance + "\n" + bs_fance + pad_string("Created by Omega Fallon.",40) + fs_fance + "\n" + fs_fance + space_fance + bs_fance)

try:
    from inspect import getsourcefile
    from os.path import abspath

    patcher_dir = abspath(getsourcefile(lambda:0))
    
    import os.path
    
    parent_folder_path = os.path.dirname(patcher_dir)
    gparent_folder_path = os.path.dirname(os.path.dirname(patcher_dir))
    
    parent_folder_name = os.path.split(parent_folder_path)[1]
    gparent_folder_name = os.path.split(gparent_folder_path)[1]
    
    print("parent_folder_name is: "+parent_folder_name)
    print("gparent_folder_name is: "+gparent_folder_name)
    
    if parent_folder_name == "mods" and gparent_folder_name == "game":
        game_dir = gparent_folder_path
    else:
        path_not_found = True
except:
    path_not_found = True
    path_finding_exception = True

if path_not_found:
    if path_finding_exception:
        print("ERROR! Something went wrong while trying to locate game files.")
    elif parent_folder_name == "mods" and (gparent_folder_name == "Scarlet Hollow" or gparent_folder_name == "ScarletHollow"):
        print("ERROR! Your 'mods' folder is placed directly inside your Scarlet Hollow directory. It should be inside the 'game' folder.")
    else:
        print("ERROR! Patcher was not able to locate game files. Make sure this patcher is in your mods folder, and that your mods folder is in your game folder!")
        
    end_input = input("\nIf you would like to try patching anyways, type and enter \"y\". This will probably not work.")

    if end_input == "y":
        game_dir = gparent_folder_path
elif path_not_found == False or end_input == "y":
    print("Your game folder directory is: " + game_dir)
    
    print("-"*80)
    
    if end_input != "y":
        print("PLEASE NOTE: This patcher functions by automatically running fragments of Python code that come with each mod. This patcher runs said code blindly. As such, you should ONLY run this patcher if you fully trust the mods which you have installed. Be wary of the potential for seriously harmful code to be disguised as mods.")
        
        end_input = input("\nType and enter \"y\" to continue.")
        
        if end_input != "y":
            exit()
    
        print("-"*80)
    
    print("Beginning patching. Checking for mods...")
    
    mods = 0
    
    all_mod_names = []
    all_mod_patch_dirs = []
    
    try:
        # Registers each mod to be detected.
        register_mod("!mod_hub","!mod_hub/mod_hub.py-frag")
        register_mod("Petty Fixes","Petty Fixes/petty_fixes.py-frag")
        register_mod("Serious Mode","Serious Mode/sm_patches.py-frag")
        register_mod("Flirt with Frou-Frou","Flirt with Frou-Frou/fwff_patches.py-frag")
        register_mod("Frou-frou Guillemets","Frou-frou Guillemets/ffg_patches.py-frag")
        register_mod("A Mod That Allows You To Say You're An OnlyFans Streamer","A Mod That Allows You To Say You're An OnlyFans Streamer/of_patches.py-frag")
        register_mod("Factual Order","Factual Order/FA_patches.py-frag")
        
        present_mods = []
        
        # Determines which mods are currently installed
        for i in range(len(all_mod_patch_dirs)):
            if exists(os.path.join(game_dir, "mods", all_mod_patch_dirs[i])):
                present_mods.append(all_mod_names[i])
        
        # Below code determines the length of the name of the longest installed mod. Calculated prior to loading any mods and is used for GUI
        longest_mod_len = 0
        
        for x in present_mods:
            if len(x) > longest_mod_len:
                longest_mod_len = len(x)
    except:
        errors += 1
        print("ERROR while registering mods.")
    else:
        print("Successfully registered all mods.")
    
    try:
        # Attempts to load each mod, if present, in sequence.
        for i in range(len(all_mod_patch_dirs)):
            load_patch(all_mod_names[i],all_mod_patch_dirs[i])

        # Runs a final pass of Petty Fixes if the other mods have made changes.
        try:
            if glo_replacements_done > 0:
                load_patch("Petty Fixes","Petty Fixes/petty_fixes.py-frag")
        except:
            errors += 1
            print("PF reload ERROR!")
    except:
        errors += 1
        print("ERROR while loading mods.")

    print("-"*80)

    if exists(os.path.join(game_dir, "mods", "!mod_hub/mod_hub.py-frag")) == False:
        print("NOTICE! Mod_hub not present. This is a base mod that is required for many other mods to function.")
    
    if errors > 0:
        if errors == 1:
            print("NOTICE! An error was encountered while patching.")
        else:
            print("NOTICE! "+str(errors)+" errors were encountered while patching.")
        
        ## TROUBLESHOOTING RECOMMENDATIONS
        
        # mods -> game
        if parent_folder_name == "mods" and gparent_folder_name == "game":
            pass
        else:
            print("Please ensure that this patcher is in your mods folder and that your mods folder is in your game folder.")
        
        # version
        print("Please ensure that you are running this PY file on the most up-to-date version of Python available.")
        
        ## Final
        end_input = input("If issues persist, contact OmegaFallon.")
    elif mods == 0:
        end_input = input("Patcher was not able to detect any mods with patcher files. As such, nothing was patched.")
    else:
        end_input = input("All patches performed successfully! My work here is done. Feel free to close the window and launch Scarlet Hollow!")