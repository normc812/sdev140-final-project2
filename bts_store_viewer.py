# File: bts_store_viewer.py

import tkinter as tk
from PIL import ImageTk, Image

class CatalogItem:
    def __init__(self, id, name, price, imagePath):
        self.id = id
        self.name = name
        self.price = price
        self.imagePath = imagePath

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
        def addItemToCatalog(id, name, price, imagePath):
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

class ViewerApp:
    def __init__(self, master):
        self.master = master
        self.image_viewer = ImageViewer(self.master)
        self.image_viewer.initialize_viewer()

    def show_viewer(self):
        self.image_viewer.show_viewer()

# This part is only executed if the script is run directly
if __name__ == "__main__":
    root = tk.Tk()
    app = ViewerApp(root)
    
    open_viewer_button = tk.Button(root, text="Open BTS Store Item Viewer", command=app.show_viewer)
    open_viewer_button.pack(pady=20)
    
    root.mainloop()
