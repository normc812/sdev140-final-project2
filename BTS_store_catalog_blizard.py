import sys
print("path is:")
print(sys.executable)

"""
nblizard
3-1-25
SDEV 140 Final Project

Purpose:  this program is a storefront for BTSllc website to:

pseudocode:
    # Import necessary libraries
    import library_for_GUI
    import library_for_image_handling

    # Define a class for catalog items
    class CatalogItem:
        def __init__(self, id, name, price, image_path):
            self.id = id
            self.name = name
            self.price = price
            self.image_path = image_path

    # Initialize an empty catalog
    catalog = {}

    # Function to add items to the catalog
    def add_item_to_catalog(id, name, price, image_path):
        new_item = CatalogItem(id, name, price, image_path)
        catalog[id] = new_item

    # Function to lookup item in catalog
    def lookup_item(id):
        return catalog.get(id, None)

    # Function to display catalog
    def display_catalog():
        for item in catalog.values():
            display_item_details(item)
            display_item_image(item.image_path)

    # Function to create order form GUI
    def create_order_form():
        order_form = create_new_window()
        
        for item in catalog.values():
            add_item_to_form(order_form, item)
        
        add_submit_button(order_form)
        
        return order_form

    # Function to handle order submission
    def submit_order(selected_items):
        total_price = 0
        for item_id, quantity in selected_items.items():
            item = lookup_item(item_id)
            if item:
                total_price += item.price * quantity
        
        display_order_summary(selected_items, total_price)

    # Main program
    def main():
        # Add items to catalog
        add_item_to_catalog(1, "Item 1", 10.99, "path/to/image1.jpg")
        etc.
        
        # Display catalog
        display_catalog()
        
        # Create and display order form
        order_form = create_order_form()
        
        # Wait for user to submit order
        selected_items = wait_for_order_submission(order_form)
        
        # Process the order
        submit_order(selected_items)

    # Run the main program
    main()
"""

#python program
# imports from tkinter

import tkinter as tk   # core GUI library for creating the user interface
from tkinter import ttk # provides modern themed widgets
from tkinter import scrolledtext
from tkinter import messagebox # displays pop-up messages like alerts or confirmations
from tkinter import Scrollbar # For adding scrollbars to widgets like canvases
import re # regular expression module, used for validating credit card owner's name
from datetime import datetime  # used for validating credit card expiration dates
import os  # The operating system module, suggested by Substack and Reddit user

import PIL  # image library for Tkinter
from PIL import Image, ImageTk  # for opening, manipulating, and displaying images

from bts_store_viewer import ViewerApp

# Help Document Dictionary  # this could be read from a file but to avoid more file reads its embedded here

help_document = {
    "Introduction": "This program is a storefront application for BTSllc, designed to allow users to browse a catalog of BTS logo items and create orders. The application provides a graphical user interface (GUI) built with Tkinter, offering an intuitive way to view items, select quantities, and submit orders.",
    "System Requirements": "Python 3.x\nTkinter (usually included with Python installations)\nPillow (PIL) library for image handling",
    "Installation": "Install Python: if necessary, download it from the official Python website and follow the installation instructions.\n2. Install Pillow: Open a terminal or command prompt and run the following command:\npip install pillow",
    "Program Overview": "The program consists of the following main components:\nCatalog Display: Shows the available items with their names, prices, and images.\nOrder Form: Allows users to enter their information and select the quantity of each item they wish to purchase.\nOrder Submission: Processes the selected items and quantities, calculates the total price, including sales tax, and displays an order summary.",
    "Usage Instructions": "Follow these instructions to use the storefront program effectively.",
    "Running the Program": "Save the Python code to a file (e.g., bts_storefront.py).\n  Run the program from the command line: `python bts_storefront.py`.",
    "Main Window": "The main window provides buttons to display the catalog and create an order.",
    "Displaying Catalog": "Click the 'Display Catalog' button to view the available items.",
    "Creating Order": "Click the 'Create Order' button to open the order form and enter your details.",
    "Entering Credit Card": "Click the 'Enter Credit Card' button to enter your details.",
    "Submitting Order": "After filling out the order form, click 'Submit Order' to process your order.",
    "Error Messages": "If you encounter an error message, carefully read the instructions to ensure that you entered your information correctly",
    "Closing Windows": "Close individual windows as needed or exit the main window to close the program. Click the X in the upper right of the open window to close it.",
}

