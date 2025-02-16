# from kivy.app import App
# from kivy.uix.button import Button
# from kivy.uix.boxlayout import BoxLayout
# import requests


# class NetworkApp(App):
#     def answer(self):
#         response = requests.get('http://127.0.0.1:8000/post/api/posts/')
        
#         if response.status_code == 200:
#             response = response.json()
            
#             print(response)
#         else:
#             print('all bad')
    
#     def build(self):
#         button = Button(text='hello world')
#         button.on_press = self.answer
        
#         return button
    
    
# app = NetworkApp()
# app.run()
    
