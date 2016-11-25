# Rent-O-Matic
We like to do activities at Vacansoleil/GWW but arranging transport can be tricky.
Programming has a solutions for everything so it’s up to you to program a
machine that allows us to rent transport!

The requirements for the Rent-O-Matic are listed below. See how far you can
get in 2 hours but keep in mind, quality over quantity!

* Make this using, Django and a frontend solution of your choice (React, jQuery etc.)
* Has to be interactive
* Keep a state during runtime but does not need to be persisted (i.e. saved to disk) after exit.
* Responds to the following commands:
- **help**
- **list**
- **info** [vehicle number]
- **rent** [vehicle number]
- **pay** [cash amount]
- **exit** (if runtime program)
* There should be different types of transport with their own properties (eg. bikes, cars, motorbikes, boats etc.)
* The Rent-O-Matic needs to be able to provide change with the least amount of euro's using the following list of possible options: [1, 2, 5, 10, 20, 50, 100, 200, 500].
* There should be a inventory of transports that can be rented (eg. multiple bikes).
* At least one transport type that is already rented and not available
* Anything unclear? Don’t be afraid to ask! :)


If you want to go wild, a bonus requirement:
- Be able to return a transport with added mileage to the inventory
