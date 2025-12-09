import requests
import os
import colorama
from colorama import Fore, Style
from itertools import chain
import warnings
from urllib3.exceptions import InsecureRequestWarning

# remone the fucking annoying ssl warning
warnings.simplefilter("ignore", InsecureRequestWarning)

# ask for class input
class_name = int(input("Enter class : "))
if class_name < 10:
    class_name = f"0{class_name}"
class_name = str(class_name)
# define variables
ppl = ""
num = ""
idk = ""
success_ppl = []
break_outer = False
break_all=False

url = f"https://super-ninenine.synology.me:9999/hshs2026/9{class_name}-{ppl}/9{class_name}{num}{idk}.jpg"   # URL with custom classes

downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")   # path to Downloads folder
save_folder = os.path.join(downloads_folder, str('9'+str(class_name)))

os.makedirs(save_folder, exist_ok=True)  #create folder if not exists

print(Fore.CYAN+"Trying to get ppl amount of the class... Please wait."+Style.RESET_ALL)

for i in range(25, 36):                # trying to find ppl amount from 25 to 35
    ppl = str(i)
    for num in range(1, 16):
        if num < 10:
            num_str = f"0{num}"
        else:
            num_str = f"{num}"
        num = num_str
        idk=""
        url = f"https://super-ninenine.synology.me:9999/hshs2026/9{class_name}-{ppl}/9{class_name}{num}{idk}.jpg" 
        response = requests.get(url, verify=False)
        
        if response.status_code == 200:  # if found ppl amount
            print("ppl amount found! ")
            print(Fore.GREEN + "ppl amount of class", str(class_name) + " is: " + ppl + "  /   response code:" + str(response.status_code) + Style.RESET_ALL)
            break_outer = True
            break
        elif response.status_code == 404: # if not found ppl amount
            idk="%20拷貝"
            url_fuck = f"https://super-ninenine.synology.me:9999/hshs2026/9{class_name}-{ppl}/9{class_name}{num}{idk}.jpg" 
            response = requests.get(url_fuck, verify=False)
            if response.status_code == 200:  # if found ppl amount with %20d拷貝
                print("ppl amount found with %20拷貝! num:{} \n link:{}".format(num, url))
                print(Fore.GREEN + "ppl amount of class", str(class_name) + " is: " + ppl + "  /   response code:" + str(response.status_code) + Style.RESET_ALL)
                break_outer=True
                break
    
    if break_outer:
        break
    elif i == 35:  # two situations: class doesn't exist or we're fucked up
        print(Fore.RED + "Sorry. We couldn't find this class or this class doesn't exsist."  + Style.RESET_ALL)
        exit()

# trying to get photos of ppl from 1 to 45 excluding 20-25

for i in chain(range(1, 20), range(26, 46)):
    if i < 10:                # make num string keep 2 digits
        num_str = f"0{i}"
    else:
        num_str = f"{i}"
    num = num_str 
    idk=""            # redefine {num} to be used in url
    url = f"https://super-ninenine.synology.me:9999/hshs2026/9{class_name}-{ppl}/9{class_name}{num}{idk}.jpg" 
    response = requests.get(url, verify=False)

    # print(f"Requesting: {url}")   # to make sure if the links work (for debugging)

    if response.status_code == 200:           # if found, save the photo
        output_path = os.path.join(save_folder, f"9{class_name}-{num_str}.jpg")
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(Fore.GREEN + f"✔ SAVED: {class_name}-{num_str}.jpg" + Style.RESET_ALL)
        success_ppl.append(num_str)
    
    elif response.status_code == 404:         # if not found, try with %20
        idk = "%20"
        url_with_idk = f"https://super-ninenine.synology.me:9999/hshs2026/9{class_name}-{ppl}/9{class_name}{num}{idk}.jpg"
        print(Fore.YELLOW + f"Retrying with %20" + Style.RESET_ALL)
        # print(f"Requesting: {url_with_idk}")   # to make sure if the links work (for debugging)
        response_retry = requests.get(url_with_idk, verify=False)
        
        if response_retry.status_code == 200: # if found with %20, save the photo
            output_path = os.path.join(save_folder, f"9{class_name}-{num_str}.jpg")
            with open(output_path, "wb") as f:
                f.write(response_retry.content)
            print(Fore.GREEN + f"✔ SAVED (retry): {class_name}-{num_str}.jpg" + Style.RESET_ALL)
            success_ppl.append(num_str)
        
        else:
            print(Fore.RED + f"Trying with %20拷貝" + Style.RESET_ALL)
            # print(Fore.LIGHTYELLOW_EX + url + Style.RESET_ALL) #for debugging
            idk="%20拷貝"
            url_with_idk_copy = f"https://super-ninenine.synology.me:9999/hshs2026/9{class_name}-{ppl}/9{class_name}{num}{idk}.jpg"
            response = requests.get(url_with_idk_copy, verify=False)
            if response.status_code == 200: # if found with %20拷貝, save the photo
                output_path = os.path.join(save_folder, f"9{class_name}-{num_str}.jpg")
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(Fore.GREEN + f"✔ SAVED (retry 2): {class_name}-{num_str}.jpg" + Style.RESET_ALL)
                success_ppl.append(num_str)
            else:
                print(Fore.RED + f"✘ NOT FOUND: {class_name}-{num_str}.jpg" + Style.RESET_ALL)
    
    else:         # if it returns this, that means we're fucked up
        print(Fore.YELLOW + f"Unexpected status code {response.status_code} for {url}" + Style.RESET_ALL)

# Final report of successfully saved files
print(Fore.CYAN + "Successfully saved files:" + Style.RESET_ALL, success_ppl)