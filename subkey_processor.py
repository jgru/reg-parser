__author__ = 'gru'

from abc import ABC, abstractmethod
from Registry import Registry

FILE_EXT_KEY = "FileExts"
RECENT_DOCS_KEY = "RecentDocs"


class ProcessorFactory():

    @staticmethod
    def get_processor(key_str, data):
        if key_str == FILE_EXT_KEY:
            return DefaultProcessor(data)
            #return FileExtProcessor(data)

        elif key_str == RECENT_DOCS_KEY:
            return RecentDocsProcessor(data)

        else:
            return DefaultProcessor(data)


class AbstractSubkeyProcessor(ABC):

    def __init__(self, data):
        self.data = data

    @abstractmethod
    def process_content(self, is_bare, is_raw):
        pass


class DefaultProcessor(AbstractSubkeyProcessor):

    def __init__(self, data):
        super().__init__(data)

    def process_content(self, is_bare, is_raw):
        return self.str_rep(is_bare, is_raw)

    def str_rep(self, is_bare, is_raw):
        data_dict = self.data
        result = ""
        bare_result = ""

        for k in data_dict.keys():

            if data_dict[k][0].value_type() != Registry.RegNone:

                result += "\n--------------------------\n"
                result += str(k) +"\n"

            for v in data_dict[k]:
                #print("Name: ", v.name())
                if v.value_type() == Registry.RegNone:
                    continue
                elif v.value_type() == Registry.RegBin:
                    result += "Datatype: " + v.value_type_str() + "\n"
                    result += self.convert_binary_data(v.value()) + "\n"
                    bare_result += self.convert_binary_data(v.value()) + "\n"
                else:
                    result += v.value() + "\n"
                    bare_result += v.value() + "\n"

            if is_bare:
                return bare_result

        return result

    # Cuts off, after first string
    @staticmethod
    def convert_binary_data(data):
        data = data[::2]
        data = data[:data.find(b'\x00')]
        return data


class FileExtProcessor(DefaultProcessor):
    def __init__(self, data):
        super().__init__(data)

    def process_content(self, is_bare, is_raw):
        return self.str_rep()


class RecentDocsProcessor(DefaultProcessor):

    def __init__(self, data):
        super().__init__(data)

    def parse_mrulistex(self, b):
        decs = []
        for i in range(len(b)//4):
            p = i*4
            val = int.from_bytes(b[p:p+4], byteorder="little")
            #print(val)
            decs.append(val)
        return decs

    def process_content(self, is_bare, is_raw):
        bare_result = ""
        result = "\n" + ("=" * 50) + "\n"
        data_dict = self.data

        for k in data_dict.keys():

            if data_dict[k][0].value_type() != Registry.RegNone:
                result += str(k.name()) + "\n"
                result += ("="*51 + "\n")

            decs = []
            items = {}
            raw_items = {}
            for v in data_dict[k]:

                if v.value_type() == Registry.RegBin:

                    if v.name() == "MRUListEx":
                        # Convert Dwords to decimal, strip of 4 * 0xFF
                        decs = self.parse_mrulistex(v.value()[:-4])
                        result += str(decs) + "\n"

                        if is_raw:
                            result += str(v.value()) + "\n"

                    else:
                        bytes = self.convert_binary_data(v.value())
                        items[int(v.name())] = bytes.decode(
                            encoding="ISO-8859-1")
                        if is_raw:
                            raw_items[int(v.name())] = str(v.value())

            for i in decs:
                result += str(i) +" = " + items[i] + "\n"
                bare_result += items[i] + "\n"

                if is_raw:
                    result += str(i) +" = " + raw_items[i] + "\n"
                    bare_result += str(i) +" = " + raw_items[i] + "\n"

            bare_result += "\n"
            result += ("-"*50 + "\n\n")

        if is_bare:
            return bare_result
        return result