def display_help():
    help_window = tk.Toplevel()
    help_window.title("BTS Logo Storefront Program - Help Document")

    # Create the main paned window
    paned_window = ttk.Panedwindow(help_window, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Frame for the buttons (left side)
    button_frame = ttk.Frame(paned_window)
    paned_window.add(button_frame, weight=1)  # Weight makes it resize

    # Frame for the text display (right side)
    text_frame = ttk.Frame(paned_window)
    paned_window.add(text_frame, weight=3)  # Weight makes it resize


    # Text Area within text_frame
    text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=60, height=20)  # Adjust width/height
    text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    text_area.configure(state='disabled')



    def show_section(heading):
        text_area.configure(state='normal')  # Enable editing temporarily
        text_area.delete("1.0", tk.END)  # Clear previous text
        text_area.insert(tk.END, heading + "\n")
        text_area.insert(tk.END, help_document[heading] + "\n\n")
        text_area.configure(state='disabled')  # Disable editing again

# Create buttons for each heading in the button_frame
    for heading in help_document.keys():
        button = ttk.Button(button_frame, text=heading, command=lambda h=heading: show_section(h))
        button.pack(side=tk.TOP, fill=tk.X, pady=5, padx=5)  # Stack them vertically, fill width


# Defines a class to represent items in the store's catalog
class CatalogItem:
    def __init__(self, id, name, price, imagePath):
        self.id = id   # unique identifier for the item
        self.name = name  # name of the item
        self.price = price  # price of the item
        self.imagePath = imagePath  #file path to the image of the item

global catalog
catalog = {}  # Initializes an empty dictionary called catalog
class Catalog:
    def __init__(self):
        self._items = {}

    def add_item(self, id, name, price, imagePath):
        new_item = CatalogItem(id, name, price, imagePath)
        self._items[id] = new_item

    def get_item(self, id):
        return self._items.get(id)

    def get_all_items(self):
        return self._items

def addItemToCatalog(id, name, price, imagePath):  # Adds a new item to the catalog
    newItem = CatalogItem(id, name, price, imagePath)
    catalog[id] = newItem           # adds new item to the catalog dictionary, 
                                    # using item's id as the key

def lookupItem(id):  # Retrieves an item from the catalog based on its id
    return catalog.get(id, None)    # uses the catalog.get(id, None) 
                                    # method to look up the item
                                    # If the item with the given id is found, 
                                    # it returns the CatalogItem object
                                    # If not found, it returns None

