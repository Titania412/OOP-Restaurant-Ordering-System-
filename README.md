# OOP-Restaurant-Ordering-System-

In this project, I created a restaurant ordering system using functions and dictionaries. The program will have:
* Rebuild using object-oriented programming (OOP)
* Display information about your restaurant.
* Let the user order from Appetizers, Entrees, Desserts, and Beverages.
* Store the order in memory using objects (not raw dictionaries).
* View and modify the current order.
* Calculate a final total including subtotal, coupon, tip, NJ sales tax (6.625%), and delivery fee 
* Save the order to a CSV file and allow viewing that file later.

<br> Specifications: <br>

The program use the following five classes <br>

1. MenuItem

<img width="910" height="480" alt="image" src="https://github.com/user-attachments/assets/e10ced59-ab39-444f-acf4-23b6b0433f40" />

<br>

2. Menu

<img width="830" height="285" alt="image" src="https://github.com/user-attachments/assets/33a14b89-821b-40e3-981a-00e321796d9e" />

<br>

3. OrderItem

<img width="601" height="256" alt="image" src="https://github.com/user-attachments/assets/f5d153d5-150c-4b1c-b3c8-55ba128a7d7e" />
<img width="895" height="102" alt="image" src="https://github.com/user-attachments/assets/7eaa5721-6e24-43ba-a481-5f3450569158" />

<br>

4. Order

<img width="902" height="518" alt="image" src="https://github.com/user-attachments/assets/4ece3eb4-665b-49a5-a1dd-832e0068d528" />

<br>

5. Restaurant

<img width="904" height="459" alt="image" src="https://github.com/user-attachments/assets/7391b505-c5f1-461b-95dd-b09998d25458" />
<img width="529" height="57" alt="image" src="https://github.com/user-attachments/assets/512392ca-a1d8-46b8-be0f-afe6e0d670e5" />

<br>
Program flow:
In the main() function:
*1. Create a Restaurant object with name, location, and URL. 
*2. Create MenuItem objects for your chosen restaurant and add them to the Menu.
*3. Run the menu loop that calls methods on your Restaurant object.

<br>
Notes:
* Each class should manage its own data. For example, Order calculates its own subtotal — Restaurant should not reach into Order’s item list to do math. 
* Test incrementally. Implement and test one class at a time. Start with MenuItem and Menu before moving to Order and Restaurant. 
* Use the starter code. Every pass statement is a method you need to implement. Do not rename classes or methods. 
