# pylint:disable=C0111,C0103
import sqlite3

conn = sqlite3.connect('data/ecommerce.sqlite')
dbb = conn.cursor()

def detailed_orders(db):
    '''return a list of all orders (order_id, customer.contact_name,
    employee.firstname) ordered by order_id'''

    query = '''
    SELECT
    orders.OrderID,
    customers.ContactName as customer_contact_name,
    employees.FirstName as employee_firstname
    from employees
    left join  Orders
	    ON orders.EmployeeID = employees.EmployeeID
    LEFT JOIN Customers
	    on orders.CustomerID = customers.CustomerID
    ORDER BY orders.OrderID
    '''
    db.execute(query)
    results = db.fetchall()
    return results


def spent_per_customer(db):
    '''return the total amount spent per customer ordered by ascending total
    amount (to 2 decimal places)
    Exemple :
        Jean   |   100
        Marc   |   110
        Simon  |   432
        ...
    '''
    query = '''
    SELECT
    customers.ContactName,
    ROUND(SUM(orderdetails.Quantity * orderdetails.UnitPrice),2) as total_amount
    FROM OrderDetails
    join Orders
        on orderdetails.OrderID = orders.OrderID
    JOIN Customers
        on orders.CustomerID = customers.CustomerID
    GROUP BY customers.ContactName
    ORDER BY total_amount ASC
    '''
    db.execute(query)
    results = db.fetchall()
    return results

def best_employee(db):
    '''Implement the best_employee method to determine who’s the best employee!'''
    query = '''
    SELECT
    employees.FirstName,
    employees.LastName,
    SUM(orderdetails.UnitPrice*orderdetails.Quantity) as total_purchase
    FROM OrderDetails
    join Orders
        on orderdetails.OrderID = orders.OrderID
    JOIN Employees
        on orders.EmployeeID =employees.EmployeeID
    GROUP BY employees.FirstName
    order by total_purchase DESC
    '''
    db.execute(query)
    results = db.fetchall()
    return results[0]

def orders_per_customer(db):
    '''Return a list of tuples where each tuple contains the contactName
    of the customer and the number of orders they made (contactName,
    number_of_orders). Order the list by ascending number of orders'''

    query = '''
    SELECT customers.ContactName, COUNT(orders.OrderID) as cnt
    FROM Customers
    left join Orders
	    on orders.CustomerID  = customers.CustomerID
    GROUP BY customers.ContactName
    order BY cnt
    '''
    db.execute(query)
    results = db.fetchall()
    return results


#print(detailed_orders(db))
#print(spent_per_customer(db))
#print(best_employee(db))
#print(orders_per_customer(db))
