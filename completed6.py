import customtkinter
import sqlite3
from PIL import Image
import google.generativeai as genai
from cryptography.fernet import Fernet


# Start the chatbot
#health_chatbot()
#key=Fernet.generate_key()



class ChatBotGui(customtkinter.CTk):
    customtkinter.set_appearance_mode("white")
    customtkinter.set_default_color_theme("blue")
    chat_started=False
    chat_icon_path=r"C:\Users\ASUS\Desktop\Code\Python_Projects\hackathon_try\Photos\Resized_Medi_bot.png"
    send_icon_path=r"C:\Users\ASUS\Desktop\Code\Python_Projects\hackathon_try\Photos\Resized_Upload_Btn.png"
    def __init__(self):
        super().__init__()
        
        my_width=self.winfo_screenwidth()
        my_height=self.winfo_screenheight()

        self.title("Chat")
        self.geometry(f"{my_width}x{my_height}")

        self.chat_bot_icon=Image.open(self.chat_icon_path)
        self.chat_bot_icon=customtkinter.CTkImage(light_image=self.chat_bot_icon,
                                                  size=(40,40))

        self.chat_bot_icon_label=customtkinter.CTkLabel(self,
                                                        text="",
                                                        image=self.chat_bot_icon)
        self.chat_bot_icon_label.pack()
        self.chat_bot_icon_label.place(relx=0.22,
                                       rely=0.03,
                                       )
        self.Chat_label=customtkinter.CTkLabel(self,
                                               text="Medi.py",
                                               text_color="black",
                                               
                                               font=("Arial", 30),
                                               
                                               )
        self.Chat_label.pack()
        self.Chat_label.place(relx=0.25,
                              rely=0.03,
                              )
        #Experimental
        self.Side_menu=customtkinter.CTkFrame(self,
                                              fg_color='grey',
                                              corner_radius=25)
        self.Side_menu.pack()
        self.Side_menu.place(relheight=1.0,
                             relwidth=0.2,
                             relx=0,
                             rely=0)


        self.Chat_Bot_Page_Button=customtkinter.CTkButton(self.Side_menu,
                                                          text='About',
                                                          corner_radius=25,
                                                          fg_color='white',
                                                          text_color='black',
                                                          )
        self.Chat_Bot_Page_Button.pack()
        self.Chat_Bot_Page_Button.place(relwidth=0.8,
                                        relheight=0.1,
                                        relx=0.05,
                                        rely=0.1)
        
        
        self.Profile_Page_Button=customtkinter.CTkButton(self.Side_menu,
                                                          text='Profile',
                                                          corner_radius=25,
                                                          fg_color='white',
                                                          text_color='black')
        self.Profile_Page_Button.pack()
        self.Profile_Page_Button.place(relwidth=0.8,
                                        relheight=0.1,
                                        relx=0.05,
                                        rely=0.25)

        #######

        self.Show_Message_Box=customtkinter.CTkTextbox(self,
                                                       fg_color='light blue',
                                                       text_color="black",
                                                       font=("Arial", 20),
                                                       corner_radius=25,
                                                       border_width=2,
                                                       border_color='black'
                                                       
                                                       )
        self.Show_Message_Box.insert("1.0","Hello, How are you feeling today?")
        self.Show_Message_Box.pack()
        self.Show_Message_Box.place(relheight=0.6,
                                    relwidth=0.66,
                                    relx=0.25,
                                    rely=0.1,)
        self.Message_Box=customtkinter.CTkEntry(self,
                                               fg_color='white',
                                               text_color="black",
                                               corner_radius=25,
                                               font=("Arial", 20),
                                               border_color="black",
                                               border_width=2,

                                               placeholder_text="Type your message here",
                                               
                                               )
        self.Message_Box.pack()
        self.Message_Box.place(relx=0.25,
                               rely=0.78,
                               relheight=0.1,
                               relwidth=0.66,
                               )
        

        self.Message_Box_icon=Image.open(self.send_icon_path)
        self.Message_Box_icon=customtkinter.CTkImage(light_image=self.Message_Box_icon,
                                                     size=(60,60))
        self.Message_Box_Button=customtkinter.CTkButton(self,
                                                        text="",
                                                        image=self.Message_Box_icon,    
                                                        fg_color='white',
                                                        command=self.Send_message,
                                                        width=60,
                                                        height=60,
                                                        hover_color='blue',
                                                        )
        self.Message_Box_Button.pack()
        self.Message_Box_Button.place(relx=0.91,
                                      rely=0.79,
                                      
                                      )


        self.mainloop()

    
    def Send_message(self):
        message=self.Message_Box.get()
        self.Message_Box.delete(0,customtkinter.END)
        
        if self.chat_started!=True:
            self.Show_Message_Box.delete("1.0",customtkinter.END)
        self.Show_Message_Box.insert(customtkinter.END,f"User : {message}\n")
        self.chat_started=True
        response,accuracy=self.get_res(message)
        print(response)
        self.Show_Message_Box.insert(customtkinter.END,f"Bot : {response}")
        self.Show_Message_Box.insert(customtkinter.END,f"Accuracy:{accuracy}")


    

    def get_res(self,user_input):
        key = "AIzaSyDdyDb0WR7cJBwT6Zj4Kbu9mV_f80Fy-zA"
        genai.configure(api_key=key)

        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
        )

        chat_session = model.start_chat(history=[])

        # 
        #. Always provide the response in English
        #extra = """Keep it short , provide diagnosis and remidie"""
        
        extra="""You are a health specialist AI
        , Extra instructions for AI no matter the language of the user's input.
        provide info in type of langue user has asked ,provide only that response and nothing else
          Answer in short but dont tell i got it etc just what i have asked 
          """
        #
        # Send user input with extra instructions
        response = chat_session.send_message(user_input + " " + extra)
        print(response.text)
        verify_percent=chat_session.send_message("verify data if its correct"+response.text)

        return response.text,verify_percent.text  # Return summarized text if available
                    
                    




    