def displayCatalog():  # Creates a new window to display all items in the catalog.
    catalogWindow = tk.Toplevel()   # Creates a new top-level window as separate window)
    catalogWindow.title("BTS Store Catalog - logo items for sale")  # Sets title of catalog window

    # Creates two frames, left_frame and right_frame, to display the catalog items in two columns
    left_frame = ttk.Frame(catalogWindow, padding="10")
    right_frame = ttk.Frame(catalogWindow, padding="10")
    left_frame.grid(row=0, column=0, sticky="nsew")
    right_frame.grid(row=0, column=1, sticky="nsew")

    # Configures the grid layout of the catalogWindow so that the two columns take up equal space
    catalogWindow.grid_columnconfigure(0, weight=1)
    catalogWindow.grid_columnconfigure(1, weight=1)

    items = list(catalog.values())      # to determine length of catalog and divide into two
    mid_point = len(items) // 2
    
    for i, item in enumerate(items):    # iterates through the items in the catalog:
        if i < mid_point:               # divides the items into two groups and places them in the left_frame 
                                        # or right_frame to create a two-column layout.
            parent_frame = left_frame
        else:
            parent_frame = right_frame

        frame = ttk.Frame(parent_frame, padding="5")
        frame.pack(fill=tk.X, pady=5)

        # For each item, it creates thumbnail frame to hold item's details (name, price, and image
        ttk.Label(frame, text=f"{item.name} - ${item.price:.2f}").pack(side=tk.LEFT)

        try:
            image = Image.open(item.imagePath)      # opens the image file using PIL.Image.open()
            image = image.resize((70, 70))          # Resize to thumbnail size
            photoImage = ImageTk.PhotoImage(image)  # creates a PhotoImage object from the image, 
                                                    # which can be displayed in a Tkinter label.
            ttk.Label(frame, image=photoImage, cursor="hand2").pack(side=tk.RIGHT)
            frame.image = photoImage                # create a label to display the image.
            
            # Includes error handling for FileNotFoundError 
            # (if the image file is not found) and other exceptions 
            # that might occur during image loading
            # If an error occurs, it displays an error message in a label
        
        except FileNotFoundError:
            ttk.Label(frame, text="Image not found", background="red", foreground="white").pack(side=tk.RIGHT)
        except Exception as e:
            ttk.Label(frame, text=f"Error loading image: {e}", background="red", foreground="white").pack(side=tk.RIGHT)


def createOrderForm():
    orderForm = tk.Toplevel()
    orderForm.title("BTS Logo Items Order Form")
    orderForm.geometry("600x800")  # Set window size

    # Create a Canvas to hold the content
    canvas = tk.Canvas(orderForm)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  

    # Add a Scrollbar
    scrollbar = Scrollbar(orderForm, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the Canvas to use the Scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Create a Frame inside the Canvas to hold the item entries
    item_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=item_frame, anchor="nw")

    # Configure grid columns
    item_frame.columnconfigure(0, weight=1)
    item_frame.columnconfigure(1, weight=1)

    customerInfo = {}

    # Customer Information Section
    ttk.Label(item_frame, text="Customer Information", font=('Helvetica', 14, 'bold')).grid(row=0, columnspan=2, pady=10)

    # Customer Information Entry fields
    fields = [
        ("Customer Name:", 'name'),
        ("Street Address:", 'street'),
        ("City:", 'city'),
        ("State:", 'state'),
        ("Zip Code:", 'zip'),
        ("Phone Number:", 'phone'),
        ("Email:", 'email')
    ]

    for i, (label, key) in enumerate(fields):
        ttk.Label(item_frame, text=label).grid(row=i+1, column=0, sticky=tk.W, padx=5, pady=2)
        entry = ttk.Entry(item_frame, width=30)
        entry.grid(row=i+1, column=1, sticky=tk.W, padx=5, pady=2)
        customerInfo[key] = entry

    # Separator
    ttk.Separator(item_frame, orient='horizontal').grid(row=len(fields)+1, columnspan=2, sticky='ew', pady=10)

    # Product Selection Section
    ttk.Label(item_frame, text="Product Selection", font=('Helvetica', 14, 'bold')).grid(row=len(fields)+2, columnspan=2, pady=10)

    selectedItems = {}
    itemStartRow = len(fields) + 3

    for i, item in enumerate(catalog.values()):
        frame = ttk.Frame(item_frame, padding="10")
        frame.grid(row=itemStartRow + i, column=0, columnspan=2, sticky=tk.EW)  

        ttk.Label(frame, text=item.name).pack(side=tk.LEFT)
        ttk.Label(frame, text=f"${item.price:.2f}").pack(side=tk.LEFT)

        quantity = tk.StringVar(value="0")
        spinbox = ttk.Spinbox(frame, from_=0, to=100, textvariable=quantity, width=5)
        spinbox.pack(side=tk.RIGHT)

        selectedItems[item.id] = quantity

    # Update scrollregion after all items are added
    item_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    ttk.Button(orderForm, text="Submit Order to Mal's E-commerce", command=lambda: submitOrder(selectedItems, customerInfo)).pack(pady=10)

    # Add mouse wheel scrolling support
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    return orderForm


