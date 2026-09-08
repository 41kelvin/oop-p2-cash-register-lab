class CashRegister:
    def __init__(self, discount=0):
        self._discount = 0
        self.discount = discount
        self.total = 0
        self.items = []
        self.previous_transactions = []

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        if type(value) is int and 0 <= value <= 100:
            self._discount = value
        else:
            print("Not valid discount")

    def add_item(self, item, price, quantity=1):
        self.total += price * quantity
        self.items.extend([item] * quantity)
        self.previous_transactions.append({
            "item": item,
            "price": price,
            "quantity": quantity,
        })

    def apply_discount(self):
        if self.discount == 0 or not self.previous_transactions:
            print("There is no discount to apply.")
            return

        multiplier = 1 - self.discount / 100
        self.total *= multiplier
        # Keep each price in sync so voiding refunds its discounted amount.
        for transaction in self.previous_transactions:
            transaction["price"] *= multiplier
        amount = format(self.total, ".2f").rstrip("0").rstrip(".")
        print(f"After the discount, the total comes to ${amount}.")

    def void_last_transaction(self):
        if not self.previous_transactions:
            print("There is no transaction to void.")
            return

        transaction = self.previous_transactions.pop()
        quantity = transaction["quantity"]
        self.total -= transaction["price"] * quantity
        if quantity:
            del self.items[-quantity:]
        if not self.previous_transactions:
            self.total = 0
