from ceci import PipelineStage
from descformats import TextFile, FitsFile, HDFFile, YamlFile

# This class represents one step in the pipeline
class pz_pdfStage1(PipelineStage):
    name = "pz_pdfStage1"
    #
    inputs = [
        ('config', YamlFile),
        ('some_input_tag', TextFile),
    ]
    outputs = [
        ('some_output_tag', TextFile),
        # More inputs can go here
    ]
    required_config = {
        'price_of_fish': None,
        'number_of_roads': 42,
        }

    def run(self):
        config = self.read_config()

        fish = config['price_of_fish']
        roads = config['number_of_roads']

        input_file = self.open_input('some_input_tag')
        input_data = input_file.read()
        input_file.close()

        # You would normally call some other function or method
        # here to generate some output.  You can use self.comm, 
        # self.rank, and self.size to use MPI.

        output = f"""
Original input text was:
{input_data}

How many roads must a man walk down?  {roads}
Price of fish = £{fish}
        """

        output_file = self.open_output('some_output_tag')
        output_file.write(output)
        output_file.close()


