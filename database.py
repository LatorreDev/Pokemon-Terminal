# The Database object is a container for all the supported Pokemon.

import os, random


class Pokemon:
    __id = ""  # ID is stored as a string because it must maintain "003" format, not "3".
    __name = ""
    __region = ""
    __path = ""  # The location of the image.

    def __init__(self, identifier, name, region, path):
        self.__id = identifier
        self.__name = name
        self.__region = region
        self.__path = path

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_region(self):
        return self.__region

    def get_path(self):
        return self.__path

    def is_extra(self):
        return self.__id is None

    def __str__(self):
        return self.get_id() + " " + self.get_name() + " at " + self.get_path()


class Database:
    __pokemon_list = []
    __pokemon_dictionary = {}
    __directory = ""  # The global location of the code.
    __MAX_ID = 493  # Highest possible Pokemon ID.
    __regions = ('kanto', 'johto', 'hoenn', 'sinnoh')

    def __init__(self):
        self.directory = os.get_exec_path()[0]
        self.__load_data()
        self.__load_extra()

    def __str__(self):
        string = "POKEMON:\n"
        for element in self.__pokemon_list:
            string += str(element) + "\n"
        return string[:-1]  # Remove the final new line ("\n").

    def get_all(self):
        # Get all the Pokemon.
        result = []
        for pokemon in self.__pokemon_list:
            result.append(pokemon)
        return result

    def get_kanto(self):
        # Get all the Pokemon from the Kanto region.
        return self.__get_region("kanto")

    def get_johto(self):
        # Get all the Pokemon from the Johto region.
        return self.__get_region("johto")

    def get_hoenn(self):
        # Get all the Pokemon from the Hoenn region.
        return self.__get_region("hoenn")

    def get_sinnoh(self):
        # Get all the Pokemon from the Sinnoh region.
        return self.__get_region("sinnoh")

    def get_extra(self):
        # Get all the Extra Pokemon images available.
        return self.__get_region(None)

    def get_regions(self):
        # Get all the supported regions.
        return self.__regions

    def __get_region(self, region):
        # Helper method for getting all the Pokemon of a specified region.
        result = []
        for pokemon in self.__pokemon_list:
            if pokemon.get_region() == region:
                result.append(pokemon)
        return result

    def pokemon_exists(self, pokemon):
        # Check for a Pokemon by ID or name.
        if type(pokemon) is int or str(pokemon).isdigit():
            return self.id_exists(pokemon)
        else:
            return self.name_exists(pokemon)

    def id_exists(self, identifier):
        # Check for Pokemon by ID.
        identifier = int(identifier)
        if identifier < 1 or identifier > self.__MAX_ID:
            return False
        else:
            return True

    def name_exists(self, name):
        # Check for Pokemon by Name.
        return name.lower() in self.__pokemon_dictionary

    def names_starting_with(self, prefix):
        # Return Pokemon who's names contain the specified prefix.
        result = []
        for pokemon in self.__pokemon_list:
            if str(pokemon.get_name()).startswith(prefix):
                result.append(pokemon)
        return result

    def get_random(self):
        # Select a random Pokemon from the database.
        random_int = random.randint(1, len(self.__pokemon_list))
        return self.__pokemon_list[random_int]

    def __load_data(self):
        # Load all the Pokemon data. This does not include the 'Extra' Pokemon.
        path = self.directory + "/./Data/pokemon.txt"
        data_file = open(path, "r+")
        for line in data_file:  # Load everything but the Pokemon from the 'Extra' folder.
            identifier = line.split(' ')[0]  # First part of the line is the id.
            name = line[len(identifier)+1:-1].lower()  # The rest is the name (minus the new line at the end).
            identifier = self.__add_zeroes(identifier)  # This statement cannot occur before name has been created.
            region = self.__determine_region(identifier)
            path = self.__determine_folder(identifier) + "/" + identifier + ".png"
            pokemon = Pokemon(identifier, name, region, path)
            self.__pokemon_list.append(pokemon)
            self.__pokemon_dictionary[pokemon.get_name()] = pokemon

    def __load_extra(self):
        # Load all the file names of the images in the Extra folder.
        for file in os.listdir(self.directory + "/./Images/Extra"):
            if file.endswith(".png"):
                name = os.path.join("/Images/Extra", file).split('/')[-1][0:-4].lower()
                path = self.directory + "/./Images/Extra"
                pokemon = Pokemon(None, name, None, path)
                if name in self.__pokemon_dictionary:
                    raise Exception("Duplicate names detected. "
                                    "The name of the file " + str(name) + ".png in the folder 'Extra' must be changed.")
                self.__pokemon_list.append(pokemon)
                self.__pokemon_dictionary[pokemon.get_name()] = pokemon

    @staticmethod
    def __add_zeroes(number):
        # Add zeroes to the front so that it begins with 3 digits. Example: "2" -> "002".
        zeroes = ""
        if int(number) < 10:
            zeroes = "00"
        elif int(number) < 100:
            zeroes = "0"
        return zeroes + str(number)

    def __determine_region(self, identifier):
        # Determine which region a Pokemon is from.
        identifier = int(identifier)
        if identifier < 1:
            raise Exception("Pokemon ID cannot be less than 1.")
        if identifier < 152:
            return "kanto"
        elif identifier < 252:
            return "johto"
        elif identifier < 387:
            return "hoenn"
        elif identifier < 494:
            return "sinnoh"
        else:
            raise Exception("Pokemon ID cannot be greater than 493.")

    def __determine_folder(self, identifier):
        # Determine which folder a Pokemon is from.
        identifier = int(identifier)
        if identifier < 1:
            raise Exception("Pokemon ID cannot be less than 1.")
        if identifier < 152:
            return self.directory + "/./Images/Generation I - Kanto"
        elif identifier < 252:
            return self.directory + "/./Images/Generation II - Johto"
        elif identifier < 387:
            return self.directory + "/./Images/Generation III - Hoenn"
        elif identifier < 494:
            return self.directory + "/./Images/Generation IV - Sinnoh"
        else:
            raise Exception("Pokemon ID cannot be greater than 493.")
