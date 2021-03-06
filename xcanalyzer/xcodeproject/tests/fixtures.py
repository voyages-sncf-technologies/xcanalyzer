import json
import os
import subprocess

from ..models import XcTarget, XcProject, XcGroup, XcFile
from ..parsers import XcProjectParser, SwiftCodeParser


# Absolute path of this project root folder.
root_path = __file__
for i in range(0, 4):
    root_path = os.path.dirname(root_path)


# Models

class XcModelsFixture():

    def any_target(self,
                   name='MyXcTarget',
                   target_type=XcTarget.Type.APPLICATION,
                   product_name='MyXcProduct',
                   resource_files=set()):
        return XcTarget(name=name, target_type=target_type, product_name=product_name, resource_files=resource_files, build_configurations=list())
    
    def any_project(self):
        targets = set([self.any_target()])
        return XcProject('/', 'MyXcProject', build_configurations=list(), targets=targets, groups=list(), files=set())
    
    def any_group(self, group_path='/MyGroup', filepath='/MyGroup', groups=list(), files=set()):
        return XcGroup(group_path, filepath, groups=groups, files=files)

    def any_file(self):
        return XcFile('/MyFile')
    
# Xcode sample project

class SampleXcodeProjectFixture():

    @property
    def project_folder_path(self):
        """ Absolute path of the folder containing `.xcodeproj` of the Xcode project sample contained in this project. """
        return os.path.join(root_path, 'SampleiOSApp')


# Parsers

class XcProjectParserFixture():

    @property
    def sample_xc_project_parser(self):
        path = SampleXcodeProjectFixture().project_folder_path
        project_parser = XcProjectParser(path, verbose=False)
        project_parser.load()

        return project_parser


class SwiftCodeParserFixture():

    def any_swift_code_parser(self, swift_code, base_discriminant='', type_counter=0):
        command = ['sourcekitten', 'structure', '--text', swift_code]
        result = subprocess.run(command, capture_output=True)
        swift_structure = json.loads(result.stdout)

        root_substructures = swift_structure.get('key.substructure', []).copy()
        parser = SwiftCodeParser(substructures=root_substructures, base_discriminant=base_discriminant, type_counter=type_counter)

        parser.parse()

        return parser


# Generators

class XcProjectGraphGeneratorFixture():

    @property
    def test_build_folder(self):
        return os.path.join(root_path, 'build', 'test')

    def any_graph_filepath(self, filename):
        return os.path.join(self.test_build_folder, filename)
