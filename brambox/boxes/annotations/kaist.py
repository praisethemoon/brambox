#
#   Copyright EAVISE
#   Author: Soulaymen Chouri
#

"""
Kaist
------
"""
import logging
from .annotation import *

__all__ = ["KaistAnnotation", "KaistParser"]
log = logging.getLogger(__name__)


class KaistAnnotation(Annotation):
    """ Kaist image annotation """

    def serialize(self):
        """ generate a Kaist annotation string """
        string = "{} {} {} {} {} {} {} {} {} {} {} 0" \
            .format(self.class_label if len(self.class_label) != 0 else '?',
                    round(self.x_top_left),
                    round(self.y_top_left),
                    round(self.width),
                    round(self.height),
                    int(self.occlusionLevel))

        return string

    def deserialize(self, string):
        """ parse a dollar annotation string """
        elements = string.split()
        self.class_label = '' if elements[0] == '?' else elements[0]
        self.x_top_left = float(elements[1])
        self.y_top_left = float(elements[2])
        self.width = float(elements[3])
        self.height = float(elements[4])
        self.occlusionLevel = int(elements[5])

        self.object_id = 0

        return self


class DollarParser(Parser):
    """
    This parser is designed to parse the KAIST dataset which is based on version3 dollar annotation format from Piotr Dollar's MATLAB toolbox_.

    Keyword Args:
        occlusion_tag_map (list, optional): When the occluded flag in the dollar text file (see below) is used as an occlusion level tag, \
        its value is used as an index on this list to obtain an occlusion fraction that will be stored in the ``occluded_fraction`` attribute.

    The dollar format has one .txt file for every image of the dataset where each line within a file represents a bounding box.
    Each line is a space separated list of values structured as follows:

        <label> <x> <y> <w> <h> <occluded> <vx> <vy> <vw> <vh> <ignore> <angle>

    ========        ===========
    Name            Description
    ========        ===========
    label           class label name (string)
    x               left top x coordinate of the bounding box in pixels (integer)
    y               left top y coordinate of the bounding box in pixels (integer)
    w               width of the bounding box in pixels (integer)
    h               height of the bounding box in pixels (integer)
    occlusionLevel  0 indicating the object is not occluded, 1 indicating the object is partially occluded, 2 indicating the object is heavilty occluded
    ========        ===========

    Example:
        >>> image_000.txt
            % bbGt version=3
            person 488 232 34 100 0 0 0 0 0 0 0
            person 576 219 27 68 0 0 0 0 0 0 0

    Note:
        if no visible bounding box is annotated, [vx, vy, vw, vh] are equal to 0.

    .. _toolbox: https://github.com/pdollar/toolbox/blob/master/detector/bbGt.m
    """
    parser_type = ParserType.MULTI_FILE
    box_type = KaistAnnotation

    def deserialize(self, string):
        """ deserialize a string containing the content of a dollar .txt file

        This deserializer checks for header/comment strings in dollar strings
        """
        result = []

        for line in string.splitlines():
            if '%' not in line:
                anno = self.box_type()
                result += [anno.deserialize(line)]

        return result