# def submitOrder processes the order submitted by the customer
def submitOrder(selectedItems, customerInfo):
    totalPrice = 0  # initialize total price for summing 
    orderSummary = "BTS Logo Order Summary:\n"  # title for order summary

    for itemId, quantityVar in selectedItems.items():  # Iterates through the selectedItems dictionary
        try:
            quantity = int(quantityVar.get())
            if quantity > 0:    # checks if the quantity is greater than 0. 
                                # If so, it retrieves the CatalogItem object 
                                # from the catalog using the item's id.
                item = lookupItem(itemId)
                if item:
                    itemTotal = item.price * quantity
                    totalPrice += itemTotal     # calculates the total price for the item 
                                                # (price * quantity) and adds it to the totalPrice.

                    orderSummary += f"{item.name} x{quantity}: ${itemTotal:.2f}\n"
                    # add a line to the orderSummary string with the item's 
                    # name, quantity, and total price
        except ValueError:
            messagebox.showerror("Input Error", f"Invalid quantity for item ID {itemId}. Please enter a valid number.")
            # error check if quantity is <=0, return
            return  # Stop order processing

    # calculate sales tax and grand total
    salesTaxRate = 0.07  # 7% sales tax
    salesTax = totalPrice * salesTaxRate
    grandTotal = totalPrice + salesTax

    # extract customer information from the customerInfo dictionary
    customerName = customerInfo['name'].get()
    customerStreet = customerInfo['street'].get()
    customerCity = customerInfo['city'].get()
    customerState = customerInfo['state'].get()
    customerZipCode = customerInfo['zip'].get()
    customerPhone = customerInfo['phone'].get()
    customerEmail = customerInfo['email'].get()

    # generate an invoice string that includes the customer's information, 
    # order summary, the subtotal, sales tax, and total price

    invoice = f"Invoice for: {customerName}\n"
    invoice += f"Address: {customerStreet}, {customerCity}, {customerState} {customerZipCode}\n"
    invoice += f"Phone: {customerPhone}\n"
    invoice += f"Email: {customerEmail}\n\n"
    invoice += orderSummary
    invoice += f"\nSubtotal: ${totalPrice:.2f}"
    invoice += f"\nSales Tax: ${salesTax:.2f}"
    invoice += f"\nTotal Price: ${grandTotal:.2f}"

    #Create new top-level window to display order summary/invoice
    summaryWindow = tk.Toplevel()
    summaryWindow.title("BTS Logo Order Summary")
    # creates a label to display invoice string in summary window
    ttk.Label(summaryWindow, text=invoice, justify=tk.LEFT).pack(padx=20, pady=20)

