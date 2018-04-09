#
# Created by Frederic TOST - November 2017
#

#
# This class manages the location of labels over an image
# Objective is to minimize overlapping
#
class BoxLabelManager:

    label_bounding_boxes = []
    bounding_boxes       = []
    image_width  = 0
    image_height = 0
    draw_rectangle = False
    draw_label     = False

    def __init__(self, _image_width, _image_height):
        self.image_width  = _image_width
        self.image_height = _image_height

    def setDrawRectangle(self, _value):
        self.draw_rectangle = _value;

    def isDrawRectangle(self):
        return self.draw_rectangle

    def isDrawLabel(self):
        return self.draw_label

    def setDrawLabel(self, _value):
        self.draw_label = _value;

    # Return the coordinates of the best label box and store it
    def addBoundingBoxAndLabelBox(self, _bounding_box, _label_width, _label_height):
        # Add the bounding box, for fun ;-)
        self.bounding_boxes.append(_bounding_box)

        left   = _bounding_box[0]
        right  = _bounding_box[2]
        top    = _bounding_box[1]
        bottom = _bounding_box[3]

        # Keep the initial propose
        first_proposal = [ left , top - _label_height, left + _label_width , top]

        # The offset will slide the box propose to the right or to the left
        x_offset = 0
        while x_offset < (right-left)-_label_width:

            #
            # Proposal 1
            #
            # First label box proposal, top/left

            proposal_label_box =  [ left + x_offset, top - _label_height, left + _label_width + x_offset, top]


            # Surface if over an existing label box 30% of area
            if self.isOverALabel(proposal_label_box)<0.3:
                # We are done
                self.label_bounding_boxes.append(proposal_label_box)
                return proposal_label_box

            #
            # Proposal 2
            #
            # Second proposal, bottom/left
            proposal_label_box = [left + x_offset, bottom , left + _label_width + x_offset, bottom + _label_height]
            if self.isOverALabel(proposal_label_box) < 0.3:
                # We are done
                self.label_bounding_boxes.append(proposal_label_box)
                return proposal_label_box

            #
            # Proposal 3
            #
            # Third proposal, top/right
            proposal_label_box = [right-_label_width - x_offset, top - _label_height, right - x_offset, top]
            if self.isOverALabel(proposal_label_box) < 0.3:
                # We are done
                self.label_bounding_boxes.append(proposal_label_box)
                return proposal_label_box

            #
            # Proposal 4
            #
            # Third proposal, bottom/right
            proposal_label_box = [right-_label_width - x_offset, bottom - _label_height, right - x_offset, bottom + _label_height]
            if self.isOverALabel(proposal_label_box) < 0.3:
                # We are done
                self.label_bounding_boxes.append(proposal_label_box)
                return proposal_label_box

            x_offset = x_offset + 20


        # Last chance
        # Rectangle is as height as the image (95%)
        if (bottom - top) > (0.95 * self.image_height):
            # Inside the rectangle
            first_proposal = [left, top, left + _label_width, top + _label_height]

        return first_proposal

    # Does the box proposal over an existing label ?
    def isOverALabel(self, _label_box):
        iou = 0
        if (_label_box[0] < 0) or (_label_box[2]>self.image_width) or \
            (_label_box[1] < 0) or (_label_box[3] > self.image_height):
            return 1

        for current_box in self.label_bounding_boxes:
            iou = self.get_intersection_over_union_v2(_label_box, current_box)
        return iou

    # Just compute the intersection over union of 2 boxes,
    # the result is in [0,1]
    def get_intersection_over_union_v2(self, boxA, boxB):
        # determine the (x, y)-coordinates of the intersection rectangle
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        # compute the area of intersection rectangle
        interArea = (xB - xA + 1) * (yB - yA + 1)

        # compute the area of both the prediction and ground-truth
        # rectangles
        boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

        # compute the intersection over union by taking the intersection
        # area and dividing it by the sum of prediction + ground-truth
        # areas - the interesection area
        iou = interArea / float(boxAArea + boxBArea - interArea)

        # return the intersection over union value
        return iou