from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import random
import os

class BillingApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.bill_no = str(random.randint(1000, 9999))

        self.name = TextInput(hint_text="Customer Name", size_hint_y=None, height=50)
        self.phone = TextInput(hint_text="Phone", size_hint_y=None, height=50)

        self.soap = TextInput(hint_text="Soap Qty", size_hint_y=None, height=50)
        self.rice = TextInput(hint_text="Rice Qty", size_hint_y=None, height=50)

        self.add_widget(self.name)
        self.add_widget(self.phone)
        self.add_widget(self.soap)
        self.add_widget(self.rice)

        btn_total = Button(text="Calculate Total", size_hint_y=None, height=50)
        btn_total.bind(on_press=self.calculate_total)

        btn_bill = Button(text="Generate Bill", size_hint_y=None, height=50)
        btn_bill.bind(on_press=self.generate_bill)

        self.add_widget(btn_total)
        self.add_widget(btn_bill)

        self.output = TextInput(readonly=True)
        scroll = ScrollView()
        scroll.add_widget(self.output)
        self.add_widget(scroll)

    def calculate_total(self, instance):
        try:
            soap = int(self.soap.text or 0)
            rice = int(self.rice.text or 0)

            self.soap_price = soap * 25
            self.rice_price = rice * 70
            self.total = self.soap_price + self.rice_price

            self.output.text = f"Total = Rs. {self.total}"
        except:
            self.output.text = "Invalid input"

    def generate_bill(self, instance):
        if self.name.text == "" or self.phone.text == "":
            self.output.text = "Enter customer details"
            return

        bill = f"""
TENT SHOP BILL
Bill No: {self.bill_no}
Name: {self.name.text}
Phone: {self.phone.text}

-------------------------
Soap: {self.soap.text} = {self.soap_price}
Rice: {self.rice.text} = {self.rice_price}

-------------------------
Total: Rs. {self.total}
"""
        self.output.text = bill

        if not os.path.exists("bills"):
            os.mkdir("bills")

        with open(f"bills/{self.bill_no}.txt", "w") as f:
            f.write(bill)

class MyApp(App):
    def build(self):
        return BillingApp()

if __name__ == "__main__":
    MyApp().run()