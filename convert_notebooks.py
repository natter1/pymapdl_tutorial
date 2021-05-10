"""
Script to convert jupyter notebooks.
"""
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import PDFExporter

notebook_filename = "bending_beam_tutorial.ipynb"

with open(notebook_filename) as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

#ep.preprocess(nb, {'metadata': {'path': 'notebooks/'}})

pdf_exporter = PDFExporter()

pdf_data, resources = pdf_exporter.from_notebook_node(nb)

with open("notebook.pdf", "wb") as f:
    f.write(pdf_data)
    f.close()




# import nbformat
# import os
# from nbconvert.preprocessors import ExecutePreprocessor
#
#
# def run_notebook(notebook_path):
#     nb_name, _ = os.path.splitext(os.path.basename(notebook_path))
#     dirname = os.path.dirname(notebook_path)
#
#     with open(notebook_path) as f:
#         nb = nbformat.read(f, as_version=4)
#
#     proc = ExecutePreprocessor(timeout=600, kernel_name='python3')
#     proc.allow_errors = True
#
#     proc.preprocess(nb, {'metadata': {'path': '/'}})
#     output_path = os.path.join(dirname, '{}_all_output.ipynb'.format(nb_name))
#
#     with open(output_path, mode='wt') as f:
#         nbformat.write(nb, f)
#
#
# if __name__ == '__main__':
#     run_notebook('bending_beam_tutorial.ipynb')





# from traitlets.config import Config, get_config
# import nbformat as nbf
# from nbconvert.exporters import HTMLExporter
# from nbconvert.preprocessors import ExecutePreprocessor
#
# #c = Config()
#
# c = get_config()
#
# #Export all the notebooks in the current directory to the sphinx_howto format.
# c.NbConvertApp.notebooks = ['*.ipynb']
# c.NbConvertApp.export_format = 'latex'
# c.Exporter.template_file = 'article'
# c.NbConvertApp.postprocessor_class = 'PDF'
#
# # Configure tag removal
# #c.TagRemovePreprocessor.remove_cell_tags = ("remove_cell",)
# #c.TagRemovePreprocessor.remove_all_outputs_tags = ('remove_output',)
# #c.TagRemovePreprocessor.remove_input_tags = ('hide-input',)
#
# # c.TagRemovePreprocessor.enabled=True
# #
# # # Configure and run out exporter
# # #c.HTMLExporter.preprocessors = ["TagRemovePreprocessor"]
# # HTMLExporter(config=c).from_filename("bending_beam_tutorial.ipynb")
