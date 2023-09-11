from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#Thie file scrapes from https://dash.swarthmore.edu/ to output 
#Swarthmore buildings and hours into filtered_output.txt and output.txt

browser=webdriver.Chrome()

browser.get("https://dash.swarthmore.edu/")

time.sleep(2)
buildings = browser.find_elements(By.CLASS_NAME, "mt-3")
file1=open("output.txt","w+")


for building in buildings:
    file1.write(building.text)
file1.close()


output=open("output.txt","r")
filtered=open("filtered_output.txt","w")
previous_line=" "
for line in output:  
    if ((line.__contains__("Open") and line[0]=="O") or line.__contains__("Closed")) and not line.__contains__("lax") and not line.__contains__("Icon"):
        if not previous_line.__contains__("Icon") and not previous_line.__contains__("day") and not previous_line.__contains__("Z"):
            filtered.write(previous_line)
            filtered.write(line)      
    previous_line=line        
filtered.close()
output.close()
browser.close()