# Defines a class to create a GUI for credit card validation (obtained from substack)
class CreditCardGUI:
    def __init__(self, master):
        self.master = master  # stores a reference to the parent window
        master.title("BTS eCommerce Credit Card Validation") # sets the title of the window
        master.geometry("500x200") # sets the size of the window in pixels
         
        self.create_widgets()  # calls the create_widgets method to create the GUI elements

    def create_widgets(self):   # Creates the GUI elements 
                                #(labels, entry fields, and buttons) 
                                # for the credit card validation form.
        # Card Number
        tk.Label(self.master, text="Card Number:").grid(row=0, column=0, sticky="e")
        self.card_number_entry = tk.Entry(self.master)
        self.card_number_entry.grid(row=0, column=1)

        # Owner Name
        tk.Label(self.master, text="Owner Name:").grid(row=1, column=0, sticky="e")
        self.owner_name_entry = tk.Entry(self.master)
        self.owner_name_entry.grid(row=1, column=1)

        # Expiration Date
        tk.Label(self.master, text="Expiration Date (MM/YY):").grid(row=2, column=0, sticky="e")
        self.expiration_date_entry = tk.Entry(self.master)
        self.expiration_date_entry.grid(row=2, column=1)

        # CCV Code
        tk.Label(self.master, text="CCV Code:").grid(row=3, column=0, sticky="e")
        self.ccv_code_entry = tk.Entry(self.master)
        self.ccv_code_entry.grid(row=3, column=1)

        # creates a "Submit" button that calls the validate_and_submit method when clicked
        submit_button = tk.Button(self.master, text="Submit", command=self.validate_and_submit)
        submit_button.grid(row=4, column=1)
        
        # creates a "Clear" button that calls the clearForm method when clicked
        clearButton = tk.Button(self.master, text="Clear", command=self.clearForm)
        clearButton.grid(row=5, column=0, columnspan=2, pady=10)

       
    def validate_and_submit(self): # validates credit card information entered by user
        # retrieves the values from the entry fields through get() method
        card_number = self.card_number_entry.get()
        owner_name = self.owner_name_entry.get()
        expiration_date = self.expiration_date_entry.get()
        ccv_code = self.ccv_code_entry.get()

    # calls the validation methods for each field  AND all must be true to validate     
        if (self.validate_credit_card_number(card_number) and
            self.validate_card_owner_name(owner_name) and
            self.validate_expiration_date(expiration_date) and
            self.validate_ccv(ccv_code)):
            messagebox.showinfo("Success", "Credit card information validated successfully!")
        else:
            messagebox.showerror("Error", "Invalid credit card information. Please check your inputs.")

    def validate_credit_card_number(self, card_number):

        # Implementation of validateCreditCardNumber function
        # validates the credit card number
            # removes spaces and hyphens from the card number
            # checks if the card number is a digit and has a valid length (13 to 19 digits)
            # uses the Luhn algorithm to check the validity of the card number
        card_number = card_number.replace(" ", "").replace("-", "")
        if not card_number.isdigit() or len(card_number) < 13 or len(card_number) > 19:
            return False
        
        total = sum(int(digit) for digit in card_number[-1::-2]) + sum(sum(divmod(int(digit)*2, 10)) for digit in card_number[-2::-2])
        return total % 10 == 0
    
    # checks if the owner's name contains only letters and spaces using a regular expression
    def validate_card_owner_name(self, owner_name):
        return bool(re.match(r'^[A-Za-z\s]+$', owner_name))
    
    # parses the expiration date (MM/YY) into month and year.
    # checks if the expiration date is in the future
    def validate_expiration_date(self, expiration_date):
        try:
            month, year = map(int, expiration_date.split('/'))
            expiration_datetime = datetime(2000 + year, month, 1)
            return expiration_datetime > datetime.now()
        except:
            return False
        
    # checks if the CCV code is a digit and has a valid length (3 or 4 digits)
    def validate_ccv(self, ccv_code):
        return ccv_code.isdigit() and (len(ccv_code) == 3 or len(ccv_code) == 4)
    
    # popup to display results  FIX ME !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # connect to validation process in validate_and_submit

    def displayResult(self, cardInfo):
        self.result_display.config(state='normal')
        self.result_display.delete('1.0', tk.END)
        self.result_display.insert(tk.END, "Credit card information validated:\n\n")
        for key, value in cardInfo.items():
            self.result_display.insert(tk.END, f"{key}: {value}\n")
        self.result_display.config(state='disabled')

    # clears the entry fields in the credit card validation form.
    def clearForm(self):
        self.card_number_entry.delete(0, tk.END)
        self.owner_name_entry.delete(0, tk.END)
        self.expiration_date_entry.delete(0, tk.END)
        self.ccv_code_entry.delete(0, tk.END)
       # self.result_display.config(state='normal')
       # self.result_display.delete('1.0', tk.END)
       # self.result_display.config(state='disabled')
    
    
