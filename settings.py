import os

root_path = os.path.dirname(os.path.abspath(__file__))  # path to this file

files = dict(data_folder=os.path.join(root_path, 'data'),
             static_folder=os.path.join(root_path, 'viewer/static'))
files.update(
    dict(
        activity_folder=os.path.join(files['data_folder'], "activity"),
        output_folder=os.path.join(files['static_folder'], "output"),
        pickle_activity_folder=os.path.join(files['data_folder'], "pickle_activity"),
        pickle_class_folder=os.path.join(files['data_folder'], "pickle_class")
    )
)
