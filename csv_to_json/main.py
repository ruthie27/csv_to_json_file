"""
@package
@description:
@author

"""
import csv
import os
import json
import logging
from datetime import date


class Upload(object):
    """Main class."""
    def __init__(self, filename):
        """Initialization."""
        self.filename = filename
        self.filepath = os.path.join('input', self.filename)
        self.target = 'output'
        self.csvdata = list()
        self.make = list()
        self.model = list()
        self.yearmodel = list()
        self.oe = list()
        self.part = list()
        self.prod_list = list()
        self.product = list()

    def parse_csv(self, file_name, start_line=1):
        """Read a CSV and return it in a JSON format."""

        with open(file_name) as f:
            reader = csv.reader(f)

            try:
                headers = next(reader)
                headers = [i.lower().strip() for i in headers[:]]
            except StopIteration:
                logging.error('No headers')

            try:
                for i in range(0, start_line - 1):
                    # Skip rows based on start_line
                    next(reader)
            except StopIteration:
                logging.error('No values from start line onwards')

            for i in reader:
                self.csvdata.append(dict(zip(headers, i)))

    def get_make_list(self):
        """Distinct make."""
        count = 0
        make_list = []
        for row in self.csvdata:
            if row['make'] not in make_list:
                count += 1
                # st_json = '{"id":"' + str(count) + '","code":"' + row['make'].strip() + '","name":"' + row['make'].strip() + '"},'
                make_list.append(row['make'])
                self.make.append({
                    'id': count,
                    'code': row['make'].strip(),
                    'name': row['make'].strip()
                    })

        header = ['id', 'code', 'name']
        self.generate_file('make', self.make, header)

    def get_model_list(self):
        """Get model with id."""
        count = 0
        model_list = []
        for row in self.csvdata:
            makename = row['make'].lower().strip()
            car_model = row['car model'].lower().strip()

            for make in self.make:
                if make['code'].lower().strip() == makename:
                    make_id = make['id']
                    continue

            key = str(make_id )+ '_' + row['car model']
            if key not in model_list:
                count += 1

                # st_json = '{"id":"' + str(count) + '","make_id":"' + str(make_id) + '","model_name":"' + row['car model'] + '","description":""},'
                model_list.append(key)
                self.model.append({
                    'id': count,
                    'make_id': make_id,
                    'model': row['car model']
                    })

        header = ['id', 'make_id', 'model']
        self.generate_file('model', self.model, header)

    def get_yearmodel_list(self):
        """Get model with id."""
        count = 0
        yearmodel_list = []
        for row in self.csvdata:
            make_id = 0
            model_id = 0
            makename = row['make'].lower().strip()
            car_model = row['car model'].lower().strip()
            year_model = row['year model'].lower().strip()
            for make in self.make:
                if make['code'].lower().strip() == makename:
                    make_id = make['id']
                    continue

            for model in self.model:
                if model['model'].lower().strip() == car_model:
                    model_id = model['id']
                    continue

            key = str(make_id )+ '_' + str(model_id) + '_' + year_model
            if key not in yearmodel_list:
                count += 1

                # st_json = '{"id":"' + str(count) + '","make_id":"' + str(make_id) + '","model_name":"' + row['car model'] +'","year_model":"' + year_model + '","description":""},'
                yearmodel_list.append(key)
                self.yearmodel.append({
                    'id': count,
                    'make_id': make_id,
                    'model_id': model_id,
                    'make': row['make'].strip(),
                    'model': row['car model'].strip(),
                    'year_model': year_model
                    })

        header = ['id', 'make_id', 'model_id', 'make', 'model', 'year_model']
        self.generate_file('yearmodel', self.yearmodel, header)

    def get_oe_list(self):
        """Distinct oe battery."""
        count = 0
        oe_list = []
        for row in self.csvdata:
            if row['oe battery'] not in oe_list and row['oe battery'] != '':
                count += 1
                # st_json = '{"id":"' + str(count) + '","category":"BATTERY","name":"OE BATTERY","code":"' + row['oe battery'].strip() + '","description":""},'
                oe_list.append(row['oe battery'])
                self.oe.append({
                    'id': count,
                    'category': 'BATTERY',
                    'name': 'OE BATTERY',
                    'code': row['oe battery'].strip(),
                    'description': ''
                    })

        header = ['id', 'category', 'name', 'code', 'description']
        self.generate_file('oe', self.oe, header)

    def get_part_list(self):
        """Get product with id."""
        part_list = []
        count = 0
        for row in self.csvdata:
            make_id = 0
            model_id = 0
            car_model_id = 0
            prod_id = 0
            oe_part_id = 0

            if row['bestbuy id'].strip() == '':
                bestbuy_id = 0
            else:
                bestbuy_id = row['bestbuy id'].lower().strip()
            
            makename = row['make'].lower().strip()
            car_model = row['car model'].lower().strip()
            year_model = row['year model'].lower().strip()
            oe_part_name = row['oe battery'].lower().strip()
            replacement = row['replacement'].lower().strip()
            price = row['price'].lower().strip()
            srp = row['srp'].lower().strip()

            for make in self.make:
                if make['code'].lower().strip() == makename:
                    make_id = make['id']
                    continue

            for model in self.model:
                if model['model'].lower().strip() == car_model:
                    model_id = model['id']
                    continue

            for yearmodel in self.yearmodel:
                if yearmodel['model_id'] == model_id and yearmodel['year_model'].lower().strip() == year_model:
                    car_model_id = yearmodel['id']
                    continue

            for oe_part in self.oe:
                if oe_part['code'].lower().strip() == oe_part_name:
                    oe_part_id = oe_part['id']
                    category = oe_part['category']
                    oe_name = oe_part['name']
                    continue

            for product in self.prod_list:
                if product['code'].lower().strip() == replacement:
                    prod_id = product['id']
                    continue

            if car_model_id not in part_list:
                count += 1
                # st_json = '{"id":"' + str(count) + '","car_model_id":"'+ str(car_model_id) + '","car_model":[{"id":"' + str(car_model_id) + '","make_id":"' + str(make_id)+'","model_id":"'+ str(model_id) +'"},'
                part_list.append(car_model_id)
                self.part.append({
                    'id': count,
                    'car_model_id': car_model_id,
                    'make_id': make_id,
                    'model_id': model_id,
                    'model_name': row['car model'].strip(),
                    'year_model': row['year model'].strip(),
                    'part_id': oe_part_id,
                    'category': 'Battery',
                    'oe_name': 'OE Battery',
                    'code': row['oe battery'].strip(),
                    'description': '',
                    'product_id': prod_id,
                    'bestbuy_id': bestbuy_id,
                    'brand': 'ENERGIZER',
                    'prod_name': row['replacement'].strip(),
                    'price': row['price'].strip(),
                    'srp': row['srp'].strip()
                    })

        # prodheader = ['id', 'car_model_id', 'prod_id', 'bestbuy_id', 'category', 'name',
        #               'code', 'description', 'replacement', 'price', 'srp', 'json']
        header = ['id', 'car_model_id','make_id', 'model_id', 'model_name', 'year_model',
                      'part_id', 'category', 'oe_name', 'code', 'description', 'product_id', 
                      'bestbuy_id', 'brand', 'prod_name', 'price', 'srp']
        self.generate_file('part', self.part, header)

    def get_prod_list(self):
        """Distinct replacement."""
        count = 0
        make_list = []
        
        for row in self.csvdata:
            if row['replacement'] == '':
                continue

            if row['replacement'] not in make_list:
                count += 1
                make_list.append(row['replacement'])
                self.prod_list.append({
                    'id': count,
                    'category': 'battery',
                    'name': row['replacement'].strip(),
                    'code': row['replacement'].strip(),
                    'bestbuy_id': row['bestbuy id'].strip(),
                    'description': '',
                    'replacement': 'Battery Replacement - ' + row['replacement'].strip(),
                    'price': row['price'].strip(),
                    'srp': row['srp'].strip(),
                    })

        # makeheader = ['id', 'category', 'name', 'code', 'description', 'replacement', 'price', 'srp']
        # targetpath = os.path.join(self.target, 'make.csv')

        # header = ['id', 'category', 'name', 'code', 'description']
        # self.generate_file('oe', self.oe, header)

    def get_product_list(self):
        product_list = []
        count = 0
        for row in self.csvdata:
            make_id = 0
            model_id = 0
            car_model_id = 0
            prod_id = 0
            
            if row['bestbuy id'].strip() == '':
                bestbuy_id = 0
            else:
                bestbuy_id = row['bestbuy id'].lower().strip()
            
            makename = row['make'].lower().strip()
            car_model = row['car model'].lower().strip()
            year_model = row['year model'].lower().strip()
            replacement = row['replacement'].lower().strip()
            price = row['price'].lower().strip()
            srp = row['srp'].lower().strip()

            for make in self.make:
                if make['code'].lower().strip() == makename:
                    make_id = make['id']
                    continue

            for model in self.model:
                if model['model'].lower().strip() == car_model:
                    model_id = model['id']
                    continue

            for yearmodel in self.yearmodel:
                if yearmodel['model_id'] == model_id and yearmodel['year_model'].lower().strip() == year_model:
                    car_model_id = yearmodel['id']
                    continue

            for product in self.prod_list:
                if product['code'].lower().strip() == replacement:
                    prod_id = product['id']
                    continue

            if car_model_id not in product_list:
                count += 1
                st_json = ''
                product_list.append(car_model_id)
                self.product.append({
                    'id': count,
                    'car_model_id': car_model_id,
                    'prod_id': prod_id,
                    'bestbuy_id': bestbuy_id,
                    'category': 'battery',
                    'name': row['replacement'].strip(),
                    'code': row['replacement'].strip(),
                    'description': '',
                    'replacement': 'Battery Replacement - ' + row['replacement'].strip(),
                    'price': row['price'].strip(),
                    'srp': row['srp'].strip()
                    })

        header = ['id', 'car_model_id', 'prod_id', 'bestbuy_id', 'category', 'name',
                      'code', 'description', 'replacement', 'price', 'srp']
        self.generate_file('product', self.product, header)

    def generate_file(self, filename, data, header):
        """Generate file."""
        self.get_filepath(filename + '.csv')
        self.write_to_csv(header, data)
        self.get_filepath(filename + '.json')
        self.write_to_json(data)


    def get_filepath(self, filename):
        """"Get path with filename."""
        self.filepath = os.path.join(self.target, filename)

    def write_to_csv(self, header, data):
        """Write to csv file."""
        with open(self.filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            for mydata in data:
                writer.writerow(mydata)
        f.close()

    def write_to_json(self, data):
        """Write to json file."""
        # #Get the file name for the new file to write
        # filter = "JSON File (*.json)|*.json|All Files (*.*)|*.*||"
        # filename = rs.SaveFileName("Save JSON file as", filter)

        # If the file name exists, write a JSON string into the file.
        with open(self.filepath, 'w') as f:
            json.dump(data, f)

    def main(self):
        """Main."""
        self.parse_csv(self.filepath)
        self.get_make_list()
        self.get_model_list()
        self.get_yearmodel_list()
        self.get_oe_list()
        self.get_prod_list()
        self.get_product_list()
        self.get_part_list()


if __name__ == "__main__":
    filename = "Sample.csv"
    upload = Upload(filename)
    upload.main()