def open_credit_card_gui():
    credit_card_window = tk.Toplevel()  # was rootcls
    
    CreditCardGUI(credit_card_window)

class ImageViewer:
    def __init__(self, master):
        self.master = master
        self.viewer_window = None
        self.currentImageIndex = 0
        self.maxHeight = 400  # pixels 
        self.maxWidth = 400   # pixels
        self.catalog = Catalog()
        self.imageList = []

    def initialize_viewer(self):
        self.create_catalog()
        self.load_images()

    def create_catalog(self):
        # Defines a class to represent items in the store's catalog
        def addItemToCatalog(id, name, price, imagePath):
            global catalog
            self.catalog.add_item(id, name, price, imagePath)

        # Add catalog items
        addItemToCatalog(1, " 1. custom bag", 19.99, "storeitems/bag.png")
        addItemToCatalog(2, " 2. ball cap red", 15.99, "storeitems/ballcap.png")
        addItemToCatalog(3, " 3. ball cap black", 20.99, "storeitems/ballcap2.png")
        addItemToCatalog(4, " 4. yourname tshirt S/M/L/XL", 20.99, "storeitems/blacktshirt.png")
        addItemToCatalog(5, " 5. calculator", 45.99, "storeitems/calculator.png")
        addItemToCatalog(6, " 6. helmut", 40.99, "storeitems/helmut.png")
        addItemToCatalog(7, " 7. mug", 15.99, "storeitems/mug.png")
        addItemToCatalog(8, " 8. pencil", 5.99, "storeitems/pencil.png")
        addItemToCatalog(9, " 9. BTS ring", 999.99, "storeitems/ring.png")
        addItemToCatalog(10, "10. ruler", 10.99, "storeitems/ruler.png")
        addItemToCatalog(11, "11. black tshirt S/M/L/XL", 25.99, "storeitems/shirt.png")
        addItemToCatalog(12, "12. white tshirt S/M/L/XL", 25.99, "storeitems/shirtw.png")
        addItemToCatalog(13, "13. sunglasses", 39.99, "storeitems/sunglasses.png")
        addItemToCatalog(14, "14. black sweatshirt S/M/L/XL", 49.99, "storeitems/sweatshirt.png")
        addItemToCatalog(15, "15. white sweatshirt S/M/L/XL", 49.99, "storeitems/whitetshirt.png")
        addItemToCatalog(16, "16. wrench", 89.99, "storeitems/wrench.png")

    def load_images(self):
        for item_id in self.catalog.get_all_items():
            image_path = self.catalog.get_item(item_id).imagePath
            try:
                image = Image.open(image_path)
                self.imageList.append(image)
            except FileNotFoundError:
                print(f"Image not found: {image_path}")

    def show_viewer(self):
        if self.viewer_window is None or not self.viewer_window.winfo_exists():
            self.viewer_window = tk.Toplevel(self.master)
            self.viewer_window.title("BTS Swag Catalog Viewer")

            # Item info (name and price)
            self.item_info = tk.Label(self.viewer_window, text="", font=("Arial", 12))
            self.item_info.grid(row=0, column=0, columnspan=3)

            # Image
            self.image_label = tk.Label(self.viewer_window)
            self.image_label.grid(row=1, column=0, columnspan=3)

            # Status bar
            self.status = tk.Label(self.viewer_window, text="", bd=1, relief=tk.SUNKEN, anchor=tk.E)
            self.status.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E)

            # Buttons (on the lowest row)
            self.buttonBackward = tk.Button(self.viewer_window, text="<<", command=self.backwardClick)
            self.buttonBackward.grid(row=3, column=0)

            buttonQuit = tk.Button(self.viewer_window, text="Close Viewer", command=self.viewer_window.destroy)
            buttonQuit.grid(row=3, column=1)

            self.buttonForward = tk.Button(self.viewer_window, text=">>", command=self.forwardClick)
            self.buttonForward.grid(row=3, column=2)

            # Display the image
            self.display_image()
        else:
            self.viewer_window.lift()

    def display_image(self):
        item_id = list(self.catalog.get_all_items().keys())[self.currentImageIndex]
        item = self.catalog.get_item(item_id)
        image = self.imageList[self.currentImageIndex]
        resized_image = image.resize((self.maxWidth, self.maxHeight), Image.LANCZOS)
        photo_image = ImageTk.PhotoImage(resized_image)
      
        self.image_label.config(image=photo_image)
        self.image_label.image = photo_image  # Keep a reference

        self.item_info.config(text=f"{item.name}\nPrice: ${item.price:.2f}")
        self.status.config(text=f"Image {self.currentImageIndex + 1} of {len(self.imageList)}")
        self.update_button_states()

    def forwardClick(self):
        self.currentImageIndex += 1
        self.display_image()

    def backwardClick(self):
        self.currentImageIndex -= 1
        self.display_image()

    def update_button_states(self):
        self.buttonBackward.config(state=tk.NORMAL if self.currentImageIndex > 0 else tk.DISABLED)
        self.buttonForward.config(state=tk.NORMAL if self.currentImageIndex < len(self.imageList) - 1 else tk.DISABLED)

