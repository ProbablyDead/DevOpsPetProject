from payment import Payment


async def callback(result):
    print("hi there")
    print(result)


print(Payment().create_payment(callback, "yakiza"))

while True:
    pass
