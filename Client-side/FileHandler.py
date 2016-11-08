import glob
import cPickle
import os

from lxml import etree
import requests
from requests.exceptions import ReadTimeout, ConnectionError

from RESTClient import RESTClient
from ExportTestResults import ExportTestResults


class WebServiceClient:

    def __init__(self):
        self.name = self
        self.ping = ""

    @staticmethod
    def get_local_file_count():
        file_count = (len(glob.glob1("data_store", "*.xml")))

        list_of_files = []
        if file_count > 0:
            list_of_files = glob.glob1("data_store", "*.xml")

        return {'Number of files': file_count,
                'List of files': list_of_files}

    @staticmethod
    def get_remote_file_count(index):
        rest_client = RESTClient()

        try:
            if rest_client.read_datafile(index):
                print "Connection is successful"

                number_of_remote_files = rest_client.get_number_of_files()

                return number_of_remote_files
        except:
            print "Server is unavailable"

    def check_transfer(self, index):
        try:
            number_of_files = self.get_local_file_count()["Number of files"]

            print("Number of local files: %s" % number_of_files)

            if index == (number_of_files - 1):
                print "File has been transferred"

                return True
            else:
                print "File has not been transferred"

                return False

        except:
            print "File cannot be transferred"

            return False

    def calculate_ping(self):
        export_test_results = ExportTestResults()

        try:
            session = requests.Session()

            request = session.get('http://127.0.0.1:5000/')

            self.ping = request.elapsed

            print 'Ping = ', self.ping

            export_test_results.write_to_file(self.ping)

        except ReadTimeout:
            print "Connection has timed out"

            self.ping = "ReadTimeout"

            export_test_results.write_to_file(self.ping)

        except ConnectionError:
            print "Failed to establish connection to Server"

            self.ping = "ConnectionError"

            export_test_results.write_to_file(self.ping)


class ResponseDeserialization:

    def __init__(self):
        self.name = self

    # TODO - Implement parse_cpu_data

    # TODO - Implement parse_memory_data
    @staticmethod
    def parse_memory_data(filename):
        try:
            total_memory = None
            task1 = None
            task2 = None

            root = etree.parse(filename)

            log_node = root.find('.//LOG-NODE')
            log_node_contents = log_node.getchildren()
            for content in log_node_contents:
                if content.get('Name') == 'Memory':
                    total_memory = content.get('Value')

            actions = root.findall('.//LOG-ACTION')

            log_action_contents = actions[0].getchildren()
            for content in log_action_contents:
                if content.get('Name') == 'Memory_Allocated':
                    task1 = content.get('Value')

            log_action_contents = actions[1].getchildren()
            for content in log_action_contents:
                if content.get('Name') == 'Memory_Allocated':
                    task2 = content.get('Value')

            print("Total Memory: %s" % total_memory)

            print("Task 1 Memory: %s" % task1)

            print("Task 2 Memory: %s" % task2)

            return [total_memory, task1, task2]

        except Exception as e:
            print(e)
            print "No memory data available"
            raise

    # TODO - Implement parse_jobs_data
    @staticmethod
    def parse_jobs_data(filename):
        try:
            energy_values = {'node_ID': [], 'energy': []}

            total_energy = 0

            root = etree.parse(filename)

            properties = root.findall('.//Property')

            for property in properties:
                if property.get('Name') == 'ID':
                    node_id = property.get('Value')

                    energy_values['node_ID'].append(node_id)

                if property.get('Name') == 'Energy':
                    energy_value = property.get('Value')

                    energy_values['energy'].append(energy_value)

                    total_energy += int(energy_value)

            # print len(energy_values)
            #
            # print energy_values
            #
            # print energy_values['node_ID'][0]
            #
            # print energy_values['energy'][0]

            # Calculate total energy usage
            print("Total Energy: %s" % total_energy)

            log_nodes = root.findall('.//LOG-NODE')

            first_log_node = log_nodes[0]

            time_stamp = first_log_node.get('Time')

            print("Time Stamp: %s" % time_stamp)

            energy_data = [total_energy, energy_values, time_stamp]

            pickle_name = 'visualizer_cache/jobs_data.p'

            # Check with pickle exists
            if os.path.isfile(pickle_name):
                # If the pickle exists delete ut
                os.remove(pickle_name)

                # And create new pickle file
                with open(pickle_name, 'wb') as pickle:
                    cPickle.dump(energy_data, pickle)

            else:
                # Pickle data to a new file
                with open(pickle_name, 'wb') as pickle:
                    cPickle.dump(energy_data, pickle)

        except Exception as e:
            print(e)
            print "No energy data available"
            raise

    # TODO - Implement parse_energy_data
    @staticmethod
    def parse_energy_data(filename):
        try:
            energy_values = {'node_ID': [], 'energy': []}

            total_energy = 0

            root = etree.parse(filename)

            properties = root.findall('.//Property')

            for property in properties:
                if property.get('Name') == 'ID':
                    node_id = property.get('Value')

                    energy_values['node_ID'].append(node_id)

                if property.get('Name') == 'Energy':
                    energy_value = property.get('Value')

                    energy_values['energy'].append(energy_value)

                    total_energy += int(energy_value)

            # print len(energy_values)
            #
            # print energy_values
            #
            # print energy_values['node_ID'][0]
            #
            # print energy_values['energy'][0]

            # Calculate total energy usage
            print("Total Energy: %s" % total_energy)

            log_nodes = root.findall('.//LOG-NODE')

            first_log_node = log_nodes[0]

            time_stamp = first_log_node.get('Time')

            print("Time Stamp: %s" % time_stamp)

            energy_data = [total_energy, energy_values, time_stamp]

            pickle_name = 'visualizer_cache/energy_data.p'

            # Check with pickle exists
            if os.path.isfile(pickle_name):
                # If the pickle exists delete ut
                os.remove(pickle_name)

                # And create new pickle file
                with open(pickle_name, 'wb') as pickle:
                    cPickle.dump(energy_data, pickle)

            else:
                # Pickle data to a new file
                with open(pickle_name, 'wb') as pickle:
                    cPickle.dump(energy_data, pickle)

        except Exception as e:
            print(e)
            print "No energy data available"
            raise


# TODO - Implement Late-timing fault detection
# TODO - Implement 404 resource not found fault detection
# TODO - Implement 500 internal server error fault detection
class FaultDetection:

    def __init__(self):
        self.name = self