# 

class ViewerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("BTS Store Item Viewer GUI")

        self.image_viewer = ImageViewer(self.master)
        self.image_viewer.initialize_viewer()

        self.open_viewer_button = tk.Button(self.master, text="Open BTS Store Item Viewer", command=self.image_viewer.show_viewer)
        self.open_viewer_button.pack(pady=20)



def main():  # create the main application window. 
    # This is the root window for the entire GUI
    root = tk.Tk()
    root.title("BTS Logo Catalog and Order System")

   # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate desired window size (at least 30% of screen)
    window_width = int(screen_width * 0.4)
    window_height = int(screen_height * 0.3)

    # Set window size - ensuring minimum 
    root.geometry(f"{window_width}x{window_height}")

    # --- Logo Images Section ---
    logo_frame = ttk.Frame(root)
    logo_frame.pack(pady=10)

    logo_folder = "logoimages"  # Specify folder name
    small_image_width = 50  # Specify small image width
    small_image_height = 50  # Specify small image height
    large_image_width = 100  # Specify large image width (twice the small one)
    large_image_height = 100  # Specify large image height (twice the small one)
    num_cols = 3  # Specify number of columns

    image_paths = []  # Load image paths from the logo folder
    try:
        for filename in os.listdir(logo_folder):  # Read list of logoimages from folder
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                image_paths.append(os.path.join(logo_folder, filename))
    # error handling code for loading images           
    except FileNotFoundError:
        messagebox.showerror("Error", f"Folder not found: {logo_folder}")
        image_paths = []
    except Exception as e:
        messagebox.showerror("Error", f"Error reading folder: {e}")
        image_paths = []

    # Display First Image (Larger, Above Others)
    if image_paths:  # Make sure there's at least one image
        try:
            first_image_path = image_paths[0]
            image = Image.open(first_image_path)
            image = image.resize((large_image_width, large_image_height))
            photoImage = ImageTk.PhotoImage(image)
            first_image_label = ttk.Label(logo_frame, image=photoImage)
            first_image_label.image = photoImage  # Keep a reference
            first_image_label.grid(row=0, column=0, columnspan=num_cols, pady=5)  # Span all columns
        
        # error handling code for loading images 
        except FileNotFoundError:
            messagebox.showerror("Error", f"Image not found: {first_image_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {e}")

    # Display Remaining Images (Smaller) in a mosaic frame
    mosaic_frame = ttk.Frame(logo_frame)
    mosaic_frame.grid(row=1, column=0, columnspan=num_cols)  # Put smaller images below the first one

    # iterate through the images to place them in the mosaic frame
    row_num = 0
    col_num = 0
    for i, image_path in enumerate(image_paths[1:]):  # Start from the second image (index 1)
        try:
            image = Image.open(image_path)
            image = image.resize((small_image_width, small_image_height))
            photoImage = ImageTk.PhotoImage(image)
            image_label = ttk.Label(mosaic_frame, image=photoImage)
            image_label.image = photoImage  # Keep a reference
            image_label.grid(row=row_num, column=col_num, padx=5, pady=5)  # Place it in the grid

            col_num += 1
            if col_num >= num_cols:
                col_num = 0
                row_num += 1

            # error handling code for loading images 
        except FileNotFoundError:
            placeholder_label = ttk.Label(mosaic_frame, text="Image not found")
            placeholder_label.grid(row=row_num, column=col_num, padx=5, pady=5)

            col_num += 1
            if col_num >= num_cols:
                col_num = 0
                row_num += 1

        except Exception as e:
            placeholder_label = ttk.Label(mosaic_frame, text=f"Error: {e}")
            placeholder_label.grid(row=row_num, column=col_num, padx=5, pady=5)

            col_num += 1
            if col_num >= num_cols:
                col_num = 0
                row_num += 1

    # --- Add items to catalog ---
    # Add multiple items to the catalog with their details -I used separate lines
    # for each addItemToCatelog but this could have been in a loop rather than
    # create a file or folder with item name and price and path to item image --
    # ran out of time to simplify this

    addItemToCatalog(1, " 1. custom bag", 19.99, "storeitems/bag.png")
    addItemToCatalog(2, " 2. ball cap red", 15.99, "storeitems/ballcap.png")
    addItemToCatalog(3, " 3. ball cap black", 20.99, "storeitems/ballcap2.png")
    addItemToCatalog(4, " 4. yourname tshirt S/M/L/XL", 20.99, "storeitems/blacktshirt.png")
    addItemToCatalog(5, " 5. calculator", 45.99, "storeitems/calculator.png")
    addItemToCatalog(6, " 6. helmut", 40.99, "storeitems/helmut.png")
    addItemToCatalog(7, " 7. mug", 15.99, "storeitems/mug.png")
    addItemToCatalog(8, " 8. pencil", 5.99, "storeitems/pencil.png")
    addItemToCatalog(9, " 9. BTS ring", 999.99, "storeitems/ring.png")
    addItemToCatalog(10, "10. ruler", 10.99, "storeitems/ruler.png")
    addItemToCatalog(11, "11. black tshirt S/M/L/XL", 25.99, "storeitems/shirt.png")
    addItemToCatalog(12, "12. white tshirt S/M/L/XL", 25.99, "storeitems/shirtw.png")
    addItemToCatalog(13, "13. sunglasses", 39.99, "storeitems/sunglasses.png")
    addItemToCatalog(14, "14. black sweatshirt S/M/L/XL", 49.99, "storeitems/sweatshirt.png")
    addItemToCatalog(15, "15. white sweatshirt S/M/L/XL", 49.99, "storeitems/whitetshirt.png")
    addItemToCatalog(16, "16. wrench", 89.99, "storeitems/wrench.png")

    # --- Buttons ---
    # Create a frame for the buttons
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)
    ttk.Button(button_frame, text="Help Topics", command=display_help).pack(pady=5)

    app = ViewerApp(button_frame)
    open_viewer_button = ttk.Button(button_frame, text="BTS Store Catalog Items", command=app.show_viewer).pack(pady=5)

    ttk.Button(button_frame, text="Display Entire Catalog", command=displayCatalog).pack(pady=5)

    ttk.Button(button_frame, text="Enter Credit Card Info Before Creating Order", command=open_credit_card_gui).pack(pady=5)
    
    ttk.Button(button_frame, text="Create Order and Invoice", command=createOrderForm).pack(pady=5)
   
    
    
    root.update_idletasks()
    root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

    
    root.mainloop()   #to continously loop the GUI

if __name__ == "__main__":
    main()
