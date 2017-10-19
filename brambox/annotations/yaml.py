#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
#   YAML annotation format
#   example file
#       img1:
#           car:
#               - [x,y,w,h]
#           person:
#               - [x,y,w,h]
#               - [x,y,w,h]
#       img2:
#           car:
#               - [x,y,w,h]
#

import yaml
from .annotation import *

__all__ = ["YamlAnnotation", "YamlParser"]


class YamlAnnotation(Annotation):
    """ YAML image annotation """

    def serialize(self):
        """ generate a yaml annotation object """
        return (self.class_label, [self.x_top_left, self.y_top_left, self.width, self.height])

    def deserialize(self, yaml_obj, class_label):
        """ parse a yaml annotation object """
        self.class_label = class_label
        self.x_top_left = yaml_obj[0]
        self.y_top_left = yaml_obj[1]
        self.width = yaml_obj[2]
        self.height = yaml_obj[3]

        self.lost = False
        self.occluded = False


class YamlParser(Parser):
    """ YAML annotation parser """
    parser_type = ParserType.SINGLE_FILE    # Darknet annotations have one file per image
    annotation_type = YamlAnnotation        # Darknet annotation type
    extension = '.yaml'

    def serialize(self, annotations):
        """ Serialize input dictionary of annotations into one string """
        result = {}
        for img_id in annotations:
            img_res = {}
            for anno in annotations[img_id]:
                if anno.lost:   # yaml does not support lost type -> ignore
                    continue
                new_anno = self.annotation_type.create(anno)
                key, val = new_anno.serialize()
                if key not in img_res:
                    img_res[key] = [val]
                else:
                    img_res[key] += [val]
            result[img_id] = img_res

        return yaml.dump(result)

    def deserialize(self, string):
        """ Deserialize an annotation file into a dictionary of annotation """
        yml_obj = yaml.load(string)

        result = {}
        for img_id in yml_obj:
            anno_res = []
            for class_label, annotations in yml_obj[img_id].items():
                for anno_yml in annotations:
                    anno = self.annotation_type()
                    anno.deserialize(anno_yml, class_label)
                    anno_res += [anno]
            result[img_id] = anno_res

        return result
