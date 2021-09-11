import keyboard


while True:  # making a loop
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        print('You Pressed A Key!')
        break  # finishing the loop
        # print("No key")
        # break  # if user pressed a key other than the given key the loop will break