class Sign_Up_Page(customtkinter.CTk):
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("blue")
    
    
    def __init__(self):
        super().__init__()
        my_width=self.winfo_screenwidth()
        my_height=self.winfo_screenheight()
        #self.state('zoomed')
        #self.attributes('-fullscreen',True)
        
        
        
        #self.all_element_side="middle"

        self.my_font=("Arial", 20)
        self.login_font=("Arial", 40)
        
        self.paddingy=5
        

        self.place_element_relx=0.2
        self.place_username_rely=0.3
        self.place_password_rely=0.45
        self.place_checkbox_rely=0.58
        self.place_button_rely=0.65

        self.login_frame_width=0.25
        self.login_frame_height=0.5
        self.login_frame_relx=0.5
        self.login_frame_rely=0.45



        self.entry_relheight=0.1
        self.entry_relwidth=0.6
        

        self.title("Sign Up")
        self.geometry(f"{my_width}x{my_height}")
        self.main_frame=customtkinter.CTkFrame(self,fg_color='light blue')
        self.main_frame.pack(fill='both',
                             expand=True)
        
        

        self.login_frame=customtkinter.CTkFrame(self.main_frame,
                                                corner_radius=10)
        self.login_frame.pack(fill='both',
                              expand=True,
                              padx=10,
                              pady=10)
        

        self.login_frame.place(relx=self.login_frame_relx,
                               rely=self.login_frame_rely,
                               relheight=self.login_frame_height,
                               relwidth=self.login_frame_width,
                               anchor='center')
        
        
        


        self.login_label=customtkinter.CTkLabel(self.login_frame,
                                                text="Login ",
                                                font=self.login_font,
                                                text_color='white',
                                                
                                                )
        self.login_label.pack(fill='y',
                              expand=True)
        self.login_label.place(relx=self.place_element_relx,
                               rely=0.1,
                               )
        


        self.username_entry = customtkinter.CTkEntry(self.login_frame,
                                                     placeholder_text='Username')
        self.username_entry.pack()

        self.username_entry.place(relx=self.place_element_relx,
                                  rely=self.place_username_rely,
                                  relheight=self.entry_relheight,
                                  relwidth=self.entry_relwidth
                                  )
        

        self.password_entry = customtkinter.CTkEntry(self.login_frame,
                                                      show="*",
                                                     placeholder_text='Password')
        self.password_entry.pack()
        self.password_entry.place(relx=self.place_element_relx,
                                  rely=self.place_password_rely,
                                  relheight=self.entry_relheight,
                                  relwidth=self.entry_relwidth)
        
        self.remember_me = customtkinter.CTkCheckBox(self.login_frame,
                                                        text="Remember Me")
        self.remember_me.pack()
        self.remember_me.place(relx=self.place_element_relx,
                               rely=self.place_checkbox_rely)

        self.loging_up_button = customtkinter.CTkButton(self.login_frame, 
                                                      text="Login",
                                                      command=self.Sign_Up_Function)
        self.loging_up_button.pack()
        self.loging_up_button.place(relx=self.place_element_relx,
                                  rely=self.place_button_rely,
                                  relheight=self.entry_relheight,
                                  relwidth=self.entry_relwidth,
                                  )
        
        
        self.mainloop()

    def open_second_page(self):
        self.withdraw()  # Hide the main page
        self.destroy()
        second_page = ChatBotGui()
    def Sign_Up_Function(self):
        print("Username Entered:",self.username_entry.get())
        print("Password Entered:",self.password_entry.get())
        if(self.username_entry.get()=='Snap' and self.password_entry.get()=='123'):
            print('Login Succes ful')
            self.withdraw()
            self.open_second_page()
            
        
           








        
def main():
    #ChatBotGui()
    Sign_Up_Page()
main()