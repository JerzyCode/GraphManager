import customtkinter


class SliderFrame(customtkinter.CTkFrame):
    def __init__(self, root, text):
        super().__init__(root)
        self.label = customtkinter.CTkLabel(self, text=text, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label.grid(row=0, column=0, padx=(20, 5), pady=(10, 0))

        self.entry = customtkinter.CTkEntry(self, placeholder_text="size", width=100)
        self.entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky='w')

        self.slider = customtkinter.CTkSlider(self, from_=0, to=100, number_of_steps=100)
        self.slider.configure(command=self.on_slider_change)
        self.slider.grid(row=1, column=0, padx=20, pady=5)

    def on_slider_change(self, value):
        self.entry.delete(0, customtkinter.END)
        self.entry.insert(0, str(int(value)))

    def get_value(self):
        return self.entry.get()

    def insert_value(self, value):
        self.entry.insert(0, value)
