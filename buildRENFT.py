import hashlib


class Ship:
  def __init__(self, name):
    self.name = name
    self.hash = hashlib.sha256(name.encode()).hexdigest()

  def __str__(self):
    return f"\tShip(name={self.name}, hash={self.hash})"


class Fleet:
  def __init__(self, name):
    self.name = name
    self.ships = []
    self.hash = hashlib.sha256(name.encode()).hexdigest()

  def add_ship(self, ship):
    self.ships.append(ship)

  def find_by_hash(self, hash_value):
    for ship in self.ships:
      if ship.hash == hash_value:
        return self, ship
    return None, None

  def __str__(self, indent=0):
    ship_strings = [str(ship) for ship in self.ships]
    indent_str = " " * indent
    return f"{indent_str}Fleet(name={self.name}, hash={self.hash}):\n{indent_str + ''.join(ship_strings)}"


class reNFT:
  def __init__(self, name):
    self.name = name
    self.fleets = []
    self.hash = hashlib.sha256(name.encode()).hexdigest()

  def add_fleet(self, fleet):
    self.fleets.append(fleet)

  def find_by_hash(self, hash_value):
    # Check fleets within reNFT first (ownership cases)
    if self.hash == hash_value:
      return self, None  # Parent reNFT found, child ship is None

    # Recursively search fleets for the hash
    for fleet in self.fleets:
      found_in_fleet, found_ship = fleet.find_by_hash(hash_value)
      if found_in_fleet:
        return found_in_fleet, found_ship  # Found in a child fleet

    # Not found in any fleets
    return None, None

  def __str__(self, indent=0):
    fleet_strings = [str(fleet) for fleet in self.fleets]
    indent_str = " " * indent
    return f"{indent_str}reNFT(name={self.name}, hash={self.hash}):\n{indent_str + ''.join(fleet_strings)}"


def main():
  # Create an reNFT
  property_address = input("Create an reNFT by entering a property address: ")
  renft = reNFT(property_address)

  # Ownership Fleet and Ship (simplified ownership eample doesn't have sub-fleets)
  owner = input("Create a fleet for Ownership. Tell me who owns this property: ")
  ownership_fleet = Fleet("Ownership")
  ownership_ship = Ship(f"{owner} Ownership Record")
  ownership_fleet.add_ship(ownership_ship)
  renft.add_fleet(ownership_fleet)

  # Building Attributes Fleet and Ship
  square_feet = input("Tell us how many square feet the property is: ")
  building_attributes_fleet = Fleet("Building Attributes")
  square_feet_ship = Ship(f"Square Feet: {square_feet}")
  building_attributes_fleet.add_ship(square_feet_ship)
  renft.add_fleet(building_attributes_fleet)

  print(f"\nreNFT created for {renft.name}")

  while True:
    # Display reNFT structure (including hash information)
    print(renft)

    # Find by hash functionality
    hash_input = input("\nEnter a hash to find its parent(s) and children (or 'q' to quit): ")
    if hash_input.lower() == 'q':
      break

    # Capture the hash input in a variable (hash_value)
    hash_value = hash_input

    parent_fleet, ship = renft.find_by_hash(hash_value)
    if ship:
      print(f"Found Ship: {ship}")
      if parent_fleet:
        print(f"Parent Fleet: {parent_fleet}")
      else:
        print(f"This hash can not be found")



if __name__ == "__main__":
  main() 
