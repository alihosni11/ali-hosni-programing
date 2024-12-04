
# the following function conveys a decoded message using the lsb of every pixel

def image_hidden_message_encoding(image, hidden_message ):
    
    output_file = image.replace(".bmp", "encrypted.bmp")
    
    binary_version_of_hidden_message = ""
    
    #im looping through each character the user has inputed and converting it in to an 8 bit binary representation
    for character in hidden_message:
        binary_version_of_hidden_message += f"{ord(character):08b}"
        
    hidden_message_length = len(binary_version_of_hidden_message)
    
    hidden_message_length_info = f"{hidden_message_length:032b}"
    
    """with open makes sure the file is properly opened and closed  
     i can use open without (with) but then i have to manage closing the file myself using the close method with f.close
     rb tells python to open the file in binary format"""   
     
    with open(image , "rb") as file:
        
        # file.read reads the file in binary format and bytearray divides it into 8 bit bytes each
        image_binary_data = bytearray(file.read())
        
    """bmp data usually starts at byte offset 54 this is due to BMP header and DIB header that come before the actual data 
    the file header contains 14 bytes which contain general info about the file including file type , file size and the offset where
    the pixel data starts,  DIB header contains more info such as width, length color format (such as RGB)
    and bit depth (how many bits are used to represent each color)"""
    #thats why i set the index to start from 54
    image_pixel_data_start = 54
    # this variable will be used to iterate over each bit of
    image_pixel_data_index = 0
    
    hidden_message_length_info_counter = 0
    
    #here im conveying the length of the message to the decoder which is a common practice in steganography
    
    for i in range(image_pixel_data_start, len(image_binary_data)):
        
        # here im using the AND and OR operations first the AND to change the lsb to zero and the OR to modify it to the bit value
        if hidden_message_length_info_counter < len(hidden_message_length_info):
             image_binary_data[i] = (image_binary_data[i] & 0b11111110) | int(hidden_message_length_info[hidden_message_length_info_counter])
             
             hidden_message_length_info_counter += 1
        else:
            break
            
    # here im changing the lsb of every pixel after the length of the message is conveyed
    
    for i in range(image_pixel_data_start + 32, len(image_binary_data)):
        
        # here im using the AND and OR operations first the AND to change the lsb to zero and the OR to modify it to the bit value

        if image_pixel_data_index < hidden_message_length:
            
            image_binary_data[i] = (image_binary_data[i] & 0b11111110) | int(binary_version_of_hidden_message[image_pixel_data_index])
            
            image_pixel_data_index += 1
        
        else:
            break
    # wb tells python to handle the file as binary data
    with open(output_file, "wb") as out_file:
        out_file.write(image_binary_data)
    with open(output_file , "rb") as out_file:   
        c = list(bytearray(out_file.read()))
        
        print("message length encoding:")
        for x in c[55: 86]:
            x = f"{x:08b}"
            print(x[-1], end = "")
        print()
        print("message encoding")
        
        for x in c[86: 86 + len(binary_version_of_hidden_message)-1]:
            x = f"{x:08b}"
            print(x[-1], end = "")
            
            
        
    
    
    
hidden_message_input = input("write hidden message:\n")

image_file_path = input("Enter file path:\n")

image_hidden_message_encoding(image_file_path, hidden_message_input)